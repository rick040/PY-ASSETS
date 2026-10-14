# Extraction toolkit

Turns the ParkingYou huisstijlhandboek PDF into one SVG per element. Vector paths and live text are
read from the source with PyMuPDF and written as tight SVG (millimetres). Nothing is rasterised.

```
python3 -I tools/run.py --src source/handbook.pdf --spec s05 --ids '^py-prod-x$' --qa
```

* `--spec REGEX` loads only spec modules whose file name matches (use it while other specs are being written).
* `--ids REGEX` builds only matching element IDs.
* `--qa` writes `build/qa/<id>.png`: source crop on the left, extracted SVG on the right. White artwork is checked on grey.
* SVGs land in `svg/<level>/<id>.svg`.

## Writing a spec

A spec module lives in `tools/specs/sNN_name.py` and registers one builder per element ID:

```python
from pyassets import gradient_shape, grad_rect, fit_items, affine, paint, Gradient, Text, rect_item, ellipse_item
from pyassets.filters import annotation, callout_dot, thin_line, dashed, stroke_only, any_of
from pyassets.registry import element, crop

@element("py-atom-picto-car", "Route voor autoverkeer", "atom", "picto", 10)
def _(src):
    return crop(src, 10, (x0, y0, x1, y1), texts=False)          # bbox in PDF points, origin top-left
```

A builder returns `items` or `(items, extra)`. `extra` may carry:
`status` ("extracted" or "rebuilt"), `notes`, `mm_per_pt`, `true_scale` (True when derived from a handbook
dimension), `dims_mm` (stated overall size, e.g. `(1000, 1250, 200)`), `tags` (e.g. `("third-party",)`).

### crop(src, pno, bbox, ...)
Returns every vector path fully inside `bbox` (plus live text spans whose centre is inside), in the
original paint order. Options: `partial=True` (paths that merely intersect), `skip=fn(path)` (drop paths),
`skip_text=fn(str)`, `texts=False`, `recolor={'#1A3580': '#FFFFFF'}`, `outline_fonts=("RWSTTDdx","Anwb")`
(turn glyphs of non-Ubuntu fonts into outlines), `under=[...]` / `over=[...]` (extra items, e.g. rebuilt shapes).
Fully clipped (invisible) paths are dropped automatically. A path that sticks out of its clip is flagged
`CLIPPED:n` in the run output: look at it in the QA image.

### Finding things
* `from pyassets.qa import groups` then `groups(src, pno, region=(x0,y0,x1,y1), gap=2)` clusters paths into
  candidate elements and prints bbox, path count and colours.
* `src.images(pno, bbox)` lists raster images (these are never copied; they are photos, renders, soft masks).
* `src.spans(pno)` lists live text spans (font, size, bbox, colour).
* Render a crop to look at it: `pymupdf` page `get_pixmap(matrix=Matrix(4,4), clip=Rect(...))`.

### Gradients
In the source every blauw to aqua fill is written by InDesign as a clip path plus either a PDF shading or a
72 ppi image inside the clip. `get_drawings()` returns neither, so such a shape shows up as nothing (or as a
flat navy frame). The clip path is the exact outline of the fill, so:

* `src.clips(pno, bbox)` returns the clip outlines as paths.
* `gradient_shape(src, pno, clip_path)` returns that shape filled with a **measured** real vector gradient
  (the colour axis is regressed from the rendered page). The result is marked rebuilt.
* For plain rectangles you can also use `grad_rect(box, 'diag'|'vert'|'horiz')`.
* Some faces carry a last flat fill (for example `#182F72` on a lichtbak face) that is a soft-masked frame or
  shadow effect. It can cover the artwork in SVG, so skip it with `skip=` or rebuild it.

### Scale
Elements are written in mm. `mm_per_pt` converts source points. For products take a stated dimension from the
drawing, measure it in points and divide: `mm_per_pt = 1000 / measured_pt`. Atoms and components that sit in a
scaled drawing use the same scale. Leave the default (0.3528) when the handbook gives no dimension and do not
set `true_scale`.

### Rules
* Vector only. Never place an image of a page. Raster content (photos, 3D renders, brick walls, car silhouette)
  is left out.
* Strip dimension lines, callout leader lines and dots, annotation text, "TOEGEPASTE KLEUR" boxes, the page
  frame, footers and the All Jobs logo. Keep artwork text as live text.
* Colours: the colour normalisation in `core.py` already maps `#1A3680` to `#1A3580`, `#010101` to
  `#1D1D1B`, RAL swatch blue `#082E7A` to `#1A3580` and grey `#A0A1A0` to `#AEAEAE`.
* Rebuilt = anything not taken straight from source paths (gradient shapes, placeholders). Say so in `status`.
* No em dashes in any text.
