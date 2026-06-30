# -*- coding: utf-8 -*-
"""
knowledge_updater.py - self-improving knowledge pipeline for Skill #141
(Internal Training & Personalized Promotion Path Designer; cluster: business-operations).

Pipeline:
  1. Fetch candidate entries from authoritative domain sources and search queries.
     - Primary fetcher: crawl4ai (web crawl + markdown extraction).
     - Fallback fetcher: a lightweight HTTP+regex adapter (no external deps beyond
       the standard library + optional `requests`).
  2. Parse each fetched document into normalized entry dicts
     (title, authors, year, venue, url, abstract).
  3. Score entries by recency + domain-keyword relevance.
  4. Deduplicate against the existing brain by a URL/DOI hash.
  5. Append dated, well-formed entries to SECOND-KNOWLEDGE-BRAIN.md.

The pipeline degrades gracefully: if no fetcher can reach the network, it logs
an INFO message and exits 0 so the skill keeps working off the existing brain.

Run modes:
  python tools/knowledge_updater.py             # live run (scheduled weekly)
  python tools/knowledge_updater.py --dry-run   # print what would be appended; write nothing
  python tools/knowledge_updater.py --verbose   # DEBUG logging

This is a pure preparation/production tool. It does not load or train any model.
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime as _dt
import hashlib
import json
import logging
import os
import re
import sys
from typing import Iterable, List, Dict, Optional, Protocol

LOG = logging.getLogger("knowledge_updater")

# ---------------------------------------------------------------------------
# Static configuration (mirrors CLAUDE.md / PROJECT-detail.md)
# ---------------------------------------------------------------------------
DEFAULT_BRAIN = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "SECOND-KNOWLEDGE-BRAIN.md"
)

ARXIV_CATEGORIES: List[str] = []  # domain relies on standards bodies, not preprints

WEB_SOURCES: List[str] = [
    "https://www.atd.org",
    "https://www.shrm.org",
    "https://www.linkedin.com/business/learning",
    "https://www.mckinsey.com",
]

SEARCH_QUERIES: List[str] = [
    "skills taxonomy future of jobs WEF",
    "learning experience design evidence",
    "competency based promotion framework",
    "training ROI Kirkpatrick measurement",
]

# Domains treated as authoritative; relevance boosts hits on these hosts.
AUTHORITATIVE_DOMAINS = {"atd.org", "shrm.org", "linkedin.com", "mckinsey.com"}

HASH_RE = re.compile(r"<!--hash:([0-9a-f]{16})-->")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclasses.dataclass(frozen=True)
class Entry:
    title: str
    authors: str
    year: str
    venue: str
    url: str
    abstract: str

    def to_dict(self) -> Dict[str, str]:
        return dataclasses.asdict(self)


# ---------------------------------------------------------------------------
# Fetcher protocol (pluggable so tests can inject fakes without a network)
# ---------------------------------------------------------------------------
class Fetcher(Protocol):
    def fetch(self, url: str) -> Optional[str]:
        """Return raw text (markdown/html) for a URL, or None on failure."""


class Crawl4AIFetcher:
    """Primary fetcher. Uses crawl4ai when installed."""

    def __init__(self) -> None:
        self._crawler = None
        try:
            from crawl4ai import WebCrawler  # type: ignore

            self._crawler = WebCrawler()
            self._crawler.warmup()
        except Exception as exc:  # pragma: no cover - environment dependent
            LOG.info("crawl4ai unavailable (%s); will use fallback fetcher.", exc)
            self._crawler = None

    @property
    def available(self) -> bool:
        return self._crawler is not None

    def fetch(self, url: str) -> Optional[str]:
        if self._crawler is None:
            return None
        try:
            res = self._crawler.run(url=url)
            return getattr(res, "markdown", "") or ""
        except Exception as exc:  # pragma: no cover - network dependent
            LOG.warning("crawl4ai fetch failed for %s: %s", url, exc)
            return None


class HttpFallbackFetcher:
    """Fallback fetcher. Uses `requests` if present, else urllib from the stdlib."""

    def __init__(self, timeout: float = 20.0, user_agent: str = "skill141-kb-updater/1.0") -> None:
        self.timeout = timeout
        self.user_agent = user_agent
        try:
            import requests  # type: ignore

            self._requests = requests
        except Exception:  # pragma: no cover - environment dependent
            self._requests = None

    @property
    def available(self) -> bool:
        return True  # urllib is always available

    def fetch(self, url: str) -> Optional[str]:
        try:
            if self._requests is not None:
                resp = self._requests.get(
                    url, timeout=self.timeout, headers={"User-Agent": self.user_agent}
                )
                resp.raise_for_status()
                return resp.text
            import urllib.request

            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # noqa: S310
                return resp.read().decode("utf-8", errors="replace")
        except Exception as exc:  # pragma: no cover - network dependent
            LOG.warning("fallback fetch failed for %s: %s", url, exc)
            return None


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------
_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
_ARXIV_ID_RE = re.compile(r"(arXiv:\d{4}\.\d{4,5})")
_YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def _strip_html(html: str) -> str:
    text = _TAG_RE.sub(" ", html)
    return _WS_RE.sub(" ", text).strip()


def _extract_title(html: str) -> str:
    m = _TITLE_RE.search(html)
    if m:
        return _strip_html(m.group(1))[:200]
    # first non-empty line as a fallback
    for line in _strip_html(html).splitlines():
        line = line.strip()
        if line:
            return line[:200]
    return "Untitled"


def _extract_year(text: str) -> str:
    m = _YEAR_RE.search(text)
    return m.group(0) if m else str(_dt.date.today().year)


def _host(url: str) -> str:
    m = re.match(r"https?://([^/]+)", url)
    return (m.group(1).lower() if m else "").lstrip("www.")


def parse_document(url: str, body: str) -> Optional[Entry]:
    """Parse a fetched document body into a normalized Entry."""
    if not body or not body.strip():
        return None
    title = _extract_title(body)
    clean = _strip_html(body)
    venue = _host(url) or url
    return Entry(
        title=title,
        authors="-",
        year=_extract_year(clean),
        venue=venue,
        url=url,
        abstract=clean[:600],
    )


def parse_arxiv_list(body: str, base_url: str) -> List[Entry]:
    out: List[Entry] = []
    for m in _ARXIV_ID_RE.finditer(body):
        aid = m.group(0).split(":")[1]
        out.append(
            Entry(
                title=f"ArXiv {aid}",
                authors="-",
                year=str(_dt.date.today().year),
                venue="arXiv",
                url=f"https://arxiv.org/abs/{aid}",
                abstract="",
            )
        )
    return out


# ---------------------------------------------------------------------------
# Scoring & dedup
# ---------------------------------------------------------------------------
RELEVANCE_KEYWORDS = [w.lower() for q in SEARCH_QUERIES for w in q.split()]


def relevance_score(title: str, abstract: str) -> float:
    blob = f"{title} {abstract}".lower()
    hits = sum(1 for k in RELEVANCE_KEYWORDS if k in blob)
    return hits / max(1, len(RELEVANCE_KEYWORDS))


def url_hash(url: str) -> str:
    return hashlib.sha256((url or "").encode("utf-8")).hexdigest()[:16]


def existing_hashes(text: str) -> set:
    return set(HASH_RE.findall(text))


def min_relevance() -> float:
    # keep any entry that hits at least one keyword (>= 1/len)
    return 1.0 / max(1, len(RELEVANCE_KEYWORDS))


# ---------------------------------------------------------------------------
# Brain file I/O
# ---------------------------------------------------------------------------
def load_brain(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def format_entry(entry: Entry, relevance: float, today: str) -> str:
    return (
        f"- {today} - **{entry.title}** ({entry.venue}, {entry.year}) "
        f"[{entry.url}] relevance={relevance:.2f} <!--hash:{url_hash(entry.url)}-->"
    )


def append_section(path: str, header: str, lines: List[str]) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n{header}\n" + "\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def collect_candidates(
    fetcher: Fetcher, sources: List[str], queries: List[str], arxiv: List[str]
) -> List[Entry]:
    entries: List[Entry] = []
    for cat in arxiv:
        q = cat.split()[0]
        url = f"https://arxiv.org/list/{q}/recent"
        body = fetcher.fetch(url)
        if body:
            entries.extend(parse_arxiv_list(body, url))
    for src in sources:
        body = fetcher.fetch(src)
        if not body:
            continue
        entry = parse_document(src, body)
        if entry:
            entries.append(entry)
    # query-driven fetch: synthesize a search URL when the fetcher is a real
    # crawler that can resolve pages; crawl4ai can fetch a google-adjacent
    # listing page via the source host. For sources without a search API we
    # skip to avoid junk; authoritative-host crawls already cover this.
    _ = queries  # reserved for a future search-API integration
    return entries


def select_new(
    entries: Iterable[Entry], seen: set, min_rel: float
) -> List[tuple]:
    scored = sorted(
        ((e, relevance_score(e.title, e.abstract)) for e in entries),
        key=lambda t: t[1],
        reverse=True,
    )
    out = []
    for entry, rel in scored:
        if not entry.url:
            continue
        h = url_hash(entry.url)
        if h in seen:
            continue
        if rel < min_rel:
            continue
        out.append((entry, rel, h))
    return out


def run(
    brain_path: str,
    sources: List[str],
    queries: List[str],
    arxiv: List[str],
    dry_run: bool,
    fetcher: Optional[Fetcher] = None,
) -> int:
    if not os.path.exists(brain_path):
        LOG.error("knowledge brain not found: %s", brain_path)
        return 2
    text = load_brain(brain_path)
    seen = existing_hashes(text)

    if fetcher is None:
        fetcher = Crawl4AIFetcher()
        if not fetcher.available:  # type: ignore[attr-defined]
            LOG.info("primary fetcher unavailable; using HTTP fallback.")
            fetcher = HttpFallbackFetcher()

    entries = collect_candidates(fetcher, sources, queries, arxiv)
    LOG.info("collected %d candidate entries.", len(entries))

    today = _dt.date.today().isoformat()
    new = select_new(entries, seen, min_relevance())
    lines = [format_entry(e, rel, today) for e, rel, _ in new]
    for h in new:
        seen.add(h[2])

    if not lines:
        LOG.info("no new entries this run (network/dedup/relevance).")
        return 0

    if dry_run:
        print(json.dumps([e.to_dict() | {"relevance": round(rel, 2)} for e, rel, _ in new], indent=2))
        LOG.info("[dry-run] would append %d entries.", len(lines))
        return 0

    append_section(brain_path, f"### Auto-crawl {today}", lines)
    LOG.info("appended %d new entries to %s", len(lines), brain_path)
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--brain", default=DEFAULT_BRAIN, help="Path to SECOND-KNOWLEDGE-BRAIN.md")
    p.add_argument("--dry-run", action="store_true", help="Print what would be appended; write nothing")
    p.add_argument("--verbose", action="store_true", help="DEBUG logging")
    p.add_argument("--sources", nargs="*", default=WEB_SOURCES, help="Override web sources")
    p.add_argument("--queries", nargs="*", default=SEARCH_QUERIES, help="Override search queries")
    p.add_argument("--arxiv", nargs="*", default=ARXIV_CATEGORIES, help="Override ArXiv categories")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    LOG.info("knowledge_updater for skill #141 (internal-training-promotion-designer)")
    return run(
        brain_path=os.path.abspath(args.brain),
        sources=args.sources,
        queries=args.queries,
        arxiv=args.arxiv,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    sys.exit(main())