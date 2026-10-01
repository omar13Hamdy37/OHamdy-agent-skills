# CUFE Study Guide v1 specification

**Status:** authoritative intended-behavior specification, authored in Phase 1.
**Plugin and skill identifier:** `cufe-study-guide`.
**Initial package version:** `0.1.0` (development; not publicly released).

This specification preserves the complete learning and document-output contract
for implementation in Phases 2–4. Requirements below describe the mature skill;
their presence in this document does not mean they are implemented in the scaffold.
The Phase 1 references identify responsibilities and implementation work rather
than reproduce this specification.

## 1. Product purpose and priorities

Transform supplied university lecture material into a complete, pedagogically
strong, practical, enjoyable, and polished study guide tailored to how the student
learns. Intelligently filter low-value material while preserving important concepts.
Act as a study-guide author, tutor, and document designer, with enough explanation
for genuine learning and enough structure for later revision and exam preparation.

The target is neither a slide transcript nor a generic summary. A shorter source
may need a longer explanation; a long repetitive source may support a shorter guide.
Do not optimize for a compression ratio or page count at the expense of learning.

### Scope and activation

Use for requests to turn university lecture slides, PDFs, or documents into study
guides; create structured learning material from lectures; produce comprehensive
but intelligently condensed study notes; or create DOCX/PDF study guides from
supplied course material. The name is stable, but applicability is determined by
this use case rather than requiring a particular university's metadata.

Exclude unrelated summarization, generic report writing, ordinary document editing,
and topics without a lecture-learning request. The description must communicate
both the capability and the circumstances in which to use it.

### Default priority order

1. Correctness.
2. Completeness of important material.
3. Understanding.
4. Practical learning.
5. Clarity.
6. Usefulness for revision and exams.
7. Conciseness where appropriate.
8. Polished presentation.

These priorities guide tradeoffs. Presentation must never hide a technical error;
conciseness must never justify silently dropping an important concept.

## 2. Runtime contract and evidence

### Inputs and preferences

Accept supplied lecture slides/PDFs/documents and the user's ordinary-language
instructions. Relevant prior inputs may be previous lecture files, previous study
guides, or a folder/path containing prior material. Inspect accessible relevant
files without treating every file in a folder as useful evidence.

The user may specify output format, learning depth, course context, quiz style,
cheatsheet preference, or other constraints naturally. Follow explicit preferences;
do not demand rigid command syntax. Infer routine choices from course material.
Ask only for missing information that materially prevents a correct useful result.

Read meaningful visual content as well as extracted text. Equations, diagrams,
plots, code, table cells, symbols, and annotations may carry essential concepts.
Do not claim coverage of unreadable or inaccessible input. Identify gaps and
uncertainty, and obtain better evidence when needed rather than inventing content.

### Sources of truth

- User instructions set the requested task, adaptations, and outputs.
- The current lecture is the syllabus and authority for course scope. Its wording,
  slide order, and formatting need not be copied.
- Prior lectures and guides supply relevant context and relationships. A prior
  guide is a secondary interpretation; check the source lecture when an important
  inconsistency can be resolved from available material.
- Added explanations may unpack course material. External enrichment must not
  silently become lecture-required content.
- Technical correctness remains the first priority. If a lecture appears wrong
  or ambiguous, distinguish the source statement from a supported correction or
  unresolved interpretation; do not faithfully reproduce a known error as fact.

During development, this specification governs v1 decisions. Phase 2 must translate
its behavior into packaged runtime references. End users must not need repository
`docs/` or `evals/` files to run the installed skill.

### Intended workflow

Inspect evidence and preferences → inventory meaningful content → plan concept
dependencies and guide coverage → author explanations and activities → add useful
connections, breakpoints, quiz, and conditional cheatsheet → audit learning and
accuracy → export requested formats → inspect rendered results → repair defects
and deliver the actual files.

This is a decision framework, not a fixed chapter template. Adapt the teaching
sequence and tooling while preserving the requirements below.

## 3. Behavioral requirements A–T

### A. Core philosophy

Teach the lecture so a student can genuinely learn from it. Preserve the default
priority order in §1. Treat the lecture as the syllabus/source of truth without
copying its wording or slide structure. Author a coherent, practical, approachable
guide that normally stands alone for understanding important course topics.

