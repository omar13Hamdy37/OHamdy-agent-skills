---
name: cufe-study-guide
description: "Create intuition-first study guides and comprehensive but intelligently condensed learning notes from supplied university lecture slides, PDFs, documents, or course material, including requests for DOCX/PDF guides. Use for lecture learning and exam revision; excludes unrelated summarization and ordinary document writing."
---

# CUFE Study Guide

Author a guide the student can learn from, with course coverage, reusable mental
models, and practical revision. Portable teaching instructions and a shared-model
DOCX/direct-PDF renderer provide the baseline. Use available capabilities honestly;
detailed decisions live below.

## Task and evidence

Interpret natural-language scope, assumed knowledge, depth, quiz, cheatsheet,
external-material, and output preferences. User instructions override defaults;
resolve correctness/capability conflicts explicitly instead of silently ignoring them.
Lectures define course scope, not necessarily optimal teaching order. Prior guides
are secondary context. Never present an ambiguous source statement as certain, an
optional addition as required, or a guessed exam prediction as course evidence.
The [content-selection reference](references/content-selection.md) owns intake,
classification, provenance, and coverage decisions.

## Workflow

Keep a compact internal inventory, dependency map, and coverage ledger; show only
planning that helps the learner. Do not begin by paraphrasing slides in order.

1. **Inspect and scope.** Read the request and current materials, infer course/subject
   and learner assumptions, check requested ranges, and identify extraction gaps.
2. **Map and select.** Inventory concepts, formulas, algorithms, methods, proofs,
   examples, and visual evidence. Map prerequisites and missing explanatory bridges;
   classify items and record planned dispositions. Inspect relevant supplied prior
   material to resolve dependencies or helpful relationships.
3. **Plan teaching units.** Order sections so prerequisites are established before
   use. Preserve course notation and important material; merge repetitions. Choose
   discipline-appropriate depth, examples, practice, and boundaries for longer guides.
4. **Teach.** Build intuition and mechanisms before unnecessary jargon. Explain
   symbols/diagrams/code, make useful comparisons, resolve misconceptions, and add
   checkpoints. Decide proof depth and optional enrichment at the relevant concept,
   respecting external-material preferences. Revisit the plan when new evidence appears.
5. **Support revision.** Finalize safe conceptual breakpoints; decide whether a
   cheatsheet earns its place. Add the end quiz and separate reasoned Answer Key
   unless waived. Use the dependency map and essential concepts to choose questions.
6. **Audit, render, and verify.** Reconcile coverage, explanations, and answers first.
   Follow [document-design.md](references/document-design.md) to construct validated
   semantic guide data and invoke the packaged renderer or a capable native mechanism.
   Inspect generated artifacts/pages, repair output defects, and return actual file
   paths/links. Disclose material evidence or verification/capability limits.

## Read references at the decision point

For every substantive guide, consult the four core references at their stages;
do not preload conditional references or reread already-loaded guidance unnecessarily.

| Stage or condition | Reference |
| --- | --- |
| Establish priorities and appropriate depth | [learning-philosophy.md](references/learning-philosophy.md) |
| Inspect, map, classify, and audit sources | [content-selection.md](references/content-selection.md) |
| Plan subject-sensitive explanations and activities | [teaching-style.md](references/teaching-style.md) |
| Review final content and resolve defects | [quality-checklist.md](references/quality-checklist.md) |
| Prior material supplied or a prior relationship needs checking | [cross-lecture-connections.md](references/cross-lecture-connections.md) |
| Multiple substantial teaching units need study-session boundaries | [breakpoints.md](references/breakpoints.md) |
| Required proof/derivation, requested depth, or a useful candidate insight | [proofs-and-derivations.md](references/proofs-and-derivations.md) |
| Quiz requested or default quiz stage reached | [quizzes.md](references/quizzes.md) |
| Cheatsheet requested or compact reference material appears useful | [cheatsheets.md](references/cheatsheets.md) |
| Organize the final content for output/export | [document-design.md](references/document-design.md) |

If the user opts out of a conditional feature, skip its reference unless needed
to resolve another decision. The quiz is normally included for substantial guides;
cheatsheets, enrichment, and prior connections require positive reasons.

## Capabilities and limits

- Use available file readers, visual inspection, OCR, or alternate extraction for
  missing source content. Follow supplied paths within the authorized task. If a
  critical gap remains, ask a targeted question; continue independent sections and
  make any delivered partial scope explicit. Never mark unread material covered.
- Search relevant prior files when accessible. An unavailable path cannot support
  a claimed prior-lecture connection; explain the limitation and use current evidence.
- Browse to verify external facts/resources only when allowed and useful. Without
  access, use supplied evidence and established explanations, label uncertainty,
  and never invent links. “No external material” excludes external enrichment and
  retrieval, not ordinary unpacking of the supplied course concepts.
- Normally target both DOCX and PDF, or the requested subset. Select available
  host-native tools or the package-relative `scripts/run_renderer.py` baseline.
  The bootstrap uses an isolated cached runtime; do not install globally or write
  generated files inside the installed plugin. If a requested format is unsupported,
  deliver supported content/output and name the limitation. Do not claim successful
  export or visual verification without doing it.

The runtime package is self-contained: references hold teaching decisions, while
scripts/assets are optional helpers. Repository specifications govern development,
not runtime loading. Normal execution must not rewrite skill files or depend on
developer evals. Personalize through the teaching choices, not repeated references
to the student's identity.
