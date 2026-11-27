// "Rondje zoeken per locatie" (RondjeSpot): split screen. Left a car circles past full car parks while a stress meter rises;
// right someone walks from our parking to a well-known place over the real route from Het kaartje (kaartjes.ts).
// Uses the first (nearest) parking of the kaartje.

export type Rondje = {
  slug: string;
  /** Slug in kaartjes.ts: the place, the map and the walking route come from there. */
  kaartje: string;
  /** The place as it reads in a sentence, for example "de Markthal". */
  naar: string;
  /** The parking as it reads in a sentence; default "Parking <naam>". */
  bij?: string;
  /** When it applies, for parkings that are not open all day (DLL opens on weekdays only from 17:00). */
  wanneer?: string;
};

const r = (kaartje: string, naar: string, extra: Partial<Rondje> = {}): Rondje => ({slug: kaartje, kaartje, naar, ...extra});
const dll = {bij: 'de DLL-garage', wanneer: "'s avonds"};

export const rondjes: Rondje[] = [
  // Eindhoven
  r('muziekgebouw-eindhoven', 'het Muziekgebouw', dll),
  r('effenaar', 'de Effenaar', dll),
  r('stratumseind', 'Stratumseind', dll),
  r('van-abbemuseum', 'het Van Abbemuseum'),
  r('philips-museum', 'het Philips Museum'),
  r('markt-eindhoven', 'de Markt'),
  r('pathe-eindhoven', 'Pathé Eindhoven'),
  r('parktheater', 'het Parktheater'),
  // Rotterdam
  r('markthal', 'de Markthal'),
  r('kubuswoningen', 'de Kubuswoningen'),
  r('de-doelen', 'De Doelen'),
  r('maritiem-museum', 'het Maritiem Museum'),
  r('pathe-schouwburgplein', 'Pathé Schouwburgplein'),
  r('maassilo', 'de Maassilo'),
  r('art-hotel-rotterdam', 'Art Hotel Rotterdam'),
  r('spelen-bij-beelen', 'Spelen bij Beelen'),
  // Amsterdam
  r('carre', 'Carré'),
  r('nemo', 'NEMO'),
  r('scheepvaartmuseum', 'het Scheepvaartmuseum'),
  r('opera-ballet', 'de Nationale Opera & Ballet'),
  // Almere and Schiedam
  r('kunstlinie', 'de Kunstlinie'),
  r('flevoziekenhuis', 'het Flevoziekenhuis'),
  r('theater-aan-de-schie', 'Theater aan de Schie', {bij: 'P+R Schiedam Centrum'}),
];
