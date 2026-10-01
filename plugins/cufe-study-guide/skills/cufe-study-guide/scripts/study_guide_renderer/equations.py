"""One cached Mathtext layout: vector paths for PDF, 600-dpi images for Word."""

import io

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.patches import PathPatch
from matplotlib.textpath import TextPath
from matplotlib.transforms import Affine2D

from .model import GuideError


class EquationCache:
    def __init__(self, color):
        self.color = color
        self.cache = {}

    def get(self, expression):
        if expression in self.cache:
            return self.cache[expression]
        try:
            if "$" in expression:
                raise ValueError("supply Mathtext without surrounding dollar delimiters")
            path = TextPath((0, 0), f"${expression}$", size=13,
                            prop=FontProperties(math_fontfamily="stix"), usetex=False)
            box = path.get_extents()
            width, height = box.width + 4, box.height + 4
            if width <= 4 or height <= 4:
                raise ValueError("empty mathematical expression")
            path = path.transformed(Affine2D().translate(2 - box.x0, 2 - box.y0))
            figure = Figure(figsize=(width / 72, height / 72), dpi=600)
            FigureCanvasAgg(figure)
            axes = figure.add_axes((0, 0, 1, 1), xlim=(0, width), ylim=(0, height))
            axes.set_axis_off()
            axes.add_patch(PathPatch(path, facecolor=self.color, linewidth=0))
            output = io.BytesIO()
            figure.savefig(output, format="png", dpi=600, transparent=True)
            result = {"path": path, "width": width, "height": height, "png": output.getvalue()}
            self.cache[expression] = result
            return result
        except (ValueError, RuntimeError) as exc:
            raise GuideError(f"Equation rendering failed for {expression!r}: {exc}. Use supported Mathtext or explicit shorter steps.") from exc


def fitted(equation, width):
    scale = min(1.0, width / equation["width"])
    if scale < 9 / 13:
        raise GuideError("Equation would be smaller than 9 pt; split it into explicit shorter equation lines")
    return equation["width"] * scale, equation["height"] * scale, scale


def draw_path(canvas, path):
    from matplotlib.path import Path
    result = canvas.beginPath()
    current = (0, 0)
    for vertices, code in path.iter_segments(curves=True, simplify=False):
        if code == Path.MOVETO:
            result.moveTo(*vertices)
            current = tuple(vertices)
        elif code == Path.LINETO:
            result.lineTo(*vertices)
            current = tuple(vertices)
        elif code == Path.CURVE3:
            control, end = vertices[:2], vertices[2:]
            c1 = [current[i] + 2 * (control[i] - current[i]) / 3 for i in range(2)]
            c2 = [end[i] + 2 * (control[i] - end[i]) / 3 for i in range(2)]
            result.curveTo(*c1, *c2, *end)
            current = tuple(end)
        elif code == Path.CURVE4:
            result.curveTo(*vertices)
            current = tuple(vertices[-2:])
        elif code == Path.CLOSEPOLY:
            result.close()
    canvas.drawPath(result, fill=1, stroke=0)
