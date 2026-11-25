// Renders the location spots (LocatieSpot, 1920x1080, 60 fps) to out/locaties/<slug>.mp4.
// node scripts/render-locaties.mjs            all locations
// node scripts/render-locaties.mjs plantage   one or more slugs
import {bundle} from '@remotion/bundler';
import {getCompositions, renderMedia} from '@remotion/renderer';
import {existsSync, mkdirSync, readdirSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..');
const wanted = process.argv.slice(2);

let browserExecutable = process.env.BROWSER_EXECUTABLE ?? null;
if (!browserExecutable && existsSync('/opt/pw-browsers')) {
  const dir = readdirSync('/opt/pw-browsers').find((d) => d.startsWith('chromium-'));
  if (dir) browserExecutable = join('/opt/pw-browsers', dir, 'chrome-linux64', 'chrome');
}

const outDir = join(root, 'out', 'locaties');
mkdirSync(outDir, {recursive: true});
const serveUrl = await bundle({entryPoint: join(root, 'src', 'index.ts'), publicDir: join(root, 'public')});
const comps = (await getCompositions(serveUrl, {browserExecutable})).filter(
  (c) => c.id.startsWith('Spot-') && (!wanted.length || wanted.includes(c.id.slice(5))),
);

for (const composition of comps) {
  const slug = composition.id.slice(5);
  const outputLocation = join(outDir, `${slug}.mp4`);
  await renderMedia({
    composition,
    serveUrl,
    codec: 'h264',
    crf: 20,
    outputLocation,
    browserExecutable,
    chromiumOptions: {gl: 'swangle'},
    onProgress: () => {},
  });
  console.log(`\n-> ${outputLocation}`);
}
