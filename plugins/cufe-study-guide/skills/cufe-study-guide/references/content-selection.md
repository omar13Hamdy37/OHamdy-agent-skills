# Content selection, planning, and coverage

Use this reference before drafting and again when reconciling the source audit.

## 1. Establish the task and readable evidence

Separate current-course inputs from prior context. Accept slides, PDFs, DOCX/course
notes, code, diagrams, screenshots, or mixtures; do not treat prior guides as new
lecture content unless the request says so. For several current lectures, infer
their order from reliable identifiers and the request; keep source IDs distinct
even if the final guide integrates topics. Ask only if ambiguity changes coverage.

Record the requested source range, exclusions, assumed knowledge, depth, external-
material permission, quiz preference/size, cheatsheet preference, and outputs. Infer
defaults from the request rather than require command syntax. Examples:

| Preference | Consequence |
| --- | --- |
| “Only slides 1–40” | Audit that range; do not silently extend it. Distinguish printed slide labels from file page indexes if they differ. |
| “Assume I know Lecture 2” | Use established concepts with a short bridge; do not reteach the whole lecture. Verify claimed relationships if its material is available. |
| “Scenario quiz”, “small quiz” | Set mode and size independently; keep essential coverage through well-chosen questions. |
| “Explain the math”, “focus on derivations” | Increase intermediate steps and interpretation within course scope. |
| “No cheatsheet”, “include a cheatsheet” | Override the automatic inclusion decision. |
| “No external material” | Do not retrieve or add external enrichment; unpack the supplied concepts using explanations and examples. |

Inspect headings and source order, then read substantive material in context.
Compare extraction with visual pages where equations, diagrams, tables, code,
annotations, or scan quality make text incomplete. Try available visual/OCR/native
reading alternatives for suspicious gaps. Do not resolve an unreadable symbol by
guessing. Track remaining gaps separately from intentional omissions.

## 2. Inventory and classify

Inventory main/subtopics, definitions, formulas with conditions, algorithms,
procedures, proof steps, worked methods, distinct examples, important diagrams,
prerequisites, repetitions, and administrative material. Give meaningful items
source locators (file and page/slide/section) where available.

| Category | Signals | Action |
| --- | --- | --- |
| **ESSENTIAL** | Explicitly taught concept, formal definition, formula, theorem, algorithm, important diagram, required proof/method, or prerequisite for later scoped content. Repeated emphasis can strengthen this signal. | Preserve meaning, conditions, and enough explanation/application for the student to use it. |
| **SUPPORTING** | Motivation, explanation, analogy, or example that helps learn essential material. | Retain the most useful support; merge/compress others without removing a distinct lesson. |
| **ENRICHMENT** | Added technique, advanced extension, or optional reasoning beyond apparent course requirements. | Include only for a concrete learning benefit and within user permission; label when scope matters. |
| **REDUNDANT** | Duplicate wording/example with no new mechanism, assumption, edge case, or instructional value. | Merge into the strongest explanation or intentionally condense/omit with a reason. |
| **ADMINISTRATIVE** | Announcements, logistics, biographies, decoration, and reference lists without instructional content. | Normally omit; preserve any actual required reading or course constraint embedded in them. |

Classification depends on meaning, not slide word count, decorative prominence,
or file length. A one-line formula can be essential and difficult. Repetition can
indicate emphasis while repeated wording is redundant: preserve the concept's
importance without reproducing every occurrence. If uncertain whether a substantive
item is essential, retain concise coverage until evidence supports removing it.
Explicit practice/objectives and worked methods are exam-relevance signals, not
proof of what will appear in the exam.

For repeated examples, identify the lesson each adds. Keep the example that best
teaches the pattern, plus examples that add an important edge case or failure mode.
Do not call distinct boundary conditions duplicates merely because syntax looks similar.

## 3. Build the concept/dependency map

Represent each concept with prerequisites, what it produces/enables, difficulty,
source items, and skipped explanatory steps. Distinguish a true prerequisite from
an association: could the learner understand this concept without the other one?
Map procedures/proofs as intact sequences. Mark gaps requiring a bridge or evidence.

Illustrative dependency chain:

```text
Tokenization → vocabulary → BPE training → merge rules → encoding unseen text → model input
```

Use the map to establish prerequisites before use, group tightly coupled steps,
insert missing bridges, choose retrieval targets in prior material, and identify
conceptually complete units for checkpoints/breaks. Later, sample important nodes,
relationships, and methods for the quiz. Do not expose a giant planning dump.

If the map appears cyclic, look for a foundational intuition that can be introduced
first and refined later. Avoid defining one unknown term through several others.
If a prerequisite lies outside requested scope, give the smallest labeled bridge
needed to explain the scoped material, or ask if the gap prevents correct treatment.
Reordering the lecture is allowed; changing its syllabus silently is not.

## 4. Distinguish provenance from importance

The five categories decide treatment; they are not paragraph-level provenance tags.
Separately distinguish **course material** (present or clearly implied), **expanded
explanation** (unpacking that material), and **optional enrichment** (beyond its
requirements). A new teaching example for a required concept is not automatically
an optional topic. An outside fact cannot establish an unsupported course claim.

Label optional proofs, advanced side notes, external techniques, and uncertain
course-scope additions where exam expectations could be confused. Avoid labels on
every explanatory sentence. Say “beyond the supplied lecture” when warranted rather
than claiming “not on the exam.” Resolve ambiguous/wrong source claims according
to [learning-philosophy.md](learning-philosophy.md).

## 5. Maintain the coverage ledger

For each meaningful source item, retain: source locator, concept/category, planned
guide location, final disposition, and a reason when compressed/omitted. Use:

- **Covered:** actual explanation/representation exists at the target location.
- **Merged:** the target teaches the shared concept; identify the items combined.
- **Intentionally condensed:** essential meaning or a supporting lesson remains;
  explain what repetitive detail was removed.
- **Intentionally omitted:** give the scope or low-value reason.
- **Unresolved evidence gap:** not readable/accessible; never count as covered.

Reconcile after drafting and after significant cuts/reordering. Inspect whether
each location explains the concept, not just mentions its name. Essential items
within requested scope cannot be omitted for brevity; unread gaps prevent an
unqualified completeness claim. Keep the ledger internal unless a compact coverage
report would help the user. Final review lives in
[quality-checklist.md](quality-checklist.md).
