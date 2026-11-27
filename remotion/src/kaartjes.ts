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
  {
    slug: 'effenaar',
    plek: 'Effenaar',
    vraag: 'Naar de Effenaar?',
    parkings: [
      {locatie: 'dll-garage', tijd: '9 min.', dx: 84, dy: -374, route: [[104,-382],[105,-380],[129,-383],[138,-387],[145,-383],[151,-348],[163,-340],[174,-339],[193,-344],[207,-319],[223,-298],[237,-269],[234,-228],[226,-208],[190,-198],[185,-188],[185,-168],[175,-159],[158,-149],[116,-142],[99,-132],[89,-34],[77,-10],[0,-11],[0,0]]},
      {locatie: 'victoriapark', tijd: '12 min.', dx: -728, dy: -190, route: [[-725,-185],[-704,-195],[-690,-212],[-686,-228],[-687,-242],[-623,-263],[-619,-262],[-592,-270],[-591,-265],[-556,-276],[-541,-286],[-538,-295],[-511,-264],[-464,-308],[-435,-281],[-330,-195],[-238,-104],[-202,-77],[-35,-12],[0,-11],[0,0]]},
      {locatie: 'td-gebouw', tijd: '18 min.', dx: -417, dy: -907, route: [[-417,-907],[-339,-854],[-341,-818],[-334,-816],[-346,-669],[-357,-648],[-407,-592],[-394,-589],[-362,-563],[-355,-549],[-250,-464],[-210,-424],[-244,-381],[-297,-292],[-328,-209],[-330,-195],[-238,-104],[-202,-77],[-35,-12],[0,-11],[0,0]]},
    ],
    kaart: {src: 'kaarten/effenaar.jpg', x0: -1828, y0: 900, w: 3165, h: 2707},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Effenaar: DLL (Garage) 646 m (8,6 min); Victoriapark 920 m (12,3 min); TD-gebouw 1303 m (17,5 min). DLL is ma-vr pas open vanaf 17:00; alleen bij plekken waar je vooral \'s avonds heen gaat.',
  },
  {
    slug: 'van-abbemuseum',
    plek: 'Van Abbemuseum',
    vraag: 'Naar het Van Abbemuseum?',
    parkings: [
      {locatie: 'td-gebouw', tijd: '5 min.', dx: -320, dy: -120, route: [[-320,-120],[-220,-50],[-216,-54],[-102,18],[-60,-21],[-37,-22],[-23,-1],[-5,-9],[0,0]]},
      {locatie: 'victoriapark', tijd: '13 min.', dx: -631, dy: 597, prijs: {bedrag: '€4,00', eenheid: 'per uur'}, route: [[-628,602],[-607,592],[-592,576],[-588,560],[-590,545],[-526,524],[-522,526],[-495,517],[-493,522],[-478,517],[-483,497],[-482,478],[-470,452],[-457,439],[-420,412],[-381,375],[-307,297],[-257,238],[-160,113],[-102,18],[-60,-21],[-37,-22],[-23,-1],[-5,-9],[0,0]]},
    ],
    kaart: {src: 'kaarten/van-abbemuseum.jpg', x0: -1731, y0: 1502, w: 2831, h: 2522},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Van Abbemuseum: TD-gebouw 389 m (5,2 min); Victoriapark 970 m (13,0 min). Victoriapark: dagtarief €4 per uur getoond (overdag), niet het avondtarief.',
  },
  {
    slug: 'philips-museum',
    plek: 'Philips Museum',
    vraag: 'Naar het Philips Museum?',
    parkings: [
      {locatie: 'victoriapark', tijd: '4 min.', dx: -179, dy: 68, prijs: {bedrag: '€4,00', eenheid: 'per uur'}, route: [[-176,72],[-155,63],[-145,52],[-138,40],[-138,16],[-123,10],[-43,-13],[-41,-7],[-26,-12],[-12,30],[10,12],[0,0]]},
      {locatie: 'td-gebouw', tijd: '11 min.', dx: 132, dy: -650, route: [[132,-650],[152,-637],[145,-629],[139,-597],[133,-594],[126,-587],[120,-515],[110,-509],[113,-499],[112,-437],[105,-437],[86,-363],[122,-345],[57,-259],[35,-237],[20,-225],[11,-223],[4,-204],[-2,-176],[3,-157],[20,-127],[85,-50],[38,-6],[36,-8],[10,12],[0,0]]},
    ],
    kaart: {src: 'kaarten/philips-museum.jpg', x0: -1314, y0: 972, w: 2600, h: 2522},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Philips Museum: Victoriapark 271 m (3,6 min); TD-gebouw 841 m (11,3 min). Victoriapark: dagtarief €4 per uur getoond (overdag), niet het avondtarief.',
  },
  {
    slug: 'stratumseind',
    plek: 'Stratumseind',
    vraag: 'Avondje Stratumseind?',
    parkings: [
      {locatie: 'dll-garage', tijd: '7 min.', dx: 202, dy: 191, route: [[222,184],[223,186],[247,183],[256,179],[263,183],[288,171],[270,133],[258,119],[198,-12],[167,9],[80,-50],[72,-37],[0,0],[0,0]]},
      {locatie: 'td-gebouw', tijd: '9 min.', dx: -299, dy: -342, route: [[-300,-342],[-200,-272],[-196,-275],[-75,-200],[-62,-216],[-49,-207],[-41,-190],[9,-159],[13,-147],[23,-139],[44,-127],[74,-104],[103,-92],[72,-37],[0,0],[0,0]]},
      {locatie: 'victoriapark', tijd: '12 min.', dx: -610, dy: 376, route: [[-607,380],[-586,370],[-572,354],[-568,338],[-570,323],[-505,302],[-501,304],[-474,295],[-473,301],[-438,290],[-423,279],[-420,270],[-393,301],[-346,258],[-280,315],[-214,200],[-113,80],[-82,47],[0,0],[0,0]]},
    ],
    kaart: {src: 'kaarten/stratumseind.jpg', x0: -1710, y0: 1280, w: 3098, h: 2522},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Stratumseind: DLL (Garage) 518 m (6,9 min); TD-gebouw 650 m (8,7 min); Victoriapark 872 m (11,6 min). DLL is ma-vr pas open vanaf 17:00; alleen bij plekken waar je vooral \'s avonds heen gaat.',
  },
  {
    slug: 'markt-eindhoven',
    plek: 'Markt',
    vraag: 'Naar de Markt in Eindhoven?',
    parkings: [
      {locatie: 'victoriapark', tijd: '8 min.', dx: -401, dy: 64, prijs: {bedrag: '€4,00', eenheid: 'per uur'}, route: [[-398,69],[-378,59],[-363,42],[-359,26],[-361,12],[-296,-9],[-292,-8],[-265,-16],[-264,-11],[-229,-22],[-214,-32],[-211,-41],[-184,-10],[-137,-54],[-108,-27],[-3,59],[-1,45],[14,5],[0,0]]},
      {locatie: 'td-gebouw', tijd: '12 min.', dx: -90, dy: -653, route: [[-91,-653],[-12,-600],[-14,-564],[-8,-562],[-19,-415],[-30,-394],[-80,-338],[-68,-335],[-36,-309],[-28,-295],[76,-210],[117,-170],[103,-155],[60,-92],[30,-38],[14,5],[0,0]]},
    ],
    kaart: {src: 'kaarten/markt-eindhoven.jpg', x0: -1501, y0: 969, w: 2718, h: 2522},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Markt Eindhoven: Victoriapark 586 m (7,8 min); TD-gebouw 856 m (11,5 min). Victoriapark: dagtarief €4 per uur getoond (overdag), niet het avondtarief.',
  },
  {
    slug: 'pathe-eindhoven',
    plek: 'Pathé Eindhoven',
    vraag: 'Naar de film in Eindhoven?',
    parkings: [
      {locatie: 'victoriapark', tijd: '10 min.', dx: -554, dy: -107, route: [[-550,-103],[-530,-113],[-515,-129],[-511,-145],[-513,-160],[-449,-180],[-445,-179],[-418,-188],[-416,-182],[-381,-193],[-366,-204],[-363,-213],[-336,-182],[-290,-225],[-261,-198],[-155,-112],[-63,-22],[-28,6],[-6,15],[0,0]]},
      {locatie: 'dll-garage', tijd: '10 min.', dx: 258, dy: -292, route: [[278,-300],[280,-297],[304,-300],[312,-304],[320,-300],[344,-312],[327,-350],[314,-364],[161,-280],[111,-285],[56,-188],[35,-140],[20,-122],[-17,-61],[11,-42],[-28,6],[-6,15],[0,0]]},
      {locatie: 'td-gebouw', tijd: '15 min.', dx: -243, dy: -825, route: [[-243,-825],[-164,-771],[-167,-735],[-160,-733],[-171,-586],[-182,-566],[-232,-509],[-220,-507],[-188,-480],[-180,-467],[-76,-382],[-35,-342],[-69,-298],[-123,-209],[-153,-127],[-155,-112],[-63,-22],[-28,6],[-6,15],[0,0]]},
    ],
    kaart: {src: 'kaarten/pathe-eindhoven.jpg', x0: -1654, y0: 915, w: 3098, h: 2640},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Pathé Eindhoven: Victoriapark 728 m (9,7 min); DLL (Garage) 742 m (9,9 min); TD-gebouw 1112 m (14,9 min). DLL is ma-vr pas open vanaf 17:00; alleen bij plekken waar je vooral \'s avonds heen gaat.',
  },
  {
    slug: 'parktheater',
    plek: 'Parktheater',
    vraag: 'Naar het Parktheater?',
    parkings: [
      {locatie: 'td-gebouw', tijd: '12 min.', dx: -519, dy: 501, route: [[-520,501],[-420,571],[-416,567],[-405,552],[-390,515],[-320,463],[-111,133],[-72,101],[-34,89],[-8,72],[-7,68],[-47,28],[-41,14],[0,0]]},
      {locatie: 'dll-garage', tijd: '17 min.', dx: -18, dy: 1034, route: [[2,1026],[3,1029],[27,1026],[36,1021],[43,1025],[68,1014],[50,976],[38,962],[22,928],[21,920],[-10,859],[-50,763],[-86,725],[-101,717],[-87,685],[-64,599],[8,415],[2,399],[-1,398],[2,364],[10,355],[27,308],[32,282],[68,168],[70,145],[70,140],[66,137],[77,96],[57,93],[-8,72],[-7,68],[-47,28],[-41,14],[0,0]]},
    ],
    kaart: {src: 'kaarten/parktheater.jpg', x0: -1620, y0: 1934, w: 2797, h: 2834},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Parktheater Eindhoven: TD-gebouw 866 m (11,5 min); DLL (Garage) 1251 m (16,7 min). DLL is ma-vr pas open vanaf 17:00; alleen bij plekken waar je vooral \'s avonds heen gaat.',
  },
  {
    slug: 'markthal',
    plek: 'Markthal',
    vraag: 'Naar de Markthal?',
    parkings: [
      {locatie: 'hofplein', tijd: '13 min.', dx: -541, dy: 592, route: [[-556,563],[-540,556],[-534,557],[-467,578],[-452,533],[-448,534],[-426,513],[-407,476],[-334,372],[-317,382],[-306,366],[-257,270],[-236,282],[-204,222],[-186,200],[-178,197],[-155,144],[-120,154],[-111,123],[-100,126],[-95,107],[-60,116],[-54,97],[-44,91],[-23,30],[-17,32],[-2,-1],[0,0]]},
    ],
    kaart: {src: 'kaarten/markthal.jpg', x0: -1656, y0: 1492, w: 2756, h: 2393},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Markthal: Hofplein 962 m (12,9 min).',
  },
  {
    slug: 'kubuswoningen',
    plek: 'Kubuswoningen',
    vraag: 'Naar de Kubuswoningen?',
    parkings: [
      {locatie: 'hofplein', tijd: '15 min.', dx: -806, dy: 523, route: [[-821,494],[-806,488],[-800,488],[-699,520],[-684,475],[-663,483],[-578,529],[-573,524],[-564,529],[-532,501],[-321,274],[-298,256],[-297,250],[-222,169],[-162,96],[-136,106],[-117,66],[-106,58],[-80,15],[-24,-18],[2,-2],[0,0]]},
    ],
    kaart: {src: 'kaarten/kubuswoningen.jpg', x0: -1921, y0: 1429, w: 3023, h: 2347},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Kubuswoningen: Hofplein 1145 m (15,4 min).',
  },
  {
    slug: 'de-doelen',
    plek: 'De Doelen',
    vraag: 'Concert in De Doelen?',
    parkings: [
      {locatie: 'hofplein', tijd: '8 min.', dx: 391, dy: 340, route: [[376,311],[392,304],[398,305],[413,259],[414,254],[394,212],[269,174],[268,176],[51,104],[52,101],[48,100],[59,66],[43,61],[44,57],[15,48],[17,44],[1,37],[0,0]]},
    ],
    kaart: {src: 'kaarten/de-doelen.jpg', x0: -1100, y0: 1270, w: 2614, h: 2200},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar De Doelen: Hofplein 606 m (8,1 min).',
  },
  {
    slug: 'maritiem-museum',
    plek: 'Maritiem Museum',
    vraag: 'Naar het Maritiem Museum?',
    parkings: [
      {locatie: 'hofplein', tijd: '12 min.', dx: -240, dy: 828, route: [[-255,800],[-240,793],[-234,794],[-218,748],[-218,742],[-237,700],[-221,647],[-224,640],[-216,623],[-156,426],[-152,423],[-146,402],[-147,397],[-122,312],[-94,193],[-94,177],[-88,175],[-85,165],[-86,154],[-72,125],[-61,109],[-62,106],[-37,67],[-28,70],[-8,4],[-6,5],[-4,-1],[0,0]]},
    ],
    kaart: {src: 'kaarten/maritiem-museum.jpg', x0: -1428, y0: 1728, w: 2600, h: 2629},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Maritiem Museum: Hofplein 892 m (11,9 min).',
  },
  {
    slug: 'pathe-schouwburgplein',
    plek: 'Pathé Schouwburgplein',
    vraag: 'Naar de film in Rotterdam?',
    parkings: [
      {locatie: 'hofplein', tijd: '10 min.', dx: 353, dy: 464, route: [[338,435],[353,428],[359,429],[374,383],[375,378],[356,336],[313,321],[305,321],[313,297],[308,290],[310,284],[298,279],[191,185],[43,135],[55,98],[51,97],[50,92],[2,75],[6,62],[-35,48],[-21,11],[-10,-6],[0,0]]},
    ],
    kaart: {src: 'kaarten/pathe-schouwburgplein.jpg', x0: -1135, y0: 1364, w: 2610, h: 2270},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Pathé Schouwburgplein: Hofplein 750 m (10,0 min).',
  },
  {
    slug: 'carre',
    plek: 'Carré',
    vraag: 'Naar Carré?',
    parkings: [
      {locatie: 'plantage', tijd: '13 min.', dx: 588, dy: 511, route: [[576,519],[544,464],[530,447],[477,353],[483,350],[459,306],[486,203],[-26,49],[-10,-3],[0,0]]},
    ],
    kaart: {src: 'kaarten/carre.jpg', x0: -1126, y0: 1419, w: 2814, h: 2322},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Koninklijk Theater Carré: Plantage 950 m (12,7 min).',
  },
  {
    slug: 'nemo',
    plek: 'NEMO',
    vraag: 'Naar NEMO?',
    parkings: [
      {locatie: 'plantage', tijd: '14 min.', dx: 32, dy: -762, route: [[19,-755],[85,-645],[88,-636],[88,-627],[130,-556],[66,-519],[86,-482],[74,-475],[82,-467],[-12,-414],[-14,-406],[-41,-381],[21,-315],[9,-309],[7,-298],[2,-294],[12,-275],[-11,-261],[-13,-253],[-21,-244],[-7,-216],[19,-137],[33,-75],[36,-17],[-7,-13],[-6,0],[0,0]]},
    ],
    kaart: {src: 'kaarten/nemo.jpg', x0: -1256, y0: 900, w: 2600, h: 2562},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar NEMO: Plantage 1018 m (13,6 min).',
  },
  {
    slug: 'scheepvaartmuseum',
    plek: 'Het Scheepvaartmuseum',
    vraag: 'Naar het Scheepvaartmuseum?',
    parkings: [
      {locatie: 'plantage', tijd: '13 min.', dx: -161, dy: -558, route: [[-174,-550],[-108,-440],[-105,-432],[-105,-423],[-63,-352],[-128,-315],[-107,-278],[-120,-271],[-111,-263],[-184,-220],[-185,-222],[-205,-209],[-207,-202],[-143,-135],[-129,-117],[-132,-115],[-122,-106],[-104,-111],[-79,-128],[-60,-126],[-15,-97],[16,-70],[103,-29],[91,-7],[59,-25],[42,-5],[21,-16],[0,0]]},
    ],
    kaart: {src: 'kaarten/scheepvaartmuseum.jpg', x0: -1352, y0: 900, w: 2600, h: 2358},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Het Scheepvaartmuseum: Plantage 997 m (13,3 min).',
  },
  {
    slug: 'opera-ballet',
    plek: 'Nationale Opera & Ballet',
    vraag: 'Naar de Opera?',
    parkings: [
      {locatie: 'plantage', tijd: '12 min.', dx: 768, dy: -66, route: [[755,-58],[720,-118],[563,-30],[554,-47],[543,-48],[529,-36],[504,-27],[471,-32],[440,-46],[426,-49],[409,-47],[253,39],[142,-37],[134,-38],[132,-33],[100,-9],[90,-23],[62,-4],[36,-42],[31,-39],[40,-27],[0,0]]},
    ],
    kaart: {src: 'kaarten/opera-ballet.jpg', x0: -1100, y0: 1060, w: 2968, h: 2200},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Nationale Opera & Ballet: Plantage 911 m (12,2 min).',
  },
  {
    slug: 'kunstlinie',
    plek: 'Kunstlinie',
    vraag: 'Naar de Kunstlinie?',
    parkings: [
      {locatie: 'p2-mandela-wtc', tijd: '17 min.', dx: 65, dy: 1056, route: [[63,1055],[61,1058],[60,1044],[46,1040],[57,1002],[49,1000],[50,997],[7,962],[8,959],[0,957],[112,513],[97,510],[61,375],[58,319],[41,235],[23,180],[17,178],[12,169],[18,139],[6,65],[-68,54],[-67,39],[-61,40],[-48,-12],[0,0]]},
      {locatie: 'p1-carlton-wtc', tijd: '17 min.', dx: -192, dy: 1025, route: [[-189,1017],[-182,984],[-105,1003],[-100,983],[-122,947],[-108,939],[-91,878],[-110,873],[-112,857],[-103,845],[-104,828],[-98,801],[-137,790],[-105,646],[-60,473],[-67,472],[-48,396],[-81,390],[-88,320],[-88,303],[-84,300],[-91,242],[-98,240],[-75,152],[-81,152],[-77,121],[-72,117],[-67,39],[-61,40],[-48,-12],[0,0]]},
    ],
    kaart: {src: 'kaarten/kunstlinie.jpg', x0: -1340, y0: 1958, w: 2600, h: 2870},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Kunstlinie: P2 Mandela WTC 1241 m (16,5 min); P1 Carlton WTC 1280 m (17,1 min). P2 Mandela: €6 per dag is een open check (IG-013).',
  },
  {
    slug: 'flevoziekenhuis',
    plek: 'Flevoziekenhuis',
    vraag: 'Naar het Flevoziekenhuis?',
    parkings: [
      {locatie: 'p2-mandela-wtc', tijd: '15 min.', dx: -223, dy: 819, route: [[-225,818],[-227,820],[-228,806],[-242,803],[-231,765],[-240,763],[-239,760],[-281,725],[-280,722],[-288,720],[-204,378],[-155,190],[-125,192],[-112,132],[-95,102],[27,134],[52,128],[67,129],[73,116],[87,54],[86,45],[79,40],[82,28],[75,16],[68,14],[67,16],[0,0]]},
      {locatie: 'p1-carlton-wtc', tijd: '16 min.', dx: -480, dy: 788, route: [[-478,780],[-470,747],[-393,766],[-389,745],[-370,749],[-368,742],[-346,727],[-296,722],[-295,718],[-288,720],[-204,378],[-155,190],[-125,192],[-112,132],[-95,102],[27,134],[52,128],[67,129],[73,116],[87,54],[86,45],[79,40],[82,28],[75,16],[68,14],[67,16],[0,0]]},
    ],
    kaart: {src: 'kaarten/flevoziekenhuis.jpg', x0: -1580, y0: 1720, w: 2767, h: 2620},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Flevoziekenhuis: P2 Mandela WTC 1130 m (15,1 min); P1 Carlton WTC 1230 m (16,4 min). P2 Mandela: €6 per dag is een open check (IG-013).',
  },
  {
    slug: 'theater-aan-de-schie',
    plek: 'Theater aan de Schie',
    vraag: 'Naar Theater aan de Schie?',
    parkings: [
      {locatie: 'pr-schiedam-centrum', tijd: '10 min.', dx: 105, dy: 634, route: [[76,599],[41,628],[34,614],[24,580],[16,526],[-65,237],[-62,228],[-72,160],[-83,140],[-81,73],[-72,41],[-26,42],[-24,-1],[0,0]]},
    ],
    kaart: {src: 'kaarten/theater-aan-de-schie.jpg', x0: -1289, y0: 1534, w: 2600, h: 2435},
    bron: 'Looproutes OpenStreetMap (26-11-2026) naar Theater aan de Schie: P+R Schiedam Centrum 747 m (10,2 min).',
  },
  {
    slug: 'maassilo',
    plek: 'Maassilo',
    vraag: 'Naar de Maassilo?',
    parkings: [
      {locatie: 'maashaven', tijd: '7 min.', dx: -372, dy: -139, prijs: {bedrag: '€25', eenheid: 'per dag gereserveerd'}, route: [[-386,-143],[-394,-119],[-425,-130],[-428,-122],[-7,20],[0,0]]},
    ],
    kaart: {src: 'kaarten/maassilo.jpg', x0: -1528, y0: 1038, w: 2628, h: 2200},
    bron: 'Looproute OpenStreetMap (27-11-2026) van Maashaven Zuidzijde 100 naar Maassilo: 513 m (6,8 min). Looptijd 7 min. volgens de locatiepagina; dagtarief met reservering €25. Maashaven open ma-vr 07-23, za 09-18, zo 09-17. Niet voor late evenementen.',
  },
  {
    slug: 'art-hotel-rotterdam',
    plek: 'Art Hotel Rotterdam',
    vraag: 'Naar Art Hotel Rotterdam?',
    parkings: [
      {locatie: 'maashaven', tijd: '8 min.', dx: -301, dy: -3, prijs: {bedrag: '€25', eenheid: 'per dag gereserveerd'}, route: [[-315,-7],[-323,17],[-354,7],[-357,14],[-227,57],[-209,4],[-195,8],[-190,-5],[-172,2],[-169,-6],[-130,6],[-124,-7],[-114,-10],[-103,-19],[-37,-75],[7,-5],[0,0]]},
    ],
    kaart: {src: 'kaarten/art-hotel-rotterdam.jpg', x0: -1475, y0: 1091, w: 2600, h: 2200},
    bron: 'Looproute OpenStreetMap (27-11-2026) van Maashaven Zuidzijde 100 naar Art Hotel Rotterdam: 569 m (7,6 min). Dagtarief met reservering €25, zonder €50; de eerste twee uur zijn niet meer gratis (Rick, 27-11-2026). Maashaven open ma-vr 07-23, za 09-18, zo 09-17. Overnachten met de auto in de garage: niet bevestigd.',
  },
  {
    slug: 'spelen-bij-beelen',
    plek: 'Spelen bij Beelen',
    vraag: 'Dagje Spelen bij Beelen?',
    parkings: [
      {locatie: 'maashaven', tijd: '16 min.', dx: 1063, dy: 221, prijs: {bedrag: '€25', eenheid: 'per dag gereserveerd'}, route: [[1049,217],[1041,241],[1010,231],[1007,238],[967,224],[965,222],[954,222],[906,205],[886,162],[778,103],[693,70],[144,-114],[125,-124],[93,-122],[35,-107],[5,-92],[-40,-62],[0,0]]},
    ],
    kaart: {src: 'kaarten/spelen-bij-beelen.jpg', x0: -1140, y0: 1158, w: 3303, h: 2200},
    bron: 'Looproute OpenStreetMap (27-11-2026) van Maashaven Zuidzijde 100 naar Spelen bij Beelen: 1222 m (16,4 min). Dagtarief met reservering €25, zonder €50; de eerste twee uur zijn niet meer gratis (Rick, 27-11-2026). Maashaven open ma-vr 07-23, za 09-18, zo 09-17.',
  },
];
