// Renders the location spots (LocatieSpot, 60 fps).
// node scripts/render-locaties.mjs                    all locations, 16:9 (1920x1080) to out/locaties/<slug>.mp4
// node scripts/render-locaties.mjs plantage           one or more slugs
// node scripts/render-locaties.mjs --reels [slugs]    9:16 reels (1080x1920) to out/reels/<slug>.mp4
// node scripts/render-locaties.mjs --chat [slugs]     chat spots, 9:16 to out/chat/ and 16:9 to out/chat-youtube/
// node scripts/render-locaties.mjs --lijst [slugs]    checklist spots, 9:16 to out/lijstje/ and 16:9 to out/lijstje-youtube/
// node scripts/render-locaties.mjs --bord [slugs]     signpost spots, 9:16 to out/bordje/ and 16:9 to out/bordje-youtube/
// node scripts/render-locaties.mjs --kaart [slugs]    map spots, 9:16 to out/kaartje/ and 16:9 to out/kaartje-youtube/
// node scripts/render-locaties.mjs --light [ids]     Amsterdam Light campaign, 9:16 to out/amsterdam-light/
// node scripts/render-locaties.mjs --vroeg [slugs]    early-booking spots, 9:16 to out/vroegboeken/ and 16:9 to out/vroegboeken-youtube/
// node scripts/render-locaties.mjs --strip [slugs]    ParkingPass spots, 9:16 to out/strippenkaart/ and 16:9 to out/strippenkaart-youtube/
// node scripts/render-locaties.mjs --rij [slugs]      entrance-route spots, 9:16 to out/rijroute/ and 16:9 to out/rijroute-youtube/
// node scripts/render-locaties.mjs --overstap [slugs] park-and-ride spots, 9:16 to out/overstap/ and 16:9 to out/overstap-youtube/
// node scripts/render-locaties.mjs --vraag [slugs]    FAQ accordions, 9:16 to out/vraag/ and 16:9 to out/vraag-youtube/
// node scripts/render-locaties.mjs --droog [slugs]    covered-garage rain spots, 9:16 to out/droog/ and 16:9 to out/droog-youtube/
// node scripts/render-locaties.mjs --rondje [slugs]   search-or-walk split screens, 9:16 to out/rondje/ and 16:9 to out/rondje-youtube/
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
const chat = args.includes('--chat');
const lijst = args.includes('--lijst');
const bord = args.includes('--bord');
const kaart = args.includes('--kaart');
const light = args.includes('--light');
const vroeg = args.includes('--vroeg');
const strip = args.includes('--strip');
const rij = args.includes('--rij');
const overstap = args.includes('--overstap');
const rondje = args.includes('--rondje');
const vraag = args.includes('--vraag');
const droog = args.includes('--droog');
const wanted = args.filter((a) => !a.startsWith('--'));
const prefixes = droog ? ['Droog-', 'DroogYT-'] : vraag ? ['Vraag-', 'VraagYT-'] : rondje ? ['Rondje-', 'RondjeYT-'] : overstap ? ['Overstap-', 'OverstapYT-'] : rij ? ['Rij-', 'RijYT-'] : strip ? ['Strip-', 'StripYT-'] : vroeg ? ['Vroeg-', 'VroegYT-'] : light ? ['Light-'] : kaart ? ['Kaart-', 'KaartYT-'] : bord ? ['Bord-', 'BordYT-'] : lijst ? ['Lijst-', 'LijstYT-'] : chat ? ['Chat-', 'ChatYT-'] : zoek ? ['Zoek-', 'ZoekYT-'] : [reels ? 'Reel-' : 'Spot-'];
const dirFor = (p) => ({'Spot-': 'locaties', 'Reel-': 'reels', 'Zoek-': 'zoek', 'ZoekYT-': 'zoek-youtube', 'Chat-': 'chat', 'ChatYT-': 'chat-youtube', 'Lijst-': 'lijstje', 'LijstYT-': 'lijstje-youtube', 'Bord-': 'bordje', 'BordYT-': 'bordje-youtube', 'Kaart-': 'kaartje', 'KaartYT-': 'kaartje-youtube', 'Light-': 'amsterdam-light', 'Vroeg-': 'vroegboeken', 'VroegYT-': 'vroegboeken-youtube', 'Strip-': 'strippenkaart', 'StripYT-': 'strippenkaart-youtube', 'Rij-': 'rijroute', 'RijYT-': 'rijroute-youtube', 'Overstap-': 'overstap', 'OverstapYT-': 'overstap-youtube', 'Rondje-': 'rondje', 'RondjeYT-': 'rondje-youtube', 'Vraag-': 'vraag', 'VraagYT-': 'vraag-youtube', 'Droog-': 'droog', 'DroogYT-': 'droog-youtube'})[p];

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
    // Search spots render in one tab: with several tabs Chrome sometimes dropped the CTA button or a card in a frame.
    concurrency: zoek || chat || lijst || bord || kaart || light || vroeg || strip || rij || overstap || rondje || vraag ? 1 : null,
    outputLocation,
    browserExecutable,
    chromiumOptions: {gl: 'swangle'},
    onProgress: () => {},
  });
  console.log(`\n-> ${outputLocation}`);
}
