# Document design and output

**Status:** Phase 1 scaffold; semantic handoff in Phase 2, generation in Phase 3.

## Purpose and scope

Own the future professional DOCX/PDF contract, visual semantics, accessibility,
minimal cover, and render verification from specification §§4–5. No templates,
palette, generator, or dependency choices are finalized here.

## Key requirements

- Normally produce both DOCX and PDF; allow either format when requested.
- Use coherent professional document design with low noise, readable hierarchy,
  consistent styles, and accessible semantic callouts.
- Potential types: core concept, important/reminder, common confusion/warning,
  worked example/application, prior-lecture connection, under-the-hood/insight,
  and optional enrichment. Color alone must never convey meaning.
- Keep grayscale/limited-color perception usable through textual labels/icons/shapes.
- Use a minimal subject-aware cover with course/topic, lecture number if known,
  and subtle relevant visual design. Report metadata appears only when requested.
- Verify rendered pages, equations, code, tables, diagrams, links, and quiz/Answer
  Key separation in each requested format.
- Preserve teaching decisions across local helpers and supported host-native tools.

## Phase 2 TODO

Define format-independent section/callout/quiz semantics and their teaching uses.
Record the Phase 3 handoff without choosing final colors or templates. Phase 3
will implement helpers/assets and render QA with actual available capabilities;
[quality-checklist.md](quality-checklist.md) owns the final acceptance gate.
