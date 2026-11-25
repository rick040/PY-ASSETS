// Render guideline figures (HTML) to PNG.
// Each HTML file holds one element with class "fig"; the PNG is a screenshot of exactly that element,
// at deviceScaleFactor 2, saved next to the HTML with the same name.
// Usage: node brand-2027/tools/render.mjs <file.html|folder> [more ...]
import { createRequire } from 'node:module';
import { readdirSync, statSync } from 'node:fs';
import { resolve, join, extname } from 'node:path';
import { pathToFileURL } from 'node:url';

// Playwright is resolved like CommonJS so a globally installed copy (NODE_PATH) is found too.
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require(require.resolve('playwright', { paths: [process.env.NODE_PATH || '', '/opt/node-tools/node_modules'].filter(Boolean) }))); }

const inputs = process.argv.slice(2);
if (!inputs.length) { console.error('usage: node render.mjs <file.html|folder> ...'); process.exit(1); }
const files = [];
for (const p of inputs) {
  const abs = resolve(p);
  if (statSync(abs).isDirectory()) {
    for (const f of readdirSync(abs)) if (extname(f) === '.html') files.push(join(abs, f));
  } else files.push(abs);
}
const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 2, viewport: { width: 2400, height: 1600 } });
let failed = 0;
for (const f of files) {
  try {
    await page.goto(pathToFileURL(f).href, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const fig = await page.$('.fig');
    if (!fig) { console.error('no .fig in', f); failed++; continue; }
    const out = f.replace(/\.html$/, '.png');
    await fig.screenshot({ path: out, omitBackground: false });
    console.log('ok', out);
  } catch (e) { console.error('fail', f, e.message); failed++; }
}
await browser.close();
process.exit(failed ? 1 : 0);
