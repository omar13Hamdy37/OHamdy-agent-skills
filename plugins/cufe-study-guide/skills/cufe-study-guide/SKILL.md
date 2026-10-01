---
name: cufe-study-guide
description: "Turn supplied university lecture slides, PDFs, or documents into structured study guides and comprehensive but intelligently condensed study notes, including DOCX/PDF guides from course material. Use for learning and revision from lectures; excludes unrelated summarization and ordinary document writing."
---

# CUFE Study Guide

Transform lecture material into a guide the student can learn from: preserve
important course content, build understanding, and support practical revision.

## Development status

This is the Phase 1 skeleton. The references record intended requirements and
Phase 2 work; the full teaching system and document generators are not implemented.
Do not represent this scaffold as a finished, validated study-guide workflow.
Detailed behavior belongs in the references rather than a growing entrypoint.

## High-level workflow

1. Inspect supplied lectures, relevant prior material, and the user's preferences.
2. Identify meaningful concepts, formulas, diagrams, and dependencies; plan
   coverage and purposeful condensation.
3. Teach with intuition, explanations, progressive examples, and practice suited
   to the subject. Add relevant prior-lecture connections and natural breakpoints.
4. Add understanding checkpoints, a meaningful quiz with a separate Answer Key,
   and a cheatsheet when useful or requested.
5. Audit coverage and technical correctness. Create the requested document formats
   with available host tooling and verify rendered outputs when implemented.

## Reference routing

Read references as their decisions become relevant; do not load every file by default.

| Decision | Reference |
| --- | --- |
| Learning priorities and intuition-first organization | [learning-philosophy.md](references/learning-philosophy.md) |
| Content selection and source coverage | [content-selection.md](references/content-selection.md) |
| Terminology, examples, bridges, comparisons, and practice | [teaching-style.md](references/teaching-style.md) |
| Relevant prior material and relationship types | [cross-lecture-connections.md](references/cross-lecture-connections.md) |
| Conceptual stopping points around focused study sessions | [breakpoints.md](references/breakpoints.md) |
| Quiz preferences and separated, reasoned answers | [quizzes.md](references/quizzes.md) |
| Course proofs, optional insights, and extended proofs | [proofs-and-derivations.md](references/proofs-and-derivations.md) |
| Whether and how to include a cheatsheet | [cheatsheets.md](references/cheatsheets.md) |
| DOCX/PDF presentation and accessibility | [document-design.md](references/document-design.md) |
| Final coverage, learning, and rendered-output checks | [quality-checklist.md](references/quality-checklist.md) |

## Source-of-truth hierarchy

- User instructions and preferences set the task and requested outputs.
- Supplied lectures define course scope and required material. Prior material
  supplies context; external sources may clarify or enrich, not silently replace
  the syllabus. Flag source ambiguity or technical errors rather than inventing facts.
- This entrypoint and packaged references define the runtime workflow. Keep
  course content, added explanation, and optional enrichment distinguishable where
  exam expectations depend on the distinction.
- During development, the repository v1 specification is authoritative until
  translated into operational references. It is not an installed runtime dependency.

Keep teaching decisions portable. Scripts and assets are optional helpers; select
available Codex or ChatGPT Work document capabilities without requiring one host.
Normal execution must not rewrite this skill or depend on developer eval files.
