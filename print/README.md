# Print files

Print-ready files made from the library designs. Page = trim + 3 mm bleed at 1:1, TrimBox set, text outlined (Ubuntu), fills as CMYK from the brand values in `tokens.json`
(PY-Blauw 100/83/0/17, PY-Aqua 69/0/21/0, white 0/0/0/0).

| File | What |
|---|---|
| `zuil-abonnees-790x1400-wit-druk.pdf` / `.svg` | Face of the subscribers column, white with blue bars, trim 790 x 1400 mm |
| `zuil-abonnees-790x1400-blauw-druk.pdf` / `.svg` | Same, PY-Blauw with aqua bars |

The foot plate is not part of the print file. `Locatienaam` is a placeholder: change the `location-name` text in the SVG (live text, variable `location name`) and run
`python3 -I tools/make_print_pdf.py print/<file>.svg` to make a new PDF. The SVGs are built by `tools/build_zuil.py`.
