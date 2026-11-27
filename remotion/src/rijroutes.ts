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
  {
    slug: 'p2-mandela-wtc',
    locatie: 'p2-mandela-wtc',
    vraag: 'Waar is de inrit van P2 Mandela WTC?',
    route: [[343,112],[339,112],[333,108],[329,105],[327,102],[324,96],[324,90],[324,87],[318,80],[302,70],[285,61],[226,45],[156,28],[137,23],[112,17],[67,6],[56,1],[51,13],[45,35],[42,48],[15,42],[8,41],[6,38],[4,36],[4,33],[5,30],[11,9],[12,6],[12,3],[10,-2],[8,-7],[2,-8]],
    lengte: 460,
    stappen: [
      {tekst: 'Via de Drossaardlaan', label: 'Drossaardlaan', x: 343, y: 112, pijl: 'rechtdoor'},
      {tekst: 'Rechtsaf de Rooseveltweg op', label: 'Rechtsaf', x: 56, y: 1, pijl: 'rechts'},
      {tekst: 'Linksaf de Mandelastraat op', label: 'Linksaf', x: 42, y: 48, pijl: 'links'},
      {tekst: 'Inrit van Parking P2 Mandela WTC', label: 'Inrit', x: 0, y: 0, pijl: 'inrit'},
    ],
    kaart: {src: 'kaarten/rij-p2-mandela-wtc.jpg', x0: -729, y0: 852, w: 1800, h: 1600},
    bron: 'Inrit op de locatiepagina. Autoroute OpenStreetMap (27-11-2026), laatste 460 meter; de routes uit alle vier richtingen volgen dit stuk.',
  },
  {
    slug: 'plantage',
    locatie: 'plantage',
    vraag: 'Waar is de inrit van Parking Plantage?',
    route: [[-323,-401],[-290,-391],[-112,-338],[-110,-338],[-110,-335],[-110,-331],[-111,-324],[-111,-321],[-112,-318],[-112,-315],[-117,-298],[-132,-249],[-133,-246],[-134,-242],[-134,-239],[-134,-235],[-134,-232],[-133,-230],[-133,-226],[-131,-223],[-130,-220],[-129,-218],[-125,-211],[-110,-184],[-62,-101],[-61,-99],[-58,-94],[-56,-90],[-53,-87],[-52,-86],[-51,-85],[-49,-81],[-46,-78],[-45,-77],[-42,-73],[-34,-60],[0,0]],
    lengte: 600,
    stappen: [
      {tekst: 'Via de Nieuwe Prinsengracht', label: 'Nieuwe Prinsengracht', x: -323, y: -401, pijl: 'rechtdoor'},
      {tekst: 'Linksaf de Roetersstraat op', label: 'Linksaf', x: -110, y: -338, pijl: 'links'},
      {tekst: 'Rechtdoor de Plantage Kerklaan op', label: 'Plantage Kerklaan', x: -133, y: -226, pijl: 'rechtdoor'},
      {tekst: 'Inrit van Parking Plantage', label: 'Inrit', x: 0, y: 0, pijl: 'inrit'},
    ],
    kaart: {src: 'kaarten/rij-plantage.jpg', x0: -1062, y0: 600, w: 1800, h: 1601},
    bron: 'Inrit op de locatiepagina. Autoroute OpenStreetMap (27-11-2026), laatste 600 meter; route vanuit het centrum en het zuiden (via de Roetersstraat); vanuit het noorden en oosten kom je via de Plantage Middenlaan.',
  },
  {
    slug: 'philips-bedrijfsschool',
    locatie: 'philips-bedrijfsschool',
    vraag: 'Waar is de inrit van de Philips Bedrijfsschool?',
    route: [[158,286],[134,268],[122,257],[119,255],[116,252],[106,243],[96,234],[87,226],[79,218],[76,216],[70,209],[55,192],[49,177],[38,150],[25,134],[12,119],[10,116],[-1,103],[-18,91],[-21,90],[-23,90],[-28,88],[-24,79],[-20,72],[-19,70],[-18,69],[-15,60],[-14,57],[-13,54],[-12,50],[-12,36],[-12,8],[-11,0],[0,0]],
    lengte: 380,
    stappen: [
      {tekst: 'Via de Glaslaan', label: 'Glaslaan', x: 158, y: 286, pijl: 'rechtdoor'},
      {tekst: 'Linksaf de Essenstraat op', label: 'Linksaf', x: -28, y: 88, pijl: 'links'},
      {tekst: 'Linksaf de Frederiklaan op', label: 'Linksaf', x: -11, y: 0, pijl: 'links'},
      {tekst: 'Inrit van Parking Philips Bedrijfsschool', label: 'Inrit', x: 0, y: 0, pijl: 'inrit'},
    ],
    kaart: {src: 'kaarten/rij-philips-bedrijfsschool.jpg', x0: -835, y0: 943, w: 1800, h: 1600},
    bron: 'Inrit op de locatiepagina. Autoroute OpenStreetMap (27-11-2026), laatste 380 meter; route vanuit het noorden en oosten; vanuit het westen kom je ook via de Essenstraat. Tweede inrit aan de Berkenstraat.',
  },
  {
    slug: 'dll-garage',
    locatie: 'dll-garage',
    vraag: 'Waar is de inrit van de DLL-garage?',
    route: [[132,-281],[128,-270],[122,-258],[118,-251],[112,-241],[104,-231],[100,-224],[93,-216],[84,-205],[77,-197],[72,-193],[70,-189],[60,-181],[54,-179],[46,-172],[42,-170],[32,-161],[25,-155],[1,-136],[-8,-129],[-29,-111],[-49,-92],[-57,-83],[-64,-75],[-78,-57],[-90,-38],[-95,-27],[-100,-17],[-109,4],[-108,15],[-107,17],[-105,22],[-102,26],[-98,31],[-92,33],[-75,40],[-72,39],[-63,34],[-43,24],[-4,2],[0,0]],
    lengte: 520,
    stappen: [
      {tekst: 'Via de Vestdijk', label: 'Vestdijk', x: 132, y: -281, pijl: 'rechtdoor'},
      {tekst: 'Rechtsaf de Kanaalstraat op', label: 'Rechtsaf', x: -109, y: 4, pijl: 'rechts'},
      {tekst: 'Inrit van Parking DLL (Garage)', label: 'Inrit', x: 0, y: 0, pijl: 'inrit'},
    ],
    kaart: {src: 'kaarten/rij-dll-garage.jpg', x0: -889, y0: 679, w: 1800, h: 1600},
    bron: 'Inrit op de locatiepagina. Autoroute OpenStreetMap (27-11-2026), laatste 520 meter; route vanuit het zuiden en westen (via de Vestdijk); vanuit het noorden en oosten kom je via de Kanaaldijk-Zuid.',
  },
  {
    slug: 'dll-parkeerdek',
    locatie: 'dll-parkeerdek',
    vraag: 'Waar is de inrit van het DLL-parkeerdek?',
    route: [[132,-281],[128,-270],[122,-258],[118,-251],[112,-241],[104,-231],[100,-224],[93,-216],[84,-205],[77,-197],[72,-193],[70,-189],[60,-181],[54,-179],[46,-172],[42,-170],[32,-161],[25,-155],[1,-136],[-8,-129],[-29,-111],[-49,-92],[-57,-83],[-64,-75],[-78,-57],[-90,-38],[-95,-27],[-100,-17],[-109,4],[-108,15],[-107,17],[-105,22],[-102,26],[-98,31],[-92,33],[-75,40],[-72,39],[-63,34],[-43,24],[-4,2],[0,0]],
    lengte: 520,
    stappen: [
      {tekst: 'Via de Vestdijk', label: 'Vestdijk', x: 132, y: -281, pijl: 'rechtdoor'},
      {tekst: 'Rechtsaf de Kanaalstraat op', label: 'Rechtsaf', x: -109, y: 4, pijl: 'rechts'},
      {tekst: 'Inrit van Parking DLL parkeerdek', label: 'Inrit', x: 0, y: 0, pijl: 'inrit'},
    ],
    kaart: {src: 'kaarten/rij-dll-garage.jpg', x0: -889, y0: 679, w: 1800, h: 1600},
    bron: 'Inrit op de locatiepagina. Autoroute OpenStreetMap (27-11-2026), laatste 520 meter; zelfde inrit als de DLL-garage, aan de Kanaalstraat; route vanuit het zuiden en westen (via de Vestdijk).',
  },
];
