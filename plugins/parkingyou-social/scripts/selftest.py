#!/usr/bin/env python3
"""Self-test of the plugin: rules parse, every archetype has a fixture, every referenced element exists, and every
archetype renders in every format and both themes without a blocking copy or brand finding.

Usage:  python3 selftest.py [--quick] [--out DIR] [--sheet sheet.png]
--quick renders the feed format only. Exit 0 when everything passes.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_brand  # noqa: E402
import check_copy  # noqa: E402
from common import PLUGIN, REMOTION, REPO, archetypes, load_json  # noqa: E402

FIXTURES = PLUGIN / "tests" / "fixtures"


def element_exists(eid: str) -> bool:
    if eid.startswith("2027/"):
        return (REPO / "brand-2027/02-build/kit/assets" / f"{eid[5:]}.svg").exists()
    if eid.endswith("-open") or eid.endswith("-whitedot"):
        return (REPO / "svg/atom" / f"{eid.rsplit('-', 1)[0]}.svg").exists()
    level = eid.split("-")[1] if eid.count("-") > 1 else ""
    return (REPO / "svg" / level / f"{eid}.svg").exists() or (REPO / "applications" / eid).exists()


def static_checks() -> list[str]:
    errors = []
    try:
        n = len(check_copy.load_rules())
        print(f"ok   copy-rules.txt: {n} rules parse")
    except Exception as e:  # noqa: BLE001
        errors.append(f"copy-rules.txt: {e}")
    arch = archetypes()["archetypes"]
    for name, a in arch.items():
        if a.get("status") == "built" and not (FIXTURES / f"{name}.json").exists():
            errors.append(f"archetype {name} has no fixture in tests/fixtures/")
    ids = set()
    for f in list(FIXTURES.glob("*.json")) + list((PLUGIN / "references").glob("*.md")) + [REMOTION / "src/social/archetypes/index.tsx", REMOTION / "src/social/themes.ts", REMOTION / "src/social/kit.tsx"]:
        ids |= set(re.findall(r"py-(?:atom|comp|prod|app)-[a-z0-9]+(?:-[a-z0-9]+)*", f.read_text(encoding="utf-8")))
    for eid in sorted(ids):
        if eid.endswith("-") or eid in ("py-atom-figure",):
            continue
        if not element_exists(eid) and not any(element_exists(f"{eid}-{v}") for v in ("walk", "white")):
            errors.append(f"element {eid} does not exist in svg/")
    print(f"ok   {len(ids)} element IDs checked" if not any(e.startswith("element") for e in errors) else "FAIL element IDs")
    return errors


def render_matrix(out: Path, quick: bool) -> tuple[list[Path], list[str]]:
    arch = archetypes()["archetypes"]
    dirs, errors = [], []
    for f in sorted(FIXTURES.glob("*.json")):
        spec = load_json(f)
        a = arch[spec["archetype"]]
        for theme in ("feed", "2027"):
            s = dict(spec, theme=theme)
            if s["ground"] not in a["grounds"][theme]:
                s["ground"] = a["grounds"][theme][0]
            s["formats"] = ["feed"] if quick else a["formats"]
            d = out / f"{theme}-{spec['archetype']}"
            d.mkdir(parents=True, exist_ok=True)
            (d / "spec.json").write_text(json.dumps(s, ensure_ascii=False), encoding="utf-8")
            for fnd in check_copy.check(s):
                if fnd.severity == "block":
                    errors.append(f"{d.name}: copy {fnd.where}: {fnd.message}")
            dirs.append(d)
    subprocess.run(["node", "scripts/sync-assets.mjs"], cwd=REMOTION, check=True, capture_output=True)
    p = subprocess.run(["node", "scripts/render-spec.mjs", *map(str, dirs)], cwd=REMOTION, capture_output=True, text=True, env={**__import__("os").environ, "PY_NO_2X": "1"})
    errors += [ln for ln in (p.stdout + p.stderr).splitlines() if ln.startswith("FAILED")]
    for d in dirs:
        spec = load_json(d / "spec.json")
        for fnd in check_brand.check(spec, d):
            if fnd.severity == "block":
                errors.append(f"{d.name}: brand {fnd.where}: {fnd.message}")
    return dirs, errors


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--sheet", type=Path, help="also write a contact sheet of every render")
    a = ap.parse_args(argv)
    errors = static_checks()
    out = a.out or Path(tempfile.mkdtemp(prefix="py-social-selftest-"))
    dirs, render_errors = render_matrix(out, a.quick)
    errors += render_errors
    n_img = sum(len([p for p in d.glob("*.png") if "@2x" not in p.name]) for d in dirs)
    print(f"{'ok  ' if not render_errors else 'FAIL'} rendered {n_img} images from {len(dirs)} fixture/theme pairs into {out}")
    if a.sheet:
        import contact_sheet

        contact_sheet.build(dirs, a.sheet, None, 8)
        print(f"     sheet: {a.sheet}")
    for e in errors:
        print("  - " + e)
    print("SELFTEST " + ("PASSED" if not errors else f"FAILED ({len(errors)} problems)"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
