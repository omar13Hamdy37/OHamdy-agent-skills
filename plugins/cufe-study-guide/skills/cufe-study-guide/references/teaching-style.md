# Teaching style and content handling

Use after the concept map is built. Select techniques that close an identified
learning gap; a concept does not need every block type below.

## Adapt to the subject

Infer the discipline from operations, notation, diagrams, and exercises, not only
the course title. Hybrid lectures can use different teaching sequences by unit.

| Subject | Emphasis and useful sequence | Useful practice |
| --- | --- | --- |
| Programming/software | concept → syntax → execution → examples → mistakes; show inputs, state, output, and edge cases. | Predict output, debug code, implement a tiny function, explain execution. |
| ML/AI/NLP | problem → data flow → model intuition → training → inference → limitations; connect code to the actual concept. | Trace training/prediction, interpret outputs, reason about data or failure cases, compare methods. |
| Digital logic/VHDL | signal flow → components → syntax-to-hardware meaning → behavior/timing where taught; distinguish simulation/description from hardware assumptions. | Trace signal changes, interpret a circuit, connect code constructs to components, predict behavior. |
| Electronics/signals/systems | physical intuition → mathematical model → derivation → calculation → physical/plot interpretation; keep units and assumptions visible. | Calculate a value, justify a derivation step, predict a parameter's effect, interpret a waveform. |
| Mathematics | motivation for definitions → assumptions → relationships/proof → worked problems → boundary cases. | Solve a small problem, test an assumption, explain a proof step or counterexample. |
| Algorithms/data structures | problem → representation/invariant → stepwise execution → correctness/cost → edge cases. | Trace state, find a broken invariant, compare methods under stated input assumptions. |
| Theory/conceptual | motivation → model → relationships → scenario → understanding check. | Explain in one's own words, apply a model, distinguish close concepts. |

These are decision aids, not mandatory chapter templates. Preserve the lecture's
notation and stated scope while reorganizing for dependencies.

## Introduce terminology without jargon recursion

At first meaningful use of an unfamiliar term, give its plain meaning in the same
sentence or immediately following sentence. Then give the formal definition if
precision matters. Define prerequisite terms first or replace them with plain
language; do not explain one unknown word with three more unknown words.

Use the same term/symbol consistently afterward. Explain a changed meaning or
notation explicitly. Avoid redefining the term in every section and defining
ordinary words without a real ambiguity. If the learner explicitly knows a term,
use it directly unless the current lecture introduces a materially different usage.

## Choose examples that add information

For a mechanism with transferable steps, use progression when useful:

1. **Tiny:** isolate the mechanism using the fewest moving parts.
2. **Realistic:** apply the same mechanism to plausible course/application data.
3. **Tricky:** change one assumption, boundary, or input to expose a failure mode.

One example is enough for a simple idea; do not manufacture three. For a difficult
idea, a definition followed by a restatement is not an example. State inputs and
assumptions, work through the decisive steps, and interpret the result. Use examples
from the lecture when they teach well; invented teaching examples must not be
presented as source/exam evidence.

Prefer runnable code when useful and an execution tool is available. Otherwise
reason through it and identify unexecuted/version-sensitive behavior honestly.
Do not claim a snippet was run unless it was. Avoid dependency installation for a
small illustrative example when existing tools or a clear trace suffice.

## Explain mechanisms under the hood

Add **Under the Hood** when a hidden state change explains observable behavior or
enables prediction. Identify input/state → operation → changed state/output →
consequence. Match detail to the learning gap; omit implementation trivia.

Examples of useful targets: what `.fit()` changes, parameter updates, how BPE
chooses/applies merges, regex cursor/consumption behavior, signal propagation,
memory layout, or an algorithm's changing state. Distinguish conceptual behavior
from library/engine/version-specific mechanics. Do not present a teaching model
as a guarantee for every implementation.

## Resolve common confusions and compare close concepts

