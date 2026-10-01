"""Deterministic local primitives shared by vector PDF and high-resolution DOCX."""

import io
import math

from PIL import Image, ImageDraw


def primitives(category):
    category = category.lower().replace("/", "_").replace("-", "_")
    shapes = []
    if any(word in category for word in ("nlp", "ai", "ml", "neural", "machine_learning")):
        for layer, count in enumerate((3, 5, 4)):
            x = 50 + layer * 135
            ys = [25 + i * 32 + (5 - count) * 16 for i in range(count)]
            for y in ys:
                shapes.append(("circle", (x, y, 6)))
            if layer:
                previous = (3, 5)[layer - 1]
                for a in range(previous):
                    py = 25 + a * 32 + (5 - previous) * 16
                    for y in ys:
                        shapes.append(("line", ((x - 135 + 6, py), (x - 6, y))))
    elif any(word in category for word in ("program", "software", "algorithm")):
        shapes.extend(("line", points) for points in [((75, 45), (40, 95), (75, 145)), ((280, 45), (315, 95), (280, 145)), ((200, 30), (150, 160))])
        for i in range(4):
            shapes.append(("line", ((100, 57 + i * 26), (240 - i * 15, 57 + i * 26))))
    elif any(word in category for word in ("signal", "system", "math")):
        shapes.append(("line", ((15, 100), (375, 100))))
        shapes.append(("line", ((45, 20), (45, 180))))
        for offset in (0, 25):
            shapes.append(("line", tuple((x, 100 + offset + 40 * math.sin((x - 45) / 32)) for x in range(45, 365, 2))))
    elif any(word in category for word in ("electronic", "logic", "vhdl", "digital")):
        for i in range(4):
            x, y = 35 + i * 78, 45 + (i % 2) * 60
            shapes.append(("rect", (x, y, 48, 38)))
            if i < 3:
                shapes.append(("line", ((x + 48, y + 19), (x + 62, y + 19), (x + 62, 45 + ((i + 1) % 2) * 60 + 19), (x + 78, 45 + ((i + 1) % 2) * 60 + 19))))
    else:
        for i in range(5):
            shapes.append(("rect", (30 + i * 58, 35 + (i % 2) * 30, 40, 100 - (i % 2) * 30)))
    return shapes


def raster(category, accent):
    scale = 5
    image = Image.new("RGB", (390 * scale, 205 * scale), "white")
    draw = ImageDraw.Draw(image)
    for kind, data in primitives(category):
        if kind == "line":
            draw.line([(round(x * scale), round(y * scale)) for x, y in data], fill=accent, width=scale)
        elif kind == "rect":
            x, y, w, h = data
            draw.rectangle((x * scale, y * scale, (x + w) * scale, (y + h) * scale), outline=accent, width=scale)
        else:
            x, y, radius = data
            draw.ellipse(((x - radius) * scale, (y - radius) * scale, (x + radius) * scale, (y + radius) * scale), fill=accent)
    stream = io.BytesIO()
    image.save(stream, format="PNG")
    return stream.getvalue()


def vector(canvas, category, x, y, width, accent):
    canvas.saveState()
    canvas.translate(x, y + width * 205 / 390)
    canvas.scale(width / 390, -width / 390)
    canvas.setStrokeColor(accent)
    canvas.setFillColor(accent)
    canvas.setLineWidth(1)
    for kind, data in primitives(category):
        if kind == "line":
            path = canvas.beginPath()
            path.moveTo(*data[0])
            for point in data[1:]:
                path.lineTo(*point)
            canvas.drawPath(path, stroke=1, fill=0)
        elif kind == "rect":
            canvas.rect(*data, stroke=1, fill=0)
        else:
            canvas.circle(*data, stroke=0, fill=1)
    canvas.restoreState()