An enjoyable guide uses clear prose, helpful examples, and a supportive tutor's
voice. Avoid distracting decoration, forced humor, or simplifying away rigor.

**Acceptance:** a student can understand important ideas and revise from the guide,
not merely recognize an outline of the slides.

### B. Intuition-first teaching

Prefer **Why → intuition → mechanism → terminology → examples** over starting
with formal definitions and jargon. When introducing new material, commonly answer:

- What is this?
- Why do we need it?
- What problem does it solve?
- How does it actually work?
- What happens internally?
- What happens in edge cases?
- How is it different from related concepts?

Use the simplest technically correct language. Introduce formal terminology when
the terminology matters, and retain technically important detail. These questions
guide explanation choices; they are not mandatory repeated headings for every idea.

**Acceptance:** motivation and a usable mental model accompany unfamiliar concepts;
plain language remains technically accurate.

### C. Intelligent content filtering

Omit or heavily compress low-value material when appropriate: course logistics,
repeated explanations, administrative slides, lecturer biography, unnecessary
references, redundant examples, and obvious filler. Keep references that establish
required reading or materially support understanding.

**Slide length must never be treated as a measure of importance.** A one-line slide
may need half a page of explanation. Remove repetition and low-value content,
not important or examinable concepts. Retain a distinct example if it teaches
an edge case or mechanism that the other examples do not cover.

The guide should normally stand alone well enough that the student does not have
to reopen the lecture merely to understand the topic. Do not compress formulas,
assumptions, diagram relationships, or definitions until their meaning is lost.

**Acceptance:** every omission/condensation has a defensible learning rationale;
importance is assessed conceptually rather than by slide size.

### D. Completeness and coverage audit

Actively guard against accidental omission. Maintain an internal lecture coverage
audit mapping meaningful source concepts to guide sections or an explicit reason
for omission/condensation. Include important formulas, diagrams, proof steps,
conditions, and examples with distinct instructional value.

Example audit shape:

```text
Topic A → Guide §2
Topic B → Guide §3
Repeated example → intentionally condensed; same mechanism taught in §3
Formula C → Guide §5.2
Diagram D → explained in Guide §6
Administrative slide → intentionally omitted; course logistics
```

Use source page/slide identifiers when available to make auditing traceable. The
audit can remain internal; it need not clutter the student's document. Resolve
unaccounted important items before export. An unreadable source is an evidence
gap, not an omission that can be marked safely complete.

**Acceptance:** each meaningful source item has a location or explicit disposition,
and no important concept is silently lost.

### E. Terminology handling

Explain a technical/domain-specific term immediately at its first meaningful use
when it may be unfamiliar. Do not assume jargon is understood because the lecture
uses it. Use a simple explanation, then the formal name where needed for precision
or exam recognition. Avoid defining ordinary language unnecessarily.

**Acceptance:** students do not need to search for an unfamiliar term before they
can follow the explanation that depends on it.

### F. Progressive examples

Where appropriate, progress **tiny → realistic → tricky**. First isolate the
mechanism, then show a plausible application, then expose a boundary condition
or common mistake. Examples must teach more than restate a definition.

For programming/technical courses, use executable or realistic examples when
useful. Keep code, outputs, units, assumptions, and calculations consistent.
Do not require three examples for concepts that need only one good illustration.

**Acceptance:** examples build transferable understanding and handle relevant
edge cases without adding redundant length.

### G. Under-the-hood explanations

Explain internal behavior when it materially improves understanding. Useful
targets include what `.fit()` really does, how BPE learns merges, why parameters
change during training, how a regex engine consumes or does not consume text,
and what signals, ports, or components actually do internally.

Tie internal steps to observable behavior and the concept being learned. Do not
overload every topic with implementation details that add no learning value.

**Acceptance:** selected mechanisms answer a real understanding gap and preserve
the distinction between a conceptual model and implementation-specific behavior.

### H. Practical learning

Include useful hands-on learning suited to the discipline: worked examples, small
exercises, code exercises, output prediction, debugging questions, calculation
practice, thought experiments, derivations, and “try it yourself” sections.

When appropriate, ask the learner to predict an answer before revealing it.
Provide enough setup and feedback to make activities usable; align them with
concepts already taught or clearly identified prerequisites.

