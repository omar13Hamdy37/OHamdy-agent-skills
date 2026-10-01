"""Compile semantics once. Both renderers consume the exact same ordered events."""

from .model import plain


def compile_guide(model, theme):
    events = []
    deferred = []
    semantic_labels = theme["semantics"]

    def add(kind, data, semantic=None, group=None):
        events.append({"kind": kind, "data": data, "semantic": semantic, "group": group})

    def paragraphs(text, semantic=None, group=None):
        add("paragraph", {"content": text}, semantic, group)

    def children(items, context=None, group=None):
        for block in items:
            kind = block["type"]
            if block.get("show_provenance"):
                paragraphs(block.get("provenance", "course_material").replace("_", " ").capitalize(), context, group)
            if kind == "callout":
                semantic = block["semantic"]
                g = block.get("id", f"group-{len(events)}")
                keep = block.get("keep_together", semantic in ("worked_example", "checkpoint", "breakpoint"))
                add("group_start", {"keep": keep}, semantic, g)
                if semantic != "core_explanation":
                    label = semantic_labels[semantic]["label"]
                    if semantic == "previous_lecture_connection":
                        label += " - " + block["relationship"].replace("_", " / ").capitalize()
                    if block.get("title"):
                        label += " - " + block["title"]
                    add("label", {"text": label, "id": block.get("id")}, semantic, g)
                elif block.get("id"):
                    add("anchor", {"id": block["id"]})
                if semantic == "previous_lecture_connection":
                    paragraphs(block["previous_context"], semantic, g)
                children(block["blocks"], None if semantic == "core_explanation" else semantic, g)
                add("group_end", {}, semantic, g)
            elif kind == "proof":
                g = block.get("id", f"proof-{len(events)}")
                add("group_start", {"keep": block.get("keep_together", True)}, "proof", g)
                labels = {"lecture_proof": "Lecture Proof / Derivation", "optional_insight": "Optional Insight Proof", "extended_proof": "Extended Proof"}
                label = labels[block["classification"]]
                if block.get("title"):
                    label += " - " + block["title"]
                add("label", {"text": label, "id": block.get("id")}, "proof", g)
                if block["classification"] != "lecture_proof":
                    paragraphs("Understanding aid - not required for memorization.", "proof", g)
                children(block["blocks"], "proof", g)
                if block.get("resource"):
                    paragraphs([block["resource"]], "proof", g)
                add("group_end", {}, "proof", g)
            elif kind == "exercise":
                g = block["id"]
                add("group_start", {"keep": True}, "exercise", g)
                add("label", {"text": "Exercise - " + block.get("title", g), "id": g}, "exercise", g)
                children(block["prompt"], "exercise", g)
                if block.get("hint"):
                    add("label", {"text": "Hint"}, "exercise", g)
                    children(block["hint"], "exercise", g)
                add("group_end", {}, "exercise", g)
                if block["solution_placement"] == "inline":
                    add("attempt_space", {})
                    add("label", {"text": "Solution / Check your reasoning"}, "exercise")
                    children(block["solution"], "exercise")
                elif block["solution_placement"] == "answer_key":
                    deferred.append(block)
            elif kind == "quiz":
                add("page_break", {})
                add("heading", {"text": block.get("title", "Quiz"), "id": block.get("id", "guide-quiz"), "level": 1}, "quiz")
                for question in block["questions"]:
                    g = question["id"]
                    add("group_start", {"keep": True}, "quiz", g)
                    add("label", {"text": g, "id": g}, "quiz", g)
                    children(question["prompt"], None, g)
                    if question.get("options"):
                        add("list", {"items": question["options"], "ordered": True, "letters": True}, None, g)
                    add("group_end", {}, "quiz", g)
            elif kind == "answer_key":
                add("page_break", {})
                add("heading", {"text": block.get("title", "Answer Key"), "id": block.get("id", "guide-answer-key"), "level": 1}, "answer_key")
                for answer in block["answers"]:
                    add("label", {"text": answer["question_id"]}, "answer_key")
                    children(answer["answer"])
                    add("label", {"text": "Reasoning"})
                    children(answer["explanation"])
                for exercise in deferred:
                    add("label", {"text": "Exercise " + exercise["id"]})
                    children(exercise["solution"])
            else:
                data = dict(block)
                data.pop("type")
                if kind != "heading" and block.get("id"):
                    add("anchor", {"id": block["id"]})
                add(kind, data, context, group)

    def section(items, level=1):
        for item in items:
            add("heading", {"text": item["title"], "id": item["id"], "level": level})
            children(item["blocks"])
            section(item.get("subsections", []), level + 1)

    section(model["sections"])
    children(model.get("end_matter", []))
    # Page-break hints must not manufacture blank pages at structural boundaries.
    cleaned = []
    for event in events:
        if event["kind"] == "page_break" and (not cleaned or cleaned[-1]["kind"] == "page_break"):
            continue
        cleaned.append(event)
    while cleaned and cleaned[-1]["kind"] == "page_break":
        cleaned.pop()
    return cleaned


def navigation(model, events):
    headings = [e["data"] for e in events if e["kind"] == "heading" and e["data"]["level"] <= 2]
    words = sum(len(plain(e["data"]["content"]).split()) for e in events if e["kind"] == "paragraph")
    choice = model.get("theme", {}).get("toc", "auto")
    return headings if choice == "always" or choice == "auto" and (len(headings) >= 10 or words >= 6000) else []
