// "Zo rijd je erin" (RijSpot): the last stretch by car to the garage entrance on a real map (OpenStreetMap data in the house
// colours), the car drives it, the steps come in as it passes them. The stretch is the part that routes from several
// directions share (OSRM car profile, routing.openstreetmap.de); street names from OpenStreetMap, the entrance from the
// location page ("Inrit ...").

export type RijStap = {
  /** Text of the step, for example "Rechtsaf de Frederik van Eedenplein op". */
  tekst: string;
  /** Short label on the map. */
  label: string;
  /** Where on the route it happens, in metres from the entrance (east, north). */
  x: number;
  y: number;
  /** Arrow direction for the step row: 'rechtdoor', 'rechts', 'links' or 'inrit'. */
  pijl: 'rechtdoor' | 'rechts' | 'links' | 'inrit';
};

export type Rijroute = {
  slug: string;
  /** Location slug from locaties.ts. */
  locatie: string;
  vraag: string;
  /** The route in metres from the entrance [east, north], start to entrance. */
  route: [number, number][];
  lengte: number;
  stappen: RijStap[];
  kaart: {src: string; x0: number; y0: number; w: number; h: number};
  bron: string;
};

export const rijroutes: Rijroute[] = [
  {
    slug: 'td-gebouw',
    locatie: 'td-gebouw',
    vraag: 'Waar is de inrit van het TD-gebouw?',
    route: [[211,-512],[156,-498],[136,-490],[123,-482],[118,-479],[106,-467],[98,-457],[96,-455],[92,-449],[89,-444],[86,-440],[82,-430],[77,-414],[74,-398],[71,-299],[69,-292],[65,-278],[60,-267],[57,-264],[51,-254],[45,-250],[-14,-172],[-72,-95],[-86,-74],[-96,-61],[-89,-56],[-67,-41],[0,0]],
    lengte: 700,
    stappen: [
      {tekst: 'Via de Edenstraat', label: 'Edenstraat', x: 86, y: -440, pijl: 'rechtdoor'},
      {tekst: 'Rechtsaf de Frederik van Eedenplein op', label: 'Rechtsaf', x: -96, y: -61, pijl: 'rechts'},
      {tekst: 'Inrit van Parking TD-gebouw', label: 'Inrit', x: 0, y: 0, pijl: 'inrit'},
    ],
    kaart: {src: 'kaarten/rij-td-gebouw.jpg', x0: -843, y0: 600, w: 1800, h: 1712},
    bron:
      'Inrit Frederik van Eedenplein (locatiepagina). Autoroute OpenStreetMap (27-11-2026): vanuit het zuiden, oosten en de Aalsterweg ' +
      'komen de routes samen op de Edenstraat en slaan rechtsaf de Frederik van Eedenplein op; getoond zijn de laatste 700 meter.',
  },
];
