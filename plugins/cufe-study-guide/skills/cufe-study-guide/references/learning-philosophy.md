# Learning philosophy

Use this reference to decide depth and explanatory organization before drafting.

## Resolve competing goals

Prioritize correctness → completeness of important material → understanding →
practical learning → clarity → revision/exam usefulness → appropriate conciseness
→ presentation. Explicit user scope and preferences still govern the task.

When shortening, remove duplicated wording and low-value detours before reducing
explanation of a difficult essential concept. When expanding, ask which learning
gap the extra text closes. Neither a heading-only outline nor a textbook-sized
detour satisfies the learning goal. Use
[content-selection.md](content-selection.md) to justify omissions and expansion.

## Build a model the student can use

For a new idea, identify the problem it solves and an observable consequence. Aim
for problem/motivation → intuition → mechanism → terminology → example →
implications. Change the order when a prerequisite definition, formal statement,
or concrete demonstration makes the idea easier to understand.

Before moving on, check whether the explanation enables the student to predict
one new case, explain a limitation, or distinguish a related idea. If it only lets
them repeat a sentence, add the missing mechanism or contrast. Common questions
to resolve are what it is, why it exists, how it works internally, what changes in
edge cases, and how it differs from its neighbors; select the relevant questions
rather than repeating the same questionnaire in every section.

Start with the simplest technically correct language, then introduce the formal
term needed for precision or course recognition. An analogy is a bridge: map it to
the real mechanism and state its important limitation. Do not let an analogy
replace an equation, algorithm, or definition whose exact meaning matters.

## Allocate depth to the difficulty

| Signal | Teaching response |
| --- | --- |
| Familiar, low-dependency fact | State it briefly; no extended analogy or forced example. |
| Terse bullet with a hidden mechanism or several prerequisites | Expand the causal steps and add a small example. |
| Method the student must execute | Show a worked method, assumptions, and an opportunity to apply it. |
| Two plausible interpretations or a common misconception | Resolve the distinction before building further material on it. |
| User assumes prior knowledge | Give only the bridge needed now; avoid reteaching the assumed unit unless a gap is evident. |
| Exam tomorrow | Emphasize essential methods, contrasts, and retrieval practice; trim optional detours without silently losing scoped course material. |

Keep the guide standalone within the requested scope and assumed knowledge. Supply
missing explanatory steps, define local notation, and explain important diagrams
instead of sending the student back to slides to understand the current topic.
Advanced requests can assume stated prerequisites; standalone does not mean
reteaching the entire discipline. Out-of-scope prerequisites get only a concise,
clearly identified bridge unless the user authorizes broader coverage.

## Engage without distracting

Choose interesting but economical examples, real-world consequences, “what changes
if...?” predictions, or small challenges that exercise the mechanism. Use a calm,
encouraging tutor's voice. Avoid childish metaphors, motivational filler, and
identity-based commentary. Engagement should increase useful thinking per page.

## Prefer correctness to apparent certainty

When evidence conflicts, inspect the surrounding source, notation, and assumptions
before correcting it. Distinguish the lecture's claim from the supported technical
interpretation where they differ. State uncertainty narrowly if it cannot be
resolved; do not invent certainty or tell the student an exam will require an
unverified claim. Preserve relevant course wording while explaining a correction.

Use [teaching-style.md](teaching-style.md) for the subject-sensitive techniques;
use [quality-checklist.md](quality-checklist.md) to test whether the resulting guide
actually explains the difficult ideas.
