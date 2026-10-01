"""Direct PDF layout with embedded fonts, links, outlines, and vector equations."""

from html import escape

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, Image, KeepTogether,
                               LongTable, PageBreak, PageTemplate, Paragraph,
                               Preformatted, Spacer, TableStyle)

from .cover_art import vector
from .equations import draw_path, fitted
from .model import image_path, plain, runs
from .plan import navigation
from .theme import font_files, table_weights


def rich(value, link_color="#235B78"):
    parts = []
    for item in runs(value):
        text = escape(item["text"]).replace("\n", "<br/>")
        if item.get("code"):
            text = '<font name="SGMono">' + text + "</font>"
        if item.get("bold"):
            text = "<b>" + text + "</b>"
        if item.get("italic"):
            text = "<i>" + text + "</i>"
        if item.get("href"):
            text = '<a href="' + escape(item["href"], quote=True) + '" color="' + link_color + '"><u>' + text + "</u></a>"
        parts.append(text)
    return "".join(parts)


class Equation(Flowable):
    def __init__(self, equation, width, color, number=None):
        super().__init__()
        self.equation, self.color, self.number = equation, color, number
        self.math_width, self.math_height, self.scale = fitted(equation, width - 55)
        self.width, self.height = width, self.math_height + 12
        self.keepWithNext = True

    def draw(self):
        self.canv.saveState()
        self.canv.translate(0, 6)
        self.canv.scale(self.scale, self.scale)
        self.canv.setFillColor(colors.HexColor(self.color))
        draw_path(self.canv, self.equation["path"])
        self.canv.restoreState()
        if self.number:
            self.canv.setFont("SGBody", 10)
            self.canv.setFillColor(colors.HexColor(self.color))
            self.canv.drawRightString(self.width, 6, "(" + self.number + ")")


class PrintCode(Preformatted):
    def wrap(self, width, height):
        self.frame_width = width
        _, inner = super().wrap(width - 12, height)
        self.inner_height = inner
        self.height = inner + 12
        return width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(self.style.backColor)
        self.canv.rect(0, 0, self.frame_width, self.height, fill=1, stroke=0)
        self.canv.translate(6, 6)
        height = self.height
        self.height = self.inner_height
        super().draw()
        self.height = height
        self.canv.restoreState()

    def split(self, width, height):
        if height < self.style.leading + 12:
            return []
        count = int((height - 12) / self.style.leading)
        if count >= len(self.lines):
            return [self]
        return [PrintCode("\n".join(self.lines[:count]), self.style),
                PrintCode("\n".join(self.lines[count:]), self.style)]


class GuidePDF(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, "guide_heading"):
            data = flowable.guide_heading
            self.canv.bookmarkPage(data["id"])
            # PDF outlines cannot skip levels; reduce jumps while retaining hierarchy.
            level = min(data["level"] - 1, getattr(self, "outline_level", -1) + 1)
            self.canv.addOutlineEntry(data["text"], data["id"], level=level, closed=False)
            self.outline_level = level


class Cover(Flowable):
    def __init__(self, model, theme):
        super().__init__()
        self.model, self.theme = model, theme
        self.width = theme["width"]
        self.height = theme["page"][1] - 2 * theme["margin"] - 4

    def draw(self):
        meta, width, y = self.model["metadata"], self.width, self.height - 45
        values = []
        if meta.get("course"):
            values.append((meta["course"], 13, "SGBody", 20))
        if "lecture_number" in meta:
            values.append((f"Lecture {meta['lecture_number']}", 12, "SGBody", 18))
        title = meta.get("title_override", meta["title"])
        values.append((title, 29 if len(title) <= 110 else 24, "SGBold", 22))
        if meta.get("subtitle"):
            values.append((meta["subtitle"], 13, "SGBody", 16))
        for text, size, font, spacing in values:
            p = Paragraph(escape(text), ParagraphStyle("cover", fontName=font, fontSize=size, leading=size * 1.25, textColor=colors.black))
            _, height = p.wrap(width, self.height)
            y -= height
            p.drawOn(self.canv, 0, y)
            y -= spacing
        art_width = width * 0.85
        art_height = art_width * 205 / 390
        vector(self.canv, meta.get("subject_category", "general"), 0, y - art_height - 30,
               art_width, colors.HexColor(self.theme["link"]))
        y -= art_height + 50
        for field in meta.get("cover_fields", []):
            p = Paragraph(escape(f"{field['label']}: {field['value']}"), ParagraphStyle("cover-meta", fontName="SGBody", fontSize=11, leading=16))
            _, height = p.wrap(width, self.height)
            y -= height
            p.drawOn(self.canv, 0, y)
        if y < 0:
            from .model import GuideError
            raise GuideError("Cover metadata is too long; shorten title/subtitle or requested cover fields")


