# OHamdy Agent Skills

A growing collection of reusable agent skills, packaged as portable plugins for
Codex and supported ChatGPT Work environments.

## Available plugins

| Plugin | Purpose | Status |
| --- | --- | --- |
| [cufe-study-guide](plugins/cufe-study-guide/) | Turn university lectures into intuition-first learning guides with source coverage, examples, practice, and revision quizzes. | Phase 2 teaching instructions implemented; development version `0.1.0`, not released. |

`cufe-study-guide` teaches through clear mental models, practical examples, relevant
prior-lecture connections, and natural study breaks while preserving important
course material. Professional DOCX/PDF rendering is planned for Phase 3; full
real-lecture regression testing and release validation belong to Phase 4.

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
2. **Study-Guide Intelligence & Learning System** — completed.
3. **Professional DOCX/PDF Generation & Visual System** — planned.
4. **Evals, Real-Lecture Testing, Self-Repair & Release** — planned.

See the [development plan](docs/development.md) and the
[v1 specification](docs/specs/cufe-study-guide-v1.md) for the intended behavior.

No software license has been selected yet.
