"""Small local harness. Traces/derivatives are private, never source fixtures."""

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SKILL = ROOT / "plugins/cufe-study-guide/skills/cufe-study-guide"
sys.path.insert(0, str(SKILL / "scripts"))


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fingerprint(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def codex_command():
    executable = shutil.which("codex.exe") or shutil.which("codex")
    if executable and Path(executable).suffix.lower() not in (".cmd", ".bat", ".ps1"):
        return [executable]
    # npm's Windows wrapper is not an executable accepted by CreateProcess.
    # Invoke its adjacent official JS launcher with argv, never a shell string.
    wrapper = shutil.which("codex.cmd") or shutil.which("codex.ps1")
    launcher = Path(wrapper).parent / "node_modules/@openai/codex/bin/codex.js" if wrapper else None
    node = shutil.which("node")
    if launcher and launcher.is_file() and node:
        return [node, str(launcher)]
    raise RuntimeError("Codex CLI not found. Install/authenticate the official CLI first.")


def selection_evidence(trace):
    """Observed read evidence, not an undocumented 'skill selected' magic string.

    Public JSONL command_execution events expose commands and their outputs. Count
    a successful read of this SKILL.md whose output contains its actual front matter.
    File listings, mentioning the name, and failed reads are not selection evidence.
    This is a conservative proxy: audit unknown traces when CLI/tool formats change.
    """
    return selection_events([json.loads(line) for line in Path(trace).read_text(encoding="utf-8").splitlines()])


def selection_events(events):
    evidence = []
    for event in events:
        item = event.get("item", {})
        if event.get("type") != "item.completed" or item.get("type") != "command_execution" or item.get("exit_code") != 0:
            continue
        command = item.get("command", "").replace("\\\\", "/").replace("\\", "/")
        output = item.get("aggregated_output", "")
        if "cufe-study-guide" in command and "SKILL.md" in command and re.search(r"(?m)^name:\s*cufe-study-guide\s*$", output):
            evidence.append({"item_id": item.get("id"), "signal": "successful SKILL.md read with matching front matter"})
    return evidence


def run_codex(prompt, folder, home=None, schema=None, writable=False, timeout=2400):
    folder = Path(folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    if home:
        env["CODEX_HOME"] = str(Path(home).resolve())
    env["PYTHONIOENCODING"] = "utf-8"
    args = [*codex_command(), "exec", "--json", "--skip-git-repo-check", "--ephemeral",
            "-C", str(folder), "-o", str(folder / "last-message.json" if schema else folder / "last-message.txt")]
    # Native Windows read-only + noninteractive approvals rejected PowerShell
    # reads in CLI 0.159.3. Keep automatic approval review in an isolated output
    # workspace; grading prompts prohibit content edits. No sandbox bypass.
    args += ["--approve-for-me"] if writable or os.name == "nt" else ["-s", "read-only"]
    if schema:
        args += ["--output-schema", str(Path(schema).resolve())]
    args += ["-"]
    (folder / "prompt.txt").write_text(prompt, encoding="utf-8")
    try:
        with (folder / "trace.jsonl").open("w", encoding="utf-8") as stdout, (folder / "stderr.txt").open("w", encoding="utf-8") as stderr:
            completed = subprocess.run(args, input=prompt, text=True, encoding="utf-8", env=env,
                                       stdout=stdout, stderr=stderr, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        write(folder / "execution.json", {"status":"timeout", "timeout_seconds":timeout})
        raise RuntimeError(f"Codex timed out; partial trace retained at {folder}") from exc
    # Do not report a disconnected/unfinished run as a passing model evaluation.
    events = [json.loads(line) for line in (folder / "trace.jsonl").read_text(encoding="utf-8").splitlines()]
    turns = [event for event in events if event.get("type") == "turn.completed"]
    result = {"exit_code": completed.returncode, "completed_turns":len(turns), "selection":selection_evidence(folder / "trace.jsonl"),
              "permission_mode":"reviewed workspace-write" if writable or os.name == "nt" else "read-only"}
    write(folder / "execution.json", result)
    if completed.returncode or not turns:
        raise RuntimeError(f"Codex execution incomplete; inspect {folder / 'stderr.txt'} and trace.jsonl")
    return result


def artifact_grade(model_path, docx_path, pdf_path, prior_supplied=False, render_pages=True):
    from study_guide_renderer.model import validate, walk_blocks
    from study_guide_renderer.theme import get_theme
    from study_guide_renderer.plan import compile_guide
    from study_guide_renderer.artifact_checks import check_docx, check_pdf, expected_links
    model_path = Path(model_path).resolve()
    model = validate(read(model_path), model_path.parent)
    theme = get_theme(model)
    events = compile_guide(model, theme)
    docx = check_docx(docx_path, events, theme)
    pdf = check_pdf(pdf_path, events, theme)
    for check in (docx, pdf):
        check.pop("text")
        if set(check["external_links"]) != expected_links(model):
            raise AssertionError("Artifact hyperlinks differ from the semantic model")
    blocks = list(walk_blocks(model))
    connections = [block for block in blocks if block.get("semantic") == "previous_lecture_connection"]
    if not prior_supplied and connections:
        raise AssertionError("Invented previous-lecture callout: no prior material supplied")
    from pypdf import PdfReader
    pages = [page.extract_text() or "" for page in PdfReader(pdf_path).pages]
    key_pages = [index for index, text in enumerate(pages) if "Answer Key" in text and not text.startswith("Contents")]
    # Contents may mention Answer Key; use the last actual section heading.
    if any(block["type"] == "quiz" for block in blocks):
        key_page = max(key_pages) if key_pages else -1
        last_question = next(block for block in blocks if block["type"] == "quiz")["questions"][-1]["id"]
        question_pages = [i for i, text in enumerate(pages[:key_page]) if re.search(r"(?m)^" + re.escape(last_question) + r"\s*$", text)]
        if not question_pages or key_page <= max(question_pages):
            raise AssertionError("Quiz/key page separation not confirmed")
    if render_pages:
        sys.path.insert(0, str(ROOT / "dev/rendering"))
        from check_rendering import inspect_pdf
        inspect_pdf(Path(pdf_path), images=True)  # every page and glyph bounds
    return {"schema":"passed", "docx":docx, "pdf":pdf,
            "previous_connections":len(connections), "block_types":sorted({b["type"] for b in blocks}),
            "semantic_types":sorted({b["semantic"] for b in blocks if "semantic" in b}),
            "cross_format_expected_content":"passed", "pdf_glyph_bounds":"passed" if render_pages else "not checked",
            "visual_review":"required; PNG generation is not visual inspection"}


DIMENSIONS = ["completeness", "clarity", "motivation", "terminology", "bridges", "mental_models", "examples",
              "practice", "filtering", "confusions", "quiz", "answers", "standalone", "concision", "fidelity"]
CRITICAL = {"completeness", "clarity", "terminology", "quiz", "answers", "standalone", "fidelity"}


def rubric_acceptance(report, profile):
    from jsonschema import Draft202012Validator
    Draft202012Validator(read(HERE / "graders/rubric.schema.json")).validate(report)
    dimensions = report["dimensions"]
    if len(dimensions) != len(DIMENSIONS) or {d["id"] for d in dimensions} != set(DIMENSIONS):
        raise AssertionError("Rubric must grade every dimension exactly once")
    if any(d["score"] is None for d in dimensions if d["id"] in CRITICAL):
        raise AssertionError("Critical dimensions cannot be N/A for a substantial lecture guide")
    ledger = report["coverage"]
    expected = {item["id"]:item for item in profile["concepts"]}
    if len(ledger) != len(expected) or {c["concept_id"] for c in ledger} != set(expected):
        raise AssertionError("Coverage ledger must account for every inventory item exactly once")
    essential_failures = [c["concept_id"] for c in ledger if expected[c["concept_id"]]["category"] == "ESSENTIAL"
                          and (c["status"] not in ("covered", "merged", "condensed") or not c["guide_location"])]
    applicable = [d["score"] for d in dimensions if d["score"] is not None]
    average = sum(applicable) / len(applicable)
    failures = [d["id"] for d in dimensions if d["id"] in CRITICAL and d["score"] < 4]
    decisions = {"filtering", "no_prior_fabrication", "breakpoints", "cheatsheet", "proofs", "quiz_correctness", "source_fidelity"}
    if len(report["decisions"]) != len(decisions) or {d["id"] for d in report["decisions"]} != decisions:
        raise AssertionError("Rubric must assess every learning/fidelity decision exactly once")
    decision_failures = [item["id"] for item in report["decisions"] if not item["acceptable"]]
    passed = not essential_failures and not failures and average >= 4.2 and not report["critical_issues"] and not decision_failures
    return {"passed":passed, "average":round(average, 3), "essential_missing":essential_failures,
            "critical_dimensions_below_4":failures,"decision_failures":decision_failures,"critical_issues":report["critical_issues"]}
