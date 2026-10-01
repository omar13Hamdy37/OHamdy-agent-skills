"""Strict shape and relationship validation before either renderer is invoked."""

import json
import re
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator
from PIL import Image

SKILL_ROOT = Path(__file__).resolve().parents[2]
ASSETS = SKILL_ROOT / "assets"


class GuideError(ValueError):
    """A useful input, capability, or output diagnostic."""


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise GuideError(f"Cannot read JSON {path}: {exc}") from exc


def walk_blocks(model):
    """Yield every content block once, including assessment and feedback blocks."""
    def blocks(items):
        for item in items:
            yield item
            for field in ("blocks", "prompt", "hint", "solution", "answer", "explanation"):
                value = item.get(field)
                if isinstance(value, list) and value and isinstance(value[0], dict) and "type" in value[0]:
                    yield from blocks(value)
            for question in item.get("questions", []):
                yield from blocks(question["prompt"])
            for answer in item.get("answers", []):
                yield from blocks(answer["answer"])
                yield from blocks(answer["explanation"])

    def sections(items):
        for section in items:
            yield from blocks(section["blocks"])
            yield from sections(section.get("subsections", []))

    yield from sections(model["sections"])
    yield from blocks(model.get("end_matter", []))


def sections(model):
    def descend(items, level):
        for section in items:
            yield section, level
            yield from descend(section.get("subsections", []), level + 1)
    yield from descend(model["sections"], 1)


def runs(value):
    return [{"text": value}] if isinstance(value, str) else value


def plain(value):
    return "".join(run["text"] for run in runs(value))


def image_path(block, base):
    path = Path(block["path"]).expanduser()
    return path.resolve() if path.is_absolute() else (base / path).resolve()


def validate(model, base):
    schema = load_json(ASSETS / "study-guide.schema.json")
    supported = {"paragraph", "heading", "list", "quote", "caption", "code", "table", "equation", "image",
                 "page_break", "callout", "proof", "exercise", "quiz", "answer_key"}
    semantics = schema["$defs"]["callout"]["properties"]["semantic"]["enum"]
    def known_types(value, location="root"):
        if isinstance(value, dict):
            if "type" in value and value["type"] not in supported:
                raise GuideError(f"Unsupported block type at {location}: {value['type']!r}")
            if "semantic" in value and value["semantic"] not in semantics:
                raise GuideError(f"Unknown semantic type at {location}: {value['semantic']!r}")
            if value.get("show_provenance") and "provenance" not in value:
                raise GuideError(f"Visible provenance requires an explicit classification at {location}")
            for key, child in value.items():
                known_types(child, f"{location}/{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                known_types(child, f"{location}/{index}")
    known_types(model)
    errors = sorted(Draft202012Validator(schema).iter_errors(model), key=lambda e: str(list(e.path)))
    if errors:
        # Select the deepest alternative error to avoid printing the entire oneOf schema.
        def deepest(error):
            return max((deepest(child) for child in error.context), key=lambda e: len(e.absolute_path)) if error.context else error
        error = deepest(errors[0])
        location = "/".join(map(str, error.absolute_path)) or "root"
        raise GuideError(f"Invalid guide at {location}: {error.message}")
    ids = set()

    def register(identifier):
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,79}", identifier):
            raise GuideError(f"Invalid ID {identifier!r}; use a letter followed by letters, digits, '_' or '-'")
        if identifier in ids:
            raise GuideError(f"Duplicate ID: {identifier}")
        ids.add(identifier)

    for section, level in sections(model):
        register(section["id"])
        if level > 6:
            raise GuideError("Section hierarchy exceeds six heading levels")
        if not section["blocks"] and not section.get("subsections"):
            raise GuideError(f"Empty section: {section['id']}")
    all_blocks = list(walk_blocks(model))
    for block in all_blocks:
        if "id" in block:
            register(block["id"])
        if block["type"] == "table":
            n = len(block["headers"])
            if any(len(row) != n for row in block["rows"]):
                raise GuideError("Table row length must match its headers")
            if "column_weights" in block and len(block["column_weights"]) != n:
                raise GuideError("Table column_weights must match its headers")
            if n > 10:
                raise GuideError("Table has more than 10 columns; split it into meaningful tables")
        if block["type"] == "image":
            path = image_path(block, base)
            try:
                with Image.open(path) as image:
                    image.verify()
            except (OSError, ValueError) as exc:
                raise GuideError(f"Missing or invalid local image {path}: {exc}") from exc
    end = model.get("end_matter", [])
    quizzes = [b for b in all_blocks if b["type"] == "quiz"]
    keys = [b for b in all_blocks if b["type"] == "answer_key"]
    if len(quizzes) > 1 or len(keys) > 1:
        raise GuideError("Version 1.0 supports one final quiz and one Answer Key")
    if any(b not in end for b in quizzes + keys):
        raise GuideError("Quiz and Answer Key must be top-level end_matter blocks")
    questions = quizzes[0]["questions"] if quizzes else []
    if quizzes and not quizzes[0].get("id"):
        register("guide-quiz")
    if keys and not keys[0].get("id"):
        register("guide-answer-key")
    for question in questions:
        register(question["id"])
    separate = [b for b in all_blocks if b["type"] == "exercise" and b["solution_placement"] == "answer_key"]
    if (quizzes or separate) and not keys:
        raise GuideError("A quiz or separate exercise solution requires an Answer Key")
    if keys:
        if quizzes and end.index(keys[0]) <= end.index(quizzes[0]):
            raise GuideError("Answer Key must follow the quiz")
        if end[-1] is not keys[0]:
            raise GuideError("Answer Key must be the final end_matter block")
        answers = [a["question_id"] for a in keys[0]["answers"]]
        expected = [q["id"] for q in questions]
        if len(answers) != len(set(answers)) or set(answers) != set(expected):
            raise GuideError("Answer Key question IDs must match every quiz question exactly once")
        if not questions and not separate:
            raise GuideError("Empty Answer Key has no quiz or separate exercise solutions")

    def values(value):
        if isinstance(value, dict):
            if "href" in value:
                href = value["href"]
                if href.startswith("#"):
                    if href[1:] not in ids:
                        raise GuideError(f"Broken internal link: {href}")
                else:
                    parsed = urlparse(href)
                    if parsed.scheme not in ("https", "http", "mailto") or not parsed.path and not parsed.netloc:
                        raise GuideError(f"Unsupported hyperlink: {href}")
                    if parsed.scheme in ("http", "https") and not parsed.netloc:
                        raise GuideError(f"Invalid hyperlink: {href}")
            for child in value.values():
                values(child)
        elif isinstance(value, list):
            for child in value:
                values(child)
    values(model)
    return model
