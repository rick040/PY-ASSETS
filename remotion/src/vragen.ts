// "Vraag het maar" (VraagSpot): the FAQ from the location page as an accordion that opens question by question. Every
// question and answer comes from the "Veelgestelde vragen" block of the location page; `kern` is the fact in the answer,
// shown big, `antwoord` the rest of the answer in short.

export type Vraag = {
  vraag: string;
  /** The fact, shown big, for example "€15" or "Ja, 24 uur". */
  kern: string;
  /** The rest of the answer, short. */
  antwoord: string;
};

export type VraagSet = {
  slug: string;
  /** Location slug from locaties.ts. */
  locatie: string;
  /** Three questions from the page. */
  vragen: [Vraag, Vraag, Vraag];
  /** CSS object-position for the location photo (it is portrait, the card is wide); default '50% 80%'. */
  fotoPositie?: string;
  bron: string;
};

export const vraagsets: VraagSet[] = [
  {
    slug: 'hofplein',
    locatie: 'hofplein',
    fotoPositie: '50% 100%',
    vragen: [
      {vraag: 'Wat kost parkeren in het weekend?', kern: '€15', antwoord: 'voor een hele dag, op zaterdag en zondag.'},
      {vraag: 'Hoeveel scheelt online reserveren?', kern: '€20 in plaats van €30', antwoord: 'voor een dagkaart op werkdagen als je vroeg boekt. Met reservering €25.'},
      {vraag: 'Is er een nachttarief?', kern: 'Ja, maximaal €15', antwoord: 'tussen 00.00 en 09.00 uur.'},
    ],
    bron:
      'Locatiepagina Hofplein, Veelgestelde vragen: weekend max. €15 per dag; werkdagen dagkaart €30 zonder, €25 met reservering, €20 bij vroeg boeken; nacht 00.00-09.00 max. €15.',
  },
];
