# CUFE Study Guide evals

These are developer/regression tests, **never runtime dependencies**. The runner
follows the official [skill-eval workflow](https://developers.openai.com/blog/eval-skills):
prompt → `codex exec --json` trace → artifacts → deterministic checks → independent
structured grading → reviewed diagnosis/repair → rerun. Normal execution never
rewrites the skill or graders.

## Commands

From the repository, use a Python environment with the hashed runtime lock plus
[developer lock](requirements.lock). See [setup and evaluation](../../docs/evaluation.md).

```text
python evals/cufe-study-guide/run_evals.py --deterministic
python evals/cufe-study-guide/run_evals.py --triggers
python evals/cufe-study-guide/run_evals.py --synthetic
python evals/cufe-study-guide/run_evals.py --real prnn-intro
python evals/cufe-study-guide/run_evals.py --real prnn-intro --existing output/phase4/real/prnn-intro
python evals/cufe-study-guide/run_evals.py --all
```

| Suite | Model calls | Private lecture | Purpose |
| --- | --- | --- | --- |
| deterministic | None | None | Public package/model/grader gates and renderer mechanics; CI safe. |
| triggers | 16 | None | Eight positive/eight negative selection requests; actual instruction-read evidence. |
| synthetic | 8 | None | Four original teaching cases, each generated then independently graded. |
| real | 2 normally | Required | Actual installed skill generation, coverage/rubric grading, artifacts and PNGs. |
| real + existing | 1 | Required | Regrade a retained actual run; never substitute manually authored content. |
| all | All above | Every configured case | Deliberate full pass; potentially substantial model usage. |

`--codex-home` selects an isolated authenticated profile with the plugin installed.
`--jobs 2` allows two independent trigger calls; default is sequential. `--case`
selects trigger or synthetic IDs; repeat it for targeted reruns. Synthetic
`--reuse-generation` regrades unchanged source/request content after a grader fix;
it rejects a changed generation prompt. `--output` stays under ignored
`output/`; `--timeout` bounds each model call. No model or effort override is added:
the developer's configured Codex defaults apply. Incomplete calls fail clearly.

## Private fixtures

Copy [local-fixtures.example.json](local-fixtures.example.json) to ignored
`local-fixtures.json`, then supply your local source path. Never copy university
PDFs into the repository. Profiles contain a reviewed SHA-256, high-level
non-verbatim concept inventory, source locators and decision checks. Add a new
profile/config entry for each future lecture. A changed hash requires reinspection,
not automatic acceptance of stale coverage targets. Prior sources are optional.

All prompts/traces, guide JSON, extracted material, diagrams, DOCX/PDF files,
page images and detailed grades remain under ignored `output/phase4/`. Public
reports contain only safe summaries. PRNN Lecture 01 is one real case, not proof
of universal teaching quality.

## Grading and release gates

The [rubric](graders/rubric.md) grades 15 dimensions on 1–5, with justified N/A.
Coverage must account for every inventory item; a name alone is not teaching.
Essential omissions, serious fidelity defects, critical dimensions below 4, an
applicable average below 4.2, or a failed learning decision block acceptance.
Absence of optional proofs, breakpoints or cheatsheets is judged, not penalized
automatically. Review model rationale against source and guide before repairs.

Artifact checks reconcile every expected content event in both formats, verify
schema/relationships, links, A4 geometry, fonts, navigation, quiz/key separation,
and PDF glyph bounds. Every PDF page is rendered. **PNG generation is not visual
review**: inspect the images and record that separately.
For a retained real run, `--review-file <receipt.json>` validates an explicit
per-page receipt against the PDF hash. The receipt must record every page,
crop/axis integrity, contents/quiz overflow, answer separation, bounds, typography,
page furniture and meaning without color. A regenerated PDF needs a new review.

No documented dedicated skill-selected event exists in the tested CLI. The
conservative proxy counts a successful `command_execution` read of the installed
`SKILL.md` with matching front matter in output; naming the skill or listing files
does not count. CLI/tool changes may require auditing this proxy. Initial native
Windows read-only calls rejected PowerShell reads; the harness uses
`--approve-for-me` in isolated run directories on Windows, with graders instructed
not to edit content and real inputs hashed before/after. It never disables
sandboxing or automatic review. Other hosts use read-only grading.

## Repair loop

Classify a failure as selection/instructions/reference/model/schema/renderer/grader/
package. Verify against actual evidence, repair that reusable layer, add a
regression, regenerate with the skill when behavior changed, and rerun the failed
case plus relevant suites. Do not hand-patch a real guide to meet a metric.
Preserve failing evidence locally. Grader errors get grader repairs.

Release also requires source/fidelity review, visual inspection, a clean
GitHub-backed marketplace install/bootstrap, a staged private-data scan, and final
remote-version discovery. These gates are outside the automated score alone.
