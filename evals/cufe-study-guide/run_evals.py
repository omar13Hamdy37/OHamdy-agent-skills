"""Public deterministic checks or explicitly requested local Codex-assisted evals."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys

from eval_support import (HERE, ROOT, SKILL, artifact_grade, fingerprint, read,
                          rubric_acceptance, run_codex, write)
from jsonschema import ValidationError


def deterministic(output):
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(HERE / "graders"), "-p", "test_*.py", "-v"], check=True, cwd=ROOT)
    subprocess.run([sys.executable, str(ROOT / "dev/rendering/check_rendering.py"), "--output-dir", str(output / "rendering")], check=True, cwd=ROOT)
    return {"public_tests":"passed", "rendering":"passed"}


def triggers(args):
    cases = read(HERE / "cases/triggers.json")
    if args.case:
        cases = [c for c in cases if c["id"] in args.case]
        if not cases:
            raise ValueError("No matching trigger cases")
    def run(case):
        folder = args.output / "triggers" / case["id"]
        result = run_codex(case["prompt"], folder, args.codex_home, timeout=args.timeout)
        selected = bool(result["selection"])
        report = {"id":case["id"], "expected":case["expected"], "selected":selected,
                  "passed":selected == case["expected"], "evidence":result["selection"]}
        write(folder / "result.json", report)
        print(f"Trigger {case['id']}: {'PASS' if report['passed'] else 'FAIL'}", flush=True)
        return report
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(run, cases))
    write(args.output / "trigger-results.json", results)
    if not all(result["passed"] for result in results):
        raise AssertionError("Trigger mismatch: inspect traces before changing the description")
    return {"passed":len(results), "positive":sum(c["expected"] for c in cases), "negative":sum(not c["expected"] for c in cases)}


def synthetic(args):
    cases = read(HERE / "fixtures/behavior-cases.json")
    if args.case:
        cases = [case for case in cases if case["id"] in args.case]
        if not cases:
            raise ValueError("No matching synthetic cases")
    results = []
    for case in cases:
        folder = args.output / "synthetic" / case["id"]
        prompt = case["request"] + "\nCurrent lecture:\n" + case["lecture"]
        if case.get("prior"):
            prompt += "\nSupplied previous lecture:\n" + case["prior"]
        generation = folder / "generation"
        if args.reuse_generation:
            if (generation / "prompt.txt").read_text(encoding="utf-8") != prompt:
                raise ValueError("Existing synthetic prompt differs; regenerate instead of reusing stale content")
            execution = read(generation / "execution.json")
        else:
            execution = run_codex(prompt, generation, args.codex_home, timeout=args.timeout)
        if not execution["selection"]:
            raise AssertionError("Synthetic case lacks actual skill-use evidence; inspect its trace")
        grade_prompt = ("Review this generated study-guide content plan independently. Read " + str(folder / "generation/last-message.txt")
                        + ". Use ONLY the following original source/request and checks, not hypothetical requirements.\n"
                        + json.dumps(case, ensure_ascii=False)
                        + f"\nReturn a pass/fail for every listed check with evidence. Use one-based indices 1 through {len(case['checks'])}, exactly once in listed order. Do not invoke the skill or edit files.")
        run_codex(grade_prompt, folder / "grading", args.codex_home, HERE / "graders/behavior.schema.json", timeout=args.timeout)
        report = read(folder / "grading/last-message.json")
        from jsonschema import Draft202012Validator
        Draft202012Validator(read(HERE / "graders/behavior.schema.json")).validate(report)
        if len(report["checks"]) != len(case["checks"]) or {c["index"] for c in report["checks"]} != set(range(1, len(case["checks"]) + 1)):
            raise AssertionError("Synthetic grader omitted or duplicated a requested check")
        passed = all(check["passed"] for check in report["checks"])
        results.append({"id":case["id"],"passed":passed,"checks":report["checks"]})
        print(f"Synthetic {case['id']}: {'PASS' if passed else 'FAIL'}", flush=True)
    write(args.output / "synthetic-results.json", results)
    if not all(result["passed"] for result in results):
        raise AssertionError("Synthetic behavior regression failed; inspect source and grader rationale")
    return {"passed":len(results)}


def grade_real(args, fixture, folder):
    profile_path = (HERE / fixture["profile"]).resolve()
    profile = read(profile_path)
    source = Path(fixture["source"]).expanduser().resolve()
    if not source.is_file() or fingerprint(source) != profile["sha256"]:
        raise ValueError("Private source missing or fingerprint differs; review inventory before updating it")
    models = sorted(folder.glob("guide.json"))
    if len(models) != 1:
        raise ValueError("Expected guide.json in run directory")
    formats = {fmt:list(folder.glob(f"*.{fmt}")) for fmt in ("docx", "pdf")}
    if any(len(files) != 1 for files in formats.values()):
        raise ValueError("Expected exactly one DOCX and PDF in run directory; previews belong in a subdirectory")
    artifacts = artifact_grade(models[0], formats["docx"][0], formats["pdf"][0], bool(fixture.get("previous_sources")))
    if args.review_file:
        sys.path.insert(0, str(HERE / "graders"))
        from visual_review import validate_review
        validate_review(read(args.review_file), fingerprint(formats["pdf"][0]), artifacts["pdf"]["pages"])
        artifacts["visual_review"] = "explicit complete receipt passed"
    write(folder / "deterministic-results.json", artifacts)
    prompt = f"""Grade an actual generated study guide independently against the supplied source and high-level inventory.
