#!/usr/bin/env python3
"""Build the ParkingYou 2027 design tokens.

Single source for brand-2027/tokens/:
  tokens.json   W3C DTCG format 2025.10 (colour values as colorSpace/components objects with hex fallback)
  tokens.css    CSS custom properties, light theme on :root, dark theme on [data-theme="dark"]
  contrast.md   computed WCAG 2.x contrast for every semantic text and UI pair

Run: python3 -I brand-2027/tools/build_tokens.py
Values come from brand-2027/02-build/core-spec.md. Change them here and in the spec together.
"""
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "tokens")

# ---------------------------------------------------------------- primitives
PRIMITIVES = {
    "blue": {"50": "#F4F6FB", "100": "#E8ECF6", "200": "#C9D2EA", "300": "#9AAAD6", "400": "#6F86C8",
             "500": "#4561B0", "600": "#2B4A9E", "700": "#1A3580", "800": "#12245A", "850": "#101C44", "900": "#0D142E"},
    "aqua": {"50": "#F0FAFC", "100": "#E3F6F9", "200": "#BDE9F0", "300": "#86D6E2", "400": "#5CC7D7",
             "500": "#32B9CD", "600": "#1E9AAD", "700": "#127C8C", "800": "#0E6170", "900": "#0A3F49"},
    "orange": {"50": "#FFF5E8", "100": "#FFE6C7", "200": "#FFCC8F", "300": "#FAAE52", "400": "#F59A26",
               "500": "#F08300", "600": "#C96800", "700": "#B35A00", "800": "#8A4500", "900": "#5C2E00"},
    "neutral": {"0": "#FFFFFF", "50": "#F7F8FA", "100": "#EEF0F3", "200": "#DDE1E7", "300": "#C2C7CF",
                "400": "#AEAEAE", "500": "#767B86", "600": "#5E6470", "700": "#434852", "800": "#2B2F36",
                "900": "#1D1D1B"},
    "red": {"100": "#FDECEA", "600": "#C4281C", "700": "#A31F15"},
}

# Production data for the brand colours. CMYK and RAL from handbook 1.3 (RAL is best match only).
# Pantone and vinyl stay null until the colour chapter (B2) proposes and the core spec approves them.
PRODUCTION = {
    # CMYK: handbook 1.3 for brand colours; PY-Diep and tints by FOGRA39 conversion (B2, D23). Pantone, RAL, vinyl: nearest by
    # CIEDE2000 (B2, D23). All matches must be confirmed on physical swatches and a lit test panel before production.
    ("blue", "700"): {"name": "PY-Blauw", "cmyk": [100, 83, 0, 17], "ral": "5002", "ralMatch": "nearest, dE 4.5",
                      "pantone": {"coated": "3597 C (alt. 287 C)", "uncoated": "280 U"},
                      "vinyl": {"opaque": "Oracal 751C-049 King blue", "translucent": "Oracal 8500-006 Intensive blue or 3M 3630-157 Sultan Blue"}},
    ("aqua", "500"): {"name": "PY-Aqua", "cmyk": [69, 0, 21, 0], "ral": "RAL Design 220 70 35", "ralMatch": "dE 1.7; RAL Classic 6027 retired (dE 10.2)",
                      "pantone": {"coated": "3115 C", "uncoated": "3115 U"},
                      "vinyl": {"opaque": "none standard: print on white vinyl with matte laminate", "translucent": "none standard: print on 3M IJ3630-20"}},
    ("orange", "500"): {"name": "PY-Oranje", "cmyk": [0, 57, 100, 0], "ral": "2003", "ralMatch": "dE 7.5; test RAL 1037 (dE 5.4) on the sample boards",
                        "pantone": {"coated": "144 C", "uncoated": "144 U"},
                        "vinyl": {"opaque": "3M 100-717 Light Orange (unverified)", "translucent": "3M 3630-74 Kumquat Orange"}},
    ("neutral", "400"): {"name": "PY-Grijs", "cmyk": [0, 0, 0, 42], "ral": "9006", "ralMatch": "hardware colour",
                         "pantone": {"coated": "Cool Gray 5 C", "uncoated": "Cool Gray 5 U"},
                         "vinyl": {"opaque": "Oracal 751C-724 Ice grey", "translucent": "Oracal 8500-076 Telegrey"}},
    ("neutral", "900"): {"name": "PY-Zwart", "cmyk": [0, 0, 0, 100], "ral": "9005", "ralMatch": "nearest",
                         "pantone": {"coated": "419 C or K 100", "uncoated": "K 100"},
                         "vinyl": {"opaque": "Oracal 751C-070M matt", "translucent": "Oracal 8500-070 Black"}},
    ("blue", "900"): {"name": "PY-Diep", "cmyk": [100, 83, 0, 80], "ral": "5004", "ralMatch": "dE 9.1, outside FOGRA39 gamut",
                      "pantone": {"coated": "5255 C", "uncoated": None},
                      "vinyl": {"opaque": "Oracal 751C-590 Blueberry", "translucent": None}},
    ("neutral", "0"): {"name": "Wit", "cmyk": [0, 0, 0, 0], "ral": "9016", "ralMatch": "dE 4.5, LRV 87",
                       "pantone": None, "vinyl": {"opaque": "Oracal 751C-010M matt", "translucent": "Oracal 8500-010 White"}},
}
# Print tints (screens of the brand colour), FOGRA39 (B2, D23). Print uses steps 50 to 300 only.
TINT_CMYK = {
    ("blue", "50"): [5, 3, 2, 0], ("blue", "100"): [10, 6, 2, 0], ("blue", "200"): [24, 15, 2, 0], ("blue", "300"): [44, 30, 2, 0],
    ("aqua", "50"): [8, 0, 3, 0], ("aqua", "100"): [16, 0, 5, 0], ("aqua", "200"): [30, 0, 9, 0], ("aqua", "300"): [50, 0, 15, 0],
    ("orange", "50"): [0, 5, 11, 0], ("orange", "100"): [0, 13, 25, 0], ("orange", "200"): [0, 25, 49, 0],
}

