"""Shared semantic palette, portable font resources, and page geometry."""

from pathlib import Path
import os
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "ohamdy-study-guide-matplotlib"))
import matplotlib
from matplotlib.ft2font import FT2Font

from .model import ASSETS, GuideError, load_json


def get_theme(model, override=None):
    name = override or model.get("theme", {}).get("name", "academic")
    theme = load_json(ASSETS / "themes/academic.json")
    if name == "grayscale":
        for item in theme["semantics"].values():
            item.update(accent="#404040", background="#F5F5F5")
        theme.update(text="#202020", muted="#505050", link="#303030", code_background="#F4F4F4", table_header="#EAEAEA")
    elif name != "academic":
        raise GuideError(f"Unknown theme: {name}")
    theme.setdefault("table_header", "#E9EFF2")
    paper = model.get("theme", {}).get("paper_size", "A4")
    theme["page"] = (595.2756, 841.8898) if paper == "A4" else (612, 792)
    theme["margin"] = theme["margin_mm"] * 72 / 25.4
    theme["width"] = theme["page"][0] - 2 * theme["margin"]
    return theme


def font_files():
    base = Path(matplotlib.get_data_path()) / "fonts/ttf"
    return {"body": base / "DejaVuSans.ttf", "bold": base / "DejaVuSans-Bold.ttf",
            "italic": base / "DejaVuSans-Oblique.ttf", "bold_italic": base / "DejaVuSans-BoldOblique.ttf",
            "mono": base / "DejaVuSansMono.ttf", "mono_bold": base / "DejaVuSansMono-Bold.ttf"}


def check_glyphs(events, metadata):
    from .artifact_checks import expected_text
    available = set(FT2Font(str(font_files()["body"])).get_charmap())
    mono = set(FT2Font(str(font_files()["mono"])).get_charmap())
    def inspect(value, glyphs):
        if isinstance(value, str):
            missing = sorted({c for c in value if not c.isspace() and ord(c) not in glyphs})
            if missing:
                raise GuideError(f"Unsupported font glyphs {missing[:8]!r}; use a suitable native renderer or supported notation")
            # Glyph presence alone cannot provide correct complex-script shaping.
            if any('\u0590' <= c <= '\u08ff' for c in value):
                raise GuideError("The baseline renderer does not support RTL/complex-script shaping; use a capable native renderer")
        elif isinstance(value, list):
            for child in value:
                inspect(child, glyphs)
    for key in ("title", "title_override", "course", "subtitle", "lecture_number"):
        inspect(str(metadata.get(key, "")), available)
    for field in metadata.get("cover_fields", []):
        inspect(field["label"] + ": " + field["value"], available)
    for text in expected_text(events):
        inspect(text, available)

    def inline_code(value):
        if isinstance(value, dict):
            if value.get("code") is True and "text" in value:
                inspect(value["text"], mono)
            for child in value.values():
                inline_code(child)
        elif isinstance(value, list):
            for child in value:
                inline_code(child)

    for event in events:
        kind, data = event["kind"], event["data"]
        if kind == "code":
            inspect(data["code"], mono)
        inline_code(data)
        for key in ("text", "label", "content", "caption", "description", "alt"):
            value = data.get(key, "")
            if isinstance(value, list):
                value = [r["text"] for r in value]
            inspect(value, available)
        if kind == "table":
            for row in [data["headers"], *data["rows"]]:
                for cell in row:
                    inspect(cell if isinstance(cell, str) else [r["text"] for r in cell], available)


def table_weights(block):
    if "column_weights" in block:
        weights = block["column_weights"]
    else:
        from .model import plain
        weights = [min(48, max(10, max(len(plain(row[i])) for row in [block["headers"], *block["rows"]]))) ** 0.5
                   for i in range(len(block["headers"]))]
    return [v / sum(weights) for v in weights]
