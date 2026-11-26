// Checklist spots (LijstSpot, "Het lijstje"): a question, four points that get ticked one by one,
// then the location (photo, name, price) and the shared CTA. One location per video.
// Every point must be on the location page (see locaties.ts `bron`). Text between [ ] is bold.

export type Lijstje = {
  slug: string;
  /** Location slug from locaties.ts. */
  locatie: string;
  /** Bold question at the top: the hook. */
  vraag: string;
  /** Light line under the question. */
  sub: string;
  /** Exactly four points, short enough for one line. */
  punten: [string, string, string, string];
  /** Source of the points, or what to check. */
  bron?: string;
};

export const lijstjes: Lijstje[] = [
  {
    slug: 'plantage',
    locatie: 'plantage',
    vraag: 'Dagje Artis?',
    sub: 'Hier parkeer je zonder zorgen:',
    punten: ['Direct [naast Artis]', '[24/7] open', '[483] parkeerplaatsen', 'Dagkaart Artis: [€17,50]'],
    bron: 'Parking Plantage: "direct naast Artis", 483 plekken, 24/7 open, dagkaart bezoekers Artis €17,50.',
  },
];
