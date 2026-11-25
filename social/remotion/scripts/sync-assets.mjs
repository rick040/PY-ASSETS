// Copies the brand library (svg/, fonts/, tokens.json) from the repo root into public/py,
// so compositions load the same files the print templates use. public/py is git-ignored.
import { cpSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const repo = resolve(here, "../../..");
const out = resolve(here, "../public/py");
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
for (const dir of ["svg", "fonts"]) cpSync(resolve(repo, dir), resolve(out, dir), { recursive: true });
cpSync(resolve(repo, "tokens.json"), resolve(out, "tokens.json"));
// Brand rule (Rick, 5 November 2026): the reverse logos are used with white and aqua only, never with the navy
// ring fill. The derived "-open" files drop the PY-Blauw fill, so the background shows through the ring.
mkdirSync(resolve(out, "derived"), { recursive: true });
for (const id of ["py-atom-logo-horizontal-reverse", "py-atom-logo-stacked-reverse", "py-atom-logo-beeldmerk-reverse"]) {
  const svg = readFileSync(resolve(repo, "svg/atom", `${id}.svg`), "utf8");
  const open = svg.replace(/fill="#1A3580"/gi, 'fill="none"');
  if (open === svg) throw new Error(`${id}: no PY-Blauw fill found, check the source`);
  writeFileSync(resolve(out, "derived", `${id}-open.svg`), open);
  // Brand rule (Rick, 6 November 2026): on light blue backgrounds the logo is all white with a white dot.
  // The library's white logo has a hole where the dot is, so this variant fills the dot white instead.
  const whiteDot = open.replace(/fill="#32B9CD"/gi, 'fill="#FFFFFF"');
  if (whiteDot === open) throw new Error(`${id}: no aqua dot found, check the source`);
  writeFileSync(resolve(out, "derived", `${id}-whitedot.svg`), whiteDot);
}
// The 2027 identity (brand-2027/): kit assets (logos incl. the navy one-colour version, de stem, de bubbel,
// de parkeerders with the beeldmerk head, angular arrows) and the Ubuntu Sans variable font, for the social theme "2027".
const b27 = resolve(repo, "brand-2027");
if (existsSync(b27)) {
  cpSync(resolve(b27, "02-build/kit/assets"), resolve(out, "2027/assets"), { recursive: true });
  cpSync(resolve(b27, "fonts"), resolve(out, "2027/fonts"), { recursive: true });
  // Own location photos from the 2027 kit (Philips Stadion, DLL garage, Evoluon, City Tower).
  cpSync(resolve(b27, "02-build/kit/photos"), resolve(out, "photos"), { recursive: true });
  cpSync(resolve(b27, "tokens/tokens.json"), resolve(out, "2027/tokens.json"));
}
console.log("synced svg/, fonts/, tokens.json and brand-2027 assets to public/py (+ open reverse logos in public/py/derived)");
