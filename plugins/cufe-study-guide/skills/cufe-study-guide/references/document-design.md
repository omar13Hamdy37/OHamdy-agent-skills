# Document design and output

Use at the reviewed-content output stage. The baseline renderer produces DOCX and
direct PDF from one validated versioned JSON guide, using package-relative assets.
A capable native document mechanism may express the same semantics instead. Keep
teaching decisions independent of tooling; never independently author the formats.

## Construct the output model

Read [guide-model.md](guide-model.md) for exact fields and examples, then consult
[study-guide.schema.json](../assets/study-guide.schema.json) as needed. Model 1.0
retains ordered sections, typed content, provenance, proof/connection types,
exercise feedback placement, and quiz/answer IDs. It is a local rendering contract,
not an OpenAI manifest schema. Do not put raw colors or per-paragraph layout hacks
in teaching content. Pass known metadata only and preserve source locators internally.

## Semantic-to-visual mapping

| Semantic content | Baseline treatment |
| --- | --- |
| Core explanation | Unboxed readable prose with true section headings. |
| Important note | Important label, muted ochre accent and pale strip. |
| Common confusion | Explicit Common Confusion label, muted rust accent. |
| Worked example | Worked Example label, blue accent, short steps grouped where feasible. |
| Previous lecture connection | Violet label with relationship type and evidenced recap. |
| Under the hood | Teal mechanism label; ordinary prose explains state changes. |
| Optional enrichment | Secondary gray label, visibly optional scope. |
| Proof | Slate classification label; optional proofs include the understanding-aid wording. |
| Exercise | Green prompt/hint labels; inline feedback follows attempt spacing, or goes to the key. |
| Checkpoint | Green Checkpoint label and compact learning targets. |
| Breakpoint | Subtle gray Good stopping point note; never an automatic page break. |
| Quiz | Strong single-column end section; questions and IDs have no adjacent answers. |
| Answer key | A separate following page/section with matching IDs and reasoning. |
| Cheatsheet | Compact grouped tables/formulas, readable type; not forced to one page. |

Color is secondary to labels, heading hierarchy, and grouping. Label strips use
pale backgrounds; normal explanation does not live in boxes. A grayscale theme
is available. Use callouts selectively so emphasis remains useful. Type and
provenance are separate: an example may explain required content; an optional
proof must still expose scope. Do not tag every explanatory paragraph.

## Preserve source objects

- Equations: supported Mathtext, nearby description, symbols/units, assumptions,
  optional number, and explicit steps/explanations. PDF uses sharp vector paths;
  Word uses 600-dpi mathematical images with semantic alt/nearby text. Unsupported
  LaTeX or equations that would shrink below 9 pt fail; supply shorter explicit
  lines or use a capable native equation mechanism. Do not turn a proof into an image.
- Code: preserve indentation, language/engine assumptions, output/trace and key-line
  explanation. Light 9 pt monospaced treatment supports visual wrapping; executable
  source remains in the model. No syntax highlighting is required by the baseline.
- Tables: meaningful headers/rows, units and conditions, optional column weights;
  padded wrapping cells and repeated headers. Keep complex formulas as associated
  equation blocks when plain/Unicode cell notation would be unclear.
- Images/diagrams: local accessible path, meaningful alt text, caption, source reference,
  width preference and explanatory text. Aspect ratio is preserved. PNG/JPEG is the
  baseline reliable input. Do not use unreadably small screenshots as fake coverage.
- Links: descriptive text and verified supplied URL or existing `#id`; both formats
  preserve links. The renderer does not browse or invent references.

## Layout, cover, and navigation

Defaults: A4, 22 mm margins, 11 pt body with approximately 16 pt leading, black
21/16/13 pt heading hierarchy, embedded runtime DejaVu fonts, restrained running
header and body page numbers starting at 1 after the cover. Short reasoning groups
are kept together when feasible; multi-page proofs paginate without extreme hacks.

The cover displays known subject/course, lecture number, title and optional subtitle.
Deterministic local abstract nodes, brackets, waveforms, traces or geometry respond
to broad subject category. Unknown subjects receive a calm geometric fallback.
Prepared by, Date, Student ID, professor, university and metadata tables remain
opt-in; only explicit `cover_fields` requests justify them.

PDF has heading outlines; Word uses structural heading styles. Linked contents
appears for a longer guide (ten navigable headings or 6,000 prose words), or by
explicit preference. It does not need a Word TOC field update. Use `theme.toc`
when the default heuristic is unsuitable; it is not a teaching requirement.

## Invoke the available mechanism

For the packaged baseline, resolve the installed skill path from the host's skill
location. Do not assume repository or cache directories. Use:

```text
python <skill-path>/scripts/run_renderer.py -- --input <guide.json> --output-dir <user-directory> --formats docx,pdf
```

The bootstrap provisions a cached isolated venv from the included hashed lock;
initial setup needs Python 3.11+, venv/pip and dependency access. It never installs
globally. `--offline` before `--` requires a ready runtime; `--runtime-dir` selects
an explicit cache. An already provisioned environment may invoke
`../scripts/render_study_guide.py` directly. Use `--validate-only` after `--` to
validate content shape, relationships, images, glyphs and equations before export.
Missing capabilities are a reason for an honest native/supported-output fallback,
not a fabricated artifact. Basic rendering has no network requirement after setup.

Choose requested formats; normally both. CLI supports a safe `--filename`, an exact
single-format `--output-path`, optional `--theme grayscale`, and `--overwrite` for
intentional regeneration. Default outputs go into `study-guides/` beside JSON;
when JSON is inside the installed package, supply an outside output directory.
Do not pollute the skill package with guides or environments. The renderer checks
all requested formats before publishing them and diagnoses real failures non-zero.

## Verify and deliver

1. Finish [quality-checklist.md](quality-checklist.md) for content before rendering.
2. Confirm actual requested files and their mechanical checks; do not equate a
   filename or file extension with successful generation.
3. Render PDF pages to images with available tools and inspect clipping, math,
   code, tables, figures, spacing, heading breaks, cover, furniture and answer
   separation. Preview DOCX with an available safe mechanism when supported;
   otherwise explicitly report that its pagination was not visually inspected.
4. Repair semantic/model or renderer defects and regenerate/reinspect affected
   outputs. Preserve equivalence across formats. Runtime repairs affect the guide,
   never the skill's instructions or developer graders.
5. Return actual usable output paths/links and concise real scope/capability limits.

The baseline supports common Latin/Greek technical content. It is not tagged PDF/UA
and does not provide complex RTL shaping; unsupported glyphs/scripts fail clearly.
Native alternatives must preserve the same teaching, visual, source-object and
assessment semantics. Keep the audit separate from the student's guide unless useful.
