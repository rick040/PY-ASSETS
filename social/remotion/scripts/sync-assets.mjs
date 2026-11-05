// Copies the brand library (svg/, fonts/, tokens.json) from the repo root into public/py,
// so compositions load the same files the print templates use. public/py is git-ignored.
import { cpSync, mkdirSync, rmSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const repo = resolve(here, "../../..");
const out = resolve(here, "../public/py");
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
for (const dir of ["svg", "fonts"]) cpSync(resolve(repo, dir), resolve(out, dir), { recursive: true });
cpSync(resolve(repo, "tokens.json"), resolve(out, "tokens.json"));
console.log("synced svg/, fonts/ and tokens.json to public/py");
