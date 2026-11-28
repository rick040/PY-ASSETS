// "Stekker erin": locations with "Elektrisch laden" under Faciliteiten on the location page (19, opened 27-11-2026).
// The pages give no number of charging points or a price per kWh, so the video says neither. `terwijl` finishes the
// sentence "Je auto laadt, terwijl jij ..." with what the page itself names as the reason to park there.
// Zoetermeer: no "eerste 2 uur gratis" (IG-014 still open). Bold parts in [brackets].
import type {Feit} from './Feiten';

export type Laden = {slug: string; terwijl: string; feiten: [Feit, Feit, Feit]; bron: string};

const laad: Feit = ['laden', '[Laadpunten] voor je auto'];
const open247: Feit = ['klok', '[24/7] open'];

const stadshart = (slug: string, derde: Feit, bron: string): Laden => ({
  slug,
  terwijl: 'boodschappen doet in het Stadshart',
  feiten: [laad, ['loop', '[2 min.] naar het Stadshart'], derde],
  bron,
});

export const laden: Laden[] = [
  {slug: 'plantage', terwijl: 'in Artis bent', feiten: [laad, ['loop', 'Direct [naast Artis]'], open247], bron: 'Laadpunten, "direct naast Artis", 24 uur open.'},
  {slug: 'zeeburgerkade', terwijl: 'Amsterdam in gaat', feiten: [laad, ['plekken', '[Overdekte] garage'], open247], bron: 'Laadpunten, overdekte garage, 24 uur.'},
  {slug: 'bos-en-lommerplantsoen', terwijl: 'met de tram de stad in gaat', feiten: [laad, ['loop', 'In [15 min.] met de tram in het centrum'], open247], bron: 'Laadpunten, met de tram in ongeveer 15 minuten in het centrum, 24 uur.'},
  {slug: 'b-amsterdam-b1', terwijl: 'aan het werk bent', feiten: [laad, ['plekken', '[853] overdekte plaatsen'], ['klok', 'Max. [€15] per dag']], bron: 'Laadpunten, 853 overdekte plaatsen, max. €15 per dag.'},
  {slug: 'diergaarde-blijdorp', terwijl: 'in de dierentuin bent', feiten: [laad, ['loop', '[2 min.] naar de dierentuin'], open247], bron: 'Elektrisch laden, 2 min tot de dierentuin, 24 uur.'},
  {slug: 'philips-bedrijfsschool', terwijl: 'het centrum in gaat', feiten: [laad, ['loop', '[10 min.] naar het centrum'], ['klok', 'Na 21:00 [€0,65] per 20 min.']], bron: 'Elektrisch laden, 10 min tot centrum, 21-09u €0,65 per 20 min.'},
  {slug: 'victoriapark', terwijl: 'het centrum in gaat', feiten: [laad, ['loop', '[2 min.] naar het centrum'], open247], bron: 'Elektrisch laden, 2 min tot centrum, 24/7.'},
  {slug: 'dll-garage', terwijl: 'uit eten bent', feiten: [laad, ['loop', '[4 min.] naar het centrum'], ['klok', 'Ma-vr open vanaf [17:00]']], bron: 'Laadpunten, 4 min tot centrum, ma-vr 17:00-06:00; pagina noemt uit eten, film, café.'},
  {slug: 'evoluon', terwijl: 'in het Evoluon bent', feiten: [laad, ['loop', '[2 min.] naar de ingang'], open247], bron: 'Laadpunten, 2 min tot de ingang van het Evoluon, 24 uur.'},
  {slug: 'at-the-park', terwijl: 'met de trein verder gaat', feiten: [laad, ['loop', '[7 min.] naar het station'], ['klok', 'Dagtarief vooraf [€7]']], bron: 'Laadpunten, 7 min tot station, dagtarief vroegboekkorting €7.'},
  {slug: 'stationsweg-ypenburg', terwijl: 'in de trein of bioscoop zit', feiten: [laad, ['loop', 'Direct [naast het station]'], ['klok', 'Open van [07:00] tot [01:00]']], bron: 'Laadpunten, direct naast station Ypenburg en Pathé, ma-zo 07:00-01:00.'},
  {slug: 'heerhugowaard-p1-zuidtangent', terwijl: 'aan het winkelen bent', feiten: [laad, ['loop', 'Direct [bij de winkels]'], ['klok', 'Max. [€9] per dag']], bron: 'Laadpunten, bij Winkelcentrum Middenwaard, max. dagtarief €9.'},
  {slug: 'p2-middenwaard', terwijl: 'aan het winkelen bent', feiten: [laad, ['plekken', '[551] overdekte plaatsen'], open247], bron: 'Laadpunten, 551 overdekte plaatsen, 24/7.'},
  {slug: 'houthavenkade', terwijl: 'het centrum in gaat', feiten: [laad, ['loop', '[6 min.] naar het centrum'], ['klok', 'Na 18:00 [€1] per uur']], bron: 'Elektrisch laden, 6 min tot centrum, 18-09u €1 per 60 min.'},
  stadshart('p1-belgielaan', ['plekken', '[326] overdekte plaatsen'], 'Laadpunten, 2 min tot Stadshart, 326 overdekte plaatsen.'),
  stadshart('p2-bovenlangs', ['plekken', '[448] overdekte plaatsen'], 'Laadpunten, 2 min tot Stadshart, 448 overdekte plaatsen; pagina: "je laadt terwijl je boodschappen doet".'),
  stadshart('p2-onderlangs', ['plekken', '[287] overdekte plaatsen'], 'Laadpunten, 2 min tot Stadshart, 287 plaatsen, overdekt.'),
  stadshart('p4-luxemburglaan', ['klok', 'In- en uitrijden [24/7]'], 'Laadpunten, 2 min tot Stadshart, in- en uitrijden 24 uur.'),
  stadshart('p5-amsterdamstraat', ['lift', '[Lift] en rolstoeltoegang'], 'Laadpunten ("laden terwijl je shopt"), 2 min tot Stadshart, lift, rolstoeltoegang.'),
];
