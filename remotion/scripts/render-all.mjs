// Renders the three stories to remotion/out/*.mp4 (1080x1920, 30 fps).
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import {existsSync, mkdirSync, readdirSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..');
const ids = process.argv.slice(2).length ? process.argv.slice(2) : ['Story1-App', 'Story2-Shoppen', 'Story3-Tagline'];

// Use a pre-installed Chromium when there is one (cloud sandbox), else let Remotion download its own.
let browserExecutable = process.env.BROWSER_EXECUTABLE ?? null;
if (!browserExecutable && existsSync('/opt/pw-browsers')) {
  const dir = readdirSync('/opt/pw-browsers').find((d) => d.startsWith('chromium-'));
  if (dir) browserExecutable = join('/opt/pw-browsers', dir, 'chrome-linux64', 'chrome');
}

mkdirSync(join(root, 'out'), {recursive: true});
const serveUrl = await bundle({entryPoint: join(root, 'src', 'index.ts'), publicDir: join(root, 'public')});

for (const id of ids) {
  const composition = await selectComposition({serveUrl, id, browserExecutable});
  const outputLocation = join(root, 'out', `${id}.mp4`);
  await renderMedia({
    composition,
    serveUrl,
    codec: 'h264',
    outputLocation,
    browserExecutable,
    chromiumOptions: {gl: 'swangle', disableWebSecurity: false},
    onProgress: ({progress}) => process.stdout.write(`\r${id} ${(progress * 100).toFixed(0)}%`),
  });
  console.log(`\n-> ${outputLocation}`);
}