Do not invoke the study-guide skill or edit content. Read the private source {source}, profile {profile_path}, semantic JSON {models[0]} and generated PDF {formats['pdf'][0]}. Use accessible run intermediates for visual/text evidence; inspect important source diagrams, not just extracted headings. The inventory is a grading aid, not a verbatim answer template. A concept counts as covered only when actually taught. Resolve source mistakes technically while preserving course scope. Grade all 15 dimensions in rubric.md at {HERE / 'graders/rubric.md'} on 1–5, or null with a concrete N/A reason. Ground each score in guide locations and evidence. Account for every inventory concept once. Intentionally omitted essential content is a failure. Don't penalize lack of advanced proofs/code absent from the source. Evaluate admin filtering, absence of fabricated prior lectures, optional enrichment/fidelity, breakpoint boundaries, cheatsheet decision, proof selection, and quiz correctness as decisions. Include critical issues only when supported by actual evidence. Return the schema; do not inflate scores or invent coverage to meet a target. Unknown/unreadable evidence must be reported rather than assumed correct."""
    before = {path:fingerprint(path) for path in [source, models[0], *formats["docx"], *formats["pdf"]]}
    run_codex(prompt, folder / "grading", args.codex_home, HERE / "graders/rubric.schema.json", timeout=args.timeout)
    if any(fingerprint(path) != digest for path, digest in before.items()):
        raise AssertionError("Grader changed an input artifact; discard its result")
    report = read(folder / "grading/last-message.json")
    acceptance = rubric_acceptance(report, profile)
    write(folder / "rubric-results.json", report)
    write(folder / "acceptance.json", acceptance)
    print(json.dumps(acceptance, indent=2))
    if not acceptance["passed"]:
        raise AssertionError("Real lecture did not meet rubric gates; inspect rationale and repair the correct reusable layer")
    return acceptance


