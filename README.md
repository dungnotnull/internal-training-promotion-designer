# Internal Training & Personalized Promotion Path Designer

> Skill #141 - business-operations cluster
> Status: v1 - production-grade, open-source ready

Design competency-based internal training programs and transparent, personalized
promotion paths using named, world-renowned HR and learning-design frameworks.
This Claude skill runs a research-first, framework-grounded workflow: it scores
your case on a weighted rubric, runs a devil's-advocate challenge, and returns a
prioritized improvement roadmap - while continuously growing a self-improving
knowledge base.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-16%20passed-brightgreen.svg)](tests/test_knowledge_updater.py)
[![Cluster](https://img.shields.io/badge/cluster-business--operations-purple.svg)](#cross-skill-wiring)

---

## Table of Contents

1. [Why this skill exists](#why-this-skill-exists)
2. [Features](#features)
3. [Frameworks used](#frameworks-used)
4. [Scoring model](#scoring-model)
5. [How it works](#how-it-works)
6. [Repository structure](#repository-structure)
7. [Quick start](#quick-start)
8. [Keeping the knowledge base current](#keeping-the-knowledge-base-current)
9. [Testing](#testing)
10. [Scope and boundaries](#scope-and-boundaries)
11. [Cross-skill wiring](#cross-skill-wiring)
12. [Contributing](#contributing)
13. [License](#license)

---

## Why this skill exists

Internal training is often **generic** and promotions are often **opaque** - two
conditions that quietly drive disengagement, regrettable attrition, and weakened
succession pipelines. This skill produces **evidence-based, competency-mapped**
development and advancement paths with transparent, fair, and auditable criteria.

It is designed for L&D leads, people-operations partners, engineering managers,
and DEI partners who need an expert-grade assessment grounded in recognized
methodology rather than opinion.

## Features

- **Framework-grounded scoring.** Every judgment maps to a named, citable framework
  (ADDIE/SAM, Kirkpatrick/Phillips, 70-20-10, Bloom, competency frameworks, 9-box
  grid, structured-rubric equity) - never ad-hoc criteria.
- **Research-first with graceful degradation.** Uses live web research when
  available and falls back to the local knowledge brain when offline, clearly
  bannered as "degraded mode".
- **Devil's-advocate challenge stage.** Tests the top assumptions and grades
  certainty (High/Medium/Low) per finding to counter confirmation bias.
- **Weighted, reproducible scorecard.** Five dimensions, a weighted total, and a
  letter grade, each score cited.
- **Traceable roadmap.** Quick wins vs. strategic moves, every action linked to a
  scored finding, with effort x impact prioritization and projected-grade math.
- **Equity is non-negotiable.** Equity recommendations are never deprioritized
  below cosmetic items, no matter their effort/impact ratio.
- **Self-improving knowledge base.** A crawl pipeline (crawl4ai primary, urllib
  fallback) appends dated, deduplicated, relevance-scored entries weekly.
- **Network-free testing.** A pluggable fetcher makes the pipeline fully unit
  testable without any network access.

## Frameworks used

| Framework | Origin / citable body | Role |
|---|---|---|
| ADDIE | Florida State University (1975), ATD | Instructional-design process: Analyze, Design, Develop, Implement, Evaluate |
| SAM | Michael Allen, Allen Interactions / ASTD Press (2012) | Iterative, agile alternative to ADDIE |
| Kirkpatrick 4 Levels | Donald Kirkpatrick (1959), Kirkpatrick Partners | Evaluation: Reaction, Learning, Behavior, Results |
| Phillips ROI | Jack J. Phillips, ROI Institute | Level 5 ROI plus isolation of effects |
| 70-20-10 | Lombardo & Eichinger, Center for Creative Leadership (1996) | Experiential / social / formal learning blend |
| Bloom's Taxonomy | Bloom (1956); Anderson & Krathwohl (2001) | Cognitive learning-objective leveling |
| Competency frameworks & 9-box | SHRM; Dreyfus; McKinsey/GE | Skill mapping and performance x potential talent review |
| Structured rubric | structured-interview & blind-review research | Bias removal in promotion criteria |

**Evidence hierarchy (used when sources conflict):**
Systematic Review / Meta-Analysis > RCT > Cohort / Longitudinal > Case Study >
Peer-reviewed practitioner research > Standards-body publications (ATD, SHRM, WEF, ISO)
> Vendor research with disclosed methodology > Expert opinion > Blog/marketing.

## Scoring model

| Dimension | Weight | What is assessed |
|---|---|---|
| Competency mapping | 25% | Role competencies defined vs. measured gaps; level descriptors |
| Learning design quality | 20% | Objectives (Bloom verbs), 70-20-10 blend, ADDIE/SAM rigor |
| Promotion-path clarity | 20% | Transparent, level-by-level criteria; evidence required to advance |
| Measurement & ROI | 20% | Kirkpatrick levels, KPIs, data-collection plan, Phillips ROI |
| Equity & engagement | 15% | Structured rubrics, bias removal, motivation design |

Letter grade: **A** 90-100, **B** 75-89, **C** 60-74, **D** below 60.

## How it works

The harness runs a fixed stage order. Each stage emits a structured result the
next stage consumes. Stages cannot be skipped; quality gates block the flow on
failure.

```
/intake/sub-intake ............... gather inputs, scope, goals, constraints
  |
/framework/sub-framework-selector . pick + justify named framework(s)
  |
research ........................ WebSearch/WebFetch + SECOND-KNOWLEDGE-BRAIN
  |
/scoring/sub-scoring-engine ...... weighted 0-100 scores + letter grade
  |
challenge ........................ devil's advocate on top assumptions
  |
/roadmap/sub-improvement-roadmap . quick wins vs. strategic moves, traceable
  |
synthesize ...................... professional report + quality gates
```

**Quality gates (all must pass before the report is delivered):**
- Every score cites a source or the chosen framework.
- The challenge stage tested the top assumptions; certainty is graded.
- Every roadmap item is prioritized by effort x impact and traceable to a finding.
- Limitations and evidence certainty are stated explicitly.
- Out-of-scope items (legal, compensation) are flagged, not asserted.
- Offline/degraded mode, if used, is bannered at the top of the report.

## Repository structure

```
internal-training-promotion-designer/
  CLAUDE.md                         Skill manifest for the harness
  README.md                         This file
  LICENSE                            MIT
  PROJECT-detail.md                  Full technical spec
  PROJECT-DEVELOPMENT-PHASE-TRACKING.md   Phase roadmap and status
  SECOND-KNOWLEDGE-BRAIN.md          Self-improving knowledge base
  skills/
    main.md                          Harness entry point (stage order, gates)
    sub-intake.md                    Intake and context gathering
    sub-framework-selector.md        Framework selection and justification
    sub-scoring-engine.md            Weighted multi-dimensional scoring
    sub-improvement-roadmap.md       Prioritized effort x impact roadmap
  tools/
    knowledge_updater.py             crawl4ai + urllib knowledge pipeline
    requirements.txt                  Python dependencies
  tests/
    test-scenarios.md                Six end-to-end harness scenarios
    test_knowledge_updater.py        Sixteen pure-function unit tests (no network)
```

## Quick start

This is a Claude skill. Load this directory as a skill (see `CLAUDE.md`), then
prompt it directly.

**Example prompts:**

- `Design onboarding for new sales hires.`
- `Make a transparent path from junior to senior engineer.`
- `How do I prove training works?`
- `Are our promotions biased?`

The harness runs the seven stages and emits the report defined in
`skills/main.md`: Executive Summary, Context & Scope, Dimension Scores, Findings
& Risks, Challenge Results, Improvement Roadmap, Limitations & Certainty, and
Sources.

## Keeping the knowledge base current

`tools/knowledge_updater.py` grows `SECOND-KNOWLEDGE-BRAIN.md` with dated,
deduplicated, relevance-scored entries. Recommended schedule: weekly (cron or
systemd timer).

Install dependencies (crawl4ai is optional; the urllib fallback is always
available):

```bash
pip install -r tools/requirements.txt
```

Preview what would be appended (writes nothing):

```bash
python tools/knowledge_updater.py --dry-run
```

Run a live update (scheduled weekly, not on-demand):

```bash
python tools/knowledge_updater.py
```

Verbose logging, or override sources:

```bash
python tools/knowledge_updater.py --verbose
python tools/knowledge_updater.py --sources https://www.atd.org https://www.shrm.org
```

CLI flags:

| Flag | Purpose |
|---|---|
| `--dry-run` | Print the JSON candidate payload; do not write to the brain |
| `--verbose` | DEBUG-level logging |
| `--brain PATH` | Override the path to SECOND-KNOWLEDGE-BRAIN.md |
| `--sources URL ...` | Override the web sources list |
| `--queries Q ...` | Override the search-queries list |
| `--arxiv CAT ...` | Override ArXiv categories (empty by default for this domain) |

The pipeline degrades gracefully: if no fetcher can reach the network, it logs an
INFO message and exits 0 so the skill keeps working off the existing brain.

## Testing

End-to-end harness scenarios are documented in `tests/test-scenarios.md`:

1. Onboarding program (happy path)
2. Promotion ladder (clarity focus)
3. Training evaluation / ROI (measurement focus)
4. Equity / bias check (non-negotiable)
5. Degraded / offline mode
6. Out-of-scope guardrail

Pure-function unit tests run without any network access:

```bash
pytest tests/test_knowledge_updater.py -v
```

Expected: **16 passed**.

## Scope and boundaries

**In scope:** internal training program design, competency maps, learning
blends, promotion ladders and criteria, training evaluation and ROI plans, and
equity/bias checks on promotion criteria.

**Out of scope** (the skill flags these and recommends a qualified reviewer; it
never asserts them): statutory employment-law advice, individual performance
improvement plans that require HRIS data access, and salary-band compensation
benchmarking.

## Cross-skill wiring

This skill belongs to the `business-operations` cluster and is composable with
sibling skills. Its sub-skills are reusable building blocks:

- `sub-intake` - the structured `case_profile` schema is portable to any cluster
  skill needing intake (audience, goal, constraints, offline flag, assumptions).
- `sub-framework-selector` - the "pick + justify a named framework" protocol
  (fit/misfit signals, justification, not_covered, confidence) is portable.
- `sub-scoring-engine` - the weighted-scoring pattern (scorecard schema, certainty
  and downgrade rules) is reusable; downstream skills supply their own dimensions.
- `sub-improvement-roadmap` - the traceable effort x impact prioritization is
  reusable; downstream skills supply their own findings.

Composition contract: each sub-skill accepts the upstream stage's structured
object and emits its own structured object (see the Output section of each
sub-skill file). Sibling skills must respect that schema to chain cleanly.

## Contributing

Contributions are welcome. Please keep the following in mind:

- Keep every judgment framework-grounded and cited; no ad-hoc criteria.
- Preserve the fixed stage order and the quality gates.
- Add or update `tests/test-scenarios.md` and `tests/test_knowledge_updater.py`
  for any behavioral change; the unit tests must stay network-free.
- Run the verification steps before submitting:

```bash
python -m py_compile tools/knowledge_updater.py tests/test_knowledge_updater.py
pytest tests/test_knowledge_updater.py -q
python tools/knowledge_updater.py --dry-run
```

## License

Released under the MIT License. See [LICENSE](LICENSE).