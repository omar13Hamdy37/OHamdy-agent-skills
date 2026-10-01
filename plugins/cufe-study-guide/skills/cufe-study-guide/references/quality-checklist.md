# Pre-output quality control

Use after drafting, before the output handoff. Review the actual explanations and
evidence rather than counting headings. Keep this checklist internal unless the
user requests an audit or needs to know a limitation.

## Review in order of consequence

| Gate | Inspect | Repair if it fails |
| --- | --- | --- |
| **Source coverage** | Reconcile every meaningful scoped item with the ledger. Essential concepts, formula conditions, important diagrams, and course proof/method steps have real guide locations. Merges/condensations preserve their lesson; omissions have reasons. | Restore missing explanation/objects; correct unjustified dispositions. An unread source gap cannot be marked complete. |
| **Teaching quality** | For each difficult concept, can the learner explain why it exists, use its mechanism, and connect it to what follows? Unfamiliar terms/symbols are explained at first use; examples/comparisons/bridges close actual gaps. | Add the missing model, step, or contrast; simplify jargon before adding more prose. Merely naming a concept is fake completeness. |
| **Accuracy** | Recompute important example calculations/units, reason through or run code where supported, and inspect formulas, assumptions, proof steps/classification, and source interpretations. Claims distinguish conceptual models from implementation specifics. | Fix the source interpretation or example and every dependent explanation/answer. Disclose unresolved ambiguity rather than invent certainty or execution evidence. |
| **Learning experience** | Practice is answerable and meaningful, checkpoints test understanding, and breakpoints follow completed units without interrupting proofs/derivations/examples/active dependencies. Enrichment has a learning benefit and an appropriate scope label. | Repair sequencing, feedback, or boundary placement; remove gratuitous enrichment and decorative checkpoints/breaks. |
| **Cross-lecture quality** | Each connection has an inspected prior locator, a valid relationship type, and a specific current benefit. Notation/assumptions align; keyword matches alone are insufficient. | Verify or remove the connection. State an inaccessible prior path accurately without pretending inspection. |
| **Quiz** | Important concepts/relationships/methods are reasonably sampled; mode/size preferences are honored; questions use taught material and plausible distractors. Independently solve them and compare with the separated, reasoned Answer Key. | Fix ambiguity, triviality, missing assumptions, or incorrect answers; check affected guide content as well. |
| **Concision** | Repetition, unnecessary detail, excessive callouts, repeated prior recaps, optional-content creep, and oversized cheatsheets are removed. Compression has not reduced essential topics to labels. | Cut low-value support first; protect the explanation needed for standalone understanding within the user's scope/assumptions. |
| **Output readiness** | Ordered sections and semantic types are consistent; equation symbols, diagram meanings, code/table structure, intact groups, links, quiz IDs/answer associations, and known metadata are ready for output. | Repair associations and missing context before passing content to the available output mechanism. |

## Verify links and expectations

Inspect any external destination used for enrichment/proofs when browsing is
allowed and available: check that it works and supports the stated purpose, not
merely that its URL is syntactically valid. Do not fabricate sources or imply
verification when access failed. Remove an unverified recommendation or state the
narrow verification limit; preserve the required course explanation.

Review optional proofs, advanced side notes, and outside techniques for clear
course/enrichment distinction. Ordinary expanded explanation does not need a tag
on every paragraph. Check explicit requested exclusions and source ranges, and
avoid unsupported exam promises. Use the provenance policy in
[content-selection.md](content-selection.md) when classification is unclear.

## Repair and decide whether the content is ready

Resolve correctness/coverage defects first, then teaching issues, then concision
and presentation semantics. Recheck the changed material and anything depending
on it: a changed equation can affect a worked example, quiz answer, and cheatsheet.
Reconcile the ledger again after cuts or reordered sections.

If an essential evidence gap cannot be resolved with available reading tools,
request the specific missing information when necessary. Continue independent
units where useful. Any delivered partial guide must state its actual scope/gap;
it cannot carry an unqualified completeness claim. Capability limitations do not
justify inventing artifacts or prior/source evidence.

Ready content covers scoped essentials, explains difficult ideas, supports practice
and revision, has accurate answers, and can stand alone under the stated learner
assumptions. Pass it under [document-design.md](document-design.md) with any real
limitations. Normal repairs affect the current guide, never the skill instructions
or developer graders.

**Export gate:** after generation, follow [document-design.md](document-design.md)
to inspect requested artifacts and rendered pages. Repair clipping, tables, code,
equations, pagination, links, and answer separation; recheck changed outputs. The
script's mechanical checks and this content pass do not certify visual quality.
State any unavailable preview honestly rather than claiming it was inspected.
