# OHamdy Agent Skills

A growing collection of reusable agent skills, packaged as portable plugins for
Codex and supported ChatGPT Work environments.

## Available plugins

| Plugin | Purpose | Status |
| --- | --- | --- |
| [cufe-study-guide](plugins/cufe-study-guide/) | Turn university lecture material into complete, practical study guides with clear explanations and polished document output. | Phase 1 scaffold; development version `0.1.0`, not released. |

`cufe-study-guide` is intended to act as a study-guide author, tutor, and document
designer. It goes beyond summarization while preserving important course material.
The teaching system and DOCX/PDF output are planned for the next phases.

## Installation

Beginner-friendly marketplace installation instructions will be finalized and
tested before release in Phase 4.

## Repository structure

```text
.agents/plugins/marketplace.json  Repository plugin catalog
plugins/                         Distributable plugins and skills
docs/                            Architecture, development plan, and specifications
evals/                           Developer tests and regression fixtures
```

## Development status

1. **Repository Foundation & Skill Architecture** — completed.
2. **Study-Guide Intelligence & Learning System** — planned.
3. **Professional DOCX/PDF Generation & Visual System** — planned.
4. **Evals, Real-Lecture Testing, Self-Repair & Release** — planned.

See the [development plan](docs/development.md) and the
[v1 specification](docs/specs/cufe-study-guide-v1.md) for the intended behavior.

No software license has been selected yet.
