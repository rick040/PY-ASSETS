// Render an HTML file to PDF with the page size set by its CSS @page rule.
// Usage: node brand-2027/tools/render_pdf.mjs <in.html> <out.pdf>
import { createRequire } from 'node:module';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require(require.resolve('playwright', { paths: [process.env.NODE_PATH || '', '/opt/node-tools/node_modules'].filter(Boolean) }))); }
const [inp, out] = process.argv.slice(2);
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(pathToFileURL(resolve(inp)).href, { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: resolve(out), preferCSSPageSize: true, printBackground: true });
await browser.close();
console.log('ok', out);
