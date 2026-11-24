"""Shared helpers for the ParkingYou social plugin scripts (stdlib only)."""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent
REPO = PLUGIN.parent.parent
REMOTION = REPO / "social" / "remotion"
POSTS = REPO / "social" / "posts"
REFS = PLUGIN / "references"
SCHEMA = PLUGIN / "schema"


@dataclass
class Finding:
    check: str          # schema | copy | facts | brand | render
    severity: str       # block | warn | info
    where: str          # slot, caption, alt, format, file
    message: str
    rule: str = ""

    def as_dict(self) -> dict:
        return asdict(self)


def load_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def archetypes() -> dict:
    return load_json(SCHEMA / "archetypes.json")


def plain(text: str) -> str:
    """Visible text of a rich string: no *key* markers, line breaks as spaces."""
    return re.sub(r"\s*\n\s*", " ", text.replace("*", "")).strip()


def texts_of(spec: dict) -> list[tuple[str, str]]:
    """Every piece of copy in a spec as (where, text): slots (recursively), caption, alt, LinkedIn caption."""
    out: list[tuple[str, str]] = []

    def walk(value, where):
        if isinstance(value, str):
            out.append((where, value))
        elif isinstance(value, dict):
            for k, v in value.items():
                if k in {"code", "icon", "illustration", "src", "type", "figure"}:
                    continue  # IDs and paths, not copy
                walk(v, f"{where}.{k}")
        elif isinstance(value, list):
            for i, v in enumerate(value):
                walk(v, f"{where}[{i}]")

    for name, value in spec.get("slots", {}).items():
        if name in {"cta", "figure"}:
            continue
        walk(value, f"slots.{name}")
    for key in ("caption", "alt", "linkedin_caption"):
        if spec.get(key):
            out.append((key, spec[key]))
    return out


def post_dir_for(spec: dict, date: str) -> Path:
    slug = spec.get("slug")
    if not slug:
        text = unicodedata.normalize("NFKD", plain(spec["slots"].get("headline", spec["id"]))).encode("ascii", "ignore").decode()
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:50].strip("-")
    return POSTS / f"{date}-{spec['id']}-{slug}"


def write_json(path: Path, data) -> None:
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
