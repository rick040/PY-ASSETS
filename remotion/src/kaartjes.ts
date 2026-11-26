// Map spots (KaartSpot, "Het kaartje"): one well-known place per video, with the nearest ParkingYou locations around it on a
// simple drawn map. Only places where none of our parkings is right next door (more than 3 minutes' walk).
// Walking times: foot route via OpenStreetMap (routing.openstreetmap.de, foot profile) from the parking address to the
// place, rounded to whole minutes. Positions on the map: the real offset in metres from the place (east = right, north = up),
// scaled to fit. The map image is drawn from OpenStreetMap data (© OpenStreetMap contributors, ODbL) in the house colours.

import type {Prijs} from './locaties';

export type KaartParking = {
  /** Location slug from locaties.ts. */
  locatie: string;
  /** Walking time as shown, for example "8 min.". */
  tijd: string;
  /** Offset of the parking from the place in metres: east (dx) and north (dy). */
  dx: number;
  dy: number;
  /** Walking route from the parking to the place, in metres [east, north], simplified. */
  route: [number, number][];
  /** Price to show when the location's default (for example an evening rate) does not fit this place. */
  prijs?: Prijs;
};

/** The map image (public/kaarten) and the area it covers, in metres from the place: west edge x0, north edge y0. */
export type KaartBeeld = {src: string; x0: number; y0: number; w: number; h: number};

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
  kaart: KaartBeeld;
  /** Where the times come from, and anything to check before posting. */
  bron: string;
};

export const kaartjes: Kaartje[] = [
  {
    slug: 'muziekgebouw-eindhoven',
    plek: 'Muziekgebouw',
    vraag: 'Naar het Muziekgebouw?',
    parkings: [
      {locatie: 'dll-garage', tijd: '8 min.', dx: 331, dy: -52, route: [[351,-60],[352,-57],[376,-60],[385,-65],[392,-61],[417,-73],[399,-110],[387,-124],[229,-39],[127,-61],[119,-75],[97,-80],[37,-102],[3,-59],[-25,-14],[0,0]]},
      {locatie: 'victoriapark', tijd: '9 min.', dx: -481, dy: 132, route: [[-478,137],[-458,127],[-443,111],[-439,95],[-441,80],[-376,59],[-372,60],[-346,52],[-344,57],[-309,47],[-294,36],[-291,27],[-264,58],[-217,14],[-152,72],[-107,-10],[-57,23],[-51,31],[-25,-14],[0,0]]},
      {locatie: 'td-gebouw', tijd: '10 min.', dx: -171, dy: -585, route: [[-171,-585],[-92,-532],[-94,-495],[-88,-494],[-99,-347],[-110,-326],[-160,-270],[-148,-267],[-116,-240],[-108,-227],[-4,-142],[37,-102],[3,-59],[-25,-14],[0,0]]},
    ],
    kaart: {src: 'kaarten/muziekgebouw-eindhoven.jpg', x0: -1581, y0: 1037, w: 3098, h: 2522},
    bron:
      'Looproutes OpenStreetMap (26-11-2026) naar Muziekgebouw Eindhoven, Jan van Lieshoutstraat 3: ' +
      'DLL (Garage) vanaf Kanaalstraat 2 630 m (8,4 min); Victoriapark 655 m (8,7 min); TD-gebouw vanaf Frederik van Eedenplein 1 758 m (10,2 min).',
  },
];
