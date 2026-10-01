"""Mechanical output checks; these do not certify visual or pedagogical quality."""

import posixpath
import re
import zipfile
from xml.etree import ElementTree as ET

from pypdf import PdfReader

from .model import GuideError, plain

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/package/2006/relationships"


def normalized(text):
    return re.sub(r"\s+", "", text.replace("\u200b", ""))


def expected_text(events):
    for event in events:
        data, kind = event["data"], event["kind"]
        if kind in ("heading", "label"):
            yield data["text"]
        elif kind in ("paragraph", "quote", "caption"):
            yield plain(data["content"])
            if data.get("attribution"):
                yield plain(data["attribution"])
        elif kind == "list":
            yield from (plain(item) for item in data["items"])
        elif kind == "table":
            for row in [data["headers"], *data["rows"]]:
                yield from (plain(cell) for cell in row)
        elif kind == "code":
            yield data["code"]
        elif kind == "equation":
            for line in data.get("lines", []):
                if line.get("explanation"):
                    yield plain(line["explanation"])
            yield data["description"]
            for symbol in data.get("symbols", []):
                yield symbol["symbol"] + ": " + symbol["meaning"]
        for key in ("caption", "source_reference", "explanation"):
            if kind not in ("quote", "caption") and isinstance(data.get(key), (str, list)):
                yield plain(data[key])


def check_content(text, events, label):
    text = normalized(text)
    for value in expected_text(events):
        if normalized(value) not in text:
            raise GuideError(f"{label} omitted or changed expected content: {value[:90]!r}")


def check_docx(path, events, theme):
    ns = {"w": W}
    with zipfile.ZipFile(path) as package:
        if package.testzip():
            raise GuideError("DOCX contains a corrupt ZIP member")
        names = set(package.namelist())
        for required in ("[Content_Types].xml", "word/document.xml", "word/styles.xml", "word/_rels/document.xml.rels"):
            if required not in names:
                raise GuideError(f"DOCX missing required part: {required}")
        links = set()
        for name in names:
            if name.endswith((".xml", ".rels")) or name == "[Content_Types].xml":
                root = ET.fromstring(package.read(name))
                if name.endswith(".rels"):
                    base = posixpath.dirname(posixpath.dirname(name))
                    for relationship in root:
                        target = relationship.attrib["Target"]
                        if relationship.attrib.get("TargetMode") == "External":
                            if relationship.attrib["Type"].endswith("/hyperlink"):
                                links.add(target)
                            continue
                        resolved = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join(base, target))
                        if resolved not in names:
                            raise GuideError(f"DOCX relationship missing its target: {name} -> {target}")
        document = ET.fromstring(package.read("word/document.xml"))
        text = "\n".join(node.text or "" for node in document.iter("{" + W + "}t"))
        check_content(text, events, "DOCX")
        styles = {p.attrib.get("{" + W + "}val") for p in document.findall(".//w:pStyle", ns)}
        if "Heading1" not in styles:
            raise GuideError("DOCX has no structural Heading1 paragraphs")
        for size in document.findall(".//w:pgSz", ns):
            dimensions = tuple(int(size.attrib["{" + W + "}" + key]) for key in ("w", "h"))
            if any(abs(v - pt * 20) > 2 for v, pt in zip(dimensions, theme["page"])):
                raise GuideError("DOCX paper geometry differs from requested page size")
        return {"valid_package": True, "heading_styles": sorted(s for s in styles if s),
                "images": len([n for n in names if n.startswith("word/media/")]),
                "embedded_fonts": len([n for n in names if n.endswith(".odttf")]),
                "external_links": sorted(links), "text": text}


def check_pdf(path, events, theme):
    reader = PdfReader(path, strict=True)
    if len(reader.pages) < 2:
        raise GuideError("PDF must contain a cover and content")
    texts, links, embedded = [], set(), set()
    for index, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        lines = text.splitlines()
        # The page callback writes the running header/footer before body content.
        # Remove that furniture when reconciling paragraphs that span pages.
        if index > 0 and len(lines) >= 2 and lines[1].strip() == str(index):
            texts.append("\n".join(lines[2:]))
        else:
            texts.append(text)
        if not text.strip():
            raise GuideError(f"PDF page {index + 1} has no extractable text")
        if any(abs(float(page.mediabox[i + 2]) - pt) > 1 for i, pt in enumerate(theme["page"])):
            raise GuideError("PDF paper geometry differs from requested page size")
        for annotation in page.get("/Annots", []):
            action = annotation.get_object().get("/A", {})
            if action.get("/URI"):
                links.add(str(action["/URI"]))
        for name, font_ref in page["/Resources"].get("/Font", {}).items():
            font = font_ref.get_object()
            descriptor = font.get("/FontDescriptor")
            if descriptor and any(key in descriptor.get_object() for key in ("/FontFile", "/FontFile2", "/FontFile3")):
                embedded.add(str(font.get("/BaseFont", name)))
    text = "\n".join(texts)
    check_content(text, events, "PDF")
    if not embedded or not reader.outline:
        raise GuideError("PDF lacks embedded content fonts or heading outlines")
    return {"parses": True, "pages": len(reader.pages), "embedded_fonts": sorted(embedded),
            "external_links": sorted(links), "outlines": bool(reader.outline), "text": text}


def expected_links(model):
    links = set()
    def descend(value):
        if isinstance(value, dict):
            if "href" in value and not value["href"].startswith("#"):
                links.add(value["href"])
            for child in value.values():
                descend(child)
        elif isinstance(value, list):
            for child in value:
                descend(child)
    descend(model)
    return links
