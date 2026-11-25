// Writes out/locaties/OVERZICHT.md from src/locaties.ts: npx tsx scripts/overzicht.ts
import {writeFileSync, mkdirSync} from 'node:fs';
import {locaties} from '../src/locaties';

const rows = locaties.map((l) => {
  const prijs = `${l.prijs.vanaf ? 'vanaf ' : ''}${l.prijs.bedrag} ${l.prijs.eenheid}`;
  const kenmerken = l.kenmerken.map(([a, b]) => (a ? `${a} ${b}` : b)).join(' · ');
  return `| [${l.naam}](${l.url}) | ${l.stad} | ${l.hook} / ${l.subhook} | ${prijs} | ${kenmerken} | ${l.bron}${l.check ? ` **Check:** ${l.check}` : ''} | \`${l.slug}.mp4\` |`;
});
const md = `# Locatiespots: overzicht

Gegenereerd uit \`src/locaties.ts\`. Data van parkingyou.nl, 25-11-2026. Rijen met **Check** eerst bevestigen voor plaatsing.

| Locatie | Stad | Hook | Prijs in ballon | Vinkjes | Bron | Video |
|---|---|---|---|---|---|---|
${rows.join('\n')}
`;
mkdirSync('out/locaties', {recursive: true});
writeFileSync('out/locaties/OVERZICHT.md', md);
console.log(`${locaties.length} locaties`);