# ---------------------------------------------------------------- semantic colour (light, dark)
SEMANTIC = {
    "surface": {
        "default": ("neutral.0", "blue.900", "Page and screen background."),
        "subtle": ("blue.50", "blue.850", "Quiet sections, input wells, table stripes."),
        "raised": ("neutral.0", "blue.800", "Cards and sheets above the page."),
        "brand": ("blue.700", "blue.700", "Navy brand field: headers, social, cards, signage faces."),
        "inverse": ("blue.900", "neutral.0", "Strongest contrast field."),
        "code": ("neutral.0", "neutral.0", "Behind QR and barcodes: always light, in every theme."),
    },
    "text": {
        "default": ("neutral.900", "neutral.0", "Body text."),
        "muted": ("neutral.600", "neutral.300", "Secondary text, captions, labels."),
        "brand": ("blue.700", "aqua.300", "Headings and brand text."),
        "on-brand": ("neutral.0", "neutral.0", "Text on surface.brand."),
        "link": ("blue.700", "aqua.300", "Links, always underlined."),
        "aqua": ("aqua.700", "aqua.300", "Aqua as text colour on light surfaces."),
        "on-code": ("blue.900", "blue.900", "QR and barcode modules on surface.code."),
    },
    "border": {
        "subtle": ("neutral.200", "blue.600", "Dividers and card edges (decorative)."),
        "strong": ("neutral.500", "blue.400", "Input and control borders, 3:1 minimum."),
    },
    "focus": {
        "ring": ("blue.900", "aqua.500", "Focus outline, 3 px with 2 px offset."),
        "ring-on-brand": ("aqua.500", "aqua.500", "Focus outline on surface.brand."),
    },
    "action": {
        "primary-bg": ("blue.700", "aqua.500", "The main button (D33): navy, aqua on dark."),
        "primary-bg-hover": ("blue.600", "aqua.400", "Hover state of the main button."),
        "primary-bg-pressed": ("blue.800", "aqua.600", "Pressed state of the main button."),
        "primary-fg": ("neutral.0", "blue.900", "Text and arrow on the main button."),
        "secondary-bg": ("neutral.0", "blue.900", "Second button: outline style, ground."),
        "secondary-bg-hover": ("blue.50", "blue.800", "Hover state of the second button."),
        "secondary-bg-pressed": ("blue.100", "blue.850", "Pressed state of the second button."),
        "secondary-fg": ("blue.700", "aqua.300", "Text and arrow of the second button."),
        "secondary-border": ("blue.700", "aqua.300", "2 px outline of the second button (D35)."),
    },
    "task": {
        "drive-bg": ("blue.700", "blue.700", "Rijden: car routes, portals, entrances, levels."),
        "drive-fg": ("neutral.0", "neutral.0", "Content on drive-bg."),
        "walk-bg": ("aqua.500", "aqua.500", "Lopen: pedestrian routes, lift, stairs, exits."),
        "walk-fg": ("blue.700", "blue.700", "Content on walk-bg."),
        "pay-bg": ("orange.500", "orange.500", "Betalen en let op: terminals, tariffs, faults."),
        "pay-fg": ("blue.900", "blue.900", "Content on pay-bg."),
    },
    "voice": {
        "arc": ("aqua.500", "aqua.500", "De stem (half arc) on white and navy; on aqua grounds use blue.700."),
    },
    "vak": {
        "line": ("neutral.200", "blue.400", "Het vak: bay lines (light ground / navy ground)."),
        "line-on-brand": ("blue.400", "blue.400", "Het vak on surface.brand."),
        "mine": ("aqua.100", "blue.600", "Jouw vak fill."),
        "mine-on-brand": ("blue.600", "blue.600", "Jouw vak fill on surface.brand."),
        "mine-edge": ("aqua.500", "aqua.500", "Jouw vak side lines, double weight."),
    },
    "figure": {
        "head": ("aqua.500", "aqua.500", "Parkeerders: head, always aqua (one-colour navy on aqua grounds)."),
        "body": ("blue.700", "neutral.0", "Parkeerders: body on light / on navy."),
    },
    "bubble": {
        "navy": ("blue.700", "blue.700", "Bubble fill; content neutral.0."),
        "aqua": ("aqua.500", "aqua.500", "Bubble fill; content blue.700."),
        "orange": ("orange.500", "orange.500", "Bubble fill: payment signs in the garage only (D31); content blue.900."),
        "white": ("neutral.0", "neutral.0", "Bubble fill; content blue.700."),
    },
    "status": {
        "free": ("aqua.700", "aqua.300", "Vrij: always with the word."),
        "full": ("orange.700", "orange.300", "Vol: always with the word."),
        "closed": ("neutral.600", "neutral.300", "Gesloten: always with the word."),
    },
    "feedback": {
        "error": ("red.600", "red.100", "Error text and icon."),
        "error-bg": ("red.100", "red.700", "Error message background."),
        "success": ("aqua.700", "aqua.300", "Success text and icon."),
        "warning": ("orange.700", "orange.300", "Warning text and icon."),
        "info": ("blue.700", "aqua.300", "Info text and icon."),
    },
}

