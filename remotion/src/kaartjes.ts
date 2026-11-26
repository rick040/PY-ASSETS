// Map spots (KaartSpot, "Het kaartje"): one well-known place per video, with the nearest ParkingYou locations around it on a
// simple drawn map. Only places where none of our parkings is right next door (more than 3 minutes' walk).
// Walking times: foot route via OpenStreetMap (routing.openstreetmap.de, foot profile) from the parking address to the
// place, rounded to whole minutes. Positions on the map: the real offset in metres from the place (east = right, north = up),
// scaled to fit; the streets are decoration, not a real map.

export type KaartParking = {
  /** Location slug from locaties.ts. */
  locatie: string;
  /** Walking time as shown, for example "8 min.". */
  tijd: string;
  /** Offset of the parking from the place in metres: east (dx) and north (dy). */
  dx: number;
  dy: number;
};

export type Kaartje = {
  slug: string;
  /** Short name on the pin. */
  plek: string;
  /** Question at the top, from frame 0. */
  vraag: string;
  /** Line under the question. Default "Parkeer op loopafstand:". */
  sub?: string;
  /** One to three parkings, nearest first. */
  parkings: KaartParking[];
  /** Where the times come from, and anything to check before posting. */
  bron: string;
};

export const kaartjes: Kaartje[] = [
  {
    slug: 'muziekgebouw-eindhoven',
    plek: 'Muziekgebouw',
    vraag: 'Naar het Muziekgebouw?',
    parkings: [
      {locatie: 'dll-garage', tijd: '8 min.', dx: 331, dy: -52},
      {locatie: 'victoriapark', tijd: '9 min.', dx: -481, dy: 132},
      {locatie: 'td-gebouw', tijd: '10 min.', dx: -171, dy: -585},
    ],
    bron:
      'Looproutes OpenStreetMap (26-11-2026) naar Muziekgebouw Eindhoven, Jan van Lieshoutstraat 3: ' +
      'DLL (Garage) vanaf Kanaalstraat 2 630 m (8,4 min); Victoriapark 655 m (8,7 min); TD-gebouw vanaf Frederik van Eedenplein 1 758 m (10,2 min).',
  },
];
