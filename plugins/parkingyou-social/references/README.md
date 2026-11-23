# References

The single set of rules for the ParkingYou social plugin. Skills load these files; templates and scripts read the same values from the library and the kennisbank.

| File | What | Read when |
|---|---|---|
| `decisions.md` | Settled conflicts (S1 to S12) and open points | Before anything else; cite an ID when a rule depends on it |
| `brand-visual.md` | Colour roles, contrast, logo, type, elements, layout and do/don't, for theme `feed` and theme `2027` | Designing or reviewing a visual |
| `brand-voice.md` | Tone, rules, words, good and bad lines, caption shape | Writing a headline, caption or alt text |
| `product-truth.md` | How to fetch facts from the kennisbank, the stable facts, and what never to claim | Any post with a price, place, count or facility |
| `copy-rules.txt` | Machine-readable `regex || reason` rules for `check_copy.py` (`WARN:` = warning) | Run by QA; edit when a rule changes |
| `pillars-and-angles.md` | The 7 pillars, audiences, angles with example hooks and item IDs, picking rules | Coming up with a post or a plan |
| `platform-specs.md` | Canvas sizes, safe zones, caption limits, carousel and video rules, UTM | Choosing formats and checking layouts |

Sources stay where they are: `tokens.json`, `elements.json`, `svg/`, `docs/print-rules.md`, `social/instagram/`, `social/remotion/` and `brand-2027/`.
These files cite them; they do not replace them. When a source changes, update the rule here and, if it settles a conflict, add a row to `decisions.md`.

`social/instagram/brand-parkingyou.md` and §7 and §8 of `social/instagram/strategy.md` are superseded by these files for production rules.
