# OHamdy Agent Skills

A growing collection of reusable agent skills, packaged as portable plugins for
Codex and supported ChatGPT Work environments.

## Quick Install

With the current Codex CLI installed and signed in:

1. Add this marketplace:

   ```bash
   codex plugin marketplace add omar13Hamdy37/OHamdy-agent-skills
   ```

2. Install CUFE Study Guide:

   ```bash
   codex plugin add cufe-study-guide@ohamdy-agent-skills
   ```

3. Start a new session and supply your lecture file.

You can also find **OHamdy Agent Skills → CUFE Study Guide** in the supported
client's Plugins Directory after adding the marketplace. These commands follow
the [official CLI reference](https://learn.chatgpt.com/docs/developer-commands).

## Use it

```text
Create a study guide from this lecture PDF.
```

```text
Create a study guide from this lecture. Make the final quiz scenario-heavy
and include a cheatsheet.
```

```text
Create a study guide from Lecture 4 and use the previous lecture folder
to connect related concepts.
```

Expect intuition-first explanations, intelligent filtering, terminology help,
examples/exercises, conceptual bridges, relevant prior connections, natural study
breaks, appropriate proofs, quizzes with separate answers, and useful cheatsheets.
The skill can produce both **Word (DOCX) and PDF**. Supply prior material when you
want grounded cross-lecture connections. Python 3.11+ is needed for the local
renderer; it sets up isolated dependencies on first use. Native document tools
may be used where supported.

## Available plugins

| Plugin | Purpose | Status |
| --- | --- | --- |
| [cufe-study-guide](plugins/cufe-study-guide/) | Turn university lectures into intuition-first learning guides with examples, practice, revision quizzes, and DOCX/PDF output. | `1.0.0` — validated on one real CUFE lecture plus public mechanical and behavior tests. |

`cufe-study-guide` teaches through clear mental models, practical examples, relevant
prior-lecture connections, and natural study breaks while preserving important
course material. A shared semantic model now drives DOCX and direct PDF rendering.
Validation covers one real introduction lecture; additional courses can be added
as private regressions. See the [validation record](docs/validation-phase4.md).

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
3. **Professional DOCX/PDF Generation & Visual System** — implemented and smoke-tested.
4. **Evals, Real-Lecture Testing, Self-Repair & Release** — implemented and validated.

See the [development plan](docs/development.md) and the
[v1 specification](docs/specs/cufe-study-guide-v1.md) and
[developer evaluation guide](docs/evaluation.md).

No software license has been selected yet.
