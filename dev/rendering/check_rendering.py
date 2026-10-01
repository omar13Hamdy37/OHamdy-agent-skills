"""Renderer mechanics only: no pedagogical fixtures, model graders, or release flow."""

import argparse
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pypdfium2 as pdfium
from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "plugins/cufe-study-guide/skills/cufe-study-guide"
FIXTURE = Path(__file__).parent / "cufe-study-guide"


def command(script, model, output, name, *extra, success=True):
    result = subprocess.run([sys.executable, str(script), "--input", str(model), "--output-dir", str(output),
                             "--filename", name, "--overwrite", *extra], capture_output=True, text=True, encoding="utf-8", cwd=output.parent)
    assert (result.returncode == 0) == success, result.stdout + result.stderr
    return result.stdout + result.stderr


def write_model(folder, name, model):
    path = folder / (name + ".json")
    path.write_text(json.dumps(model, indent=2) + "\n", encoding="utf-8")
    return path


def inspect_pdf(path, images=False):
    document = pdfium.PdfDocument(path)
    all_pages = []
    for index, page in enumerate(document):
        text = page.get_textpage()
        width, height = page.get_size()
        for char in range(text.count_chars()):
            box = text.get_charbox(char)
            if box[2] - box[0] > 0.1 and box[3] - box[1] > 0.1:
                assert box[0] >= 25 and box[2] <= width - 25, (path.name, index + 1, box)
                assert box[1] >= 20 and box[3] <= height - 20, (path.name, index + 1, box)
        all_pages.append(text.get_text_range())
        if images:
            folder = path.parent / (path.stem + "-pages")
            folder.mkdir(exist_ok=True)
            bitmap = page.render(scale=1.6)
            bitmap.to_pil().save(folder / f"page-{index + 1:02}.png")
            bitmap.close()
        text.close()
        page.close()
    document.close()
    return all_pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "output/phase3/mechanics")
    args = parser.parse_args()
    folder = args.output_dir.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    script = SKILL / "scripts/render_study_guide.py"
    model = json.loads((FIXTURE / "smoke.json").read_text(encoding="utf-8"))
    for section in model["sections"]:
        for block in section["blocks"]:
            if block["type"] == "image":
                block["path"] = str(FIXTURE / block["path"])
    fixture = write_model(folder, "smoke", model)
    expected_semantics = set(json.loads((SKILL / "assets/themes/academic.json").read_text(encoding="utf-8"))["semantics"])
    found_semantics = set()
    def collect(value):
        if isinstance(value, dict):
            semantic = value.get("semantic", value.get("type"))
            if semantic in expected_semantics:
                found_semantics.add(semantic)
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)
    collect(model)
    assert found_semantics == expected_semantics, expected_semantics - found_semantics
    summary = {}
    command(script, fixture, folder, "smoke")
    pages = inspect_pdf(folder / "smoke.pdf", images=True)
    assert len(pages) == 6
    assert "Equations code tables and diagrams" not in pages[1]  # repaired orphan heading
    assert "Answer Key" not in pages[-2]
    assert "Answer Key" in pages[-1]
    summary["smoke"] = {"pdf_pages": len(pages), "semantic_types": len(found_semantics), "glyph_bounds": "passed"}

    robust = copy.deepcopy(model)
    robust["sections"][0]["title"] = "A long heading that wraps naturally while staying with the first explanation " * 3
    robust["theme"]["toc"] = "always"
    extra = [
        {"type": "code", "language": "Python", "code": 'result = "' + "long_identifier_" * 30 + '"\nprint(result)'},
        {"type": "table", "headers": [f"Column {i}" for i in range(8)], "rows": [[f"Wrapped detail {i} with a meaningful condition" for i in range(8)] for _ in range(3)]},
        {"type": "equation", "latex": r'A = \sum_{i=1}^{n} x_i^2 + \frac{a+b+c+d}{e+f+g+h} + \sqrt{u^2+v^2} + \alpha + \beta + \gamma + \delta', "description": "Large equation retains its complete expression at a readable scale."},
        {"type": "paragraph", "content": [{"text": "https://example.com/" + "layout-segment/" * 30, "href": "https://example.com/" + "layout-segment/" * 30}]},
        {"type": "proof", "classification": "lecture_proof", "title": "Multi page reasoning group", "blocks": [
            {"type": "paragraph", "content": f"Step {i}. " + "This mechanical paragraph checks continuing proof layout and readable pagination without imposing a single giant unbreakable group. " * 4}
            for i in range(1, 21)]},
        {"type": "heading", "id": "near-end", "level": 2, "text": "Heading after a long reasoning group"},
        {"type": "paragraph", "content": "The heading must remain with this short explanatory paragraph."}]
    robust["sections"][1]["blocks"] += extra
    robust_path = write_model(folder, "robust", robust)
    command(script, robust_path, folder, "robust")
    robust_pages = inspect_pdf(folder / "robust.pdf", images=True)
    assert sum("Step " in page for page in robust_pages) > 1
    summary["robust"] = {"pdf_pages": len(robust_pages), "cases": ["long heading", "long code line", "wide table", "large equation", "multi-page proof", "long URL", "near-end heading", "explicit linked contents", "wide source image"], "glyph_bounds": "passed"}

    minimal = {"schema_version": "1.0", "metadata": {"title": "Minimal metadata" ,"subject_category":"unknown-subject"}, "theme":{"name":"grayscale","paper_size":"Letter"}, "sections": [{"id": "minimal", "title": "A useful fallback", "blocks": [{"type": "paragraph", "content": "No optional metadata is required."}]}]}
    minimal_path = write_model(folder, "minimal", minimal)
    command(script, minimal_path, folder, "minimal")
    inspect_pdf(folder / "minimal.pdf", images=True)
    summary["minimal"] = "missing optional metadata, unknown subject, grayscale, Letter passed"

    # Real-guide failure generalized: a moderate linked contents list must not
    # strand its last entry on an otherwise empty page. No university content.
    navigation_model = copy.deepcopy(minimal)
    navigation_model["theme"] = {"name":"academic", "paper_size":"A4", "toc":"always"}
    navigation_model["sections"] = [{"id":f"topic-{i}", "title":f"Topic {i:02}: A clear conceptual unit with useful explanatory context",
                                     "blocks":[{"type":"paragraph","content":f"Original mechanical explanation for unit {i}."}]}
                                    for i in range(1, 31)]
    navigation_path = write_model(folder, "navigation", navigation_model)
    command(script, navigation_path, folder, "navigation")
    navigation_pages = inspect_pdf(folder / "navigation.pdf", images=True)
    assert "Contents" in navigation_pages[1] and "Topic 30:" in navigation_pages[1]
    assert "Original mechanical explanation" in navigation_pages[2]
    summary["contents_density"] = "30 linked entries fit a readable contents page; body starts next page"

    # A tall image checks aspect preservation independently of the wide smoke diagram.
    tall_path = folder / "tall.png"
    image = Image.new("RGB", (120, 600), "white")
    ImageDraw.Draw(image).rectangle((10, 10, 110, 590), outline="black", width=3)
    image.save(tall_path)
    tall = copy.deepcopy(minimal)
    tall["sections"][0]["blocks"].append({"type":"image","path":str(tall_path),"alt":"A tall outlined rectangle.","caption":"An unusual aspect ratio is preserved."})
    tall_model = write_model(folder, "tall", tall)
    command(script, tall_model, folder, "tall")
    inspect_pdf(folder / "tall.pdf", images=True)
    summary["tall_image"] = "passed"

    for name, mutation in {
        "unknown_block": lambda m: m["sections"][0]["blocks"].append({"type":"mystery"}),
        "unknown_semantic": lambda m: m["sections"][0]["blocks"].append({"type":"callout","semantic":"mystery","blocks":[{"type":"paragraph","content":"x"}]}),
        "bad_version": lambda m: m.update(schema_version="2.0"),
        "missing_image": lambda m: m["sections"][0]["blocks"].append({"type":"image","path":"missing.png","alt":"missing"}),
        "bad_equation": lambda m: m["sections"][0]["blocks"].append({"type":"equation","latex":r'\unsupported{x}',"description":"Unsupported notation"}),
        "broken_answers": lambda m: m["end_matter"][-1]["answers"].pop(),
        "duplicate_id": lambda m: m["sections"][1].update(id=m["sections"][0]["id"]),
        "bad_link": lambda m: m["sections"][0]["blocks"].append({"type":"paragraph","content":[{"text":"unsafe link","href":"javascript:alert(1)"}]})
    }.items():
        invalid = copy.deepcopy(model)
        mutation(invalid)
        invalid_path = write_model(folder, name, invalid)
        diagnostics = command(script, invalid_path, folder, name, success=False)
        assert "Rendering failed:" in diagnostics
        assert not (folder / (name + ".docx")).exists() and not (folder / (name + ".pdf")).exists()
    malformed = folder / "malformed.json"
    malformed.write_text('{broken',encoding='utf-8')
    command(script, malformed, folder, "malformed", success=False)
    summary["input_failures"] = "9 failures diagnosed before output publication"

    occupied = folder / "blocked-output"
    occupied.write_text('a file occupies the requested directory',encoding='utf-8')
    command(script, minimal_path, occupied, "blocked", success=False)
    summary["output_failure"] = "occupied output path rejected"
    command(script, fixture, folder, "repeat")
    for fmt in ("docx","pdf"):
        assert (folder / ("smoke."+fmt)).read_bytes() == (folder / ("repeat."+fmt)).read_bytes(), fmt
    summary["determinism"] = "both outputs byte-identical on repeat"

    relocated = folder / "installed plugin with spaces"
    shutil.copytree(SKILL.parent.parent, relocated, ignore=shutil.ignore_patterns("__pycache__"), dirs_exist_ok=True)
    relocated_script = relocated / "skills/cufe-study-guide/scripts/render_study_guide.py"
    command(relocated_script, fixture, folder, "relocated")
    summary["relocation"] = "copied installed package rendered from unrelated working directory"
    (folder / "results.json").write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__ == "__main__":
    main()
