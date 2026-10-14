"""Element registry. Spec modules in tools/specs register one builder per element ID."""
from __future__ import annotations

from typing import Callable

import re

from .core import NORMALISE_LOG, Element, Source, cutout

BUILDERS: dict[str, Callable] = {}
META: dict[str, dict] = {}


def element(id: str, name_nl: str, level: str, category: str, page, **meta):
    """Decorator: the wrapped function receives (src) and returns a list of items."""

    def deco(fn):
        BUILDERS[id] = fn
        META[id] = dict(id=id, name_nl=name_nl, level=level, category=category, page=page, **meta)
        return fn

    return deco


class DocElement:
    """Element made by the composer (compose.Doc): same attributes the manifest needs as Element."""

    def __init__(self, doc, meta):
        for k, v in meta.items():
            setattr(self, k, v)
        self.doc = doc
        self.built_from = list(doc.built_from) or list(meta.get("built_from") or [])
        self.variables = list(doc.variables) or list(meta.get("variables") or [])
        self.normalised = {}
        self.items = []
        self.mm_per_pt = 1.0
        self.true_scale = meta.get("true_scale", False)
        self.dims_mm = meta.get("dims_mm")
        self.tags = tuple(meta.get("tags") or ())
        self.notes = meta.get("notes", "")
        self.status = meta.get("status", "rebuilt")

    def size_mm(self):
        return self.doc.size()

    def svg(self):
        return self.doc.svg()

    def colors(self):
        import re

        return sorted({c.upper() for c in re.findall(r'(?:fill|stroke|stop-color)="(#[0-9A-Fa-f]{6})"', self.doc.svg())})


def build(src: Source, id: str) -> Element:
    meta = dict(META[id])
    srcname = meta.pop("src", None)
    before = dict(NORMALISE_LOG)
    res = BUILDERS[id](src)
    if isinstance(res, tuple):
        items, extra = res
        meta.update(extra)
    else:
        items = res
    if hasattr(items, "boxes"):  # compose.Doc
        el = DocElement(items, meta)
        el.src = srcname
        return el
    if re.match(r"^py-atom-(picto|figure)-", id):
        items = cutout(items)  # single-colour masters: white gap paths become real holes
    after = NORMALISE_LOG
    norm = {k: after[k] - before.get(k, 0) for k in after if after[k] - before.get(k, 0) > 0}
    meta.setdefault("notes", "")
    el = Element(items=items, **meta)
    el.src = srcname
    el.normalised = norm  # {source colour: path count} replaced by the 1.3 brand value
    return el


def crop(src: Source, pno: int, bbox, partial=False, skip=None, skip_text=None, texts=True, recolor=None,
         outline_fonts=(), tol=0.6, under=(), over=()):
    """Standard extraction: vector paths and live text inside a source rectangle."""
    items = list(under)
    paths = src.paths(pno, bbox, partial=partial, skip=skip, tol=tol)
    gl = src.glyph_paths(pno, bbox, outline_fonts) if outline_fonts else []
    allp = paths + gl
    # keep original paint order
    allp.sort(key=lambda p: getattr(p, "seq", 1e9))
    if recolor:
        for p in allp:
            if isinstance(p.fill, str) and p.fill in recolor:
                p.fill = recolor[p.fill]
            if isinstance(p.stroke, str) and p.stroke in recolor:
                p.stroke = recolor[p.stroke]
    items += allp
    if texts:
        items += src.texts(pno, bbox, skip_text=skip_text, recolor=recolor)
    items += list(over)
    return items
