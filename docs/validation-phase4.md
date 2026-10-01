# Phase 4 validation record

Performed **2026-10-02**, against Phase 3 baseline
`91d1aeb61636042d391e6200d8f35d9400f9c5b5`. This report contains safe summaries,
not source excerpts, private paths, generated study content or execution traces.
Earlier validation records remain unchanged as development history.

## Environment and official guidance

- Windows, PowerShell, Python 3.13.5; isolated development/runtime environments.
- Codex CLI 0.159.3; configured `gpt-6.1-sol`, `xhigh` for model-assisted runs.
- Runtime locks retain python-docx 1.2.0, ReportLab 4.5.1, Matplotlib 3.11.2,
  Pillow 12.3.0, jsonschema 4.26.0 and pypdf 6.19.0 plus hashed transitives.
  lxml is already a python-docx dependency; the namespace repair adds no dependency.
- Developer-only pypdfium2 5.13.0 and PyYAML 6.0.2 have a separate hashed lock.
- Official skills/eval/CLI/plugin guidance was rechecked. Sources and material
  decisions are in [architecture](architecture.md). No packaging restructure.
- Current CLI supports marketplace registration and `plugin add name@marketplace`;
  the README uses these actual commands, not an invented `plugin install` command.
- Native Windows read-only, noninteractive runs initially rejected PowerShell file
  reads. Those incomplete selection runs were discarded. Corrected runs retain
  automatic approval review inside isolated workspaces; no sandbox bypass.

## Private fixture and actual skill execution

- Identifier: **PRNN Lecture 01 — Introduction**; source `01 Introduction.pdf`.
- Type: PDF, 89 pages; printed slide numbering diverges from PDF page indices.
- SHA-256: `75f47799398ab94a41066fb7740efc842c299c80fd3760932a9d76b3938e58df`.
- No previous lecture supplied. Zero previous-lecture callouts were generated.
- Source text and meaningful diagrams were inspected. The public profile contains
  24 non-verbatim groups: 22 essential, one supporting and one administrative.
- The actual GitHub-installed skill was run through `codex exec --json`; successful
  installed `SKILL.md` reads, progressive reference use and generated artifacts are
  retained in the ignored trace. The generator did not receive the grading inventory.
- Initial output underwent the skill's own crop/navigation/quiz QA. Parent review
  found and repaired a reusable DOCX namespace bug, then rerendered the final
  semantic JSON unchanged. No parent hand-edit of teaching content to pass a grader.
- Source, model and both artifacts were hashed before/after independent grading;
  the grader did not mutate them. The structured result passed its output schema.

## Coverage and pedagogical result

All **22/22 essential groups** were taught: 21 covered and one merged with its
duplicate treatment. Supporting historical material was condensed; administration
was intentionally omitted while course/title context was retained. No essential
group missing. The local ledger additionally accounts for all 89 source pages.

Independent grading average: **4.8/5**; no critical dimension below 4, no critical
issue and all seven learning/fidelity decisions acceptable.

| Dimension | Score |
| --- | --- |
| Important-content completeness | 5 |
| Conceptual clarity | 5 |
| Motivation / why | 5 |
| Terminology | 4 |
| Conceptual bridges | 5 |
| Mental models / mechanisms | 5 |
| Examples | 5 |
| Practical learning | 4 |
| Content filtering | 5 |
| Common confusions | 5 |
| Quiz quality | 4 |
| Answer quality | 5 |
| Standalone usefulness | 5 |
| Concision | 5 |
| Source fidelity | 5 |

The three scores of 4 reflect minor opportunities: briefly unpack a few early
terms, provide more independent procedural practice, and distribute quiz coverage
more broadly. These are not essential omissions or incorrect answers. The rubric
is evidence reviewed against source/guide, not a guarantee of perfect instruction.

Administrative filtering, absence of fabricated prior material, five completed-unit
breakpoints, the compact revision sheet, one clearly optional insight proof, all
eight mixed quiz answers and source fidelity passed independent review. The lecture
did not require a proof; no proof quota was imposed. Source ambiguities were
qualified rather than blindly repeated. All three external clarification links
were verified as relevant official resources and exist in both output formats.

## Public and original behavior tests

- **15 public unit checks passed:** package/front matter/resources/privacy,
  complete rubric accounting and rejection gates, actual-read selection evidence,
  proof/key relationship validity, Word compatibility namespaces and hash-bound
  complete visual-review receipts.
- Rendering smoke: both formats, **six PDF pages**, all **14 semantic types**.
- Robust mechanics: 12-page fixture covering long headings/code/URLs, wide tables,
  large equations, multi-page proofs, near-page-end headings, links and wide images.
- Missing optional metadata, unknown subject, Letter/grayscale mode, tall image,
  30-entry contents density, nine invalid-input failures, occupied output path,
  byte-identical repeat output and relocation passed.
- **16/16 trigger controls passed:** eight explicit/implicit/preference-rich
  positives and eight adjacent negative requests. Selection uses successful JSONL
  instruction-read evidence, a documented conservative proxy, not an undocumented
  magic string. No description broadening was needed.
- **4/4 original behavior cases passed:** useful prior relationships with irrelevant
  context ignored, proof scope/unverified links, syntax-heavy cheatsheet/mechanisms,
  and short conceptual material with no prior/cheatsheet/artificial breakpoint.
- Two grader errors were corrected: explicit one-based check indices, and accepting
  a valid conceptual assumptions quiz instead of imposing an unrequested scenario
  quota. Targeted regrading reused unchanged generation; no skill distortion.
