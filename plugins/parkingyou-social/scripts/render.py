#!/usr/bin/env python3
"""Render one or more post specs: validate, check copy and facts, render every format, check the brand, write qa.json.

Usage:
  python3 render.py <spec.json> [<spec.json> ...] [--date YYYY-MM-DD] [--out DIR] [--no-render]

Each spec gets its own folder social/posts/<date>-<id>-<slug>/ (or DIR/<id>-<slug> with --out) holding
spec.json, facts.json (copied when it sits next to the source spec), the PNGs, caption.md and qa.json.
A blocking finding before the render skips the render; a blocking finding after it marks the post "blocked".
Exit status: 0 = every post passed (warnings allowed), 1 = at least one post is blocked, 2 = usage error.
"""
from __future__ import annotations

import argparse
import datetime as dt
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_copy  # noqa: E402
from common import REMOTION, SCHEMA, Finding, archetypes, load_json, plain, post_dir_for, write_json  # noqa: E402

BUILT_THEMES = {"feed", "2027"}


def validate(spec: dict) -> list[Finding]:
    out: list[Finding] = []
    try:
        import jsonschema  # optional

        v = jsonschema.Draft202012Validator(load_json(SCHEMA / "post-spec.schema.json"))
        for e in v.iter_errors(spec):
            out.append(Finding("schema", "block", "/".join(map(str, e.path)) or "spec", e.message))
    except ImportError:
        for key in ("id", "archetype", "theme", "formats", "ground", "slots", "caption", "alt"):
            if key not in spec:
                out.append(Finding("schema", "block", key, "missing"))
    if out:
        return out

    a = archetypes()
    arch = a["archetypes"].get(spec["archetype"])
    if not arch:
        return [Finding("schema", "block", "archetype", f'unknown archetype "{spec["archetype"]}"')]
    if arch.get("status") != "built":
        out.append(Finding("schema", "block", "archetype", f'archetype "{spec["archetype"]}" is not built yet'))
    if spec["theme"] not in BUILT_THEMES:
        out.append(Finding("schema", "block", "theme", f'theme "{spec["theme"]}" is not built yet'))
    if spec["ground"] not in arch["grounds"].get(spec["theme"], []):
        out.append(Finding("schema", "block", "ground", f'ground "{spec["ground"]}" is not allowed for {spec["archetype"]} in theme {spec["theme"]} (allowed: {arch["grounds"].get(spec["theme"])})'))
    for f in spec["formats"]:
        if f not in arch["formats"]:
            out.append(Finding("schema", "block", "formats", f'format "{f}" is not available for {spec["archetype"]} (available: {arch["formats"]})'))

    slots = spec["slots"]
    for name, rule in arch["slots"].items():
        value = slots.get(name)
        if value in (None, "", []):
            if rule.get("required"):
                out.append(Finding("schema", "block", f"slots.{name}", "required slot is empty"))
            continue
        if isinstance(value, str):
            n = len(plain(value))
            if rule.get("max_chars") and n > rule["max_chars"]:
                out.append(Finding("schema", "block", f"slots.{name}", f"{n} characters, limit {rule['max_chars']}"))
            lines = value.count("\n") + 1
            if rule.get("max_lines") and lines > rule["max_lines"]:
                out.append(Finding("schema", "block", f"slots.{name}", f"{lines} lines, limit {rule['max_lines']}"))
        if isinstance(value, list):
            if rule.get("max_items") and len(value) > rule["max_items"]:
                out.append(Finding("schema", "block", f"slots.{name}", f"{len(value)} items, limit {rule['max_items']}"))
            if rule.get("min_items") and len(value) < rule["min_items"]:
                out.append(Finding("schema", "block", f"slots.{name}", f"{len(value)} items, at least {rule['min_items']}"))
    for name in slots:
        if name not in arch["slots"]:
            out.append(Finding("schema", "warn", f"slots.{name}", f"slot is not used by {spec['archetype']} and will not appear"))
    return out


