// "Parkeer en stap over" (OverstapSpot): park, walk to the station or metro, ride on. A line map like a metro map with three
// stops (parking, walk, station) and a departure board with the places the location page names. Every fact from the page.

export type Overstap = {
  slug: string;
  /** Location slug from locaties.ts. */
  locatie: string;
  vraag: string;
  sub: string;
  /** Price pill at the parking stop, for example "Hele dag vanaf €7". */
  prijs: string;
  /** Walking time to the station as the page states it; "naast de deur" when it is right next to it. */
  lopen: string;
  station: string;
  vervoer: 'trein' | 'metro';
  /** Places the page names as destinations. */
  naar: string[];
  /** Condition to show small under the price, if any (for example a P+R rate). */
  voorwaarde?: string;
  bron: string;
};

export const overstappen: Overstap[] = [
  {
    slug: 'at-the-park',
    locatie: 'at-the-park',
    vraag: 'Met de trein naar Den Haag?',
    sub: 'Parkeer in Rijswijk en stap over:',
    prijs: 'Hele dag vanaf €7',
    lopen: '7 min.',
    station: 'Station Rijswijk',
    vervoer: 'trein',
    naar: ['Den Haag', 'Delft', 'Rotterdam'],
    bron:
      'Locatiepagina At the Park: "Je loopt vanaf de garage in zeven minuten naar het station" en "zet je auto hier neer voor € 7 tot € 9 per dag ' +
      'en reis met de trein door naar Den Haag, Delft of Rotterdam". Dagkaart €12, met reservering €9, vroegboekkorting €7.',
  },
];