**Acceptance:** the learner has meaningful opportunities to apply and reason,
not only read explanations or memorize vocabulary.

### I. Common-confusion callouts

Detect likely misconceptions and include visually distinct **Common Confusion**
notes when helpful. Explain why the confusion occurs and the correct mental model.
Examples include grayscale versus binary image, feature extraction versus machine
learning, training versus inference, tokenizer versus language model, and lookahead
versus consumed characters.

Use relevant misconceptions rather than a decorative warning for every section.

**Acceptance:** a callout resolves a specific misunderstanding and uses a textual
label as well as its visual treatment.

### J. Explicit comparisons

When related concepts are easy to confuse, use concise comparisons or tables.
Choose distinguishing dimensions that matter for use and understanding.

Useful examples: stemming versus lemmatization, ML versus deep learning, training
versus inference, lookahead versus lookbehind, combinational versus sequential
logic, and feature extraction versus a learned model.

**Acceptance:** comparisons explain meaningful differences and relationships;
they do not rely on misleading oversimplification.

### K. Conceptual bridges

Reconstruct explanatory bridges that the lecture skips because the lecturer
assumes the relationship is obvious. Explicitly explain how consecutive ideas
connect when that relationship helps the student understand the next concept.

Example chain: **text → tokens → vocabulary → BPE → tokenizer → language model
input**. Explain what each transition contributes instead of merely listing names.
Reorder material when it helps dependency-aware teaching while preserving coverage.

**Acceptance:** a student can explain why the next idea follows and how it uses
the previous idea.

### L. Learning checkpoints

After meaningful groups of concepts, include compact understanding checkpoints
such as **You should now be able to explain...**. Test causal reasoning, distinctions,
prediction, or application rather than rote repetition of definitions.

**Acceptance:** checkpoints expose whether the learner understands the group of
concepts and are positioned after a coherent learning unit.

### M. Adaptive structure

Adapt pedagogy to the subject without imposing one identical chapter structure.
Illustrative sequences:

| Discipline | Possible teaching sequence |
| --- | --- |
| Programming | concept → syntax → example → code → common mistake → exercise |
| Machine learning | problem → intuition → training → prediction → example → limitations |
| Signals/electronics | physical intuition → mathematical model → derivation → worked example → interpretation |
| Theory | motivation → concept → relationship → example → understanding check |

These are examples, not rigid templates. Maintain a consistent visual system
while adapting the explanatory sequence, practice, and mathematical detail.

**Acceptance:** organization follows the subject's learning needs while document
hierarchy and semantic design remain consistent.

### N. Pomodoro-friendly conceptual breakpoints

Provide useful natural stopping points roughly corresponding to **30 minutes of
focused study**. Conceptual continuity is more important than exactly 30 minutes.
Estimates must consider reasoning and activities, not just reading length; do not
promise an exact pace for every learner.

Never split a proof, dependency chain, worked example, tightly coupled explanation,
or concept whose next section is essential to complete it. Prefer a natural
boundary somewhat earlier or later over an arbitrary time/page target. A short
lecture need not gain decorative break markers just to mimic a longer guide.

Example note: **Good stopping point — the next section begins a mostly independent
concept. You can safely take a break here.**

**Acceptance:** each breakpoint closes a coherent unit and allows safe resumption;
the notes are genuinely useful rather than evenly spaced decoration.

### O. Cross-lecture connections

When previous lecture files, previous study guides, or a folder/path of prior
material are provided, intelligently inspect relevant sources and add connections
that improve understanding. Ground a connection in inspected evidence; do not
invent a lecture number, prerequisite, or prior explanation.

Classify useful relationships as:

- **Prerequisite:** knowledge needed for the current concept.
- **Continuation:** a previous idea developed further.
- **Contrast:** a distinction from related prior material.
- **Reuse/application:** an earlier technique applied in the current context.

Example wording:

- **Prerequisite — This relies on convolution introduced in Lecture 2.**
- **Continuation — The previous lecture introduced tokens; this lecture explains
  how the vocabulary can be learned.**

Give enough recap or a helpful pointer that the connection aids learning. Do not
add connections merely to prove previous files were read. When none are relevant,
omit them. If prior material is unavailable, disclose that limitation instead of
claiming inspection.

