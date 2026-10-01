# Repository guidance

- Verify current official OpenAI plugin and Agent Skills documentation before
  changing packaging or discovery conventions. Record material changes in
  `docs/architecture.md` with sources and a verification date.
- Keep `SKILL.md` concise: purpose, essential workflow, constraints, and reference
  routing. Put detailed reusable teaching behavior in skill references.
- `docs/specs/cufe-study-guide-v1.md` is the development authority for v1. Phase 2
  must translate it into self-contained runtime references; installed skills must
  not depend on repository `docs/` or `evals/`.
- Keep eval cases, fixtures, graders, and development repair loops in `evals/`.
  Normal skill execution must not rewrite skill instructions.
- Preserve the same teaching intelligence across Codex and supported ChatGPT
  Work environments. Scripts/assets are helpers, not the sole implementation.
- Update specifications and documentation when behavior materially changes.
  Keep the README concise and honest about implementation status.
- Validate JSON, YAML/front matter, package-relative paths, links, and meaningful
  behavior affected by a change. Review the complete diff before committing.
- Avoid unnecessary dependencies, services, generated binaries, and compatibility
  layers. Do not choose a license or claim a release without the owner's direction.
- Development occurs on Windows: use portable relative paths, UTF-8, and LF in
  tracked text. Preserve user work; do not force-push.
