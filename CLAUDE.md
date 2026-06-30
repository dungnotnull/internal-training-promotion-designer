# CLAUDE.md - Internal Training & Personalized Promotion Path Designer (Skill #141)

**Slug:** `internal-training-promotion-designer`  -  **Cluster:** `business-operations`  -  **Source idea:** 141  -  **Phase:** Built (v1, production-grade)

## Tagline
Designs internal training programs and personalized promotion paths using modern HR and learning-design frameworks.

## Problem This Skill Solves
Internal training is often generic and promotions opaque, driving disengagement and attrition. This skill designs evidence-based, competency-mapped development and advancement paths with transparent, fair criteria.

## Harness Flow Summary
1. **Intake** (`sub-intake`) - structured `case_profile`.
2. **Framework selection** (`sub-framework-selector`) - named, citable, justified.
3. **Research** (WebSearch/WebFetch + SECOND-KNOWLEDGE-BRAIN) - highest-tier evidence; degrade gracefully offline.
4. **Scoring** (`sub-scoring-engine`) - weighted 0-100 scores with citations + letter grade.
5. **Challenge** - devil's-advocate review of the top assumptions; certainty graded.
6. **Roadmap** (`sub-improvement-roadmap`) - prioritized quick wins vs. strategic moves, traceable.
7. **Synthesize** - professional deliverable; Quality Gates enforced before presenting.

## Gates
- Every score cites a source or the chosen framework.
- Challenge stage completed; top assumptions tested; certainty graded.
- Roadmap items prioritized by effort x impact and traceable to findings.
- Limitations and evidence certainty stated explicitly.
- Out-of-scope items (legal, compensation) flagged, not asserted.
- Offline/degraded mode bannered at the top of the report.

## Sub-skills
- `skills/sub-intake.md` - Intake & Context Gathering: collect the structured inputs, scope, and goals; ask clarifying questions only for what is missing; record explicit assumptions.
- `skills/sub-framework-selector.md` - Evaluation Framework Selector: pick the best-fit named framework(s) and justify the choice against the case profile (with fit/misfit signals).
- `skills/sub-scoring-engine.md` - Scoring Engine: apply the multi-dimensional rubric to produce weighted scores with evidence citations, a weighted total, and a letter grade.
- `skills/sub-improvement-roadmap.md` - Improvement Roadmap: prioritized, effort x impact-ranked recommendations traceable to findings; quick wins separated from strategic moves.

## Cross-Skill Wiring (business-operations cluster)
This skill is composable with sibling skills in the `business-operations` cluster. The sub-skills below are reusable as building blocks by other cluster skills:
- `sub-intake` reusable by any cluster skill needing a structured `case_profile` (audience, goal, constraints, offline flag, assumptions).
- `sub-framework-selector` reusable as a generic "pick + justify a named framework" stage; the framework catalog is domain-specific, but the selection protocol (fit/misfit signals, justification, not_covered, confidence) is cluster-portable.
- `sub-scoring-engine` reusable as a weighted-scoring pattern; downstream skills supply their own dimensions/weights/citations and reuse the scorecard schema and certainty/downgrade rules.
- `sub-improvement-roadmap` reusable as a traceable, effort x impact prioritization stage; downstream skills supply their findings and reuse the quick-win/strategic-move bucketing and projected-grade math.

Sibling skills that can compose with this one (as the cluster grows):
- Talent/skills-gap analysis skills -> consume `sub-scoring-engine` competency-mapping dimension.
- Org-design / role-architecture skills -> consume `sub-framework-selector` and `sub-improvement-roadmap`.
- Employee-engagement & retention skills -> consume `sub-intake` and the Equity & engagement dimension.
- Performance-review design skills -> consume `sub-framework-selector` (structured rubric) and `sub-improvement-roadmap`.

Composition contract: each sub-skill accepts the upstream stage's structured object and emits its own structured object (see the Output section in each sub-skill file). Sibling skills must respect that schema to chain cleanly.

## Tools Required
- `WebSearch`, `WebFetch` - live evidence and standards updates.
- `Read`, `Write` - load knowledge base, emit deliverables.
- `Bash` - run `tools/knowledge_updater.py` (use `--dry-run` for previews; live runs are scheduled, not on-demand).
- Skill tool - invoke sub-skills in sequence.

## Knowledge Sources
- ArXiv: n/a (domain relies on standards bodies and practitioner literature).
- Authoritative domain sources:
  - https://www.atd.org
  - https://www.shrm.org
  - https://www.linkedin.com/business/learning
  - https://www.mckinsey.com
- Crawl queries: skills taxonomy future of jobs WEF; learning experience design evidence; competency based promotion framework; training ROI Kirkpatrick measurement.

## Supporting Tools
- `tools/knowledge_updater.py` - crawl4ai-primary, urllib-fallback pipeline that grows `SECOND-KNOWLEDGE-BRAIN.md` (weekly cron recommended). Deduplicates by URL/DOI hash; degrades gracefully (exit 0) when offline.

## Active Development Tasks
- [x] Scaffold full deliverable set
- [x] Define 4 deep sub-skills with real domain content
- [x] Production-grade `tools/knowledge_updater.py` (pluggable fetcher, dry-run, dedup, graceful degradation)
- [x] SECOND-KNOWLEDGE-BRAIN seeded with cited framework references
- [x] Test scenarios (6) + pytest pure-function suite (16 tests, no network)
- [x] Open-source scaffolding (README, LICENSE, requirements)
- [x] Cross-skill wiring documented for the business-operations cluster
- [ ] Expand SECOND-KNOWLEDGE-BRAIN via first scheduled live crawl
- [ ] Add regression cases from real user runs

## Related Root Docs
- `README.md` - open-source readme.
- `PROJECT-detail.md` - full technical spec.
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` - phase roadmap & status.
- `SECOND-KNOWLEDGE-BRAIN.md` - self-improving knowledge base.