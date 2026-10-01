"""Meaningful public regression gates; no private lectures or model calls."""

import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval_support import (DIMENSIONS, HERE, ROOT, SKILL, read, rubric_acceptance,
                          selection_events)
from study_guide_renderer.model import GuideError, validate
from study_guide_renderer.artifact_checks import check_markup_namespaces
from lxml import etree
from jsonschema import Draft202012Validator
import yaml
from visual_review import validate_review


class PackageChecks(unittest.TestCase):
    def test_manifest_and_marketplace(self):
        manifest = read(SKILL.parents[1] / "plugin.json")
        market = read(ROOT / ".agents/plugins/marketplace.json")
        self.assertEqual(manifest["name"], "cufe-study-guide")
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(manifest["$schema"], "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
        self.assertNotIn("license", manifest)
        self.assertEqual(manifest["repository"], "https://github.com/omar13Hamdy37/OHamdy-agent-skills")
        self.assertEqual(market["name"], "ohamdy-agent-skills")
        for plugin in market["plugins"]:
            self.assertEqual(plugin["source"]["source"], "local")
            path = (ROOT / plugin["source"]["path"]).resolve()
            self.assertTrue(path.is_relative_to(ROOT))
            self.assertTrue((path / "plugin.json").is_file())
            self.assertEqual(plugin["policy"], {"installation":"AVAILABLE", "authentication":"ON_USE"})

    def test_front_matter_and_runtime_links(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        matter = yaml.safe_load(text.split("---", 2)[1])
        self.assertEqual(matter["name"], "cufe-study-guide")
        self.assertLess(len(matter["description"]), 1024)
        for path in SKILL.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"(?i)TODO.*Phase 2")
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("#"):
                    continue
                resolved = (path.parent / target.split("#")[0]).resolve()
                self.assertTrue(resolved.is_relative_to(SKILL), (path, target))
                self.assertTrue(resolved.exists(), (path, target))

    def test_all_public_json_and_schemas(self):
        files = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT, text=True).splitlines()
        for name in files:
            path = ROOT / name
            if path.suffix == ".json":
                model = read(path)
                if name.endswith(".schema.json"):
                    Draft202012Validator.check_schema(model)
        self.assertEqual(len(read(HERE / "cases/triggers.json")), 16)

    def test_private_inputs_are_excluded(self):
        files = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT, text=True).splitlines()
        for name in files:
            self.assertFalse(name.startswith(("output/", "outputs/")), name)
            self.assertNotIn(Path(name).name, {"local-fixtures.json", "auth.json", "trace.jsonl", "extracted.json"})
            self.assertNotIn(Path(name).suffix.lower(), {".pdf", ".docx"}, name)
            if Path(name).suffix in {".md", ".json", ".py", ".yml", ".yaml"}:
                content = (ROOT / name).read_text(encoding="utf-8")
                self.assertNotRegex(content, r"(?i)[A-Z]:[\\/]CUFE[\\/]", name)
        ignored = subprocess.run(["git", "check-ignore", "evals/cufe-study-guide/local-fixtures.json", "output/phase4/private.pdf"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(ignored.returncode, 0)
        self.assertEqual(len(ignored.stdout.splitlines()), 2)


def good_report():
    return {"dimensions":[{"id":name,"score":5,"evidence":"section evidence","rationale":"reason"} for name in DIMENSIONS],
            "coverage":[{"concept_id":"essential","guide_location":"section 1","status":"covered","treatment":"explanation and example"}],
            "decisions":[{"id":name,"acceptable":True,"rationale":"evidence"} for name in ["filtering","no_prior_fabrication","breakpoints","cheatsheet","proofs","quiz_correctness","source_fidelity"]],
            "critical_issues":[]}


class GraderRegressions(unittest.TestCase):
    profile = {"concepts":[{"id":"essential","category":"ESSENTIAL"}]}

    def test_word_compatibility_prefixes_must_remain_declared(self):
        mc = 'http://schemas.openxmlformats.org/markup-compatibility/2006'
        invalid = etree.fromstring(f'<settings xmlns:mc="{mc}" mc:Ignorable="w14"/>')
        with self.assertRaises(GuideError): check_markup_namespaces(invalid, "settings.xml")
        valid = etree.fromstring(f'<settings xmlns:mc="{mc}" xmlns:w14="urn:word14" mc:Ignorable="w14"/>')
        check_markup_namespaces(valid, "settings.xml")

    def test_visual_receipt_requires_all_pages_and_crop_quiz_checks(self):
        receipt = {"pdf_sha256":"hash", "reviewer":"reviewer", "pages":[{"number":1,"inspected":True,"issues":[]}],
                   "checks":{name:True for name in ["crop_labels_axes","contents_overflow","quiz_spillover","quiz_answer_separation","clipping_collisions","typography_tables_equations","headers_footers","grayscale_meaning"]}}
        self.assertTrue(validate_review(receipt, "hash", 1))
        with self.assertRaises(AssertionError): validate_review(receipt, "new-hash", 1)
        with self.assertRaises(AssertionError): validate_review(receipt, "hash", 2)
        for check in ("crop_labels_axes", "quiz_spillover"):
            broken = copy.deepcopy(receipt); broken["checks"][check] = False
            with self.assertRaises(AssertionError): validate_review(broken, "hash", 1)

    def test_complete_strong_report_passes(self):
        self.assertTrue(rubric_acceptance(good_report(), self.profile)["passed"])

    def test_essential_omission_blocks_even_high_average(self):
        for status in ("intentionally omitted", "missing"):
            report = good_report()
            report["coverage"][0]["status"] = status
            self.assertFalse(rubric_acceptance(report, self.profile)["passed"])

    def test_names_without_location_are_not_coverage(self):
        report = good_report(); report["coverage"][0]["guide_location"] = ""
        self.assertFalse(rubric_acceptance(report, self.profile)["passed"])

    def test_missing_duplicate_dimensions_rejected(self):
        for edit in (lambda r:r["dimensions"].pop(), lambda r:r["dimensions"][0].update(id="clarity")):
            report = good_report(); edit(report)
            with self.assertRaises(AssertionError): rubric_acceptance(report, self.profile)

    def test_missing_decision_rejected(self):
        report = good_report(); report["decisions"].pop()
        with self.assertRaises(AssertionError): rubric_acceptance(report, self.profile)

    def test_critical_low_score_and_fidelity_issue_block(self):
        report = good_report(); report["dimensions"][0]["score"] = 3
        self.assertFalse(rubric_acceptance(report, self.profile)["passed"])
        report = good_report(); report["critical_issues"] = ["Invented prior lecture"]
        self.assertFalse(rubric_acceptance(report, self.profile)["passed"])

    def test_unknown_coverage_rejected(self):
        report = good_report(); report["coverage"][0]["concept_id"] = "unknown"
        with self.assertRaises(AssertionError): rubric_acceptance(report, self.profile)

    def test_selection_requires_actual_successful_read(self):
        def event(command, output, code=0):
            return {"type":"item.completed","item":{"id":"i1","type":"command_execution","command":command,"aggregated_output":output,"exit_code":code}}
        for value in [event("rg --files cufe-study-guide/SKILL.md", "SKILL.md"), event("cat cufe-study-guide/SKILL.md", "name: cufe-study-guide\n", 1)]:
            self.assertEqual(selection_events([value]), [])
        self.assertEqual(len(selection_events([event("cat /installed/cufe-study-guide/SKILL.md", "---\nname: cufe-study-guide\n---\n")])), 1)

    def test_model_rejects_invalid_proof_and_key_relationships(self):
        model = read(ROOT / "dev/rendering/cufe-study-guide/smoke.json")
        for section in model["sections"]:
            section["blocks"] = [b for b in section["blocks"] if b["type"] != "image"]
        validate(model, ROOT)
        broken = copy.deepcopy(model)
        broken["end_matter"][-1]["answers"][0]["question_id"] = "no-such-question"
        with self.assertRaises(GuideError): validate(broken, ROOT)
        broken = copy.deepcopy(model)
        broken["sections"][0]["blocks"].append({"type":"proof","classification":"optional_insight","provenance":"course_material","blocks":[{"type":"paragraph","content":"wrong classification"}]})
        with self.assertRaises(GuideError): validate(broken, ROOT)


if __name__ == "__main__":
    unittest.main()
