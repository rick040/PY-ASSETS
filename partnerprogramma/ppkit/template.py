"""Templates vullen: {velden}, tekstomslag (data-flow) en QR-codes (data-qr). Een template is een gewone SVG."""
import re
import xml.etree.ElementTree as ET
from . import brand, flow, qr

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
ET.register_namespace("xml", "http://www.w3.org/XML/1998/namespace")

FIELD = re.compile(r"\{([a-z_]+)\}")


def fill_fields(s, values):
    if s is None:
        return None

    def sub(m):
        k = m.group(1)
        if k not in values:
            raise KeyError(f"onbekend veld {{{k}}}")
        return str(values[k])

    return FIELD.sub(sub, s)


def _q(tag):
    return "{%s}%s" % (SVG, tag)


def _runs(el, values):
    base_face = flow._style_face(el.attrib, "regular")
    base = {"face": base_face, "fill": el.attrib.get("fill")}
    runs = []
    if el.text:
        runs.append((fill_fields(el.text, values), base))
    for ch in el:
        tag = ch.tag.split("}")[-1]
        if tag == "br":
            runs.append((None, None))
        elif tag == "tspan":
            st = {"face": flow._style_face(ch.attrib, base_face), "fill": ch.attrib.get("fill") or el.attrib.get("fill")}
            runs.append((fill_fields("".join(ch.itertext()), values), st))
        if ch.tail:
            runs.append((fill_fields(ch.tail, values), base))
    # lege woorden en regelovergangen in de bron-XML (inspringing) platslaan
    clean = []
    for t, st in runs:
        if t is not None:
            t = re.sub(r"[ \t]*\n[ \t]*", " ", t)
        clean.append((t, st))
    return clean, base


def process(svg, values):
    """Vul een template. Geeft (svg, info) met info per QR en per tekstblok."""
    root = ET.fromstring(svg.encode("utf-8"))
    info = {"qr": [], "flow": []}

    def walk(parent):
        for i, ch in enumerate(list(parent)):
            tag = ch.tag.split("}")[-1]
            if tag == "text" and "data-flow" in ch.attrib:
                frag, meta = _flow(ch, values)
                parent[i] = ET.fromstring(f'<g xmlns="{SVG}">{frag}</g>')
                info["flow"].append(meta)
            elif tag == "rect" and "data-qr" in ch.attrib:
                url = fill_fields(ch.attrib["data-qr"], values)
                qx, qy, qw = float(ch.attrib["x"]), float(ch.attrib["y"]), float(ch.attrib["width"])
                if "data-qr-center" in ch.attrib:   # plaat (code plus rustzone) gecentreerd om dit punt
                    cx, cy = map(float, ch.attrib["data-qr-center"].split())
                    qx, qy = cx - qw / 2, cy - qw / 2
                frag, meta = qr.draw(url, qx, qy, qw,
                                     fill=ch.attrib.get("fill", brand.BLAUW), plate=ch.attrib.get("data-qr-plate", brand.WIT))
                parent[i] = ET.fromstring(f'<g xmlns="{SVG}">{frag}</g>')
                info["qr"].append(meta)
            else:
                for k, v in list(ch.attrib.items()):
                    if "{" in v:
                        ch.attrib[k] = fill_fields(v, values)
                if tag in ("text", "tspan", "title"):
                    for node in ch.iter():
                        if node.text and "{" in node.text:
                            node.text = fill_fields(node.text, values)
                        if node.tail and "{" in node.tail:
                            node.tail = fill_fields(node.tail, values)
                walk(ch)

    walk(root)
    out = ET.tostring(root, encoding="unicode")
    left = FIELD.findall(re.sub(r"<[^>]*>", "", out))
    if left:
        raise KeyError(f"niet ingevulde velden: {left}")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + out, info


def _flow(el, values):
    spec = el.attrib["data-flow"].split()
    w, h = float(spec[0]), float(spec[1])
    def pt(v):   # "26" is punten, "120u" is eenheden van het vel
        return float(v[:-1]) / brand.PT if v.endswith("u") else float(v)
    max_pt = pt(spec[2]) if len(spec) > 2 else float(el.attrib.get("font-size", "10")) / brand.PT
    min_pt = pt(spec[3]) if len(spec) > 3 else max_pt
    lh = float(spec[4]) if len(spec) > 4 else 1.2
    ls = float(el.attrib.get("letter-spacing", 0))
    runs, base = _runs(el, values)
    pt_, lines = flow.fit(runs, w, h, max_pt, min_pt, lh, ls)
    size = pt_ * brand.PT
    x, y = float(el.attrib["x"]), float(el.attrib["y"])
    align = el.attrib.get("data-align", "start")
    va = el.attrib.get("data-valign")
    if va == "middle":
        y += (h - len(lines) * size * lh) / 2
    elif va == "bottom":
        y += h - len(lines) * size * lh
    frag = flow.render(lines, x, y, size, lh, el.attrib.get("fill", brand.ZWART), align, w, ls)
    return frag, dict(id=el.attrib.get("id"), pt=pt_, lines=len(lines), height=len(lines) * size * lh, box_h=h)
