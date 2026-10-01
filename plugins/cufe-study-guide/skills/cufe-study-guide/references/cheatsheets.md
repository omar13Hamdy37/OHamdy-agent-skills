# Cheatsheets

Use when requested or when the lecture has material worth looking up quickly.

## Decide inclusion

1. If the user says not to include one, omit it. If explicitly requested, include
   one within the supplied scope unless evidence/capabilities make it impossible.
2. Otherwise, ask whether a compact reference would save searching through the
   guide during revision. Positive signals include substantial regex patterns,
   formulas, syntax, transformation rules, APIs/functions, commands, mappings,
   repeated procedures, or close concepts needing quick comparison.
3. Check negative signals: a very short lecture, largely conceptual discussion
   without useful lookup material, or a cheatsheet that would repeat most of the
   guide. Prefer omission when automatic inclusion adds no real revision benefit.

This is a usefulness decision, not a fixed formula count. A requested cheatsheet
for a conceptual lecture can be a compact set of distinctions/decision cues; do
not invent formulas or expand course scope just to fill it. Keep the decision
internal unless the request needs an explanation.

## Build for rapid revision

Select the high-use material already taught. Group by the lookup task: choose a
pattern, recall a formula, apply a transformation, compare concepts, or select an
API. Include the minimum context that prevents incorrect application:

| Material | Keep alongside the compact entry |
| --- | --- |
| Formula | Symbol meaning/units, applicability, and critical assumptions. |
| Syntax/regex/command | Purpose, representative usage, engine/context conditions, and an important trap. |
| API/function | Input/output role and relevant state change, not only its name. |
| Transformation/procedure | Preconditions and decisive steps or mapping. |
| Comparison | The distinguishing dimension and a practical decision cue. |

Use a tiny example if it disambiguates the lookup. Do not paste every worked
example, repeat complete explanations, or introduce untaught advanced tricks.
Optional items remain distinguishable from course reference material. Keep all
entries consistent with the guide and verified answers.

A cheatsheet complements understanding; it cannot replace the guide's explanations
or be used to mark an otherwise untaught essential concept covered. If it grows
into a second full chapter, cut low-use entries and repeated prose.

Default to a compact appendix/section before the final quiz, preserving the
guide's normal end quiz and separated Answer Key. A separately requested sheet can
be a separate output when supported. At semantic handoff, identify its groups,
entries, conditions, and relationship to the guide under
[document-design.md](document-design.md). Use
[quality-checklist.md](quality-checklist.md) to reconcile accuracy and scope.
