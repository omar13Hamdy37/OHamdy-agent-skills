# Semantic document contract

Use when organizing reviewed content for the available output mechanism. This is
the skill's authoring contract, not an OpenAI manifest schema or a required file
serialization. Exact palette, templates, spacing, and rendering implementation
belong to Phase 3.

## Keep the teaching structure independent of the renderer

Represent the guide as ordered sections with stable headings/identifiers and
typed content blocks. Readable Markdown plus descriptive labels, a host-native
document outline, or an equivalent structured representation can express this.
Do not require one script, tool ID, JSON engine, or local filesystem path.

For a block, retain its type, title/meaning, content, necessary assumptions, and
links/references to related blocks. Keep course/enrichment scope and source locators
internally where needed for audit; show provenance labels only when they affect
student expectations. Preserve intact groups and answer associations rather than
flattening everything into undifferentiated paragraphs.

## Semantic content types

| Type | Meaning and content the output mechanism must preserve |
| --- | --- |
| **Core explanation** | Motivation, mental model, mechanism, terminology, and implications in the chosen teaching order. |
| **Important note** | A consequential condition, assumption, or reminder, with a specific title when useful. |
| **Common confusion** | Mistaken idea, why plausible, correct model, and useful contrast. |
| **Example** | Inputs/assumptions, decisive worked steps, result, and interpretation. |
| **Previous lecture connection** | Relationship type, evidenced earlier topic/locator, concise recap, and current relevance. |
| **Under the hood** | Internal state/operations and their observable consequence. |
| **Optional enrichment** | Clear beyond-course scope, benefit, relevant prerequisites, and verified external link when used. |
| **Proof** | Classification, claim, assumptions, steps, interpretation, and optional label when applicable. |
| **Exercise** | Prompt before solution, inputs/constraints, feedback association, and meaningful attempt opportunity. |
| **Checkpoint** | Compact understanding target after a completed conceptual group. |
| **Breakpoint** | Safe stopping boundary and concise completion/next-unit note. |
| **Quiz** | End-of-guide question group with IDs, mode, assumptions, and no interleaved answers. |
| **Answer key** | Separate group after the quiz, matching IDs, correct results, and reasoning. |
| **Cheatsheet** | Compact revision groups/entries with applicability and essential conditions. |

Type and provenance are separate: a proof can be course material or optional; an
example can explain required content without needing a visible enrichment label.
Use plain sections for ordinary explanation and callouts selectively, so semantic
types do not imply a decorated box around every block.

## Preserve equations, diagrams, code, and tables

- **Equation:** retain editable/meaningful notation where possible, symbol definitions,
  units/domain, assumptions, explanatory text, and derivation/example relationships.
  Do not hand off only an equation image when its meaning can be retained as text.
- **Diagram/plot:** retain an accessible source object/locator when available and a
  semantic description of labels, components, edges/directions, axes/units, and the
  instructional takeaway. Indicate whether preservation or clearer recreation is
  intended; missing/uncertain elements cannot be invented by the renderer.
- **Code/procedure:** retain language/engine assumptions, indentation, relevant
  input/output, commentary, and trace associations. Keep verified execution status
  accurate. Output formatting must not silently change behavior or notation.
- **Table:** preserve column meanings, units, row associations, conditions, and
  scope. Use a table because the comparison/mapping helps, not merely for decoration.

Mark a proof, worked example, or algorithm walkthrough as an intact conceptual
group. Mark the final Answer Key as separate from the question group; an in-section
exercise instead needs nearby prompt-then-feedback separation. These are semantic
constraints, not Phase 2 page-layout code.

## Prepare the output handoff

Pass the reviewed ordered content, known course/topic/lecture identifiers, requested
formats, user preferences, required object/link associations, and any unresolved
source/capability limits. Keep the internal coverage ledger separate from the
student-facing document unless the user would benefit from seeing a concise audit.

Normally target both DOCX and PDF, or the requested subset. Use supported native
capabilities/helpers without changing teaching decisions. If only one format or
plain structured content is available, deliver that supported result and explain
the missing requested capability. Never rename text to a document extension or
claim an export/render verification that was not performed.

Provide cover metadata only when known: subject/course, lecture number if known,
and lecture/topic title. A later cover should be minimal and subject-aware with
subtle relevant visual design. Prepared by, Submitted to, Date, Student ID,
professor fields, and large metadata tables are opt-in. Do not infer missing values.

## Phase 3 responsibilities

The renderer must provide low-noise hierarchy, consistent accessible styling, and
semantic signals beyond color: textual labels/icons/shapes must remain understandable
in grayscale and with limited color perception. Preserve readable content in each
requested artifact, working links, intact conceptual groups, and separation of
quiz answers from immediate view. Phase 3 implements and verifies actual rendering,
then repairs defects in the exports. No final colors, templates, pagination,
headers/footers, artwork, equation renderer, or image pipeline is specified here.
