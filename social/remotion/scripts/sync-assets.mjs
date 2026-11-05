// Copies the brand library (svg/, fonts/, tokens.json) from the repo root into public/py,
// so compositions load the same files the print templates use. public/py is git-ignored.
import { cpSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
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
}
console.log("synced svg/, fonts/ and tokens.json to public/py (+ open reverse logos in public/py/derived)");
