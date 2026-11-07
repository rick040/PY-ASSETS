# Figure kit

Every figure in the guideline is one HTML file rendered to PNG. Using this kit keeps all chapters in one visual voice.

## Folder per chapter

```
brand-2027/02-build/<NN-name>/
  chapter.md            the chapter text (Dutch)
  figures/<name>.html   one figure per file
  figures/<name>.png    rendered by the script (commit both)
```

## Writing a figure

- Start from `brand-2027/02-build/00-core/figures/bubble-anatomy.html` (copy its head).
- Link the kit: `<link rel="stylesheet" href="../../kit/kit.css">`. It loads the tokens (`var(--py-...)`), Ubuntu Sans and Ubuntu.
- One root element with class `fig` and a fixed `width` and `height` inline. Standard sizes: 1200 x 675 (wide), 1200 x 900, 1200 x 1200, or the real format.
- Only colours from the tokens (CSS variables `--py-color-*`, `--py-*` semantic) or the hex values in core-spec.md. Garage context background `#24272C` (class `fig--garage`) is allowed for mock-up surroundings only.
- Logos and pictograms: `<img src="../../kit/assets/<file>.svg">`. Never retype or redraw the logo. The bubble path is in `kit/assets/bubble.svg` (inline it as SVG when you need to colour it).
- Photos: ParkingYou's own location photos in `kit/photos/` (Philips Stadion, Evoluon, City Tower, DLL Garage). Do not use stock or AI images of real places.
- Captions and annotations inside a figure: class `note`, `eyebrow`, `do`, `dont`, `measure`, `measure-label`.
- Copy in figures: Dutch, real values where known, otherwise a placeholder in square brackets like `[prijs]`. No em dashes, no emoji.

## Rendering

```
node brand-2027/tools/render.mjs brand-2027/02-build/<NN-name>/figures/
```
Renders every `.html` in the folder to a `.png` beside it at 2x. Look at the PNG before you hand it in.
