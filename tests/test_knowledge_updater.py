# -*- coding: utf-8 -*-
"""
Pure-function unit tests for tools/knowledge_updater.py.

These tests deliberately avoid any network access: they exercise the parser,
scoring, dedup, and formatting helpers with deterministic in-memory inputs.
Run with:  pytest tests/test_knowledge_updater.py
"""
import os
import sys
import tempfile

import pytest

TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools"))
sys.path.insert(0, TOOLS_DIR)

import knowledge_updater as ku  # noqa: E402


# ---------------------------------------------------------------------------
# Entry / dataclass
# ---------------------------------------------------------------------------
def test_entry_to_dict_roundtrip_keys():
    e = ku.Entry("T", "A", "2024", "venue", "http://x", "abs")
    d = e.to_dict()
    assert set(d.keys()) == {"title", "authors", "year", "venue", "url", "abstract"}
    assert d["title"] == "T"


# ---------------------------------------------------------------------------
# relevance_score
# ---------------------------------------------------------------------------
def test_relevance_score_zero_for_unrelated():
    assert ku.relevance_score("nothing relevant here", "blank") == 0.0


def test_relevance_score_increases_with_keywords():
    base = ku.relevance_score("competency framework", "")
    assert base > 0.0
    more = ku.relevance_score("competency based promotion framework", "")
    assert more >= base


def test_relevance_score_is_bounded_0_to_1():
    e = ku.Entry(
        " ".join(ku.RELEVANCE_KEYWORDS), "-", "2024", "venue", "http://x", "abstract"
    )
    assert 0.0 <= ku.relevance_score(e.title, e.abstract) <= 1.0


def test_min_relevance_is_positive():
    assert ku.min_relevance() > 0.0


# ---------------------------------------------------------------------------
# url_hash / dedup
# ---------------------------------------------------------------------------
def test_url_hash_stable_and_short():
    h1 = ku.url_hash("https://example.com/a")
    h2 = ku.url_hash("https://example.com/a")
    assert h1 == h2
    assert len(h1) == 16
    assert ku.url_hash("https://example.com/a") != ku.url_hash("https://example.com/b")


def test_existing_hashes_finds_tags():
    text = "blah <!--hash:abcdef0123456789--> more <!--hash:fedcba9876543210-->"
    assert ku.existing_hashes(text) == {"abcdef0123456789", "fedcba9876543210"}


def test_existing_hashes_empty_when_none():
    assert ku.existing_hashes("no hashes here") == set()


# ---------------------------------------------------------------------------
# parse_document
# ---------------------------------------------------------------------------
def test_parse_document_extracts_title_from_html():
    html = "<html><head><title>Kirkpatrick Four Levels Explained</title></head><body>2023 content</body></html>"
    entry = ku.parse_document("https://www.atd.org/article", html)
    assert entry is not None
    assert "Kirkpatrick" in entry.title
    assert entry.year == "2023"
    assert entry.venue == "atd.org"


def test_parse_document_returns_none_for_empty():
    assert ku.parse_document("http://x", "") is None
    assert ku.parse_document("http://x", "   ") is None


def test_parse_arxiv_list_finds_ids():
    body = "see arXiv:2301.00001 and also arXiv:2402.00234 in the listing"
    entries = ku.parse_arxiv_list(body, "https://arxiv.org/list/cs/recent")
    assert len(entries) == 2
    assert entries[0].url == "https://arxiv.org/abs/2301.00001"
    assert entries[0].venue == "arXiv"


# ---------------------------------------------------------------------------
# format_entry / append_section / run with a fake fetcher (no network)
# ---------------------------------------------------------------------------
class _FakeFetcher:
    def __init__(self, pages):
        self._pages = pages

    def fetch(self, url):
        return self._pages.get(url)


def test_format_entry_contains_hash_and_relevance():
    e = ku.Entry("Title", "A", "2024", "venue", "https://x", "abs")
    line = ku.format_entry(e, 0.42, "2026-06-30")
    assert "Title" in line
    assert "2026-06-30" in line
    assert "relevance=0.42" in line
    assert f"<!--hash:{ku.url_hash(e.url)}-->" in line


def test_run_dry_run_writes_nothing_and_prints_json(tmp_path, capsys):
    brain = tmp_path / "BRAIN.md"
    brain.write_text("# Brain\n\n## Existing\n- old\n", encoding="utf-8")
    pages = {
        "https://www.atd.org": "<title>competency based promotion framework</title>2024 ATD",
        "https://www.shrm.org": "<title>training ROI Kirkpatrick measurement guide</title>2023 SHRM",
        "https://www.linkedin.com/business/learning": None,
        "https://www.mckinsey.com": None,
    }
    rc = ku.run(
        brain_path=str(brain),
        sources=list(pages.keys()),
        queries=ku.SEARCH_QUERIES,
        arxiv=[],
        dry_run=True,
        fetcher=_FakeFetcher(pages),
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "relevance" in out  # json dry-run payload
    # brain unchanged
    assert "Auto-crawl" not in brain.read_text(encoding="utf-8")


def test_run_appends_new_entries_and_dedupes(tmp_path):
    brain = tmp_path / "BRAIN.md"
    seed = "# Brain\n\n"
    brain.write_text(seed, encoding="utf-8")

    pages = {
        "https://www.atd.org": "<title>competency based promotion framework</title>2024",
    }
    fake = _FakeFetcher(pages)

    # monkeypatch collect_candidates to use the fake fetcher path indirectly:
    orig_collect = ku.collect_candidates

    def patched(fetcher, sources, queries, arxiv):
        entries = []
        for src in sources:
            body = fetcher.fetch(src)
            if body:
                e = ku.parse_document(src, body)
                if e:
                    entries.append(e)
        return entries

    ku.collect_candidates = patched
    try:
        # we still need run() to use our fake fetcher; run() builds its own
        # fetcher, so call the lower-level pieces directly for determinism.
        text = ku.load_brain(str(brain))
        seen = ku.existing_hashes(text)
        entries = patched(fake, list(pages.keys()), ku.SEARCH_QUERIES, [])
        new = ku.select_new(entries, seen, ku.min_relevance())
        assert len(new) == 1
        lines = [ku.format_entry(e, rel, "2026-06-30") for e, rel, _ in new]
        ku.append_section(str(brain), "### Auto-crawl 2026-06-30", lines)
    finally:
        ku.collect_candidates = orig_collect

    after = brain.read_text(encoding="utf-8")
    assert "Auto-crawl 2026-06-30" in after
    assert ku.url_hash("https://www.atd.org") in after

    # second pass: dedup
    seen2 = ku.existing_hashes(after)
    entries2 = patched(fake, list(pages.keys()), ku.SEARCH_QUERIES, [])
    new2 = ku.select_new(entries2, seen2, ku.min_relevance())
    assert new2 == []


def test_run_missing_brain_returns_error_code(tmp_path):
    rc = ku.run(
        brain_path=str(tmp_path / "missing.md"),
        sources=ku.WEB_SOURCES,
        queries=ku.SEARCH_QUERIES,
        arxiv=[],
        dry_run=True,
    )
    assert rc == 2


def test_cli_parser_has_expected_flags():
    p = ku.build_parser()
    ns = p.parse_args(["--dry-run", "--verbose", "--brain", "X.md"])
    assert ns.dry_run is True
    assert ns.verbose is True
    assert ns.brain == "X.md"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))