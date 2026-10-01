# CUFE Study Guide eval foundation

These are developer/regression tests, not runtime dependencies. The distributable
plugin must work without this directory. Phase 1 reserves directories and the
testing plan; no fixtures, grader implementations, or eval runner exist yet.

## Directory responsibilities

- `cases/`: future prompts, expected outcomes, preferences, and requirement IDs.
- `fixtures/`: future real lecture inputs, previous lectures/guides, and small
  inspectable output references with provenance and appropriate reuse permission.
- `graders/`: future deterministic checks and learning/design grading rubrics.
- Generated run artifacts belong in ignored `runs/` or `results/` directories.

## Planned categories

| Category | What future checks assess |
| --- | --- |
| should-trigger | Supplied lecture slides/PDFs/documents requested as study guides, learning notes, or DOCX/PDF revision material. |
| should-not-trigger | Unrelated summarization, ordinary document writing, and requests without the lecture-learning use case. |
| lecture coverage | Important concepts, formulas, diagrams, and justified condensation/omission in the coverage audit. |
| terminology quality | Unfamiliar terms explained at first meaningful use; ordinary words not overdefined. |
| conceptual clarity | Intuition, mechanisms, bridges, comparisons, and appropriate technical depth. |
| breakpoint quality | Useful approximate 30-minute sessions without broken dependency chains. |
| cross-lecture relationships | Relevant, grounded prerequisites, continuations, contrasts, and applications. |
| quiz quality | Meaningful understanding tests, preference adaptation, separated Answer Key, and correct reasoning. |
| proof classification | Lecture proof versus optional understanding aid versus linked extended proof. |
| cheatsheet decisions | Included when requested or useful; omitted when it adds little value. |
| DOCX generation | Requested artifact exists and preserves content, structure, and semantic styles. |
| PDF generation | Requested artifact exists and preserves readable content and working links. |
| visual/render checks | Page layout, readable formulas/tables/code, callouts, hierarchy, and accessibility. |

## Complementary grading

**Deterministic checks** will verify artifact existence, requested formats,
expected sections, a separate Answer Key for substantial guides unless waived,
syntactically valid links, required metadata when known/requested, and structural
invariants. Do not require invented course metadata or report-style cover fields.
Link syntax does not prove that a destination works; check external reachability
separately when network access permits it.

**Rubric/model grading** will assess explanation quality, beginner-friendliness,
conceptual completeness, useful progressive examples, accurate relationships,
quiz reasoning, and whether breakpoints preserve learning continuity. Render
inspection will assess the actual exported pages. Existence checks alone cannot
establish good pedagogy or polished output.

Map future cases to the [v1 specification](../../docs/specs/cufe-study-guide-v1.md)
and its acceptance criteria. Define evidence-based pass conditions and diagnose
failures instead of grading exact wording or copying implementation instructions.

## Phase 4 loop

**build → eval → diagnose → repair → rerun** is the developer workflow. Preserve
failed-run evidence and review changes to the skill, helpers, and graders. Normal
student execution must never rewrite the skill to improve its own evaluation score.
