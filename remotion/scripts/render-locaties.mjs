// Renders the location spots (LocatieSpot, 60 fps).
// node scripts/render-locaties.mjs                    all locations, 16:9 (1920x1080) to out/locaties/<slug>.mp4
// node scripts/render-locaties.mjs plantage           one or more slugs
// node scripts/render-locaties.mjs --reels [slugs]    9:16 reels (1080x1920) to out/reels/<slug>.mp4
// node scripts/render-locaties.mjs --zoek [slugs]     search spots, 9:16 to out/zoek/<slug>.mp4 and 16:9 to out/zoek-youtube/<slug>.mp4
import {bundle} from '@remotion/bundler';
import {getCompositions, renderMedia} from '@remotion/renderer';
import {existsSync, mkdirSync, readdirSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..');
const args = process.argv.slice(2);
const reels = args.includes('--reels');
const zoek = args.includes('--zoek');
const wanted = args.filter((a) => !a.startsWith('--'));
const prefixes = zoek ? ['Zoek-', 'ZoekYT-'] : [reels ? 'Reel-' : 'Spot-'];
const dirFor = (p) => ({'Spot-': 'locaties', 'Reel-': 'reels', 'Zoek-': 'zoek', 'ZoekYT-': 'zoek-youtube'})[p];

let browserExecutable = process.env.BROWSER_EXECUTABLE ?? null;
if (!browserExecutable && existsSync('/opt/pw-browsers')) {
  const dir = readdirSync('/opt/pw-browsers').find((d) => d.startsWith('chromium-'));
  if (dir) browserExecutable = join('/opt/pw-browsers', dir, 'chrome-linux64', 'chrome');
}

const serveUrl = await bundle({entryPoint: join(root, 'src', 'index.ts'), publicDir: join(root, 'public')});
const prefixOf = (id) => prefixes.find((p) => id.startsWith(p));
const comps = (await getCompositions(serveUrl, {browserExecutable})).filter(
  (c) => prefixOf(c.id) && (!wanted.length || wanted.includes(c.id.slice(prefixOf(c.id).length))),
);

for (const composition of comps) {
  const prefix = prefixOf(composition.id);
  const slug = composition.id.slice(prefix.length);
  const outDir = join(root, 'out', dirFor(prefix));
  mkdirSync(outDir, {recursive: true});
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
