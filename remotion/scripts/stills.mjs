// Renders stills: node scripts/stills.mjs <outDir> <compositionId[,id...]|all> <frame> [<frame> ...]
// "all" renders every Spot-* composition.
import {bundle} from '@remotion/bundler';
import {getCompositions, renderStill, selectComposition} from '@remotion/renderer';
import {existsSync, mkdirSync, readdirSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..');
const [outDir, id, ...frames] = process.argv.slice(2);
let browserExecutable = process.env.BROWSER_EXECUTABLE ?? null;
if (!browserExecutable && existsSync('/opt/pw-browsers')) {
  const dir = readdirSync('/opt/pw-browsers').find((d) => d.startsWith('chromium-'));
  if (dir) browserExecutable = join('/opt/pw-browsers', dir, 'chrome-linux64', 'chrome');
}
mkdirSync(outDir, {recursive: true});
const serveUrl = await bundle({entryPoint: join(root, 'src', 'index.ts'), publicDir: join(root, 'public')});
const ids = id === 'all' ? null : id.split(',');
const list = ids ?? (await getCompositions(serveUrl, {browserExecutable})).map((c) => c.id).filter((c) => c.startsWith('Spot-'));
for (const cid of list) {
  const composition = await selectComposition({serveUrl, id: cid, browserExecutable});
  for (const f of frames) {
    const output = join(outDir, `${cid}_${String(f).padStart(3, '0')}.png`);
    await renderStill({composition, serveUrl, output, frame: Number(f), browserExecutable, chromiumOptions: {gl: 'swangle'}});
  }
  console.log(cid);
}
