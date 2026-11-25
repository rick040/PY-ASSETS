# ParkingYou brand 2027

The 2027 refresh of the ParkingYou identity: research, the approved direction, the guideline and the design tokens. Everything new lives in this folder; no existing file in the repository was changed or removed.

## Deliverables

| What | Where |
|---|---|
| Full guideline (Dutch, 14 chapters, 100 figures) | Docs: https://claude.ai/artifact/NrNDkQnCPs7eJNxJPLVGEr · source: `03-guide/volledig/ParkingYou-huisstijl-2027.md` |
| Short guideline (PDF, 16 pages) | `03-guide/kort/ParkingYou-huisstijl-2027-kort.pdf` |
| One-page summary | Docs: https://claude.ai/artifact/FoWMf5K2Z8yjhJCH79ujkn · `03-guide/samenvatting.md` |
| Design System "ParkingYou 2027" | https://claude.ai/artifact/BtHiMUGNLmPHxmoX4qAAth |
| Key mockups (entrance sign, booking screen, social post, subscription card, business card) | https://claude.ai/artifact/Fxwo8aj5LgyP7myJw25UBA |
| Core spec, single source of truth with decision log D1 to D48 | `02-build/core-spec.md` |
| Design tokens (W3C DTCG 2025.10), CSS and contrast table | `tokens/tokens.json`, `tokens/tokens.css`, `tokens/contrast.md` |

The artifacts are private until shared from their Share menu.

## Folders

| Folder | Content |
|---|---|
| `00-intake/` | Brief every workstream received |
| `01-research/` | Research R1 to R5 and the three directions |
| `02-build/` | Core spec, chapter sources (`<NN>/chapter.md`) and figures (`figures/*.html` and `.png`), the figure kit (`kit/`: logos, parkeerders, stem, bubble, arrows, photos) |
| `03-guide/` | Assembled guideline, short PDF, summary, appendix |
| `tokens/` | Generated tokens; do not edit by hand |
| `tools/` | Generators and renderers |
| `fonts/` | Ubuntu Sans (Ubuntu Font Licence, free) |

## Rebuild

```
python3 -I brand-2027/tools/build_tokens.py          # tokens.json, tokens.css, contrast.md
node brand-2027/tools/render.mjs brand-2027/02-build/<NN-name>/figures/   # figures to PNG
python3 -I brand-2027/tools/assemble_guide.py        # full guideline markdown
python3 -I brand-2027/tools/build_short_guide.py     # short PDF
```
