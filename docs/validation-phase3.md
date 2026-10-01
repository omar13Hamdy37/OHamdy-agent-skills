# Phase 3 validation record

Validation performed on 2026-10-01/02, against the Phase 2 baseline
`b0c292b8112f5a90f8a0af442d7f5e6772d63d1a`. This records renderer mechanics and
inspection, not production readiness or Phase 4 pedagogical evaluation.

## Environment and dependencies

- Windows, PowerShell, Python 3.13.5; baseline minimum Python 3.11.
- Isolated workspace development environment and a separately provisioned
  bootstrap environment. Global Python packages were not changed.
- Runtime: python-docx 1.2.0, ReportLab 4.5.1, Matplotlib 3.11.2, Pillow 12.3.0,
  jsonschema 4.26.0, pypdf 6.19.0. Complete transitive versions/hashes are locked.
- Development and bootstrapped runtime dependency compatibility checks passed.
- Development-only PDFium inspection: pypdfium2 5.13.0, separately locked.
- Existing global PyYAML 6.0.2 ran the official skill-creator quick validator.
  It is not a rendering dependency. Codex CLI 0.159.3 exposes plugin management
  but no plugin validation subcommand in its help.
- No Microsoft Word, Adobe Acrobat, or LibreOffice dependency for generation.
  No proprietary font, downloaded artwork, MCP server, or rendering service.

Official packaging/resource guidance was rechecked; sources and compatibility
decisions are recorded in [architecture](architecture.md). Portable packaging
was preserved. Initial isolated dependency provisioning succeeded using the
hashed lock. Cached offline rendering succeeded; a cold offline runtime reports
that setup is required rather than pretending dependencies exist.

## Fixture and commands

[smoke.json](../dev/rendering/cufe-study-guide/smoke.json) is explicitly synthetic
rendering-development material, with a tiny intentional source diagram. It does
not represent a lecture or test pedagogical quality. Generated DOCX/PDF/PNG files
and caches stayed in ignored `output/phase3/`.

```text
.venv/Scripts/python.exe dev/rendering/check_rendering.py
python <skill>/scripts/run_renderer.py --runtime-dir output/phase3/runtime --offline -- --input <smoke.json> --output-dir <user-output> --formats docx,pdf
python -X utf8 <official-skill-creator>/scripts/quick_validate.py <skill>
```

The final smoke outputs are `output/phase3/mechanics/smoke.docx` and `smoke.pdf`.
The PDF has **6 pages**. All fourteen semantic types are exercised: normal core
explanation, important note, common confusion, worked example, previous connection,
under-the-hood insight, optional enrichment, proof, exercise, checkpoint,
breakpoint, quiz, Answer Key, and cheatsheet. Structural content includes three
heading levels, rich prose, lists, quotation/caption, code, equations, tables,
source diagram, external links, and an internal section link.

## Model, structure, and portability

- JSON syntax and Draft 2020-12 schema validity checked. The fixture and edge
  models passed shape and relationship validation before rendering.
- Portable plugin manifest validated against the published schema cached during
  Phase 2; marketplace source path still resolves to the correct plugin.
- YAML/front matter passed the official skill-creator quick validator. Local
  Markdown/reference paths were checked; tracked text is UTF-8 with LF.
- Unknown block/semantic/version, invalid image/equation/link, duplicate IDs,
  missing quiz answers, and malformed JSON fail with diagnostics and no artifacts.
- Source assets resolve from the input directory; schema, theme, fonts, and scripts
  resolve from installed package/runtime locations. A copied package in a path
  containing spaces rendered from an unrelated working directory.
- Existing output protection and occupied-directory failures checked. Single-format
  exact output paths, default output location, Windows-safe/reserved filenames,
  validation-only mode, and rejection of output inside the plugin checked.
- Unsupported glyphs are rejected, including in list items, equation descriptions,
  and explicitly requested cover fields. Ordinary block anchors and extended-proof
  resource links were exercised separately.

External targets were compared to supplied model URLs and checked structurally;
the renderer did not fetch or certify their educational quality. The deliberately
synthetic long URL in the mechanical case is layout data, not an educational source.

## DOCX checks

Both smoke and robustness outputs passed ZIP integrity, XML parsing, required
OOXML parts, internal relationship target resolution, expected content, links,
and page geometry checks. Additional smoke inspection checked:

- True Heading 1/2/3 paragraph styles with outline levels.
- A4 setup; body numbering restarted at 1 and a PAGE footer field.
- Embedded source/equation/cover images and figure semantic descriptions.
- Padded tables with repeated header rows and short-row splitting protection.
- Paragraph-property ordering relative to bookmarks.
- Six embedded DejaVu font variants. Deobfuscation produced valid TTF files;
  font embedding permission flags allow unrestricted embedding.
