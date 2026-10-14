#!/usr/bin/env python3
"""List the drawings of one print page with bbox in mm (page coordinates, origin top left of the MediaBox).

usage: python3 -I tools/print_probe.py source/print/Maashaven.pdf [page_index_from_0]
Also: `--spans` lists live text with origin (baseline) in mm.
"""
import sys
import pymupdf

mm = lambda v: round(v / 72 * 25.4, 1)


def hx(c):
    return "-" if c is None else "#%02X%02X%02X" % tuple(round(v * 255) for v in c[:3])


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    f, pn = args[0], int(args[1]) if len(args) > 1 else 0
    p = pymupdf.open(f)[pn]
    if "--spans" in sys.argv:
        for b in p.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    if s["text"].strip():
                        print(repr(s["text"])[:50], s["font"], "size", mm(s["size"]), "origin", [mm(v) for v in s["origin"]], "bbox", [mm(v) for v in s["bbox"]])
        return
    for i, dr in enumerate(p.get_drawings()):
        r = dr["rect"]
        print(i, dr["type"], "fill", hx(dr.get("fill")), "stroke", hx(dr.get("color")) if dr["type"] != "f" else "-", dr.get("width"),
              "items", len(dr["items"]), "bbox", [mm(r.x0), mm(r.y0), mm(r.x1), mm(r.y1)], "w x h", mm(r.width), mm(r.height))


if __name__ == "__main__":
    main()
