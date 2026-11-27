// "Rondje zoeken per locatie" (RondjeSpot): split screen. Left a car circles past full car parks while a stress meter rises;
// right someone walks from our parking to a well-known place over the real route from Het kaartje (kaartjes.ts).
// Uses the nearest parking of the kaartje.

export type Rondje = {
  slug: string;
  /** Slug in kaartjes.ts: the place, the map and the walking route come from there. */
  kaartje: string;
  /** The place as it reads in a sentence, for example "de Markthal". */
  naar: string;
};

export const rondjes: Rondje[] = [{slug: 'markthal', kaartje: 'markthal', naar: 'de Markthal'}];
