# PROJECT-detail.md - Internal Training & Personalized Promotion Path Designer (Skill #141)

## Executive Summary
Designs internal training programs and personalized promotion paths using modern
HR and learning-design frameworks. This skill is a full Claude harness in the
**business-operations** cluster. It runs a research-first, framework-grounded
workflow that scores the subject against named world-renowned methodologies, runs
a devil's-advocate challenge, and returns a prioritized improvement roadmap, while
continuously updating its knowledge base.

## Problem Statement
Internal training is often generic and promotions opaque, driving disengagement and
attrition. This skill designs evidence-based, competency-mapped development and
advancement paths and makes the criteria for advancement transparent and fair.

## Target Users & Use Cases
Practitioners, reviewers, and decision-makers who need an expert-grade,
evidence-based assessment in this domain. Trigger examples:
1. **Onboarding program** - "Design onboarding for new sales hires" -> competency map, ADDIE program, 70-20-10 blend, Kirkpatrick eval, roadmap.
2. **Promotion ladder** - "Make a transparent path from junior to senior engineer" -> competency levels, criteria, evidence required, fairness checks.
3. **ROI measurement** - "How do I prove training works?" -> Kirkpatrick/Phillips measurement plan, KPIs, data collection.
4. **Bias check** - "Are our promotions biased?" -> flags subjective criteria, structured rubric, equity scoring.
5. **Degraded mode** - "Design offline" -> falls back to SECOND-KNOWLEDGE-BRAIN, signals it cannot fetch latest trends.

## Harness Architecture
```
/internal-training-promotion-designer (skills/main.md)
  |-- sub-intake .................... gather inputs & scope
  |-- sub-framework-selector ...... choose world-renowned framework(s)
  |-- [research] WebSearch/WebFetch + SECOND-KNOWLEDGE-BRAIN
  |-- sub-scoring-engine .......... multi-dimensional weighted scoring
  |-- [challenge] devil's-advocate assumption review
  |-- sub-improvement-roadmap ..... prioritized effort x impact actions
  `-- synthesize .................. professional deliverable + quality gates
