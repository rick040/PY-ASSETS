// "Vroeg boeken loont" (VroegSpot): the three day rates of a location (without booking, with booking, booked early),
// the first two struck through, the early rate wins with the saving. Data from the "Tarieven" block of each location page
// (parkingyou.nl, 27-11-2026). DLL garage and parking deck are left out: closed on weekdays during office hours.

export type Tarief = {label: string; bedrag: number};

export type Vroegboek = {
  slug: string;
  /** Location slug from locaties.ts. */
  locatie: string;
  vraag: string;
  /** Which ticket this is, under the question. */
  wat: string;
  /** Two or three: the usual rate, with booking, and booked early when there is one. The last one wins. */
  tarieven: Tarief[];
  /** Closing line; {prijs} becomes the winning price. Default "Boek ruim vooraf en betaal {prijs}." */
  slot?: string;
  bron: string;
};

const drie = (zonder: number, met: number, vroeg: number, eerste = 'Zonder reservering'): [Tarief, Tarief, Tarief] => [
  {label: eerste, bedrag: zonder},
  {label: 'Met reservering', bedrag: met},
  {label: 'Ruim vooraf geboekt', bedrag: vroeg},
];

export const vroegboeken: Vroegboek[] = [
  {slug: 'plantage', locatie: 'plantage', vraag: 'Hele dag in Amsterdam?', wat: 'Dagkaart van 09:00 tot 18:00', tarieven: drie(45, 42, 30), bron: '09-18u zonder reservering €45, met reservering €42, vroegboekkorting €30.'},
  {slug: 'cruquius', locatie: 'cruquius', vraag: 'Dagje Amsterdam Oost?', wat: 'Dagtarief', tarieven: drie(25, 22.5, 17.5), bron: 'Dagtarief zonder reservering €25,00, met reservering €22,50, vroegboekkorting €17,50.'},
  {slug: 'zeeburgerkade', locatie: 'zeeburgerkade', vraag: 'Hele dag in Amsterdam?', wat: 'Dagtarief', tarieven: drie(25, 22.5, 17.5), bron: 'Dagtarief zonder reservering €25,00, met reservering €22,50, vroegboekkorting €17,50.'},
  {slug: 'bos-en-lommerplantsoen', locatie: 'bos-en-lommerplantsoen', vraag: 'Dagje Amsterdam?', wat: 'Dagtarief', tarieven: drie(17.5, 16, 14), bron: 'Dagtarief zonder reservering €17,50, met reservering €16, vroegboekkorting €14.'},
  {slug: 'hofplein', locatie: 'hofplein', vraag: 'Werkdag in Rotterdam?', wat: 'Dagtarief, maandag tot en met vrijdag', tarieven: drie(30, 25, 20), bron: 'Dagtarief zonder reservering ma t/m vrij €30, met reservering €25, vroegboekkorting €20.'},
  {slug: 'shopping-center', locatie: 'shopping-center', vraag: 'Dagje Alexandrium?', wat: 'Dagtarief', tarieven: drie(12.5, 11, 9), bron: 'Dagtarief zonder reservering €12,50, met reservering €11, vroegboekkorting €9.'},
  {slug: 'europoint', locatie: 'europoint', vraag: 'Hele dag in Rotterdam?', wat: 'Dagtarief', tarieven: drie(15, 14, 12, 'Maximaal dagtarief'), bron: 'Max. dagtarief €15, dagtarief met reservering €14, vroegboekkorting €12.'},
  {slug: 'td-gebouw', locatie: 'td-gebouw', vraag: 'Dagje Eindhoven?', wat: 'Dagtarief', tarieven: drie(15, 14, 12), bron: 'Dagtarief zonder reservering €15, met reservering €14, vroegboekkorting €12.'},
  {slug: 'philips-bedrijfsschool', locatie: 'philips-bedrijfsschool', vraag: 'Hele dag in Eindhoven?', wat: 'Dagtarief', tarieven: drie(15, 14, 12), bron: 'Dagtarief zonder reservering €15, met reservering €14, vroegboekkorting €12. Niet tijdens wedstrijden en grote evenementen.'},
  {slug: 'at-the-park', locatie: 'at-the-park', vraag: 'Werkdag in Rijswijk?', wat: 'Dagtarief', tarieven: drie(12, 9, 7), bron: 'Dagtarief zonder reservering €12, met reservering €9, vroegboekkorting €7.'},
  {slug: 'maashaven', locatie: 'maashaven', vraag: 'Hele dag in Rotterdam-Zuid?', wat: 'Dagtarief · eerste 2 uur gratis', tarieven: [{label: 'Zonder reservering', bedrag: 50}, {label: 'Met reservering', bedrag: 25}], slot: 'Reserveer online en betaal {prijs}.', bron: 'Dagtarief zonder reservering €50, met reservering €25; eerste twee uur gratis. Open ma-vr 07-23, za 09-18, zo 09-17.'},
];