- The public CI workflow runs no model/private tests. Both Linux and Windows jobs
  passed on release-candidate commit `25d7e15c7d69aa377cec6af0b2372ee51d2227d1`:
  [public CI run](https://github.com/omar13Hamdy37/OHamdy-agent-skills/actions/runs/36938544560).

## Real artifacts and visual inspection

- Semantic schema 1.0 and relationship/provenance validation passed.
- DOCX ZIP/OOXML parts/relationships, true Heading 1/2 styles, A4 geometry, expected
  ordered content, nine tables, 20 embedded images, six embedded font variants,
  hyperlinks and separate quiz/Answer Key passed.
- The first DOCX could not open normally in Word despite earlier ZIP/XML checks.
  Preserving namespace declarations fixed this. Repaired smoke and real documents
  opened normally, read-only, in existing Word 16.0; real document enumeration
  returned 598 paragraphs and nine tables.
- Word's two headless PDF-export methods stalled. Only the verified read-only QA
  documents/helpers were closed. No trustworthy DOCX page preview resulted:
  **DOCX pagination was not visually inspected**. Word is not a runtime dependency.
- Direct PDF parses strictly: **34 pages**, extractable expected text, embedded
  fonts, bookmarks/internal navigation, three external link targets, sane metadata
  and no accidental blank pages or out-of-page text glyphs.
- Cross-format checks reconcile every compiled expected content item with DOCX
  and PDF; major sections, examples, practice, formulas, diagrams, revision sheet,
  quiz and reasoned answers are equivalent.
- **Every one of the 34 final PDF page PNGs was visually inspected**, including
  complete figure labels/axes, equations, tables, captions, headers/footers,
  contents, study stops, revision density and quiz/key separation. The quiz is
  page 32, the Answer Key pages 33–34. No severe defect remains.
- A six-row supporting table continues with a repeated header; some figure groups
  leave whitespace to retain context. Both are readable pagination tradeoffs.
  Semantic headings and figure labels/shapes preserve meaning without color.
- An explicit 34-page receipt matches the final PDF SHA-256; creating PNGs alone
  never counts as visual review. Final user artifacts remain locally under ignored
  `output/phase4/prnn-lecture-01/final/` with trace, ledger and grades.

## Repairs and regression protection

| Finding | Reusable repair / protection |
| --- | --- |
| Word rejected an XML-valid package | Use namespace-preserving lxml for font embedding; check prefix-valued compatibility declarations in every part; valid/invalid regression. |
| Linked contents stranded its final entry | Compact readable navigation styling in both formats; original 30-entry mechanical regression. |
| Two instructional crops contained cut labels/neighboring text | Explicit crop/axes/legend QA in document instructions; mandatory hash-bound visual receipt checks. |
| Sparse final quiz spill page | Skill runtime QA condensed nonessential wording; general navigation/quiz overflow instructions and visual receipt protection. |
| Optional proof provenance could contradict classification | Reject contradictory provenance in schema/model; public invalid-input regression. |
| Native Windows read-only selection evidence was blocked | Reviewed isolated-workspace execution; incomplete runs fail rather than count as skill failures. |
| Grader indices / overstrict conceptual-quiz criterion | Explicit one-based schema/prompt and source-faithful understanding criterion; rerun affected original cases. |

## Marketplace and release gates

Pre-release testing registered this **GitHub repository** in an isolated Codex home,
installed cached version 0.1.0, listed it as enabled/available, read the discovered
skill and provisioned a fresh isolated runtime from that installed package. Its
own remote checkout fixture rendered both formats (six PDF pages), independently
of the development runtime paths. Relocation and cached offline rendering also pass.
Normal global Codex configuration was left unchanged.

The pushed release candidate `25d7e15c7d69aa377cec6af0b2372ee51d2227d1` was then
tested in a **new isolated profile** against GitHub `main`:

- Marketplace registered; plugin installed/discovered as **1.0.0**, enabled,
  `AVAILABLE`, `ON_USE`. The official manifest schema passes.
- All 29 runtime files byte-match the reviewed package, including scripts,
  references, schema and theme assets. No original checkout path is required.
- Full trigger suite repeated against this installed version: **16/16 passed**.
- Fresh isolated dependency bootstrap completed. An initially stalled setup was
  retried with standard noninteractive pip/timeouts and succeeded; provisioning
  time depends on package-index connectivity. No global environment was changed.
- The installed package rendered its remotely fetched public fixture from an
  unrelated output working directory: valid DOCX and six-page PDF, all mechanical
  content/link/resource checks passed. Its new runtime dependency check passed.
- Cached offline rendering from the installed v1 package passed as well. Temporary
  authentication-cache copies were removed after model-assisted tests.

All local, real-source, artifact, visual, public CI and GitHub-package gates pass.
**Release decision: accept v1.0.0**, with the limitations below. Annotated tagging
and a repeat GitHub-backed discovery check against the pushed tag complete the
release procedure. No license was chosen and no universal-directory submission
was made.

## Privacy, limitations and future scope

Private lecture PDF remains outside Git. Actual source paths are only in ignored
local configuration. Extracts, images, traces, detailed grading and generated
DOCX/PDF/JSON are ignored and retained locally, not distributed with the plugin.
The commit review additionally scans staged paths/text for private paths and
substantial source/guide phrase overlap. Only the hash and high-level profile are public.

One real introduction lecture does not validate dense signals derivations, complex
proofs, RTL or large code listings. Those mechanics were exercised synthetically;
future real lectures should be added through the existing profile/local-config
mechanism. macOS, native Work document output and full accessibility conformance
remain unverified. Baseline math is Mathtext rather than complete LaTeX; Word math
is sharp graphics, PDF is not tagged PDF/UA, and complex RTL shaping is unsupported.
No software license has been selected, so public availability should not be read
as a grant of software redistribution/reuse rights.
