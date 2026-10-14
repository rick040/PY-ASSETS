#!/usr/bin/env python3
"""Build SVGs for registered elements and optional QA sheets.

usage: python3 -I tools/run.py --src source/handbook.pdf [--ids REGEX] [--qa] [--out svg]
"""
import argparse, importlib, os, pkgutil, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from pyassets import Source  # noqa: E402
from pyassets import registry  # noqa: E402
from pyassets import qa  # noqa: E402


def load_specs(only=None):
    sd = os.path.join(HERE, "specs")
    sys.path.insert(0, sd)
    for m in sorted(pkgutil.iter_modules([sd]), key=lambda m: m.name):
        if only and not re.search(only, m.name):
            continue
        importlib.import_module(m.name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--ids", default=".*")
    ap.add_argument("--qa", action="store_true")
    ap.add_argument("--qa-dir", default=os.path.join(HERE, "..", "build", "qa"))
    ap.add_argument("--out", default=os.path.join(HERE, "..", "svg"))
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--spec", default=None, help="regex on spec module names; load only these (use while other specs are in progress)")
    a = ap.parse_args()
    load_specs(a.spec)
    src = Source(a.src)
    pat = re.compile(a.ids)
    n = 0
    for id_ in sorted(registry.BUILDERS):
        if not pat.search(id_):
            continue
        el = registry.build(src, id_)
        n += 1
        w, h = el.size_mm()
        warn = sum(1 for it in el.items if getattr(it, "clipped", False))
        print(f"{id_:55s} {len(el.items):4d} items  {w:7.1f} x {h:6.1f} mm  {el.status}" + (f"  CLIPPED:{warn}" if warn else ""))
        if not a.no_write:
            d = os.path.join(a.out, el.level)
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, id_ + ".svg"), "w", encoding="utf8") as f:
                f.write(el.svg())
        if a.qa:
            qa.compare(src, el, path=os.path.join(a.qa_dir, id_ + ".png"))
    print(n, "elements")


if __name__ == "__main__":
    main()