def real(args):
    config = read(args.local_fixtures)
    fixture = config["cases"][args.real]
    folder = args.existing.resolve() if args.existing else args.output / "real" / args.real
    if not folder.is_relative_to(ROOT / "output"):
        raise ValueError("Private runs and grades must stay in the ignored output directory")
    if not args.existing:
        source = Path(fixture["source"]).expanduser().resolve()
        prior = fixture.get("previous_sources", [])
        profile = read(HERE / fixture["profile"])
        if not source.is_file() or fingerprint(source) != profile["sha256"]:
            raise ValueError("Private fixture unavailable or changed")
        prompt = f"""Use $cufe-study-guide to create a complete study guide from {fixture['course']} — Lecture {fixture['lecture_number']}: {fixture['title']}.
Source: {source}. Previous supplied material: {json.dumps(prior)}.
Teach in the default skill style. Omit course/admin filler intelligently; preserve all important concepts. Explain unfamiliar terminology, add examples/bridges, appropriate checkpoints and conceptual study breaks, and a small meaningful mixed quiz with a separate reasoned Answer Key. Decide cheatsheet/proof usefulness from the actual lecture. Generate both DOCX and PDF plus guide.json in {folder.resolve()}. Preserve a local coverage ledger. Use the installed skill and inspect important source diagrams. Keep all intermediates in this ignored output directory. Do not modify skill instructions, repository sources, or global environments. Available development Python: {sys.executable}."""
        result = run_codex(prompt, folder, args.codex_home, writable=True, timeout=args.timeout)
        if not result["selection"]:
            raise AssertionError("Cannot verify actual skill use; inspect execution trace")
    else:
        from eval_support import selection_evidence
        if not selection_evidence(folder / "trace.jsonl"):
            raise AssertionError("Existing guide lacks skill-use evidence")
    return grade_real(args, fixture, folder)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deterministic", action="store_true", help="Public local checks, no model/private source")
    parser.add_argument("--triggers", action="store_true", help="16 selection prompts: Codex calls")
    parser.add_argument("--synthetic", action="store_true", help="Original behavior cases + structured independent Codex grading")
    parser.add_argument("--reuse-generation", action="store_true", help="Regrade matching synthetic prompts without regenerating unchanged content")
    parser.add_argument("--real", metavar="CASE", help="Private source -> actual skill -> artifacts -> rubric")
    parser.add_argument("--all", action="store_true", help="All suites plus every configured private case (model costs)")
    parser.add_argument("--existing", type=Path, help="Grade an existing real run; no regeneration")
    parser.add_argument("--review-file", type=Path, help="Explicit per-page visual receipt for the exact real PDF")
    parser.add_argument("--local-fixtures", type=Path, default=HERE / "local-fixtures.json")
    parser.add_argument("--codex-home", type=Path, help="Optional isolated, pre-authenticated profile with plugin installed")
    parser.add_argument("--output", type=Path, default=ROOT / "output/phase4/evals")
    parser.add_argument("--case", action="append", help="Select trigger/synthetic IDs; repeatable")
    parser.add_argument("--jobs", type=int, choices=(1,2), default=1, help="At most two independent trigger calls")
    parser.add_argument("--timeout", type=int, default=2400, help="Per Codex call; timeout is an incomplete eval")
    args = parser.parse_args()
    args.output = args.output.resolve()
    if not any((args.deterministic,args.triggers,args.synthetic,args.real,args.all)):
        parser.error("Choose a suite; --deterministic is fully local")
    if not args.output.is_relative_to(ROOT / "output"):
        parser.error("Eval outputs must stay in the repository's ignored output directory")
    if args.existing and not args.real:
        parser.error("--existing requires --real")
    summary = {}
    try:
        if args.deterministic or args.all: summary["deterministic"] = deterministic(args.output)
        if args.triggers or args.all: summary["triggers"] = triggers(args)
        if args.synthetic or args.all: summary["synthetic"] = synthetic(args)
        if args.real: summary[args.real] = real(args)
        elif args.all:
            for case in read(args.local_fixtures)["cases"]:
                args.real = case
                summary[case] = real(args)
        write(args.output / "suite-results.json", summary)
        print("Requested evals passed. Visual review and remote installation checks remain separate release gates.")
        return 0
    except (ValueError, OSError, KeyError, ValidationError, AssertionError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Eval failed: {exc}", file=sys.stderr)
        write(args.output / "suite-results.json", {"completed":summary,"error":str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
