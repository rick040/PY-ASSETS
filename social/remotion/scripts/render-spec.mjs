// Renders post specs (plugins/parkingyou-social) with the PY-Post composition, one bundle for the whole batch.
// For every format of every spec it writes, into the spec's folder:
//   <format>.png        1x, the upload file
//   <format>@2x.png     2x, for review
//   qa/<format>-bg.png  1x with all text hidden (check_brand.py reads the pixels behind the text)
//   qa/layout-<format>.json  boxes, colours and variants of every QA-tagged element
// Usage: node scripts/render-spec.mjs <post-dir> [<post-dir> ...]   (each dir holds spec.json)
// Browser: REMOTION_BROWSER, or the pre-installed headless shell in /opt/pw-browsers when present.
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");

const findBrowser = () => {
  if (process.env.REMOTION_BROWSER) return process.env.REMOTION_BROWSER;
  const base = "/opt/pw-browsers";
  if (!existsSync(base)) return undefined;
  for (const d of readdirSync(base).filter((n) => n.startsWith("chromium_headless_shell-"))) {
    const p = resolve(base, d, "chrome-headless-shell-linux64/chrome-headless-shell");
    if (existsSync(p)) return p;
  }
  return undefined;
};

const dirs = process.argv.slice(2);
if (!dirs.length) {
  console.error("usage: node scripts/render-spec.mjs <post-dir> [...]");
  process.exit(2);
}
const browserExecutable = findBrowser();
const serveUrl = await bundle({ entryPoint: resolve(root, "src/index.ts"), publicDir: resolve(root, "public"), rootDir: root });

let failed = 0;
for (const dir of dirs.map((d) => resolve(d))) {
  const spec = JSON.parse(readFileSync(resolve(dir, "spec.json"), "utf8"));
  mkdirSync(resolve(dir, "qa"), { recursive: true });
  const slides = spec.archetype === "carrousel" ? spec.slots.slides.map((_, i) => i) : [undefined];
  for (const format of spec.formats) {
    for (const slide of slides) {
      const tag = slide === undefined ? format : `${format}-${String(slide + 1).padStart(2, "0")}`;
      try {
        let layout = null;
        const onBrowserLog = (log) => {
          if (log.text.startsWith("PY_QA_LAYOUT ")) layout = JSON.parse(log.text.slice(13));
          else if (log.type === "error") console.error(`[${spec.id} ${tag}] ${log.text}`);
        };
        const inputProps = { spec, format, slide };
        const composition = await selectComposition({ serveUrl, id: "PY-Post", inputProps, browserExecutable, logLevel: "error" });
        const common = { serveUrl, composition, frame: 0, browserExecutable, imageFormat: "png", onBrowserLog, logLevel: "error" };
        await renderStill({ ...common, inputProps, output: resolve(dir, `${tag}.png`), scale: 1 });
        if (!layout) throw new Error("no QA layout logged");
        writeFileSync(resolve(dir, "qa", `layout-${tag}.json`), JSON.stringify({ format, slide: slide ?? null, width: composition.width, height: composition.height, elements: layout }, null, 1));
        if (!process.env.PY_NO_2X) await renderStill({ ...common, inputProps, output: resolve(dir, `${tag}@2x.png`), scale: 2 });
        // Remotion renders the props of the selected composition, so the text-hidden pass needs its own selection.
        const qaProps = { ...inputProps, hideText: true };
        const qaComposition = await selectComposition({ serveUrl, id: "PY-Post", inputProps: qaProps, browserExecutable, logLevel: "error" });
        await renderStill({ ...common, composition: qaComposition, inputProps: qaProps, output: resolve(dir, "qa", `${tag}-bg.png`), scale: 1 });
        console.log(`rendered ${spec.id} ${tag}`);
      } catch (e) {
        failed++;
        console.error(`FAILED ${spec.id} ${tag}: ${e.message}`);
      }
    }
  }
}
process.exit(failed ? 1 : 0);
