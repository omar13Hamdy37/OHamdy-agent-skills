# Development plan

## Phase 1 — Repository Foundation & Skill Architecture

Establish GitHub linkage, current portable packaging, one extensible repository
marketplace, focused skill metadata, reference responsibilities, and the v1
specification. Create eval directories without implementing the regression suite.

Exit gate: structural validation, a complete requirements review, full diff review,
and a meaningful commit pushed to `origin/main` when authentication allows it.
See the [Phase 1 validation record](validation-phase1.md).

## Phase 2 — Study-Guide Intelligence & Learning System

Turn [the v1 specification](specs/cufe-study-guide-v1.md) into operational runtime
references. Implement coverage planning, intuitive teaching, practical activities,
terminology, misconceptions, conceptual bridges, adaptive organization,
cross-lecture relationships, breakpoints, quizzes, proof classification, and
cheatsheet decisions. Keep `SKILL.md` focused and update its scaffold status only
when justified.

Exit gate: all requirements A–T have actionable, self-contained reference guidance;
learning behavior can be reviewed without assuming a particular export script.
Output remains compatible with the Phase 3 design contract.

## Phase 3 — Professional DOCX/PDF Generation & Visual System

Implement document helpers/assets as needed, semantic styles, minimal subject-aware
covers, accessible callouts, layout, and DOCX/PDF export. Use host-native capabilities
where supported. The normal expected output is both formats, with either selectable
by the user.

Exit gate: actual rendered documents are inspected and corrected; teaching content,
equations, diagrams, code, quiz answers, links, and hierarchy survive both exports.
Do not select dependencies until a concrete implementation need justifies them.

## Phase 4 — Evals, Real-Lecture Testing, Self-Repair & Release

- Implement the full eval suite and deterministic plus rubric/model graders.
- Add real lecture fixtures with permission and appropriate provenance; do not
  commit private student/course material indiscriminately.
- Run **build → eval → diagnose → repair → rerun** until failures are resolved.
- Perform release validation in clean, supported host environments, including
  actual plugin installation, skill discovery, and end-to-end document generation.
- Finalize versioning, changelog, release metadata, and the public README. The
  owner must choose a license before any license is added.
- Provide **very simple marketplace download/install instructions for users**:
  a short verified path from adding the GitHub marketplace to selecting/installing
  the plugin and beginning a new session. Avoid developer internals in that section.

Self-repair is a reviewed developer activity. The mature skill must not modify its
own instructions or graders during normal student use.

## Working conventions

Keep runtime changes under the plugin, development documentation under `docs/`,
and regression materials under `evals/`. Update the specification when intended
behavior changes; do not silently weaken a requirement to satisfy a grader.

No package dependencies are required by Phase 1. Available local validation tools
are developer conveniences, not plugin requirements. Current OpenAI CLI commands
are documented in the [official command reference](https://learn.chatgpt.com/docs/developer-commands).
Use `codex plugin list --marketplace ohamdy-agent-skills --available --json` as a
read-only catalog check where supported. Prefer an isolated temporary Codex home
for checks that write cache or configuration, and do not install into a user's
normal profile just to validate the scaffold.

Before committing, parse JSON and skill YAML/front matter, verify source/reference
paths and links, inspect placeholders, run appropriate checks, and review the
complete staged diff. Phase 1 validation is structural; teaching and rendered-output
evals belong to subsequent phases.
