# Authoring the versioned guide model

Read when using the packaged renderer. Version **1.0** is a JSON-compatible content
contract, not an OpenAI plugin manifest. The canonical shape is in
[study-guide.schema.json](../assets/study-guide.schema.json). Unsupported fields,
types, versions, relationships, and unreadable images fail before publication.

## Minimum input and rich text

```json
{
  "schema_version": "1.0",
  "metadata": {"title": "Tokenization and BPE", "course": "NLP", "lecture_number": 4, "subject_category": "nlp", "output_language": "en"},
  "sections": [{
    "id": "tokenization",
    "title": "Why text needs tokens",
    "blocks": [{"type": "paragraph", "content": "A tokenizer converts text into units the model can use."}]
  }]
}
```

`metadata.title` is required. Course, lecture number, subtitle, subject category,
output language, and `title_override` are optional. Do not invent missing values.
Only explicit user requests justify `cover_fields: [{"label": "...", "value": "..."}]`.
`source_context` may retain `lectures`, `previous`, and `limitations` string arrays
for audit; it is not automatically printed. Explain any material limitation in the
guide/delivery where appropriate.

Each section has `id`, `title`, `blocks`, and optional nested `subsections` with the
same shape. IDs begin with a letter, contain letters/digits/underscores/hyphens,
are at most 80 characters, and are unique across the guide. Up to six heading
levels are supported. `end_matter` is an optional ordered array of content blocks.

Rich text is either a string or an array of runs, for example:

```json
[{"text":"The method "},{"text":".fit()","code":true},{"text":" updates parameters.","bold":true},{"text":"Read the reference","href":"https://example.com/"}]
```

Runs support `text`, `bold`, `italic`, `code`, and `href`. Use explicit runs rather
than Markdown syntax inside strings. Links can use HTTP(S), mailto, or `#id` for a
known guide anchor. The renderer preserves supplied URLs; the teaching layer
verifies educational sources. The example URL above illustrates syntax only.

## Structural blocks

| `type` | Required fields; useful options |
| --- | --- |
| `paragraph` | `content`: rich text. |
| `heading` | `id`, `text`, `level` (1–6); prefer sections for the main hierarchy. |
| `list` | `items`: rich-text array; `ordered: true` for numbering. |
| `quote` | `content`; optional rich-text `attribution`. |
| `caption` | `content`. |
| `code` | `code` preserving indentation; optional `language`, rich-text `caption`. |
| `table` | `headers`: rich-text cells; `rows`: arrays of the same cell count; optional positive `column_weights`, `caption`. |
| `equation` | `description` and either `latex` or `lines: [{"latex": "...", "explanation": "..."}]`; optional `number`, `symbols: [{"symbol":"R", "meaning":"resistance in ohms"}]`. |
| `image` | Local `path`, meaningful `alt`; optional `caption`, `explanation`, `source_reference`, `width_fraction` (0.2–1). |
| `page_break` | No content; use sparingly. Quiz/key separation is automatic. |

Image paths resolve against the input JSON's directory, or may be explicit absolute
paths supplied by the teaching layer. Images are not fetched from the web. Use PNG
or JPEG for reliable cross-format embedding. Keep diagram explanations in the same
image block when possible. Equations use Matplotlib Mathtext without `$` delimiters;
fractions, sums, integrals, Greek letters, superscripts/subscripts are supported.
Full LaTeX environments/macros are not. Use explicit shorter `lines` for long or
multi-step derivations and preserve assumptions/symbol meanings in text. Formulas
in table cells can use readable Unicode/plain notation; use an equation block when
typesetting is needed. Equations are not one giant proof image.

## Semantic blocks and relationship fields

Use `{"type":"callout", "semantic":"...", "blocks":[...]}` for:
`core_explanation`, `important_note`, `common_confusion`, `worked_example`,
`previous_lecture_connection`, `under_the_hood`, `optional_enrichment`, `checkpoint`,
`breakpoint`, or `cheatsheet`. Optional `title` adds a specific title alongside the
semantic label. Ordinary paragraphs already represent normal explanations; do not
wrap every paragraph in a callout.

- A prior connection also requires `relationship` (`prerequisite`, `continuation`,
  `contrast`, `reuse_application`) and `previous_context` with the inspected locator/
  necessary recap. Put its specific current benefit in `blocks`.
- A proof uses `type: "proof"`, `classification` (`lecture_proof`, `optional_insight`,
  `extended_proof`), and `blocks`. An extended proof also requires `resource:
  {"text": "descriptive title", "href": "verified URL"}`. Optional classifications
  receive the understanding-aid label automatically. If supplied, their
  `provenance` must be `optional_enrichment`, never course material or expanded
  required explanation. This consistency is validated before either export.
- An exercise uses `type: "exercise"`, `id`, `prompt` blocks, optional `hint` blocks,
  and `solution_placement` (`inline`, `answer_key`, `none`). The first two require
  `solution` blocks; `none` excludes them. A separate solution requires an Answer
  Key and is automatically collected there.
- A quiz uses `type: "quiz"`, `mode`, and `questions`. Each question has `id`,
  `question_type`, and `prompt` blocks. Types: `conceptual`, `scenario`, `terminology`,
  `multiple_choice`, `code_tracing`, `calculation`, `short_answer`. Multiple-choice
  questions require at least two rich-text `options`; other types exclude options.
- An answer key uses `type: "answer_key"` and `answers: [{"question_id":"Q1",
  "answer":[...], "explanation":[...]}]`. Every quiz question has exactly one answer.
  Quiz and key appear only at top-level `end_matter`; the key follows the quiz and
  is the last block. Version 1.0 supports one final quiz/key per integrated guide.
  An empty `answers` array is valid only when the key collects separate exercises.

Quiz modes are `conceptual`, `scenario_heavy`, `terminology`, `exam_style`,
`code_tracing`, `calculation_heavy`, and `mixed`. The renderer preserves the choice;
it does not generate questions or decide what is important.

Blocks may carry `provenance` (`course_material`, `expanded_explanation`,
`optional_enrichment`), `source_refs` (string locators), `id`, and `keep_together`.
Only `show_provenance: true` requests a visible provenance label and needs an
explicit classification. Optional proof/enrichment labels still remain visible.
Small reasoning groups are kept together where feasible; large groups paginate.
`keep_together` is a hint for semantic groups, not a promise to fit a long proof.

## Theme and final validation

Optional `theme` supports `name: "academic" | "grayscale"`, `paper_size: "A4" |
"Letter"`, and `toc: "auto" | "always" | "never"`. Defaults: academic, A4, auto.
Automatic linked contents appears at ten navigable headings or 6,000 prose words;
it is a layout heuristic, not a pedagogical threshold. PDF heading outlines and
Word navigation styles remain available without a contents page.

Follow [document-design.md](document-design.md) for invocation and visual QA.
Validation catches mechanics and supported capabilities; it cannot establish
lecture coverage, explanation quality, or external-source reliability. Unsupported
scripts/fonts or complex RTL shaping require a capable native renderer with the
same semantic content. Preserve the model version; future incompatible changes
need an explicit migration rather than silent interpretation.
