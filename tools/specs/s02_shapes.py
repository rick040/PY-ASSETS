"""1.4 Huisstijlvormen (p9)."""
from pyassets import Gradient, affine, fit_items, grad_rect, gradient_shape, items_box, paint, rect_item, Text
from pyassets.registry import crop, element

SRC = "p9"
BUBBLE = (357, 204, 462, 330)  # volvlak bubble geometry, used for rebuilt bubbles


@element("py-atom-logo-beeldmerk-color", "Beeldmerk", "atom", "logo", 9)
def _(src):
    return crop(src, 9, (158, 204, 263, 330), texts=False)


@element("py-atom-shape-bubble-solid", "volvlak", "atom", "shape", 9, variables=("fill colour",))
def _(src):
    return crop(src, 9, BUBBLE, texts=False)


@element("py-atom-shape-circle", "cirkel", "atom", "shape", 9, variables=("fill colour",))
def _(src):
    return crop(src, 9, (754, 204, 858, 309), texts=False)


@element("py-atom-shape-bubble-image-mask", "afbeeldingsmasker", "atom", "shape", 9, variables=("image",),
         built_from=("py-atom-shape-bubble-solid",))
def _(src):
    shape = paint(crop(src, 9, BUBBLE, texts=False), "#AEAEAE")
    for s in shape:
        s.fill_opacity = 0.25
    b = items_box(shape)
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2 - 8
    label = Text(cx, cy, "afbeelding", "Ubuntu Light", 300, False, 11, "#AEAEAE", anchor="middle", box=(cx - 30, cy - 10, cx + 30, cy + 3))
    return shape + [label], {"status": "rebuilt", "notes": "Source photo is a third-party raster (175 px). Replaced by an empty bubble with a placeholder label."}


@element("py-atom-shape-bubble-gradient", "verloop", "atom", "shape", 9, built_from=("py-atom-shape-bubble-solid", "py-tok-gradient-verloop"))
def _(src):
    shapes = [c for c in src.clips(9, (950, 195, 1070, 335)) if len(c.segs) > 5]  # the bubble outline (clip of the shading)
    return [gradient_shape(src, 9, shapes[0])], {"status": "rebuilt", "notes": "Bubble outline is the clip path of the source shading; the gradient is re-measured and written as a real SVG gradient."}


@element("py-atom-shape-bracket-arc", "beugelboog met slogan", "atom", "shape", 9, variables=("slogan text",))
def _(src):
    return crop(src, 9, (160, 440, 306, 569), skip=lambda p: p.fill == "#AEAEAE")


@element("py-atom-shape-separator-arc", "scheidingsboog", "atom", "shape", 9)
def _(src):
    return crop(src, 9, (356, 458, 448, 550), texts=False)


@element("py-atom-shape-pill-solid", "pil, vol", "atom", "shape", 9, variables=("fill colour",))
def _(src):
    return crop(src, 9, (485, 483, 728, 533), texts=False)


@element("py-atom-shape-pill-outline-gradient", "pil met rand op verloop", "atom", "shape", 9,
         built_from=("py-atom-shape-pill-solid", "py-tok-gradient-verloop"), variables=("pill colour",))
def _(src):
    panel = [c for c in src.clips(9, (770, 440, 1085, 575))]
    under = [gradient_shape(src, 9, panel[0])]
    pill = crop(src, 9, (800, 478, 1052, 538), texts=False)
    return under + pill, {"status": "rebuilt", "notes": "Gradient panel rebuilt as a vector gradient from the clip path of the source shading. Pill is extracted."}