def run_optional(module: str, *args) -> list[Finding]:
    """Checks that arrive in phase 3 (check_facts, check_brand) report as info until they exist."""
    try:
        mod = __import__(module)
    except ImportError:
        return [Finding(module.replace("check_", ""), "info", "-", f"{module}.py is not built yet (phase 3)")]
    return mod.check(*args)


def render(dirs: list[Path]) -> dict[Path, str]:
    if not (REMOTION / "node_modules").exists():
        subprocess.run(["npm", "ci", "--no-audit", "--no-fund"], cwd=REMOTION, check=True)
    subprocess.run(["node", "scripts/sync-assets.mjs"], cwd=REMOTION, check=True, capture_output=True)
    p = subprocess.run(["node", "scripts/render-spec.mjs", *map(str, dirs)], cwd=REMOTION, capture_output=True, text=True)
    errors: dict[Path, str] = {}
    for line in (p.stdout + p.stderr).splitlines():
        if line.startswith("FAILED"):
            for d in dirs:
                spec_id = load_json(d / "spec.json")["id"]
                if line.startswith(f"FAILED {spec_id} "):
                    errors[d] = errors.get(d, "") + line + "\n"
    if p.returncode and not errors:
        errors = {d: p.stderr[-2000:] for d in dirs}
    return errors


def caption_md(spec: dict) -> str:
    tags = " ".join(spec.get("hashtags", []))
    parts = [f"# {spec['id']} {plain(spec['slots'].get('headline', ''))}", "", "## Caption", "", spec["caption"]]
    if tags and tags not in spec["caption"]:
        parts += ["", tags]
    parts += ["", "## Alt text", "", spec["alt"]]
    if spec.get("linkedin_caption"):
        parts += ["", "## LinkedIn", "", spec["linkedin_caption"]]
    return "\n".join(parts) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("specs", nargs="+", type=Path)
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--out", type=Path, help="write post folders here instead of social/posts/")
    ap.add_argument("--no-render", action="store_true", help="only run the checks that need no render")
    a = ap.parse_args(argv)

    jobs = []
    for src in a.specs:
        spec = load_json(src)
        d = post_dir_for(spec, a.date)
        if a.out:
            d = a.out / d.name.split("-", 3)[-1]
        d.mkdir(parents=True, exist_ok=True)
        if src.resolve() != (d / "spec.json").resolve():
            shutil.copyfile(src, d / "spec.json")
        if (src.parent / "facts.json").exists() and src.parent.resolve() != d.resolve():
            shutil.copyfile(src.parent / "facts.json", d / "facts.json")
        findings = validate(spec)
        findings += check_copy.check(spec)
        if not any(f.check == "schema" and f.severity == "block" for f in findings):
            facts = load_json(d / "facts.json") if (d / "facts.json").exists() else None
            findings += run_optional("check_facts", spec, facts)
        jobs.append((d, spec, findings))

    to_render = [d for d, _, f in jobs if not any(x.severity == "block" for x in f)]
    errors = {} if a.no_render or not to_render else render(to_render)

    blocked_any = False
    for d, spec, findings in jobs:
        if d in errors:
            findings.append(Finding("render", "block", "render", errors[d].strip()))
        elif d in to_render and not a.no_render:
            findings += run_optional("check_brand", spec, d)
        status = "blocked" if any(f.severity == "block" for f in findings) else "warn" if any(f.severity == "warn" for f in findings) else "pass"
        blocked_any |= status == "blocked"
        (d / "caption.md").write_text(caption_md(spec), encoding="utf-8")
        write_json(d / "qa.json", {"id": spec["id"], "date": a.date, "status": status, "rendered": d in to_render and not a.no_render and d not in errors, "findings": [f.as_dict() for f in findings]})
        print(f"{status.upper():8} {spec['id']}  {d}")
        for f in findings:
            if f.severity != "info":
                print(f"         {f.severity:5} {f.check}/{f.where}: {f.message}")
    return 1 if blocked_any else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
