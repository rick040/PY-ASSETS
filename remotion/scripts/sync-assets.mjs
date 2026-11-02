// Copies the brand assets the stories use from the library (repo root) into
// remotion/public, so svg/, fonts/ and tokens.json stay the single source of truth.
import {cpSync, mkdirSync, rmSync, existsSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const repo = join(here, '..', '..');
const pub = join(here, '..', 'public');

for (const dir of ['svg', 'fonts']) {
  const src = join(repo, dir);
  if (!existsSync(src)) throw new Error(`Missing ${src}`);
  rmSync(join(pub, dir), {recursive: true, force: true});
  mkdirSync(join(pub, dir), {recursive: true});
  cpSync(src, join(pub, dir), {recursive: true});
}
console.log('Synced svg/ and fonts/ into remotion/public');