**Acceptance:** connections have an accurate source and instructional purpose,
with a relationship type that fits the evidence.

### P. End-of-lecture quiz

Every substantial guide should end with a small but meaningful quiz unless the
user asks otherwise. A substantial guide teaches enough connected concepts to
benefit from a real understanding check; do not invent a universal page threshold.
Default to compact but significant coverage, testing whether the lecture was
understood rather than whether terms were seen.

Accept natural-language preferences for conceptual, scenario-heavy, terminology,
exam-style, code-tracing, calculation-heavy, or mixed quizzes. Adapt type and depth
to course content and the user's preference; terminology questions can still test
distinctions and use rather than rote recall.

Place answers in a separate **Answer Key** after the quiz so they are not immediately
visible while attempting questions. In exports, use deliberate spacing/pagination
or another appropriate separation. Explain reasoning, not merely the correct
option. Check answers against the guide and source evidence.

**Acceptance:** meaningful concepts are sampled, preference is respected, answers
are separated, and each answer's reasoning is correct.

### Q. Proofs and derivations

Include proofs/derivations when useful, with clear classification:

| Type | Rule |
| --- | --- |
| **Lecture Proof / Derivation** | Present in the supplied lecture; treat it as course material and preserve important reasoning, assumptions, and steps. |
| **Optional Insight Proof** | Not explicitly required by the lecture, but short and useful for understanding instead of memorization. Label **Understanding aid — not required for memorization.** |
| **Extended Proof** | Useful but too long for the guide; provide a clickable link to a clear, credible external explanation instead of importing excessive length. |

The extended-proof option is for enrichment; do not discard a lecture-required
proof solely because it is long. Course coverage and conceptual continuity still
apply. Clearly separate external enrichment from lecture-required content, verify
the link, and explain what the reader gains from it.

This is especially relevant to electronics, signals, mathematics, neural networks,
and algorithms. Preserve algebra, units, notation, assumptions, and logical steps.

**Acceptance:** classification and exam expectations are unambiguous; course
proofs remain covered and optional material is labeled accurately.

### R. Cheatsheets

Create a cheatsheet when the user explicitly requests one, or when the lecture
naturally benefits because it contains substantial syntax, formulas, rules,
transformations, mappings, APIs/functions, comparisons, or patterns.

Do not force a cheatsheet into every lecture. Make it a useful revision aid with
conditions, notation, and essential distinctions; it must not substitute for the
explanations in the guide. Choose placement or a separate artifact to suit the
request and future output design.

**Acceptance:** explicit requests are honored; automatic inclusion has a clear
revision benefit and does not encourage incorrect memorization.

### S. Source fidelity and enrichment distinction

When useful for course/exam expectations, distinguish material directly from the
lecture, expanded explanation that makes the lecture understandable, and optional
enrichment beyond lecture requirements. Use strategic labels or section grouping;
do not plaster a provenance tag onto every paragraph.

The student should be able to answer: **Do I need to know this for the course,
or is this here to deepen understanding?** Avoid unsupported claims about what
will appear on an exam. Added explanation of a required concept is not automatically
optional just because the lecturer omitted that explanation.

**Acceptance:** relevant scope distinctions are visible without adding visual noise
or misclassifying explanatory course material.

### T. Final quality-control pass

Before final export, verify all of the following, repairing defects found:

- Important lecture concepts are covered and coverage-audit dispositions are valid.
- No important formula is accidentally missing; assumptions and notation remain clear.
- Diagrams are handled appropriately: preserved, redrawn, or explained with their
  important relationships intact; unreadable evidence is not treated as understood.
- Technical terminology is explained at first meaningful use where unfamiliar.
- Examples, code outputs, calculations, and exercises are correct.
- Explanations are technically accurate and not misleading.
- Relationships and transitions between concepts are clear.
- Optional enrichment is labeled where the distinction matters.
- Proofs and derivations are classified correctly.
- External links work; inability to verify a link is disclosed and resolved where possible.
- Breakpoints occur at sensible conceptual boundaries.
- Cross-lecture connections are actually relevant and evidence-backed.
- The quiz covers meaningful concepts and fits any requested style.
- The Answer Key is separate, correct, and explains reasoning.
- Unnecessary repetition has been removed.
- The guide can reasonably stand on its own for understanding.
- Formatting and semantic styling are consistent.
- Requested DOCX/PDF artifacts render correctly after export, including final repairs.

