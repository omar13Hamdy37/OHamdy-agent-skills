#!/usr/bin/env python3
"""Validate, render, mechanically inspect, and atomically publish requested outputs."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import unicodedata
import uuid
import shutil
from contextlib import contextmanager


@contextmanager
def staging_directory(directory):
    # Inherit the output directory ACL; Python 3.13's private Windows tempfile ACL
    # can exclude the execution token in managed workspaces.
    stage = directory / (".guide-stage-" + uuid.uuid4().hex)
    stage.mkdir()
    try:
        yield stage
    finally:
        if stage.resolve().parent != directory.resolve() or stage.is_symlink():
            raise RuntimeError("Refusing cleanup outside the artifact staging directory")
        shutil.rmtree(stage)


def safe_stem(value):
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value)
    value = re.sub(r"\s+", "_", value).strip(" ._")[:120].rstrip(" ._") or "Study_Guide"
    if value.split(".")[0].upper() in {"CON", "PRN", "AUX", "NUL", *[f"COM{i}" for i in range(1, 10)], *[f"LPT{i}" for i in range(1, 10)]}:
        value = "Guide_" + value
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--output-path", type=Path, help="Exact destination for a single selected format")
    parser.add_argument("--filename", help="Shared filename stem; Windows-invalid characters are sanitized")
    parser.add_argument("--formats", default="docx,pdf")
    parser.add_argument("--theme", choices=("academic", "grayscale"))
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--report", type=Path, help="Optional mechanical validation JSON record")
    args = parser.parse_args(argv)
    try:
        from study_guide_renderer.model import SKILL_ROOT, GuideError, load_json, validate
        from study_guide_renderer.theme import check_glyphs, get_theme
        from study_guide_renderer.plan import compile_guide
        from study_guide_renderer.equations import EquationCache
        formats = list(dict.fromkeys(args.formats.split(",")))
        if not formats or any(f not in ("docx", "pdf") for f in formats):
            raise GuideError("--formats must be docx, pdf, or docx,pdf")
        source = args.input.expanduser().resolve()
        model = validate(load_json(source), source.parent)
        theme = get_theme(model, args.theme)
        events = compile_guide(model, theme)
        check_glyphs(events, model["metadata"])
        equations = EquationCache(theme["text"])
        for event in events:
            if event["kind"] == "equation":
                from study_guide_renderer.equations import fitted
                data = event["data"]
                for line in data.get("lines", [{"latex": data.get("latex")} ]):
                    fitted(equations.get(line["latex"]), theme["width"] - 55)
        if args.validate_only:
            print("Valid study guide 1.0; semantic relationships, images, glyphs, and equations checked.")
            return 0
        if args.output_path:
            if len(formats) != 1 or args.output_dir or args.filename:
                raise GuideError("--output-path requires one format and cannot be combined with --output-dir/--filename")
            target = args.output_path.expanduser().resolve()
            if target.suffix.lower() != "." + formats[0]:
                raise GuideError("--output-path extension must match the selected format")
            directory, destinations = target.parent, {formats[0]: target}
        else:
            directory = (args.output_dir.expanduser().resolve() if args.output_dir else source.parent / "study-guides")
            meta = model["metadata"]
            parts = [meta.get("course", "")]
            if "lecture_number" in meta:
                parts.append("Lecture_" + str(meta["lecture_number"]).zfill(2))
            parts.extend([meta.get("title_override", meta["title"]), "Study_Guide"])
            stem = safe_stem(args.filename or "_".join(p for p in parts if p))
            destinations = {fmt: directory / (stem + "." + fmt) for fmt in formats}
        if directory.is_relative_to(SKILL_ROOT.parents[1]):
            raise GuideError("Output must be outside the installed plugin; pass --output-dir for a user workspace")
        for target in destinations.values():
            if target == source:
                raise GuideError("Output must not overwrite the input model")
            if target.exists() and not args.overwrite:
                raise GuideError(f"Output exists: {target}; use --overwrite to replace this generated artifact")
        report = args.report.expanduser().resolve() if args.report else None
        if report:
            if report in destinations.values() or report == source or report.is_relative_to(SKILL_ROOT.parents[1]):
                raise GuideError("--report must be outside the installed plugin and distinct from input/artifacts")
            if report.exists() and not args.overwrite:
                raise GuideError("Report already exists; use --overwrite to replace it")
            report.parent.mkdir(parents=True, exist_ok=True)
        directory.mkdir(parents=True, exist_ok=True)
        result = {"schema_version": "1.0", "input_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "artifacts": {}}
        from study_guide_renderer.artifact_checks import check_docx, check_pdf, expected_links
        with staging_directory(directory) as stage:
            for fmt, target in destinations.items():
                staged = stage / target.name
                if fmt == "docx":
                    from study_guide_renderer.docx_renderer import WordRenderer
                    from study_guide_renderer.font_embedding import embed_fonts
                    WordRenderer(model, theme, equations, source.parent).render(events, staged)
                    embed_fonts(staged)
                    check = check_docx(staged, events, theme)
                else:
                    from study_guide_renderer.pdf_renderer import PDFRenderer
                    PDFRenderer(model, theme, equations, source.parent).render(events, staged)
                    check = check_pdf(staged, events, theme)
                if set(check["external_links"]) != expected_links(model):
                    raise GuideError(f"{fmt.upper()} hyperlinks differ from the guide model")
                check.pop("text")
                result["artifacts"][fmt] = {"path": str(target), **check}
            publish_paths = {target: stage / target.name for target in destinations.values()}
            if report:
                staged_report = stage / "validation-report.json"
                staged_report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
                publish_paths[report] = staged_report
            # Keep old artifacts until every requested format has rendered and passed checks.
            published, backups = [], {}
            try:
                for index, (target, staged_file) in enumerate(publish_paths.items()):
                    if target.exists():
                        backup = stage / (f"previous-{index}-" + target.name)
                        os.replace(target, backup)
                        backups[target] = backup
                    os.replace(staged_file, target)
                    published.append(target)
            except OSError:
                for target in published:
                    target.unlink(missing_ok=True)
                for target, backup in backups.items():
                    os.replace(backup, target)
                raise
        for fmt, check in result["artifacts"].items():
            pages = f" ({check['pages']} pages)" if "pages" in check else ""
            print(f"{fmt.upper()}: {check['path']}{pages}")
        print("Mechanical artifact checks passed; inspect rendered pages before delivery.")
        return 0
    except ImportError as exc:
        print(f"Missing renderer dependency: {exc}. Use the packaged run_renderer.py bootstrap.", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"Rendering failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
