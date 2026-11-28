// "Droog naar binnen": covered garages only (facility "Overdekte garage" on the location page, or "overdekte plaatsen" in
// the page text for B. Amsterdam). Heerhugowaard P1 is left out: it is mostly an open lot with a covered basement that has
// shorter opening hours. Facts from the location pages, opened 27-11-2026. Bold parts in [brackets].

export type DroogIcoon = 'plekken' | 'loop' | 'lift' | 'klok' | 'camera';

export type Droog = {
  slug: string;
  feiten: [[DroogIcoon, string], [DroogIcoon, string], [DroogIcoon, string]];
  bron: string;
};

const lift: [DroogIcoon, string] = ['lift', '[Lift] en rolstoeltoegang'];
const liftAlleen: [DroogIcoon, string] = ['lift', 'Met de [lift] naar buiten'];
const open247: [DroogIcoon, string] = ['klok', '[24/7] open'];
const plekken = (n: string): [DroogIcoon, string] => ['plekken', `[${n}] overdekte plaatsen`];
const loop = (t: string): [DroogIcoon, string] => ['loop', t];

const stadshart = (slug: string, n: string, derde: [DroogIcoon, string], bron: string): Droog => ({
  slug,
  feiten: [plekken(n), loop('[2 min.] naar het Stadshart'), derde],
  bron,
});

export const droog: Droog[] = [
  {slug: 'cruquius', feiten: [plekken('177'), lift, open247], bron: 'Overdekte garage, 177 plaatsen, lift, rolstoeltoegang, 24/7.'},
  {slug: 'zeeburgerkade', feiten: [plekken('120'), lift, open247], bron: 'Overdekte garage, 120 plaatsen, lift, rolstoeltoegang, 24 uur.'},
  {slug: 'b-amsterdam-b1', feiten: [plekken('853'), ['camera', '[Cameratoezicht]'], open247], bron: '"853 overdekte plaatsen" in de paginatekst, cameratoezicht, 24 uur.'},
  {slug: 'hofplein', feiten: [plekken('300'), loop('[8 min.] naar het centrum'), lift], bron: '300 overdekte plaatsen, 8 min tot centrum, lift, rolstoeltoegang.'},
  {slug: 'shopping-center', feiten: [plekken('129'), loop('[3 min.] naar de winkels'), open247], bron: 'Overdekt, 129 plaatsen, "drie minuten van de winkels", 24/7.'},
  {slug: 'europoint', feiten: [plekken('1.133'), ['camera', '[Cameratoezicht]'], open247], bron: 'Overdekte garage, 1.133 plaatsen, cameratoezicht, 24/7.'},
  {slug: 'philips-stadion', feiten: [plekken('700'), loop('[9 min.] naar het centrum'), lift], bron: 'Overdekte garage, 700 plaatsen, 9 min tot centrum, lift, rolstoeltoegang.'},
  {slug: 'dll-garage', feiten: [plekken('284'), loop('[4 min.] naar het centrum'), ['klok', 'Ma-vr open vanaf [17:00]']], bron: 'Overdekte garage, 284 plaatsen, 4 min tot centrum, ma-vr 17:00-06:00.'},
  {slug: 'at-the-park', feiten: [plekken('800'), loop('[7 min.] naar het station'), lift], bron: 'Overdekte garage, 800 plaatsen, 7 min tot station, lift, rolstoeltoegang.'},
  {slug: 'pr-schiedam-centrum', feiten: [plekken('759'), loop('[4 min.] naar Schiedam Centraal'), lift], bron: '759 plaatsen, overdekt, 4 min tot Schiedam Centraal, lift, rolstoeltoegang.'},
  {slug: 'p2-middenwaard', feiten: [plekken('551'), loop('Direct [bij de winkels]'), liftAlleen], bron: '551 overdekte plaatsen, direct bij winkelcentrum, lift.'},
  {slug: 'p1-carlton-wtc', feiten: [plekken('125'), loop('[4 min.] naar het centrum'), liftAlleen], bron: 'Overdekte garage, 125 plaatsen, 4 min tot centrum, lift.'},
  {slug: 'p2-mandela-wtc', feiten: [plekken('250'), loop('[4 min.] naar het centrum'), liftAlleen], bron: 'Overdekte garage, 250 plaatsen, 4 min tot centrum, lift.'},
  {slug: 'houthavenkade', feiten: [plekken('81'), loop('[6 min.] naar het centrum'), open247], bron: 'Overdekte garage, 81 plaatsen, 6 min tot centrum, 24 uur.'},
  stadshart('p1-belgielaan', '326', lift, '326 overdekte plaatsen, 2 min tot Stadshart, lift, rolstoeltoegang.'),
  stadshart('p2-bovenlangs', '448', lift, '448 overdekte plaatsen, 2 min tot Stadshart, lift, rolstoeltoegang.'),
  stadshart('p2-onderlangs', '287', lift, 'Overdekt, 287 plaatsen, 2 min tot Stadshart, lift, rolstoeltoegang.'),
  stadshart('p4-luxemburglaan', '453', lift, '453 overdekte plaatsen, 2 min tot Stadshart, lift, rolstoeltoegang.'),
  stadshart('p5-amsterdamstraat', '439', lift, '439 overdekte plaatsen, 2 min tot Stadshart, lift, rolstoeltoegang.'),
  stadshart('p8-nederlandlaan', '659', ['klok', 'Inrijden tot [22.30 uur]'], 'Overdekt, 659 plaatsen, 2 min tot Stadshart, inrijden 07:00-22:30.'),
  stadshart('p9-duitslandlaan', '582', liftAlleen, '582 overdekte plaatsen, 2 min tot Stadshart, lift.'),
];