# component tier (D11): components read these; they alias semantic tokens
COMPONENT = {
    "button": {"primary.bg": "action.primary-bg", "primary.bg-hover": "action.primary-bg-hover",
               "primary.bg-pressed": "action.primary-bg-pressed", "primary.fg": "action.primary-fg",
               "secondary.bg": "action.secondary-bg", "secondary.bg-hover": "action.secondary-bg-hover",
               "secondary.bg-pressed": "action.secondary-bg-pressed", "secondary.fg": "action.secondary-fg",
               "focus-ring": "focus.ring"},
    "input": {"bg": "surface.default", "fg": "text.default", "border": "border.strong", "border-error": "feedback.error",
              "label": "text.default", "hint": "text.muted"},
    "card": {"bg": "surface.raised", "border": "border.subtle", "title": "text.brand", "meta": "text.muted"},
    "ticket": {"code-bg": "surface.code", "code-fg": "text.on-code"},
}
COMPONENT_SIZE = {"button-height": 48, "button-height-large": 56, "input-height": 48, "input-height-large": 56,
                  "chip-height": 36, "tag-height": 28, "hit-area-min": 44, "topbar-height-phone": 56,
                  "topbar-height-desktop": 72, "bottombar-height": 64, "focus-ring-width": 3, "focus-ring-offset": 2,
                  "border-width": 1, "border-width-strong": 2, "progress-height": 4, "plate-band-width": 36,
                  "thumb-size": 96}