- Code, equation descriptions/symbols, exercise feedback, quiz questions,
  separate Answer Key, cheatsheet, and supplied link targets were present.

**DOCX was not visually previewed.** The bundled preview helper failed because
`pdf2image` was unavailable; LibreOffice/Poppler were also absent from PATH.
No claim is made about exact Word/other-reader pagination. Generation and OOXML
checks succeeded independently of those optional preview tools.

## PDF and cross-format checks

pypdf parsed outputs in strict mode; every page had extractable text. Checks covered
paper size, embedded content fonts, heading outlines, external link annotations,
metadata, and expected content. Internal navigation destinations were exercised.
PDFium rendered pages and checked glyph bounds against page edges.

Every expected ordered content item was reconciled against both outputs, including
headings, labels, prose, lists, table cells, code source characters, equation
descriptions and symbol definitions, image captions/explanations, exercise feedback,
quiz/key, and cheatsheet. Equations share the same cached mathematical layout;
Word receives 600-dpi graphics and PDF vector outlines. Link target sets match the
input in both formats. This is content reconciliation, not a claim that extracted
equation graphics become searchable mathematics.

Repeated rendering produced byte-identical DOCX and PDF for the smoke model.
Native host exports and different document readers were not compared here.

## Visual inspection and repairs

All six smoke PDF pages were rendered to PNG and inspected, including the cover,
callouts, equations, code, tables, diagram/explanation, exercises, checkpoint,
breakpoint, cheatsheet, quiz, and Answer Key. All twelve robustness PDF pages were
also inspected. Minimal metadata/grayscale/Letter and tall-image content pages
were inspected.

Inspection found an orphaned section heading and absent PDF code shading. Repairs
combined heading/group pagination correctly and drew an actual light code background.
The repaired pages were rerendered and inspected. Compact tables now stay together
where feasible; nested layout groups are flattened before height estimation.

The inspected pages have readable type, restrained labeled accents, sharp equations,
preserved diagram proportions, near-figure explanation, and distinct quiz/key pages.
Long code and URLs wrap within margins; the wide table repeats its header. Large
proofs continue across pages instead of forming an oversized unbreakable box.

Text contrast was calculated using relative luminance for body, muted text, links,
code, and semantic label accents against white and their pale fills; every tested
pair exceeds 4.5:1 (minimum measured 5.54:1). Textual labels preserve meaning without
color. These checks do not establish full WCAG or PDF/UA compliance.

## Mechanical robustness results

| Case | Result |
| --- | --- |
| Long heading and near-end heading | Wrapped; stayed with following explanation. |
| Long code line | Complete source characters retained; visual wraps stayed in margins. |
| Eight-column table | Wrapped cells and repeated headers; no page overflow. |
| Large equation | Sharp, complete expression at readable scale. |
| Multi-page proof | Paginated normally with preserved text. |
| Long URL | Wrapped and remained clickable. |
| Wide and tall source images | Aspect ratios preserved. |
| Missing optional metadata/unknown subject | Minimal cover and geometric fallback worked. |
| Grayscale and Letter | Both formats rendered with requested geometry/theme. |
| Invalid input and occupied output path | Nonzero diagnostics; no half-published documents. |
| Offline cached runtime/relocated plugin | Both formats generated successfully. |
| Repeated identical model | Byte-identical outputs. |

The robustness PDF has 12 pages; the minimal and tall-image PDFs each have 2.
The developer smoke check remains separate from the untouched `evals/` scaffolding.

## Specification review and deferred work

Requirements A-T, the document-output contract, and portability requirements remain
unchanged from Phase 2. Eight pedagogical references are byte-identical. Phase 3
implements their rendering handoff: shared model, meaningful visual identities,
minimal subject-aware cover, DOCX/PDF, equations/code/tables/images/links/navigation,
artifact checks, and portable helpers. Small implementation clarifications were
added without changing the teaching decisions.

Known limits are detailed in [rendering](rendering.md): Mathtext subset; graphical
Word equations; untagged PDF; limited glyph/shaping/localization support; no syntax
highlighting; reader-dependent Word pagination; initial dependency setup required.
Windows Python 3.13 was exercised, not all advertised baseline versions/OSes.

Phase 4 owns real CUFE lecture coverage/teaching tests, full trigger/non-trigger
and rubric evals, build/eval/repair iterations, clean-host/reader testing including
DOCX visual inspection, release validation, and the final simple marketplace
instructions. No eval corpus, model grader, CI/release pipeline, tag, or public
release was created in Phase 3. Version 0.1.0 remains unreleased.