class PDFRenderer:
    def __init__(self, model, theme, equations, base):
        self.model, self.theme, self.equations, self.base = model, theme, equations, base
        names = {"body": "SGBody", "bold": "SGBold", "italic": "SGItalic", "bold_italic": "SGBoldItalic", "mono": "SGMono", "mono_bold": "SGMonoBold"}
        for key, path in font_files().items():
            if names[key] not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont(names[key], str(path)))
        pdfmetrics.registerFontFamily("SGBody", normal="SGBody", bold="SGBold", italic="SGItalic", boldItalic="SGBoldItalic")
        pdfmetrics.registerFontFamily("SGMono", normal="SGMono", bold="SGMonoBold", italic="SGMono", boldItalic="SGMonoBold")
        self.styles = {}
        for semantic in [None, *theme["semantics"]]:
            indent = 12 if semantic and semantic not in ("quiz", "answer_key", "cheatsheet") else 0
            self.styles[semantic] = ParagraphStyle(str(semantic), fontName="SGBody", fontSize=theme["body_size"], leading=theme["leading"],
                                                  textColor=colors.HexColor(theme["text"]), spaceAfter=7, leftIndent=indent, allowWidows=0, allowOrphans=0, splitLongWords=1)

    def paragraph(self, value, semantic=None, **options):
        style = ParagraphStyle("block", parent=self.styles[semantic], **options)
        return Paragraph(rich(value, self.theme["link"]), style)

    def event(self, event):
        kind, data, semantic = event["kind"], event["data"], event["semantic"]
        if kind == "heading":
            size = (21, 16, 13, 12, 11, 11)[data["level"] - 1]
            p = self.paragraph(data["text"], fontName="SGBold", fontSize=size, leading=size * 1.25, textColor=colors.black,
                               spaceBefore=18 if data["level"] == 1 else 12, spaceAfter=8, keepWithNext=True)
            p.guide_heading = data
            return [p]
        if kind == "anchor":
            return [Paragraph('<a name="' + escape(data["id"]) + '"/>', self.styles[None])]
        if kind == "label":
            markup = escape(data["text"])
            if data.get("id"):
                markup = '<a name="' + escape(data["id"]) + '"/>' + markup
            config = self.theme["semantics"].get(semantic, {})
            style = ParagraphStyle("label", parent=self.styles[semantic], fontName="SGBold", leading=15, spaceBefore=8, spaceAfter=6,
                                   keepWithNext=True, textColor=colors.HexColor(config.get("accent", self.theme["text"])),
                                   backColor=colors.HexColor(config["background"]) if config else None, borderPadding=5)
            return [Paragraph(markup, style)]
        if kind in ("paragraph", "caption", "quote"):
            options = {"fontSize": 9, "leading": 13, "textColor": colors.HexColor(self.theme["muted"])} if kind == "caption" else {}
            if kind == "quote":
                options.update(fontName="SGItalic", leftIndent=18)
            result = [self.paragraph(data["content"], semantic, **options)]
            if data.get("attribution"):
                result.append(self.paragraph(data["attribution"], fontSize=9, leading=13))
            return result
        if kind == "list":
            result = []
            for index, item in enumerate(data["items"], 1):
                marker = f"{chr(64 + index)}." if data.get("letters") else f"{index}." if data.get("ordered") else "\u2022"
                p = self.paragraph(item, semantic, leftIndent=18, bulletIndent=2, spaceAfter=4)
                p.bulletText = marker
                result.append(p)
            return result
        if kind == "code":
            style = ParagraphStyle("code", fontName="SGMono", fontSize=self.theme["code_size"], leading=12, spaceAfter=8,
                                   backColor=colors.HexColor(self.theme["code_background"]), borderPadding=6)
            width = self.theme["width"] - 12
            chars = max(20, int(width / pdfmetrics.stringWidth("M", "SGMono", self.theme["code_size"])))
            result = [self.paragraph(data["language"], fontSize=9, leading=13, keepWithNext=True)] if data.get("language") else []
            result.append(PrintCode(data["code"].expandtabs(4), style, maxLineLength=chars, splitChars=" /", newLineChars=""))
            if data.get("caption"):
                result.append(self.paragraph(data["caption"], fontSize=9, leading=13))
            return result
        if kind == "equation":
            result = []
            lines = data.get("lines", [{"latex": data.get("latex")}])
            for index, line in enumerate(lines):
                result.append(Equation(self.equations.get(line["latex"]), self.theme["width"], self.theme["text"], data.get("number") if index == len(lines) - 1 else None))
                if line.get("explanation"):
                    result.append(self.paragraph(line["explanation"], semantic))
            result.append(self.paragraph(data["description"], semantic))
            for symbol in data.get("symbols", []):
                result.append(self.paragraph(symbol["symbol"] + ": " + symbol["meaning"], semantic))
            return result
        if kind == "table":
            rows = [[self.paragraph(cell, fontSize=self.theme["table_size"], leading=13, spaceAfter=0,
                                    fontName="SGBold" if index == 0 else "SGBody") for cell in row]
                    for index, row in enumerate([data["headers"], *data["rows"]])]
            table = LongTable(rows, colWidths=[self.theme["width"] * weight for weight in table_weights(data)],
                              repeatRows=1, splitByRow=1, splitInRow=1, hAlign="LEFT")
            table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(self.theme["table_header"])),
                                       ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F8F8")]),
                                       ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor(self.theme["border"])),
                                       ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                       ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                                       ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
            table.spaceAfter = 10
            result = [table]
            if data.get("caption"):
                result.append(self.paragraph(data["caption"], fontSize=9, leading=13))
            source_rows = [data["headers"], *data["rows"]]
            if len(source_rows) <= 5 and sum(len(plain(cell)) for row in source_rows for cell in row) <= 600:
                height = sum(flow.wrap(self.theme["width"], 700)[1] for flow in result)
                if height < 230:
                    return [KeepTogether(result)]
            return result
        if kind == "image":
            from PIL import Image as PillowImage
            path = image_path(data, self.base)
            with PillowImage.open(path) as image:
                ratio = image.height / image.width
            width = min(self.theme["width"] * data.get("width_fraction", 1), 320 / ratio)
            result = [Image(str(path), width=width, height=width * ratio, hAlign="LEFT")]
            for key in ("caption", "source_reference", "explanation"):
                if data.get(key):
                    result.append(self.paragraph(data[key], semantic, fontSize=9 if key != "explanation" else 11, leading=13 if key != "explanation" else 16))
            return [KeepTogether(result)] if sum(flow.wrap(self.theme["width"], 700)[1] for flow in result) < 420 else result
        if kind == "page_break":
            return [PageBreak()]
        if kind == "attempt_space":
            return [Spacer(1, 18)]
        raise ValueError(f"Unsupported PDF event: {kind}")

    def render(self, events, path):
        theme, meta = self.theme, self.model["metadata"]
        document = GuidePDF(str(path), pagesize=theme["page"], title=meta.get("title_override", meta["title"]),
                            author="", subject=meta.get("course", ""), pageCompression=1, invariant=1)
        frame = Frame(theme["margin"], theme["margin"], theme["width"], theme["page"][1] - 2 * theme["margin"],
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

        def page(canvas, doc):
            if doc.page == 1:
                return
            canvas.saveState()
            canvas.setFont("SGBody", 9)
            canvas.setFillColor(colors.HexColor(theme["muted"]))
            title = meta.get("course", meta.get("title_override", meta["title"]))
            while pdfmetrics.stringWidth(title, "SGBody", 9) > theme["width"]:
                title = title[:-2]
            canvas.drawString(theme["margin"], theme["page"][1] - 33, title)
            canvas.drawRightString(theme["page"][0] - theme["margin"], 30, str(doc.page - 1))
            canvas.restoreState()

        document.addPageTemplates(PageTemplate(id="guide", frames=frame, onPage=page))
        story = [Cover(self.model, theme), PageBreak()]
        toc = navigation(self.model, events)
        if toc:
            heading = self.paragraph("Contents", fontName="SGBold", fontSize=21, leading=26, spaceAfter=14)
            story.append(heading)
            for item in toc:
                story.append(self.paragraph([{"text": item["text"], "href": "#" + item["id"]}], leftIndent=(item["level"] - 1) * 12))
            story.append(PageBreak())
        stack = []
        for event in events:
            if event["kind"] == "group_start":
                stack.append(([], event["data"]["keep"]))
                continue
            if event["kind"] == "group_end":
                flows, keep = stack.pop()
                # Combine nested small groups before estimating height; KeepTogether
                # itself requires a live canvas when wrapped by ReportLab.
                def flatten(items):
                    for flow in items:
                        if isinstance(flow, KeepTogether):
                            yield from flatten(flow._content)
                        else:
                            yield flow
                flows = list(flatten(flows))
                height = sum(flow.wrap(theme["width"], 700)[1] + flow.getSpaceBefore() + flow.getSpaceAfter() for flow in flows)
                result = [KeepTogether(flows)] if keep and height < 230 else flows
                (stack[-1][0] if stack else story).extend(result)
                continue
            (stack[-1][0] if stack else story).extend(self.event(event))
        # Avoid nested KeepTogether containers separating a heading from its group.
        joined = []
        index = 0
        while index < len(story):
            current = story[index]
            if hasattr(current, "guide_heading") and index + 1 < len(story) and isinstance(story[index + 1], KeepTogether):
                joined.append(KeepTogether([current, *story[index + 1]._content]))
                index += 2
            else:
                joined.append(current)
                index += 1
        document.build(joined)
