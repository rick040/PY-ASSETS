// Renders every static post (compositions PY-POST-*) to renders/posts/<id>-<slug>.png with one bundle.
// Usage: node scripts/render-posts.mjs [browser-executable]
import { bundle } from "@remotion/bundler";
import { getCompositions, renderStill } from "@remotion/renderer";
import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const browserExecutable = process.argv[2] || process.env.REMOTION_BROWSER || undefined;
const out = resolve(root, "renders/posts");
mkdirSync(out, { recursive: true });
const serveUrl = await bundle({ entryPoint: resolve(root, "src/index.ts"), publicDir: resolve(root, "public"), rootDir: root });
const { POSTS, STILL_FRAME } = await import("../src/posts/meta.mjs");
const comps = (await getCompositions(serveUrl, { browserExecutable })).filter((c) => c.id.startsWith("PY-POST-"));
for (const composition of comps) {
  const id = composition.id.replace("PY-POST-", "");
  const output = resolve(out, `${id}-${POSTS[id]}.png`);
  await renderStill({ serveUrl, composition, frame: STILL_FRAME, output, browserExecutable, imageFormat: "png", scale: 1 });
  console.log("rendered", output);
}