The content checks precede export; render checks follow export and must be repeated
for changed pages/artifacts after repairs. File existence alone is insufficient.

**Acceptance:** final content and actual rendered deliverables pass the relevant
checks; the delivery report states any remaining source/tool limitations honestly.

## 4. Document-output contract (primarily Phase 3)

### Formats and delivery

Create polished **`.docx` and `.pdf`** files. The user may request either or both;
normal use is expected to produce both. Use professional document authoring rather
than a mechanical Markdown-to-Word appearance.

Preserve consistent content across requested formats, with usable heading hierarchy,
readable mathematics, tables, diagrams, code, exercises, and clickable external
links. Inspect actual rendered pages, correct clipping/overflow and poor page
breaks, and verify quiz/answer separation. Deliver actual accessible file links.
Do not claim a format was generated if the available host cannot create it.

### Semantic visual system

Use a consistent semantic design system. Exact colors are deferred to Phase 3;
meaning must stay stable. Potential categories:

| Semantic type | Intended signal |
| --- | --- |
| Core concept | The main idea or essential model. |
| Important/reminder | A condition, rule, or recall cue worth keeping in mind. |
| Common confusion/warning | A likely misconception, boundary, or mistake. |
| Worked example/practical application | Reasoning in action and hands-on practice. |
| Previous-lecture connection | A useful relationship with inspected prior material. |
| Under-the-hood/insight | Internal mechanisms that improve understanding. |
| Optional enrichment | Material beyond lecture requirements. |

**Color must not be the only signal.** Each semantic type also needs a textual
heading, icon, or shape, with textual identification wherever meaning would
otherwise be ambiguous. Remain understandable with limited color perception and
grayscale printing.

Optimize for low visual noise, strong hierarchy, readability, consistency,
accessibility, and focused studying. Avoid excessive decoration and unnecessary
callouts. Keep content semantics separate from exact palette/template decisions
so both local generators and host-native artifact tools can express the same system.

### Cover page

Create a visually attractive, subject-aware, minimal cover. Normally show only
the subject/course name, lecture number if known, lecture/topic name, and subtle
subject-related artwork or visual design. Do not invent missing metadata.

Do not automatically add **Prepared by**, **Submitted to**, **Date**, **Student ID**,
professor fields, or large metadata tables. Include such report-style details only
when explicitly requested. The cover must support studying rather than imitate
a university submission form.

## 5. Work/Codex portability

The skill's intelligence must not depend on one specific local script. Teaching
workflow and decisions live in portable instructions/references. Scripts/assets
are document-generation helpers, selected only when justified by actual needs.

Target flows:

```text
Codex → same skill intelligence → document tools/scripts → DOCX/PDF
ChatGPT Work, where supported → same skill intelligence → native artifact/document capabilities → DOCX/PDF
```

Avoid unnecessary hard-coded host names, absolute development paths, tool IDs,
or a mandatory Python/Node engine in runtime pedagogy. Detect available tooling
and retain the same coverage, learning, quiz, and design decisions across hosts.
Availability of repo marketplace installation and output tools is surface-specific;
validate supported flows before claiming compatibility at release.

No MCP server, external account authentication, npm installer, or network service
is required for the Phase 1 skills-only package. Runtime learning must not depend
on eval assets or repository development documentation.

## 6. Reference ownership and implementation boundaries

All references are under
`plugins/cufe-study-guide/skills/cufe-study-guide/references/`.

| Reference | Primary responsibility | Requirement coverage |
| --- | --- | --- |
| `learning-philosophy.md` | Priorities, intuition-first teaching, standalone learning, and discipline adaptation. | A, B, M |
| `content-selection.md` | Keep/omit/compress decisions, important source items, and coverage audit. | C, D, S |
| `teaching-style.md` | Terminology, progressive examples, mechanisms, practice, misconceptions, comparisons, bridges, and checkpoints. | E–M |
| `cross-lecture-connections.md` | Prior-material inspection and useful relationship classification. | O |
| `breakpoints.md` | Approximate study sessions and intact conceptual boundaries. | N |
| `quizzes.md` | Substantial-guide quiz, natural-language preferences, and Answer Key. | P |
| `proofs-and-derivations.md` | Course proofs, optional insights, and linked extended proofs. | Q, S |
| `cheatsheets.md` | Explicit/automatic inclusion and revision usefulness. | R |
| `document-design.md` | Format contract, semantic design, accessibility, minimal cover, and render QA. | §4, §5 |
| `quality-checklist.md` | Final learning, coverage, accuracy, and rendered-output gates. | D, T |

