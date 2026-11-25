#!/usr/bin/env python3
"""Brand check on rendered posts: palette, contrast on the real pixels, safe zones, overlaps, logo, theme rules.

Usage:  python3 check_brand.py <post-dir> [...]
Reads, per format (and carousel slide) tag: <tag>.png, qa/<tag>-bg.png (text hidden) and qa/layout-<tag>.json.
Exit 1 when a blocking finding is found.

Rules (references/brand-visual.md, decisions.md):
- palette: outside library artwork and photos, every pixel must be a theme colour, a point on the verloop, or an
  edge blend between two theme colours (anti-aliasing). Catches lighting effects, tints and stray colours (S13).
- contrast: measured where the glyphs are (pixels that differ between the post and its text-hidden render),
  against the declared text colour. A post is seen at about 0.4x on a phone; text counts as large from 24 px
  (19 px bold) at that size, then 3:1 is enough, otherwise 4.5:1.
- safe zones and overlaps: text and logo inside the safe box of the format, no two text blocks on top of each other.
- logo: exactly one, the right file for the ground and theme, at least 60 px high on the canvas, clear space free.
- theme 2027: the logo plus at most two of {stem, figure, bubble, arrow}, at most one parkeerder.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import REPO, Finding, archetypes, load_json  # noqa: E402

PHONE = 0.4          # display scale of a 1080 px post on a phone
OFF_LIMIT = 0.003    # share of checked pixels that may be off-palette (anti-aliasing between three colours)
OFF_DIST = 14.0      # RGB distance that still counts as on-palette


def _hex(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def palette(theme: str) -> dict[str, tuple[int, int, int]]:
    if theme == "2027":
        t = load_json(REPO / "brand-2027/tokens/tokens.json")["color"]
        pick = {"blauw": ("blue", "700"), "diep": ("blue", "900"), "paper": ("blue", "50"), "aqua": ("aqua", "500"), "wit": ("neutral", "0")}
        return {k: _hex(t[g][s]["$value"]["hex"]) for k, (g, s) in pick.items()}
    t = load_json(REPO / "tokens.json")["colors"]
    ids = {"blauw": "py-tok-color-blauw", "aqua": "py-tok-color-aqua", "oranje": "py-tok-color-oranje", "grijs": "py-tok-color-grijs", "zwart": "py-tok-color-zwart"}
    p = {k: _hex(t[v]["hex"]) for k, v in ids.items()}
    p["wit"] = (255, 255, 255)
    return p


def verloop_points() -> list[tuple[int, int, int]]:
    stops = load_json(REPO / "tokens.json")["gradients"]["py-tok-gradient-verloop"]["stops"]
    pts = []
    for a, b in zip(stops, stops[1:]):
        ca, cb = np.array(_hex(a["hex"]), float), np.array(_hex(b["hex"]), float)
        for t in np.linspace(0, 1, 24):
            pts.append(tuple(ca + (cb - ca) * t))
    return pts


def lum(rgb: np.ndarray) -> np.ndarray:
    c = rgb / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def contrast(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    la, lb = lum(a), lum(b)
    return (np.maximum(la, lb) + 0.05) / (np.minimum(la, lb) + 0.05)


def off_palette(img: np.ndarray, mask: np.ndarray, colours: list[tuple]) -> tuple[float, list[str]]:
    px = img[mask].reshape(-1, 3).astype(float)
    if not len(px):
        return 0.0, []
    if len(px) > 120_000:
        px = px[np.random.default_rng(0).choice(len(px), 120_000, replace=False)]
    cols = np.array(colours, float)
    best = np.full(len(px), np.inf)
    for i in range(len(cols)):          # distance to every segment between two allowed colours (and the points)
        for j in range(i, len(cols)):
            a, b = cols[i], cols[j]
            d = b - a
            dd = float(d @ d)
            t = np.zeros(len(px)) if dd == 0 else np.clip((px - a) @ d / dd, 0, 1)
            dist = np.linalg.norm(px - (a + t[:, None] * d), axis=1)
            best = np.minimum(best, dist)
    off = px[best > OFF_DIST]
    share = len(off) / len(px)
    top = []
    if len(off):
        q = (off // 8 * 8).astype(int)
        vals, counts = np.unique(q, axis=0, return_counts=True)
        top = ["#%02X%02X%02X" % tuple(v) for v in vals[np.argsort(-counts)][:4]]
    return share, top


def boxes_overlap(a: dict, b: dict) -> float:
    x = max(0, min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"]))
    y = max(0, min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"]))
    return x * y / max(1, min(a["w"] * a["h"], b["w"] * b["h"]))


def logo_ok(theme: str, ground: str, variant: str) -> bool:
    if theme == "2027":
        return variant == ("2027/logo-horizontal-color" if ground == "white" else "2027/logo-horizontal-reverse")
    return variant == ("py-atom-logo-horizontal-color" if ground == "white" else "py-atom-logo-horizontal-reverse-open")


def check_tag(spec: dict, d: Path, tag: str) -> list[Finding]:
    out: list[Finding] = []
    lay = load_json(d / "qa" / f"layout-{tag}.json")
    fmt = archetypes()["formats"][lay["format"]]
    W, H = lay["width"], lay["height"]
    final = np.asarray(Image.open(d / f"{tag}.png").convert("RGB")).astype(float)
    bg = np.asarray(Image.open(d / "qa" / f"{tag}-bg.png").convert("RGB")).astype(float)
    els = lay["elements"]
    theme = spec["theme"]
    ground = spec["ground"]
    if spec["archetype"] == "carrousel" and lay.get("slide") is not None:
        ground = "navy" if lay["slide"] % 2 == 0 else "white"
    if spec["archetype"] == "foto-kop":
        ground = "navy"

    # palette: everything except library artwork, logos and photos
    mask = np.ones((H, W), bool)
    for e in els:
        if e["kind"] in ("logo", "graphic"):
            b = e["box"]
            mask[max(0, b["y"]):max(0, b["y"] + b["h"]), max(0, b["x"]):max(0, b["x"] + b["w"])] = False
    cols = list(palette(theme).values()) + (verloop_points() if theme == "feed" and ground == "verloop" else [])
    share, top = off_palette(bg, mask, cols)
    if share > OFF_LIMIT:
        out.append(Finding("brand", "block", tag, f"{share:.1%} of the background is not a brand colour (most: {', '.join(top)})", "S13 exact colours"))

    sx, sy = fmt["safe"]["left"], fmt["safe"]["top"]
    ex, ey = W - fmt["safe"]["right"], H - fmt["safe"]["bottom"]
    texts = [e for e in els if e["kind"] == "text"]
    for e in texts:
        b, name = e["box"], e["name"]
        # safe zone
        if b["x"] < sx - 2 or b["y"] < sy - 2 or b["x"] + b["w"] > ex + 2 or b["y"] + b["h"] > ey + 2:
            out.append(Finding("brand", "block", f"{tag}/{name}", f"text outside the safe zone ({b['x']},{b['y']} {b['w']}x{b['h']}; safe {sx},{sy} to {ex},{ey})", "platform-specs.md §2"))
        # contrast on the glyphs
        x0, y0 = max(0, b["x"]), max(0, b["y"])
        x1, y1 = min(W, b["x"] + b["w"]), min(H, b["y"] + b["h"])
        if x1 <= x0 or y1 <= y0 or not e.get("fg"):
            continue
        diff = np.abs(final[y0:y1, x0:x1] - bg[y0:y1, x0:x1]).sum(axis=2)
        glyph = diff > 40
        if glyph.sum() < 20:
            out.append(Finding("brand", "block", f"{tag}/{name}", "text is not visible against its ground", "contrast"))
            continue
        fg = np.array(_hex(e["fg"]), float)
        ratios = contrast(bg[y0:y1, x0:x1][glyph], fg[None, :])
        worst = float(np.percentile(ratios, 5))
        size = (e.get("size") or 40) * PHONE * (1080 / W if W > 1080 else 1)  # a wider canvas is shown at the same width
        large = size >= 24 or (e.get("bold") and size >= 18.66)
        need = 3.0 if large else 4.5
        if worst < need:
            out.append(Finding("brand", "block", f"{tag}/{name}", f"contrast {worst:.2f}:1 behind the text, needs {need}:1 ({'large' if large else 'normal'} text)", "brand-visual.md §2"))
        if size < 12:
            out.append(Finding("brand", "warn", f"{tag}/{name}", f"text is {size:.0f} px on a phone (under 12 px is hard to read)", "brand-visual.md §2"))
    # overlaps between text blocks
    for i, a in enumerate(texts):
        for b in texts[i + 1:]:
            if boxes_overlap(a["box"], b["box"]) > 0.04:
                out.append(Finding("brand", "block", f"{tag}/{a['name']}+{b['name']}", "two text blocks overlap", "layout"))

    # text on top of artwork (watermark and full-bleed photos excluded; text sits in or on its own shapes)
    arts = [e for e in els if e["kind"] == "graphic" and e["name"] not in ("watermark", "media")]
    for t in texts:
        for a in arts:
            if a["name"].startswith(t["name"]) or t["name"].startswith(a["name"].split("-image")[0] + "-number"):
                continue
            if boxes_overlap(t["box"], a["box"]) > (0.01 if a["name"] == "figure" else 0.08):
                out.append(Finding("brand", "block", f"{tag}/{t['name']}+{a['name']}", "text runs into an image or figure", "layout"))

    # logo
    logos = [e for e in els if e["kind"] == "logo"]
    if len(logos) != 1:
        out.append(Finding("brand", "block", tag, f"{len(logos)} logos, expected 1", "brand-visual.md"))
    for lg in logos:
        b = lg["box"]
        if not logo_ok(theme, ground, lg["variant"]):
            out.append(Finding("brand", "block", f"{tag}/logo", f"logo {lg['variant']} is not the version for ground {ground} in theme {theme}", "brand-visual.md §3.2/§4.2"))
        if b["h"] < 56 * (W / 1080 if W > 1080 else 1) * (0.62 if lay["format"] == "landscape" else 1):
            out.append(Finding("brand", "block", f"{tag}/logo", f"logo is {b['h']} px high; minimum about 60 px on a 1080 canvas", "CS 2 minimum size"))
        if b["x"] < sx - 2 or b["y"] < sy - 2 or b["x"] + b["w"] > ex + 2 or b["y"] + b["h"] > ey + 2:
            out.append(Finding("brand", "block", f"{tag}/logo", "logo outside the safe zone", "platform-specs.md §2"))
        pad = 0.5 * b["h"] * 0.83
        zone = {"x": b["x"] - pad, "y": b["y"] - pad, "w": b["w"] + 2 * pad, "h": b["h"] + 2 * pad}
        for e in els:
            if e is lg or e["name"] in ("watermark", "media") or e["kind"] == "graphic" and e["name"] == "watermark":
                continue
            if boxes_overlap(zone, e["box"]) * min(zone["w"] * zone["h"], e["box"]["w"] * e["box"]["h"]) > 0.02 * zone["w"] * zone["h"]:
                out.append(Finding("brand", "block", f"{tag}/logo", f"{e['name']} is inside the clear space of the logo", "CS 2 clear space"))

    # figures may not be cut off by the canvas
    for e in els:
        if e["name"] == "figure":
            b = e["box"]
            if b["x"] < 0 or b["y"] < 0 or b["x"] + b["w"] > W or b["y"] + b["h"] > H:
                out.append(Finding("brand", "block", f"{tag}/figure", "figure is cut off by the canvas edge", "CS 4b"))

    # theme rules
    names = [e["name"] for e in els]
    if theme == "2027":
        n_el = sum(1 for e in els if e["name"] in ("stem", "figure", "bubble") or (e.get("variant") or "").startswith("2027/arrow"))
        if n_el > 2:
            out.append(Finding("brand", "block", tag, f"{n_el} identity elements besides the logo; 2027 allows at most two", "CS 4b"))
        if names.count("figure") > 1:
            out.append(Finding("brand", "block", tag, "more than one parkeerder", "CS 4b"))
    else:
        if names.count("price") > 1:
            out.append(Finding("brand", "warn", tag, "more than one price badge", "brand-visual.md §3.4"))

    # grid crop (feed 4:5 shows as 3:4 in the profile grid)
    if lay["format"] == "feed":
        cx0 = (W - fmt.get("grid_crop", {}).get("width", W)) / 2
        for e in els:
            if e["name"] in ("headline", "logo"):
                b = e["box"]
                if b["x"] < cx0 or b["x"] + b["w"] > W - cx0:
                    out.append(Finding("brand", "info", f"{tag}/{e['name']}", "partly outside the 3:4 profile-grid crop", "platform-specs.md §2"))

    # third-party marks
    third = third_party_ids()
    for e in els:
        v = e.get("variant") or ""
        if v in third and not any(v in a.get("what", "") for a in spec.get("approvals", [])):
            out.append(Finding("brand", "warn", f"{tag}/{e['name']}", f"{v} is a third-party mark; needs approval", "S10"))
    return out


_third: set[str] | None = None


def third_party_ids() -> set[str]:
    global _third
    if _third is None:
        _third = {e["id"] for e in load_json(REPO / "elements.json")["elements"] if "third-party" in (e.get("tags") or [])}
    return _third


def tags_of(d: Path) -> list[str]:
    return sorted(p.name[len("layout-"):-len(".json")] for p in (d / "qa").glob("layout-*.json"))


def check(spec: dict, d: Path) -> list[Finding]:
    d = Path(d)
    tags = tags_of(d)
    if not tags:
        return [Finding("brand", "block", "render", "no layout files; the post was not rendered")]
    out: list[Finding] = []
    for tag in tags:
        out += check_tag(spec, d, tag)
    return out


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    blocked = False
    for arg in argv:
        d = Path(arg)
        spec = load_json(d / "spec.json")
        for f in check(spec, d):
            blocked |= f.severity == "block"
            print(f"{spec['id']}  {f.severity.upper():5}  {f.where}: {f.message}  [{f.rule}]")
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
