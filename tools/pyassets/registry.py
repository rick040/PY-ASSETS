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


def build(src: Source, id: str) -> Element:
    meta = dict(META[id])
    before = dict(NORMALISE_LOG)
    res = BUILDERS[id](src)
    if isinstance(res, tuple):
        items, extra = res
        meta.update(extra)
    else:
        items = res
    if re.match(r"^py-atom-(picto|figure)-", id):
        items = cutout(items)  # single-colour masters: white gap paths become real holes
    after = NORMALISE_LOG
    norm = {k: after[k] - before.get(k, 0) for k in after if after[k] - before.get(k, 0) > 0}
    meta.setdefault("notes", "")
    el = Element(items=items, **meta)
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
