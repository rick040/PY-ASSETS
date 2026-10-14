# Print toolkit (PM-137)

Builds the new print elements (svg/), the applications (applications/<id>/) and the manifests from the ten PDFs in `source/print/`.
It extends the handbook toolkit (`tools/README.md`: Source, crop, registry). Read that first for extraction basics.

```
python3 -I tools/build_print.py --spec p40 --no-json      # build only your spec module, do not touch the manifests
python3 -I tools/build_print.py                           # full build (writes elements.json, tokens.json observed, applications.json)
```
Always use `--spec <your module prefix> --no-json` while working. Specs live in `tools/specs_print/pNN_name.py`.
One module owns its elements and its applications. Never edit another module, `tools/pyassets/*` or the manifests (tell the lead instead).

## Decisions already taken (from the approved Phase 1)

* Master blue = official token (`#1A3580`, CMYK 100/83/0/17). Every other print blue is drift and is NOT used in templates or library elements.
* New library elements (atoms, components): extracted from the print files with colours normalised to the tokens (PRINT_NORMALISE does it
  automatically while building elements: the seven blues to `#1A3580`, aqua variants to `#32B9CD`, `#000000` to `#1D1D1B`). Light aqua
  (CMYK 54/0/14/0, viewer `#68CBDB`) has no token and stays as sampled (observed).
* `reference.svg` = faithful reproduction of the source page (source colours, original copy including typos). NOT normalised.
* `template.svg` = official colours from tokens.json (hex), correct trim and **3 mm bleed** (10 mm for the uitrit sign), every variable is live Ubuntu text
  (`data-variable`) or a placeholder group, corrected copy (typos fixed, record original and corrected under `copy_corrections`).
* Stickers (diefstal, laadkabel) and the uitrit sign get a `cut-contour` group (ThruCut, 1 pt stroke, 0.2 mm inside the trim). Sticker corner
  radius is a proposal (4.2 mm, the radius seen on the diefstal footer); say so in notes.
* Reuse: when a print element equals a library element, `place()` the library SVG (and list it in built_from). Do not add near duplicates.
  Existing IDs are never changed. Variants get a suffix.
* Third-party marks (payment brands, partners, GLOW): extract the white mark as is, tag `tags=("third-party",)`, note "reference only, source the official file". Do not redraw.
* No em dashes or en dashes in any text you write (notes, names, copy).
* Vector only. No raster. QR modules in Maashaven are a clip path: `src.clips(pno, bbox)` returns them.
* Transparency: tints in the source are transparency groups (aqua 10 percent input fields, aqua 5 percent watermark, navy 5 percent signature box,
  25 percent inactive GLOW pills). `crop()` returns paths with `gop`; use `regroup(src, pno, items)` (pyassets.core) to turn them into
  `Group` items with opacity, or set `fill_opacity` on a single path. Check with a render that the tint looks like the source.

## Registering an element

```python
from pyassets import printsrc
from pyassets.compose import Doc
from pyassets.registry import crop, element
from pyassets.apps import application

@element("py-atom-demo", "Demo atoom", "atom", "icon", 1, src="laadkabel",     # src = key in printsrc.SOURCES, page = source page
         variables=("colour",), notes="...", tags=(), status="extracted")      # status extracted or rebuilt
def _(src):
    return crop(src, 1, printsrc.box_mm(76, 12, 181, 111), texts=False)         # bbox in mm of the PAGE (origin top left of the MediaBox)
```
* `python3 -I tools/print_probe.py source/print/<file>.pdf <page0>` lists every drawing with bbox in mm (add `--spans` for live text with baseline origin).
* `printsrc.box_mm(x0, y0, x1, y1)` converts page mm to source points for `crop`. Find coordinates with `tools/pyassets/qa.py: groups(src, pno, region=...)`
  or by listing drawings (`src.drawings(pno)`; each has `rect`, `fill`, `seq`).
* Return `items` (extracted), `(items, extra)` or a `Doc` (composed). A tight `Doc` (`Doc(id, title, tight=True)`) becomes a component built from library SVGs
  plus live text; its `built_from` and `variables` are collected automatically.
* Rebuilt = anything that is not source paths (constructions, redrawn parts, composed from library elements with new positions). Say why in notes.
* IDs: `py-{level}-{category}-{name}[-{variant}]`, lowercase kebab-case. Level is atom, comp or prod. Dutch name in `name_nl`.
* Element order inside one build run is atoms, comps, prods, then sorted by ID. A comp may `place()` an atom of the same run.

## Composer (`pyassets/compose.py`)

All coordinates are mm, relative to the TRIM corner for templates; for `tight=True` docs free coordinates.
`Doc.place(ref_id, x, y, w=|h=|scale=, anchor="tl|tc|tr|cl|cc|cr|bl|bc|br", recolor={"#1A3580": "#FFFFFF"}, opacity=, rotate=, flip_x=, flip_y=)`
puts a library SVG; `rect`, `circle`, `line`, `path`, `text(x, y_baseline, s, size, fill, weight=400|500|700, italic, anchor, spacing, variable=, runs=[(text, weight)...])`,
`group(id)` (context manager), `uses(*ids)` (record tokens or pattern comps in built_from without placing), `cut_contour(x0, y0, x1, y1, rx=)`, `placeholder(id, x0, y0, x1, y1, label, variable=)`,
`guides(trim_w, trim_h)` (hidden trim group). `place()` returns the placed box, use it to align the next item.
See `tools/specs_print/p01_tagline.py` for a complete example (atom, two comps, one application with reference and template).

## Application

```python
@application("py-app-demo", "Dutch name", "sticker", trim_mm=(250, 300), source=[("laadkabel", [1])], bleed_mm=3.0,
             variants=("",), status="rebuilt", cut_contour={"spot": "ThruCut", "stroke_pt": 1, "inset_mm": 0.2, "corner_radius_mm": 4.2, "note": "proposal"})
def _(ctx):
    d = ctx.Doc("py-app-demo", "title", trim=(250, 300), bleed=3.0)
    ...
    return dict(reference={"": ctx.reference("laadkabel", 1, omit=lambda p: ..., outline_fonts=())}, template={"": d},
                omitted=["hidden grey underlay"], copy_corrections=[{"original": "...", "corrected": "..."}], notes="...")
```
* `variants=("front", "back")`: files are `reference-front.svg`, `template-front.svg`; variant IDs are `<id>-front`. Return dicts keyed by variant.
* Template content order: background (named `background` or `bleed-background`, runs into the bleed), design elements, `variables` as live text, `cut-contour`, `guides`.
* Group every library element or comp you place inside `with d.group("<element id>"):` when that helps the exploded view; `built_from` is collected from `place()`/`uses()`.
* Reference: `ctx.reference(key, pno, variant=, omit=, outline_fonts=, skip_text=)`. `omit(path)` drops hidden leftovers (list them in `omitted`).
  Texts in non-Ubuntu fonts (ArialMT) must be outlined: `outline_fonts=("ArialMT",)`.

## Checks before you hand in

1. Build your spec, render every reference.svg, template.svg and new element SVG to PNG (`cairosvg.svg2png`, grey or navy background for white artwork) and LOOK at them next to the source page render.
2. Reference must match the source visually (colours, tints, positions). Template must be the same layout in token colours.
3. Template viewBox must equal trim + 2 x bleed (check with `Doc.size()`).
4. No em or en dashes, no raster, no `clipPath`/`mask`/`filter`.
