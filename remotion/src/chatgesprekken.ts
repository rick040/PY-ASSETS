// Chat spots (ChatSpot, "Het appje"): a question comes in, the answer is a location card plus a short tip,
// a reply closes the chat, then the shared CTA. One location per chat. Plain chat bubbles in the house style
// (no messenger branding). Every fact in the tip must be on the location page (see locaties.ts `bron`).

export type Chatgesprek = {
  slug: string;
  /** Location slug from locaties.ts. */
  locatie: string;
  /** Incoming question: the hook. */
  vraag: string;
  /** Short tip under the card. */
  tip: string;
  /** Reply that closes the chat. */
  reactie: string;
  /** Second pill on the card; defaults to the walking time or first fact of the location. */
  kenmerk?: string;
  /** Source of the facts in the tip, or what to check. */
  bron?: string;
};

export const chatgesprekken: Chatgesprek[] = [
  {
    slug: 'plantage-artis',
    locatie: 'plantage',
    vraag: 'Waar parkeren we zaterdag bij Artis?',
    kenmerk: 'Direct naast Artis',
    tip: 'Met een Artis-kaartje parkeer je er de hele dag voor €17,50.',
    reactie: 'Top, dan reserveer ik die!',
    bron: 'parkingyou.nl, Parking Plantage: "direct naast Artis", dagkaart bezoekers Artis €17,50.',
  },
];