```

## Full Sub-Skill Catalog
### sub-intake - Intake & Context Gathering
- **Purpose:** Convert a loose request into a structured `case_profile` (subject, audience, goal, constraints, existing artifacts, known gaps, offline flag, assumptions).
- **Inputs:** raw user request + any attached artifacts.
- **Outputs:** `case_profile` object + one-paragraph restatement.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** all required schema fields populated (from user or explicit assumption); case_type classified; assumptions labeled.

### sub-framework-selector - Evaluation Framework Selector
- **Purpose:** Pick the best-fit named framework(s) and justify against the case profile.
- **Inputs:** `case_profile`.
- **Outputs:** `framework_selection` (primary + up to 2 supporting, justification, not_covered, confidence).
- **Tools:** Read, WebSearch/WebFetch.
- **Quality gate:** primary framework named and citable; justification references the case profile; fit/misfit signals stated; confidence downgraded when assumptions exist.

### sub-scoring-engine - Scoring Engine
- **Purpose:** Apply the rubric to produce weighted 0-100 scores with citations, weighted total, and letter grade.
- **Inputs:** `case_profile`, `framework_selection`, research.
- **Outputs:** `scorecard` (per-dimension scores, citations, certainty, degraded_dimensions, summary).
- **Tools:** Read, WebSearch/WebFetch.
- **Quality gate:** every dimension cited; scores map to stated rubric bands; weighted total consistent with grade; degraded dimensions capped at Medium certainty.

### sub-improvement-roadmap - Improvement Roadmap
- **Purpose:** Generate prioritized, effort x impact-ranked recommendations traceable to findings; separate quick wins from strategic moves.
- **Inputs:** `scorecard` + challenge results.
- **Outputs:** `roadmap` (quick_wins, strategic_moves, sequencing, projected_grade with math, risks_to_delivery).
- **Tools:** Read.
- **Quality gate:** every recommendation traces to a finding; effort/impact/lift/owner populated; equity items never deprioritized below cosmetic items.

## Evaluation Frameworks (World-Renowned, Citable)
| Framework / Standard | Origin / citable body | Role in this skill |
|---|---|---|
| ADDIE | Florida State University (1975), ATD | Instructional-design process (Analyze-Design-Develop-Implement-Evaluate). |
| SAM | Michael Allen, Allen Interactions / ASTD Press (2012) | Iterative, agile alternative to ADDIE. |
| Kirkpatrick 4 Levels | Donald Kirkpatrick (1959), Kirkpatrick Partners | Training evaluation: Reaction-Learning-Behavior-Results. |
| Phillips ROI Methodology | Jack J. Phillips, ROI Institute | Adds Level 5 ROI + isolation of effects. |
| 70-20-10 model | Lombardo & Eichinger, Center for Creative Leadership (1996) | Experiential/social/formal learning blend. |
| Bloom's Taxonomy | Bloom (1956); Anderson & Krathwohl (2001) | Cognitive learning-objective leveling. |
| Competency frameworks & 9-box grid | SHRM competency model; Dreyfus; McKinsey/GE | Skill mapping and performance-potential talent review. |
| Equity / structured rubric | structured-interview & blind-review research | Bias removal in promotion criteria. |

## Evidence Hierarchy (prefer higher when sources conflict)
Systematic Review / Meta-Analysis > RCT > Cohort / Longitudinal > Case Study >
Peer-reviewed practitioner research > Standards-body publications (ATD, SHRM, WEF, ISO) >
Vendor research with disclosed methodology > Expert opinion > Blog/marketing.

## Scoring Model
| Dimension | Weight | What is assessed |
|---|---|---|
| Competency mapping | 25% | role competencies defined vs. measured gaps; level descriptors |
| Learning design quality | 20% | objectives (Bloom verbs), 70-20-10 blend, ADDIE/SAM rigor |
| Promotion-path clarity | 20% | transparent, level-by-level criteria, evidence to advance |
| Measurement & ROI | 20% | Kirkpatrick levels, KPIs, data-collection plan, Phillips ROI |
| Equity & engagement | 15% | structured rubrics, bias removal, motivation design |

Each dimension is scored 0-100 with cited evidence; the weighted total yields a
letter grade (A: 90+, B: 75-89, C: 60-74, D: <60). Rationale: weights emphasize
competency mapping (the foundation) and split design/clarity/measurement evenly,
with equity weighted enough that opaque or biased criteria cannot score A.

## Skill File Format Specification
- Frontmatter: `name`, `description`.
- Required sections: Role & Persona, Workflow (Harness Flow), Sub-skills Available,
  Tools, Output Format, Quality Gates (plus Scope & Error Handling in main.md).

## E2E Execution Flow
1. Parse user request; if inputs insufficient, `sub-intake` asks targeted questions.
2. `sub-framework-selector` picks framework(s) and justifies the choice.
3. Research stage gathers highest-tier evidence; degrade gracefully to
   SECOND-KNOWLEDGE-BRAIN if offline.
4. `sub-scoring-engine` scores each dimension with citations.
5. Challenge stage stress-tests the top assumptions and grades certainty.
6. `sub-improvement-roadmap` produces ranked, traceable actions.
7. Synthesize deliverable; run Quality Gates; present.

**Error handling:** missing inputs -> ask, then assume + downgrade certainty;
conflicting evidence -> present both, prefer higher tier, grade certainty Medium;
tool failure -> fallback + explicit limitation notice; out-of-scope (legal,
compensation) -> flag and hand off, never assert.

## SECOND-KNOWLEDGE-BRAIN Integration
- Sources: ATD, SHRM, LinkedIn Learning (business), McKinsey.
- ArXiv categories: n/a (domain relies on standards bodies and practitioner literature).
- Crawl queries: skills taxonomy future of jobs WEF; learning experience design evidence;
  competency based promotion framework; training ROI Kirkpatrick measurement.
- Append format: dated `### Auto-crawl YYYY-MM-DD` sections with Title, Venue, Year,
  URL, relevance score, and a `<!--hash:-->` dedup tag.
- Updater: `tools/knowledge_updater.py` (crawl4ai primary, urllib fallback,
  `--dry-run` to preview, weekly cron recommended).

## Supporting Tools Spec
`tools/knowledge_updater.py`: inputs = source list + queries; outputs = appended
SECOND-KNOWLEDGE-BRAIN entries; schedule = weekly cron; dedup by URL/DOI hash;
graceful degradation (exit 0) when network unavailable. Pluggable `Fetcher`
protocol enables deterministic unit testing without a network.

## Quality Gates (must all pass before final output)
- Every score cites at least one source or the chosen framework.
- Challenge stage completed; top assumptions tested; certainty graded.
- Roadmap items prioritized by effort x impact and traceable to findings.
- Limitations and evidence certainty stated explicitly.
- Out-of-scope items flagged, not asserted.
- Offline/degraded mode, if used, bannered at the top of the report.

## Test Scenarios
See `tests/test-scenarios.md` (6 scenarios: onboarding, promotion ladder, ROI,
bias check, degraded mode, out-of-scope guardrail) and `tests/test_knowledge_updater.py`
(16 pure-function unit tests).

## Key Design Decisions
1. Framework-grounded scoring (no ad-hoc criteria).
2. Research-first with graceful degradation to the local knowledge brain.
3. Mandatory challenge stage to counter confirmation bias.
4. Standard quality gates enforced before delivery.
5. Equity items are non-negotiable in roadmap prioritization.
6. Self-improving knowledge base via weekly crawl (dedup + relevance filtering).
7. Pluggable fetcher for deterministic, network-free testing.