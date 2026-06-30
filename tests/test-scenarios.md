# Test Scenarios - Internal Training & Personalized Promotion Path Designer (Skill #141)

These scenarios validate the harness end-to-end: stage order, framework grounding,
scoring with citations, gates, roadmap traceability, and graceful degradation.
Each scenario lists the user input, expected behavior, stage-by-stage assertions,
explicit pass criteria, and edge-case probes. Run them by executing the harness
against the given input and checking every assertion.

Minimum 5 scenarios (below). Add real user runs to Regression Notes as they occur.

---

### Scenario 1: Onboarding program (happy path)
- **User input:** "Design onboarding for new sales hires."
- **Expected behavior:** Skill builds a competency map, an ADDIE program, a 70-20-10 blend, a Kirkpatrick evaluation plan, and a roadmap.
- **Stage assertions:**
  1. sub-intake classifies case_type: onboarding program and emits a full case_profile.
  2. sub-framework-selector selects ADDIE primary, with 70-20-10, Bloom, Kirkpatrick supporting; justification names the case profile.
  3. Research stage returns at least one cited source per dimension (or degraded flag).
  4. sub-scoring-engine returns five 0-100 scores with citations and a weighted total.
  5. Challenge stage tests the top 3 assumptions; certainty graded.
  6. sub-improvement-roadmap returns quick wins + strategic moves, each traceable.
- **Pass criteria:** correct stage order; framework named and citable; every score cited; roadmap prioritized by effort x impact; limitations stated.
- **Edge probes:** what if sales-hire count is unknown? -> assumption recorded, certainty downgraded.

### Scenario 2: Promotion ladder (clarity focus)
- **User input:** "Make a transparent path from junior to senior engineer."
- **Expected behavior:** Skill defines competency levels, evidence required to advance, fairness checks.
- **Stage assertions:**
  1. Intake classifies promotion ladder; captures levels and current criteria (or assumptions).
  2. Framework selector picks Competency framework primary, Bloom + Equity/structured rubric supporting.
  3. Scoring weights Promotion-path clarity (20%) heavily; flags any subjectivity.
  4. Roadmap includes a structured-rubric recommendation if promotion criteria were subjective.
- **Pass criteria:** stage order correct; competency levels explicit; evidence-to-advance stated; equity recommendation present if subjective; limitations stated.

### Scenario 3: Training evaluation / ROI (measurement focus)
- **User input:** "How do I prove training works?"
- **Expected behavior:** Skill designs a Kirkpatrick Levels 1-4 plan with KPIs, a data-collection plan, and Phillips ROI where dollars are required.
- **Stage assertions:**
  1. Intake classifies training evaluation / ROI; asks if dollars/ROI required.
  2. Framework selector picks Kirkpatrick 4 Levels primary, Phillips ROI + 70-20-10 supporting.
  3. Scoring Measurement & ROI dimension cites Kirkpatrick and (if ROI) Phillips.
  4. Roadmap includes a data-collection / isolation-of-effects action.
- **Pass criteria:** all 4 Kirkpatrick levels addressed; KPIs named; data-collection plan present; limitations stated.

### Scenario 4: Equity / bias check (non-negotiable)
- **User input:** "Are our promotions biased?"
- **Expected behavior:** Skill flags subjective criteria, recommends structured rubric and blind/standardized review, scores equity low if criteria are opaque.
- **Stage assertions:**
  1. Intake captures existing criteria and any fairness data.
  2. Framework selector picks Equity/structured rubric primary, 9-box + Competency supporting.
  3. Scoring flags Equity & engagement certainty; opaque criteria score low.
  4. Roadmap equity items are NOT deprioritized below cosmetic items (per sub-improvement-roadmap gate).
- **Pass criteria:** subjective criteria flagged; structured-rubric recommendation present; equity roadmap items prioritized correctly; out-of-scope legal conclusions flagged, not asserted.

### Scenario 5: Degraded / offline mode
- **User input:** "Design offline." (or any run where WebSearch/WebFetch/crawl4ai fail)
- **Expected behavior:** Harness completes off SECOND-KNOWLEDGE-BRAIN, labels the report DEGRADED MODE, states the snapshot date, and downgrades Measurement & ROI + Equity to certainty Medium at most.
- **Stage assertions:**
  1. Intake sets offline_mode: true.
  2. Research stage skips live fetch, loads the brain, states the snapshot date.
  3. Scoring lists degraded_dimensions; no dimension certainty High.
  4. Report top banner states "DEGRADED MODE - knowledge base snapshot dated YYYY-MM-DD".
- **Pass criteria:** stage order intact; frameworks still named; scores cite brain entries; degraded banner present; limitations explicit.

### Scenario 6: Out-of-scope guardrail
- **User input:** "Set salary bands for senior engineers."
- **Expected behavior:** Skill flags compensation benchmarking as out of scope, refuses to assert salary numbers, and recommends a qualified reviewer.
- **Pass criteria:** no salary numbers asserted; out-of-scope flag present; handoff recommended; L&D-relevant guidance (competency leveling) still provided.

---

## Regression Notes
- Append real user runs here as new scenarios with their pass/fail outcomes.
- Run the knowledge updater in dry-run mode to verify the pipeline produces well-formed, deduplicated entries without writing.
- Run the pytest suite to verify pure functions (relevance, dedup, parsing, formatting) without network access.