# pairs that carry text or UI meaning: (fg, bg, kind) with kind text (4.5) or ui (3.0) or large (3.0)
PAIRS = [
    ("text.default", "surface.default", "text"), ("text.default", "surface.subtle", "text"),
    ("text.muted", "surface.default", "text"), ("text.muted", "surface.subtle", "text"),
    ("text.brand", "surface.default", "text"), ("text.link", "surface.default", "text"),
    ("text.aqua", "surface.default", "text"), ("text.on-brand", "surface.brand", "text"),
    ("text.default", "surface.raised", "text"), ("text.muted", "surface.raised", "text"),
    ("border.strong", "surface.default", "ui"), ("focus.ring", "surface.default", "ui"),
    ("focus.ring-on-brand", "surface.brand", "ui"),
    ("action.primary-fg", "action.primary-bg", "text"), ("action.primary-fg", "action.primary-bg-hover", "text"),
    ("action.primary-fg", "action.primary-bg-pressed", "text"), ("action.secondary-fg", "action.secondary-bg", "text"),
    ("action.secondary-fg", "action.secondary-bg-hover", "text"), ("action.secondary-fg", "action.secondary-bg-pressed", "text"),
    ("text.on-code", "surface.code", "text"), ("status.free", "surface.raised", "text"), ("status.full", "surface.raised", "text"),
    ("task.drive-fg", "task.drive-bg", "text"), ("task.walk-fg", "task.walk-bg", "text"),
    ("task.pay-fg", "task.pay-bg", "text"),
    ("status.free", "surface.default", "text"), ("status.full", "surface.default", "text"),
    ("status.closed", "surface.default", "text"),
    ("feedback.error", "surface.default", "text"), ("feedback.error", "feedback.error-bg", "text"),
    ("feedback.success", "surface.default", "text"), ("feedback.warning", "surface.default", "text"),
    ("feedback.info", "surface.default", "text"),
]

# ---------------------------------------------------------------- other families
SPACE = [("0", 0), ("1", 4), ("2", 8), ("3", 12), ("4", 16), ("5", 24), ("6", 32), ("7", 48), ("8", 64), ("9", 96), ("10", 128)]
RADIUS = [("none", 0, "Signage panels, photos in layouts."), ("s", 4, "Tags, small chips."),
          ("m", 8, "Inputs, small cards."), ("l", 16, "Cards, sheets, dialogs."),
          ("xl", 24, "Phone sheets, large media."), ("pill", 999, "Buttons, chips, route boards.")]
SHADOW = [("1", "0 1 2 0 0.08", "Hairline lift: inputs on subtle surfaces."),
          ("2", "0 6 18 0 0.10", "Cards."),
          ("3", "0 16 40 0 0.16", "Sheets, dialogs, menus.")]
DURATION = [("instant", 0, "No movement."), ("reduced", 120, "The fade that replaces motion under prefers-reduced-motion (D19)."), ("fast", 120, "Hover, press, small state changes."),
            ("moderate", 200, "Expand, collapse, sheet in."), ("slow", 320, "Page level changes."),
            ("expressive", 600, "The bubble: brand moments in reels and splash only.")]
EASING = [("standard", [0.2, 0, 0, 1], "Default for UI movement."),
          ("enter", [0, 0, 0, 1], "Elements entering."),
          ("exit", [0.3, 0, 1, 1], "Elements leaving."),
          ("bubble", [0.34, 1.3, 0.64, 1], "The bubble pop (slight overshoot), expressive only.")]

