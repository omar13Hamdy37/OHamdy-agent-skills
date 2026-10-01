"""Validate an explicitly authored visual-review receipt, never infer one."""


def validate_review(report, pdf_sha256, page_count):
    if report.get("pdf_sha256") != pdf_sha256:
        raise AssertionError("Visual receipt belongs to a different PDF; inspect the regenerated pages")
    pages = report.get("pages", [])
    if len(pages) != page_count or {page.get("number") for page in pages} != set(range(1, page_count + 1)):
        raise AssertionError("Visual review must account for every PDF page exactly once")
    if not report.get("reviewer") or any(page.get("inspected") is not True for page in pages):
        raise AssertionError("PNG creation alone is not evidence of visual inspection")
    required = {"crop_labels_axes", "contents_overflow", "quiz_spillover", "quiz_answer_separation",
                "clipping_collisions", "typography_tables_equations", "headers_footers", "grayscale_meaning"}
    checks = report.get("checks", {})
    if set(checks) != required or not all(value is True for value in checks.values()):
        raise AssertionError("A required visual regression check is missing or failed")
    if any(issue.get("severity") == "critical" for page in pages for issue in page.get("issues", [])):
        raise AssertionError("Critical visual defect remains unresolved")
    return True
