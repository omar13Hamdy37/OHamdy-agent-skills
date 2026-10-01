# Development and evaluation

Public reproducible tests and private real-lecture validation are separate.
The [eval README](../evals/cufe-study-guide/README.md) defines cases, signals,
rubric gates and repair behavior. [Phase 4 validation](validation-phase4.md)
records actual results rather than treating the framework as evidence of success.

## Local setup

Use Python 3.11+ and an isolated environment. Windows example:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install --require-hashes -r plugins/cufe-study-guide/skills/cufe-study-guide/scripts/requirements.lock -r evals/cufe-study-guide/requirements.lock
.venv/Scripts/python.exe evals/cufe-study-guide/run_evals.py --deterministic
```

On Linux/macOS use `.venv/bin/python`. Developer-only dependencies are PDFium
for inspection and PyYAML for front matter. Runtime dependency/bootstrap behavior
is documented in [rendering](rendering.md); evals are never needed by end users.
CI runs only the public deterministic suite, without private source/model credentials.

## Model-assisted tests

Install/authenticate the official Codex CLI, register this GitHub marketplace and
install its plugin using the [README](../README.md#quick-install). Model calls use
your configured model/effort and incur the corresponding usage. Prefer targeted
reruns before the complete suite. Current
[developer commands](https://learn.chatgpt.com/docs/developer-commands) document
`exec --json`, structured `--output-schema`, and plugin management.

```text
python evals/cufe-study-guide/run_evals.py --triggers
python evals/cufe-study-guide/run_evals.py --synthetic
python evals/cufe-study-guide/run_evals.py --real prnn-intro
```

The first two use original prompts/material. The real suite requires ignored
`evals/cufe-study-guide/local-fixtures.json`. It checks the source fingerprint,
runs the actual installed skill, validates artifacts, then uses an independent
structured grader. `--existing <ignored-run-directory>` regrades a retained actual
run with instruction-read evidence; it does not author a replacement guide.
All detailed results stay local and ignored.

For isolation, create an existing temporary `CODEX_HOME` and pass that environment
to child CLI processes, then `--codex-home <profile>` to the runner. Authenticate
the profile using official [options](https://learn.chatgpt.com/docs/auth).
An auth cache is a credential: never print/commit it; remove temporary copies after
testing. Keep normal global configuration untouched. Windows commands are
automatically reviewed inside run workspaces.
Real-source/model/artifact hashes detect grader mutation. On hosts where read-only
file reads work, graders use read-only mode.

## Adding another real lecture

1. Keep the lecture outside Git; inspect text **and meaningful diagrams**.
2. Add a small non-verbatim profile under `cases/`: identifier, filename, SHA-256,
   page count, essential/supporting/admin concepts and locators.
3. Add its source path, course/title, profile and optional previous sources to
   ignored `local-fixtures.json`; run `--real <identifier>`.
4. Review coverage, rubric, fidelity and every rendered PDF page. Convert actual
   failures into general regressions; do not overfit rules to slide numbers.

Source images/extracted text/traces/generated guides belong under `output/`.
Only safe summary scores/high-level findings belong in public validation.

## Release review

Run the public suite, trigger controls, original behavioral regressions and all
available real cases. Audit rubric failures, inspect pages, preview DOCX with an
already available reader if possible, and compare both formats to their shared
model. Test the package from GitHub in isolation, including cold bootstrap and
package-relative resources. Scan staged paths/text for private data/credentials
and inspect the complete diff before commit.

Promote to 1.0.0 only when all gates pass. Commit/push without force, annotate/push
the release tag, and repeat remote marketplace discovery against the pushed version.
Do not select a license or submit to a universal directory.