FONT_STACK = ["Ubuntu Sans", "Ubuntu", "system-ui", "-apple-system", "Segoe UI", "Roboto", "Arial", "sans-serif"]
# name: size px, line height px, weight, letter spacing em, width axis, numeric
TYPE_SCREEN = [
    ("display-xl", 64, 68, 800, -0.01, 100, False),
    ("display-l", 48, 52, 800, -0.01, 100, False),
    ("heading-xl", 40, 44, 700, -0.005, 100, False),
    ("heading-l", 32, 38, 700, 0, 100, False),
    ("heading-m", 24, 30, 700, 0, 100, False),
    ("heading-s", 20, 26, 700, 0, 100, False),
    ("body-l", 18, 28, 400, 0, 100, False),
    ("body-m", 16, 24, 400, 0, 100, False),
    ("body-s", 14, 20, 400, 0, 100, False),
    ("label-l", 16, 24, 600, 0, 100, False),
    ("label-m", 14, 20, 600, 0.01, 100, False),
    ("label-s", 12, 16, 600, 0.02, 100, False),
    ("numeric-xl", 56, 60, 800, 0, 100, True),
    ("numeric-m", 20, 26, 700, 0, 100, True),
]
TYPE_PRINT = [  # pt, leading pt
    ("print-display", 48, 50, 800), ("print-h1", 32, 36, 700), ("print-h2", 22, 26, 700),
    ("print-h3", 15, 19, 700), ("print-body", 10, 14, 400), ("print-small", 8, 11, 400),
    ("print-legal", 7, 9, 400),
]


def hex_to_rgb01(h):
    h = h.lstrip("#")
    return [round(int(h[i:i + 2], 16) / 255, 4) for i in (0, 2, 4)]


