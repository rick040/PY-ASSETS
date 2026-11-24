#!/usr/bin/env python3
"""Copy check: references/copy-rules.txt against every slot, the caption, the alt text and the LinkedIn caption.

Usage:  python3 check_copy.py <post-dir or spec.json> [...]
Exit 1 when a blocking rule matches. A rule whose reason starts with "WARN:" is a warning.
An approval in spec["approvals"] whose "what" text appears in the warning reason silences that warning.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import REFS, Finding, load_json, texts_of  # noqa: E402


def load_rules(path: Path = REFS / "copy-rules.txt"):
    rules = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if " || " not in line:
            raise ValueError(f"copy-rules.txt line {n}: missing ' || '")
        pattern, reason = line.split(" || ", 1)
        rules.append((re.compile(pattern, re.IGNORECASE), reason.strip(), n))
    return rules


def check(spec: dict, rules=None) -> list[Finding]:
    rules = rules or load_rules()
    approvals = [a.get("what", "").lower() for a in spec.get("approvals", [])]
    findings: list[Finding] = []
    for where, text in texts_of(spec):
        for rx, reason, line in rules:
            m = rx.search(text)
            if not m:
                continue
            warn = reason.startswith("WARN:")
            msg = reason[5:].strip() if warn else reason
            if warn and any(a and a in (m.group(0).lower() + " " + msg.lower()) for a in approvals):
                continue
            findings.append(Finding("copy", "warn" if warn else "block", where, f'"{m.group(0)}": {msg}', f"copy-rules.txt:{line}"))
    return findings


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    blocked = False
    for arg in argv:
        p = Path(arg)
        spec = load_json(p / "spec.json" if p.is_dir() else p)
        for f in check(spec):
            blocked |= f.severity == "block"
            print(f"{spec['id']}  {f.severity.upper():5}  {f.where}: {f.message}  [{f.rule}]")
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
