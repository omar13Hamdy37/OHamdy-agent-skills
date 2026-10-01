# Phase 1 validation record

Validated on **2026-10-01**. This record covers the foundation package, not the
future teaching system or document-generation behavior.

## Checks and evidence

| Check | Result |
| --- | --- |
| JSON parsing | Both repository JSON files parse successfully. |
| Portable manifest | Passes the downloaded Agent Plugins 1.0.0 JSON Schema using its Draft 2020-12 validator. |
| Marketplace shape | Checked against current OpenAI documentation and fixed-commit official Codex types; source and policies accepted by Codex CLI. |
| Skill front matter | Parsed with PyYAML; OpenAI's bundled `skill-creator/scripts/quick_validate.py` reports `Skill is valid!`. |
| Discovery metadata | Skill name matches its folder; description is 304 characters and covers capability, lecture triggers, and scope boundaries. |
| Runtime structure | Root `skills/` contains one valid skill, ten linked references, and empty helper directories. Entry point is 61 lines. |
| Path resolution | Marketplace source resolves from repository root to the intended plugin; all local Markdown links resolve and runtime links stay within the plugin. |
| External links | All ten unique documentation/schema/GitHub URLs returned HTTP 200; the `.git` HTTP URL redirects to the correct repository page. |
| Text conventions | UTF-8 without BOM, LF, final newlines, and no trailing whitespace in nonempty tracked text. |
| Scaffold cleanup | No accidental template text, dummy URLs, or generic unfinished metadata; Phase 2 TODO headings are intentional requested implementation notes. |
| Scope/dependencies | No dependency manifests, MCP wiring, generators, eval runner, binary assets, workflows, installer, or license introduced. |
| Git review | Full staged diff and whitespace checks reviewed before the Phase 1 commit. |

PyYAML and `jsonschema` were already available local validation tools. They are not
plugin dependencies. No validation runner or package installation requirement was
added to the repository.

## Actual Codex CLI check

With **Codex CLI 0.159.3**, an isolated temporary profile was used for:

```text
codex plugin marketplace add <repository-root> --json
codex plugin marketplace list --json
codex plugin list --marketplace ohamdy-agent-skills --available --json
codex plugin add cufe-study-guide@ohamdy-agent-skills --json
```

All four commands succeeded. Before the explicit temporary install, listing showed
`cufe-study-guide@ohamdy-agent-skills`, version `0.1.0`, `AVAILABLE`, `ON_USE`,
`installed: false`, and `enabled: false`. Installation preserved every plugin file
byte-for-byte, including `skills/cufe-study-guide/SKILL.md` and its references.
The user's normal Codex profile and installed plugins were not changed.

The restricted sandbox initially prevented the CLI from resolving its temporary
home; the same isolated check succeeded with permitted execution. The CLI's
temporary-home helper-alias warning did not affect the successful commands.

## Requirements review

The master specification was manually checked against the Phase 1 request:

- A–D: priorities, intuition-first teaching, intelligent filtering, standalone
  learning, and the internal source-coverage audit.
- E–M: terminology, progressive examples, internal mechanisms, practical learning,
  misconceptions, comparisons, bridges, checkpoints, and discipline adaptation.
- N–T: conceptual study breaks, relevant prior relationships, quiz modes and Answer
  Key, proof classification, conditional cheatsheets, source/enrichment distinction,
  and every final quality-control item.
- Future output: both selectable formats, semantic styling, accessibility beyond
  color, minimal subject-aware cover, and actual render verification.
- Portability and evaluation: host-independent teaching references, optional helpers,
  separate deterministic/rubric/visual evals, real-lecture fixtures in Phase 4,
  reviewed repair loop, and no self-modification during normal use.
- Phase boundaries: no Phase 2/3/4 implementation or release claims; final public
  installation instructions remain reserved for Phase 4.

Automated checks also confirmed the ordered A–T headings and the ten expected
reference responsibilities. Heading presence alone was not treated as proof of
requirement completeness.

## Remaining validation belongs to later phases

Teaching outcomes, real-lecture regression grading, DOCX/PDF generation, rendered
page quality, ChatGPT Work installation, and the final GitHub-marketplace user flow
have not been tested in Phase 1. The CLI check establishes package/catalog parsing
and a local temporary install; it does not establish mature skill behavior or
universal host availability.