Use a **Common Confusion** callout when a plausible wrong inference would obstruct
later learning. Include the mistaken idea, why it sounds plausible, the correct
model, and a tiny contrast if useful. For example, a tokenizer and a language model
both process text, which invites conflation; explain their different roles in the
pipeline instead of merely saying they differ.

Use a comparison when the learner must choose between or distinguish similar
concepts. Choose dimensions such as purpose, inputs/outputs, state changes,
conditions, timing, limitations, or practical use. Useful pairs include training/
inference, feature extraction/learned model, stemming/lemmatization, ML/deep
learning, lookahead/lookbehind, and combinational/sequential logic. Tables help
aligned dimensions; a short contrast is enough for a single distinction. Avoid
false dichotomies and categorical claims where the boundary depends on context.

Explain the model in ordinary prose unless the callout earns emphasis. Excessive
callouts weaken hierarchy; do not highlight every fact, example, and definition.

## Bridge concepts and check understanding

For each planned transition, ask what the previous unit supplies and why the next
unit needs it. Insert a short bridge if that relationship is missing. A tokenization
pipeline should explain the contributions of tokens, vocabulary, learned merge
rules, encoding, and model inputs, not simply list them. Distinguish an added
explanatory bridge from a claim that the lecturer taught an external technique.

After a coherent group, add a compact **Checkpoint — You should now be able to
explain...**, predict, distinguish, or apply something. Choose one or a few tasks
that expose the unit's central model; do not repeat the heading list. If a checkpoint
needs untaught knowledge, fix the sequence or identify the prerequisite. Checkpoints
assess understanding; [breakpoints.md](breakpoints.md) decides whether to pause.

## Practical activities and answer placement

Select tasks from the subject table that exercise an important concept. Provide
inputs, constraints, relevant assumptions, and a clear question. For a new method,
show a worked example before asking for independent application. Thought experiments
and “try it yourself” activities can be more useful than code where the concept is
physical or theoretical. Include reasoning feedback, not just a numeric result.

For a small in-section exercise, put the prompt first and explicitly invite a
prediction or short attempt. Then provide a labeled **Solution / Check your
reasoning** after a meaningful separator or following explanatory block. Keep it
near enough for easy feedback; do not require a frustrating hunt across the guide.
Use a host's reveal capability only if available. The final quiz's answers instead
remain grouped in the separate [Answer Key](quizzes.md).

## Handle source objects as teaching content

### Diagrams and plots

Identify the diagram's purpose, labels/components, arrow or signal direction,
relationships, and the behavior the student should notice. Explain the path of one
input/signal or a meaningful change. For plots, explain axes, units, trends, and
what follows from them. Do not infer causation from an unlabeled arrow or a plot
without supporting evidence, and do not substitute “see diagram” for explanation.

Preserve source locator and enough semantics for later recreation: components,
connections, label meanings, direction, axes/units, and the instructional takeaway.
Mark illegible relationships as unresolved; visual extraction is not proof of
interpretation. Use [document-design.md](document-design.md) at handoff.

### Equations

For each important equation, define symbols and units/domains, state assumptions
and applicability, explain what changes with what, and connect the relationship to
intuition. Preserve course notation or explain any translation. Show substitution
and a worked calculation when application matters; derive steps when required or
useful under [proofs-and-derivations.md](proofs-and-derivations.md).

Check dimensions, signs, domains, and limiting behavior where meaningful. Keep an
equation's explanatory context even if the cheatsheet later compresses it. A list
of unexplained formulas is not a taught method.

### Code and procedures

Identify language/library or engine assumptions when behavior depends on them.
Explain key lines, non-obvious syntax, input/state changes, and expected behavior.
Add output/trace when it clarifies the mechanism; distinguish an API's mechanics
from the underlying concept. For a long snippet, focus commentary on decisive
steps while retaining important context and avoiding incorrect simplification.

### Tables

Use tables for aligned comparisons, mappings, trace states, or compact revision
lookups. Keep units, conditions, and meaningful labels. Use prose for causal
explanations and a list for independent points; not every list belongs in a table.
