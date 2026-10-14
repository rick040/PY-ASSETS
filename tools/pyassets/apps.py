"""Application registry (level `app`): print pieces built from library elements plus variables.

    @application("py-app-demo", "Demo", "card", variants=("front", "back"), source=[("EvoluonPasjes.pdf", [1, 2])], ...)
    def _(ctx):
        return dict(reference={"front": svg_str, ...}, template={"front": Doc, ...}, variables={"front": {...}}, ...)

A variant of "" means the application has one version (files reference.svg and template.svg).
"""
from __future__ import annotations

APPS: dict = {}
APP_META: dict = {}


def application(id, name_nl, type, trim_mm, source, variants=("",), bleed_mm=3.0, status="extracted", cut_contour=None,
                source_files=None, tags=(), **meta):
    def deco(fn):
        APPS[id] = fn
        APP_META[id] = dict(id=id, name_nl=name_nl, type=type, trim_mm=list(trim_mm), source=source, variants=list(variants),
                            bleed_mm=bleed_mm, status=status, cut_contour=cut_contour, tags=list(tags), **meta)
        return fn

    return deco