Phase 1 files contain purpose, scope, relevant key requirements, and actionable
Phase 2 TODO notes. Phase 2 replaces scaffolding with operational guidance, resolves
overlap by linking the owning reference, and retains progressive disclosure.
Keep `SKILL.md` as the concise entrypoint, not a copy of this master specification.

Document design has a Phase 2 semantic handoff and Phase 3 implementation. Scripts
and assets remain empty until a concrete helper/template requirement is implemented.

## 7. Evaluation architecture (foundation now; implementation in Phase 4)

Developer/regression evals live in `evals/cufe-study-guide/`, outside distributable
runtime plugin content. Reserve `cases/`, `fixtures/`, and `graders/`. Do not create
fake lecture fixtures or a full runner in Phase 1.

Future categories: should-trigger, should-not-trigger, lecture coverage,
terminology quality, conceptual clarity, breakpoint quality, cross-lecture
relationships, quiz quality, proof classification, cheatsheet decisions, DOCX
generation, PDF generation, and visual/render checks.

Combine deterministic checks with rubric/model grading:

- **Deterministic:** file existence, requested DOCX/PDF creation, expected sections,
  separate Answer Key, syntactically valid links, no missing required metadata
  when it is known/requested, correct package paths, and structured coverage
  invariants. Syntax checks do not replace link reachability or content review.
- **Rubric/model:** explanation quality, beginner-friendliness, conceptual
  completeness, useful examples, appropriate depth, grounded prior relationships,
  meaningful quizzes, and pedagogically sensible breakpoints.
- **Visual/render:** inspect actual exported pages for readability, hierarchy,
  accessibility, clipping, pagination, and faithful formulas/diagrams/code.

Phase 4 implements **build → eval → diagnose → repair → rerun** using real lecture
fixtures, with developer review of fixes. The mature skill itself must not rewrite
its instructions, fixtures, or graders during normal user execution.

## 8. Phase acceptance and exclusions

### Phase 1 completion

- The intended Windows workspace is a Git repository on `main`, with `origin`
  pointing to `https://github.com/omar13Hamdy37/OHamdy-agent-skills.git`.
- Current official formats are checked and significant choices are sourced in
  `docs/architecture.md`; portable plugin/marketplace paths are structurally valid.
- All JSON and skill YAML/front matter parse; source paths resolve, references
  remain within the package, and the skill is structurally discoverable.
- Requirements A–T, document design, portability, and eval boundaries are recorded
  here, with concise reference ownership and no missing behavior.
- Repository links/URLs and placeholders are reviewed, dependencies are unnecessary,
  `git status` and the complete diff are reviewed, and an initial commit is made.
- Push to `origin/main` without force when permitted; preserve the local commit
  and report the actual blocker if pushing fails.

### Phase 1 exclusions

Do not implement the complete teaching system, final document generator, full eval
runner, final design templates, fake sample lectures, or large binary assets.
Do not add unnecessary Python/Node dependencies, an npm installer, MCP servers,
GitHub Actions without a compelling foundation need, or npm/public-directory
publication. Do not choose a software license, create `LICENSE`, bloat the entrypoint,
or copy this specification's detailed prose into every reference.

### Later-phase acceptance

Phase 2 implements the learning contract in portable references. Phase 3 implements
and visually verifies professional document output. Phase 4 implements full evals,
real-lecture testing, reviewed repair iterations, clean-environment release
validation, final README, and **very short, beginner-friendly marketplace
download/install instructions**. No phase may claim another phase's unimplemented
capabilities as complete.

The [development plan](../development.md) defines phase handoffs; the
[eval foundation](../../evals/cufe-study-guide/README.md) records future test ownership.
