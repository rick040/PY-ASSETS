// Signpost spots (BordSpot, "Het bordje"): one location per video, a street sign with four nearby places and the walking time.
// Walking times: foot route from the parking address via OpenStreetMap (routing.openstreetmap.de, foot profile), rounded
// to whole minutes. Arrows point the compass way from the parking to the place (up = north, 8 directions), not the route.
// Partner names (Artis, PSV, Pathé) as text only, no logos.

export type Bord = {
  /** Name of the place on the sign. */
  naar: string;
  /** Walking time as shown, for example "6 min." or "naast de deur". */
  tijd: string;
  /** Compass bearing from the parking to the place in degrees (0 = north), drawn as one of 8 arrows. */
  richting: number;
};

export type Bordje = {
  slug: string;
  /** Location slug from locaties.ts. */
  locatie: string;
  /** Question at the top, from frame 0. */
  vraag: string;
  /** Line under the question. Default "Alles op loopafstand:". */
  sub?: string;
  borden: [Bord, Bord, Bord, Bord];
  /** Where each time comes from, so it can be checked. */
  bron: string;
};

export const bordjes: Bordje[] = [
  {
    slug: 'plantage',
    locatie: 'plantage',
    vraag: 'Dagje Amsterdam?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Artis', tijd: 'naast de deur', richting: 107},
      {naar: 'Verzetsmuseum', tijd: '1 min.', richting: 6},
      {naar: 'Hortus Botanicus', tijd: '6 min.', richting: 267},
      {naar: 'Waterlooplein', tijd: '12 min.', richting: 283},
    ],
    bron:
      'Artis: "direct naast de ingang van Artis" (locatiepagina). Looproutes OpenStreetMap (26-11-2026) vanaf Plantage Kerklaan 38: ' +
      'Verzetsmuseum 94 m (1,2 min), Hortus Botanicus 415 m (5,5 min), Waterlooplein 894 m (12,1 min).',
  },
];
