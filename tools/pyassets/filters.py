"""Predicates for `skip=` in crop(): strip dimension lines, callout dots and similar annotations."""
from __future__ import annotations

ANNOT = {"#1D1D1B", "#706F6F", "#9D9D9C", "#808080", "#000000", "#0D0E10", "#575756", "#878787", "#B2B2B2", "#4D4D4D"}


def w(p):
    return p.box[2] - p.box[0]


def h(p):
    return p.box[3] - p.box[1]


def callout_dot(p, maxsize=5.5):
    """Small filled round bullet at the end of a callout line."""
    return p.fill in ANNOT and p.stroke is None and w(p) < maxsize and h(p) < maxsize and abs(w(p) - h(p)) < 1.2


def stroke_only(p):
    return p.fill is None and p.stroke is not None


def dashed(p):
    return bool(p.dashes)


def thin_line(p, maxw=1.2):
    """Straight hairline (dimension line, leader, centre line) drawn as a stroke or a very thin fill."""
    return (p.fill is None and p.stroke is not None and (w(p) < 0.01 or h(p) < 0.01)) or (
        p.fill in ANNOT and (w(p) < 0.01 or h(p) < 0.01)
    )


def any_of(*fs):
    return lambda p: any(f(p) for f in fs)


def annotation(p):
    """Typical dimension and callout furniture: dots, hairlines, dashed lines."""
    return callout_dot(p) or thin_line(p) or dashed(p)