def lum(h):
    c = [int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def resolve(ref):
    s, k = ref.split(".")
    return PRIMITIVES[s][k]


def color_value(h):
    return {"colorSpace": "srgb", "components": hex_to_rgb01(h), "hex": h.lower()}


def build():
    os.makedirs(OUT, exist_ok=True)
    tokens = {
        "$description": "ParkingYou 2027 design tokens. Source: brand-2027/02-build/core-spec.md. Generated by brand-2027/tools/build_tokens.py; do not edit by hand.",
        "color": {},
        "semantic": {},
    }
    # primitives
    for scale, steps in PRIMITIVES.items():
        grp = {"$type": "color"}
        for step, hx in steps.items():
            t = {"$value": color_value(hx)}
            prod = PRODUCTION.get((scale, step))
            if prod:
                t["$description"] = prod["name"]
                t["$extensions"] = {"nl.parkingyou.production": {
                    "cmyk": prod["cmyk"], "ral": prod["ral"], "ralMatch": prod["ralMatch"],
                    "pantone": prod["pantone"], "vinyl": prod["vinyl"]}}
            elif (scale, step) in TINT_CMYK:
                t["$extensions"] = {"nl.parkingyou.production": {"cmyk": TINT_CMYK[(scale, step)], "use": "print tint"}}
            grp[step] = t
        tokens["color"][scale] = grp
    # semantic colour
    for group, items in SEMANTIC.items():
        grp = {"$type": "color"}
        for name, (light, dark, desc) in items.items():
            grp[name] = {"$value": "{color.%s}" % light, "$description": desc,
                         "$extensions": {"nl.parkingyou.modes": {"dark": "{color.%s}" % dark}}}
        tokens["semantic"][group] = grp
    # component tier
    comp = {}
    for c, items in COMPONENT.items():
        grp = {"$type": "color"}
        for name, ref in items.items():
            grp[name] = {"$value": "{semantic.%s}" % ref}
        comp[c] = grp
    comp["size"] = {"$type": "dimension", **{k: {"$value": {"value": v, "unit": "px"}} for k, v in COMPONENT_SIZE.items()}}
    tokens["component"] = comp
    # verloop
    tokens["gradient"] = {"verloop": {
        "$type": "gradient",
        "$deprecated": "Retired in v2 (D31): no gradients. Kept only to document the old handbook verloop.",
        "$description": "Marketing only (screen headers, printed posters and panels). Never in wayfinding, cut vinyl, powder coat or lightbox film. Text only on the navy part (0 to 45 percent).",
        "$value": [{"color": "{color.blue.700}", "position": 0}, {"color": "{color.blue.700}", "position": 0.45},
                   {"color": "{color.aqua.500}", "position": 1}],
        "$extensions": {"nl.parkingyou.gradient": {"angleDeg": 135, "fallback": "{color.blue.700}"}}}}
    # dimension families
    tokens["space"] = {"$type": "dimension", **{k: {"$value": {"value": v, "unit": "px"}} for k, v in SPACE}}
    tokens["radius"] = {"$type": "dimension", **{k: {"$value": {"value": v, "unit": "px"}, "$description": d} for k, v, d in RADIUS}}
    tokens["shadow"] = {"$type": "shadow"}
    for k, spec, d in SHADOW:
        x, y, blur, spread, alpha = spec.split()
        tokens["shadow"][k] = {"$description": d, "$value": {
            "color": {"colorSpace": "srgb", "components": hex_to_rgb01("#0D142E"), "alpha": float(alpha), "hex": "#0d142e"},
            "offsetX": {"value": int(x), "unit": "px"}, "offsetY": {"value": int(y), "unit": "px"},
            "blur": {"value": int(blur), "unit": "px"}, "spread": {"value": int(spread), "unit": "px"}}}
    tokens["duration"] = {"$type": "duration", **{k: {"$value": {"value": v, "unit": "ms"}, "$description": d} for k, v, d in DURATION}}
    tokens["easing"] = {"$type": "cubicBezier", **{k: {"$value": v, "$description": d} for k, v, d in EASING}}
    # typography
    tokens["font"] = {
        "family": {"$type": "fontFamily", "sans": {"$value": FONT_STACK, "$description": "Ubuntu Sans, variable (wdth 75 to 100, wght 100 to 800), Ubuntu Font Licence 1.0, free."},
                   "logo": {"$value": ["Ubuntu"], "$description": "Wordmark only, always as outlines from the logo files."}},
        "weight": {"$type": "fontWeight", "regular": {"$value": 400}, "medium": {"$value": 500},
                   "semibold": {"$value": 600}, "bold": {"$value": 700}, "extrabold": {"$value": 800}},
    }
    typo = {"$type": "typography"}
    for name, size, lh, wt, ls, wd, num in TYPE_SCREEN:
        t = {"$value": {"fontFamily": "{font.family.sans}", "fontSize": {"value": size, "unit": "px"},
                        "fontWeight": wt, "letterSpacing": {"value": round(ls * size, 2), "unit": "px"},
                        "lineHeight": round(lh / size, 4)}}
        ext = {"wdth": wd}
        if num:
            ext["fontVariantNumeric"] = "tabular-nums"
        t["$extensions"] = {"nl.parkingyou.type": ext}
        typo[name] = t
    for name, size, lead, wt in TYPE_PRINT:
        typo[name] = {"$value": {"fontFamily": "{font.family.sans}", "fontSize": {"value": size, "unit": "px"},
                                 "fontWeight": wt, "letterSpacing": {"value": 0, "unit": "px"},
                                 "lineHeight": round(lead / size, 4)},
                      "$description": "Print: fontSize is in pt (DTCG has no pt unit; value carries pt).",
                      "$extensions": {"nl.parkingyou.type": {"unit": "pt"}}}
    tokens["typography"] = typo
    # signage cap height rule
    tokens["signage"] = {
        "$description": "Signage legibility: cap height 10 mm per metre reading distance. Ubuntu Sans cap height is 0.693 em, so font size in mm = cap height / 0.693.",
        "cap-height-mm-per-metre": {"$type": "number", "$value": 10,
                                    "$description": "Millimetres of cap height per metre of reading distance."},
        "cap-height-ratio": {"$type": "number", "$value": 0.693},
    }
    with open(os.path.join(OUT, "tokens.json"), "w") as f:
        json.dump(tokens, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # CSS
    def var(group, name):
        return "--py-%s-%s" % (group, name)
    lines = ["/* ParkingYou 2027 tokens. Generated by brand-2027/tools/build_tokens.py from core-spec.md; do not edit by hand. */",
             "@font-face { font-family: 'Ubuntu Sans'; src: url('../fonts/UbuntuSans[wdth,wght].ttf') format('truetype'); font-weight: 100 800; font-stretch: 75% 100%; font-style: normal; }",
             ":root {"]
    for scale, steps in PRIMITIVES.items():
        for step, hx in steps.items():
            lines.append("  --py-color-%s-%s: %s;" % (scale, step, hx))
    for group, items in SEMANTIC.items():
        for name, (light, dark, desc) in items.items():
            lines.append("  %s: var(--py-color-%s);" % (var(group, name), light.replace(".", "-")))
    for k, v in SPACE:
        lines.append("  --py-space-%s: %dpx;" % (k, v))
    for k, v, d in RADIUS:
        lines.append("  --py-radius-%s: %dpx;" % (k, v))
    for k, spec, d in SHADOW:
        x, y, blur, spread, alpha = spec.split()
        lines.append("  --py-shadow-%s: %spx %spx %spx %spx rgba(13, 20, 46, %s);" % (k, x, y, blur, spread, alpha))
    for k, v, d in DURATION:
        lines.append("  --py-duration-%s: %dms;" % (k, v))
    for k, v, d in EASING:
        lines.append("  --py-easing-%s: cubic-bezier(%s);" % (k, ", ".join(str(x) for x in v)))
    lines.append("  --py-font-sans: %s;" % ", ".join("'%s'" % f if " " in f else f for f in FONT_STACK))
    for name, size, lh, wt, ls, wd, num in TYPE_SCREEN:
        lines.append("  --py-type-%s: %d %dpx/%dpx var(--py-font-sans);" % (name, wt, size, lh))
    for c, items in COMPONENT.items():
        for name, ref in items.items():
            g, n = ref.split(".", 1)
            lines.append("  --py-%s-%s: var(--py-%s-%s);" % (c, name.replace(".", "-"), g, n))
    for k, v in COMPONENT_SIZE.items():
        lines.append("  --py-size-%s: %dpx;" % (k, v))
    lines.append("}")
    lines.append("[data-theme=\"dark\"] {")
    for group, items in SEMANTIC.items():
        for name, (light, dark, desc) in items.items():
            lines.append("  %s: var(--py-color-%s);" % (var(group, name), dark.replace(".", "-")))
    lines.append("}")
    lines.append("@media (prefers-reduced-motion: reduce) { :root { --py-duration-moderate: 0ms; --py-duration-slow: 0ms; --py-duration-expressive: 0ms; } }  /* fast and reduced stay: a 120 ms fade replaces movement */")
    with open(os.path.join(OUT, "tokens.css"), "w") as f:
        f.write("\n".join(lines) + "\n")

    # contrast table
    rows = ["# Contrast table (computed)", "",
            "WCAG 2.x relative luminance. Text pairs need 4.5:1, UI and large text 3:1. Generated by build_tokens.py.", "",
            "| Foreground | Background | Light | Dark | Need | Result |", "|---|---|---|---|---|---|"]
    fails = 0
    for fg, bg, kind in PAIRS:
        g1, n1 = fg.split(".", 1)
        g2, n2 = bg.split(".", 1)
        lf, df = SEMANTIC[g1][n1][0], SEMANTIC[g1][n1][1]
        lb, db = SEMANTIC[g2][n2][0], SEMANTIC[g2][n2][1]
        cl = contrast(resolve(lf), resolve(lb))
        cd = contrast(resolve(df), resolve(db))
        need = 4.5 if kind == "text" else 3.0
        ok = cl >= need and cd >= need
        fails += 0 if ok else 1
        rows.append("| %s | %s | %.2f:1 | %.2f:1 | %.1f:1 | %s |" % (fg, bg, cl, cd, need, "pass" if ok else "FAIL"))
    rows += ["", "## Brand pairs used on print and signage", "", "| Pair | Ratio | Use |", "|---|---|---|"]
    for a, b, use in [("#FFFFFF", "#1A3580", "white on PY-Blauw: all signage text"),
                      ("#1A3580", "#32B9CD", "PY-Blauw on PY-Aqua: walk signs, aqua bubble"),
                      ("#0D142E", "#F08300", "PY-Diep on PY-Oranje: payment signs in the garage only"),
                      ("#1A3580", "#FFFFFF", "PY-Blauw on white: print text"),
                      ("#FFFFFF", "#32B9CD", "white on PY-Aqua: NOT allowed"),
                      ("#FFFFFF", "#F08300", "white on PY-Oranje: NOT allowed"),
                      ("#1A3580", "#F08300", "PY-Blauw on PY-Oranje: large text only (24 px or 19 px bold and up)")]:
        rows.append("| %s on %s | %.2f:1 | %s |" % (a, b, contrast(a, b), use))
    with open(os.path.join(OUT, "contrast.md"), "w") as f:
        f.write("\n".join(rows) + "\n")
    return fails


if __name__ == "__main__":
    n = build()
    print("tokens built; failing pairs:", n)
