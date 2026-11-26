// Signpost spots (BordSpot, "Het bordje"): one location per video, a street sign with four nearby places and the walking time.
// Walking times: foot route from the parking address via OpenStreetMap (routing.openstreetmap.de, foot profile), rounded
// to whole minutes. Arrows point the compass way from the parking to the place (up = north, 8 directions), not the route.
// Where the location page states a walking time (Artis, Maassilo, Evoluon, Stadshart ...), that time is used instead.
// Partner names (Artis, PSV, Pathé) as text only, no logos. Left out: Lentse plas and Pathé Ede (only the cinema itself
// is within about 20 minutes' walk).

export type Bord = {
  /** Name of the place on the sign. */
  naar: string;
  /** Walking time as shown, for example "6 min." or "naast de deur". */
  tijd: string;
  /** Compass bearing from the parking to the place in degrees (0 = north), drawn as one of 8 arrows. */
  richting: number;
};

export type Bordje = {
  slug: string;
  /** Location slug from locaties.ts. */
  locatie: string;
  /** Question at the top, from frame 0. */
  vraag: string;
  /** Line under the question. Default "Alles op loopafstand:". */
  sub?: string;
  /** Three or four places, nearest first where possible. */
  borden: Bord[];
  /** Where each time comes from, so it can be checked. */
  bron: string;
};

export const bordjes: Bordje[] = [
  {
    slug: 'plantage',
    locatie: 'plantage',
    vraag: 'Dagje Amsterdam?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Artis', tijd: 'naast de deur', richting: 107},
      {naar: 'Verzetsmuseum', tijd: '1 min.', richting: 6},
      {naar: 'Hortus Botanicus', tijd: '6 min.', richting: 267},
      {naar: 'Waterlooplein', tijd: '12 min.', richting: 283},
    ],
    bron:
      'Artis: "direct naast de ingang van Artis" (locatiepagina). Looproutes OpenStreetMap (26-11-2026) vanaf Plantage Kerklaan 38: ' +
      'Verzetsmuseum 94 m (1,2 min), Hortus Botanicus 415 m (5,5 min), Waterlooplein 894 m (12,1 min).',
  },
  {
    slug: 'cruquius',
    locatie: 'cruquius',
    vraag: 'Naar Amsterdam Oost?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Museum Perron Oost', tijd: '8 min.', richting: 266},
      {naar: 'Javaplein', tijd: '14 min.', richting: 212},
      {naar: 'Flevopark', tijd: '15 min.', richting: 162},
      {naar: 'Brouwerij \'t IJ', tijd: '21 min.', richting: 259},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Museum Perron Oost 625 m (8,3 min); Javaplein 1066 m (14,3 min); Flevopark 1132 m (15,1 min); Brouwerij \'t IJ 1547 m (20,6 min).',
  },
  {
    slug: 'zeeburgerkade',
    locatie: 'zeeburgerkade',
    vraag: 'Dagje Amsterdam Oost?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Museum Perron Oost', tijd: '10 min.', richting: 268},
      {naar: 'Javaplein', tijd: '15 min.', richting: 222},
      {naar: 'Flevopark', tijd: '16 min.', richting: 173},
      {naar: 'Lloyd Hotel', tijd: '20 min.', richting: 303},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Museum Perron Oost 763 m (10,2 min); Javaplein 1109 m (14,8 min); Flevopark 1166 m (15,6 min); Lloyd Hotel 1478 m (19,7 min). The Harbour Club eruit: failliet (Rick, 26-11-2026).',
  },
  {
    slug: 'bos-en-lommerplantsoen',
    locatie: 'bos-en-lommerplantsoen',
    vraag: 'Naar Bos en Lommer?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Bos en Lommerplein', tijd: '2 min.', richting: 340},
      {naar: 'Erasmuspark', tijd: '4 min.', richting: 127},
      {naar: 'Metro De Vlugtlaan', tijd: '9 min.', richting: 303},
      {naar: 'Mercatorplein', tijd: '15 min.', richting: 152},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Bos en Lommerplein 153 m (2,1 min); Erasmuspark 280 m (3,7 min); Metro De Vlugtlaan 671 m (9,0 min); Mercatorplein 1114 m (15,0 min).',
  },
  {
    slug: 'b-amsterdam-b1',
    locatie: 'b-amsterdam-b1',
    vraag: 'Naar B. Amsterdam?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'B. Amsterdam', tijd: 'naast de deur', richting: 0},
      {naar: 'Metro Henk Sneevlietweg', tijd: '11 min.', richting: 46},
      {naar: 'Delflandplein', tijd: '19 min.', richting: 50},
      {naar: 'Nieuwe Meer', tijd: '20 min.', richting: 183},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. B. Amsterdam: "Kom je voor een van de bedrijven in het B. Amsterdam Business Park, dan sta je pal naast de deur" (locatiepagina); Metro Henk Sneevlietweg 804 m (10,7 min); Delflandplein 1446 m (19,3 min); Nieuwe Meer 1493 m (20,0 min).',
  },
  {
    slug: 'hofplein',
    locatie: 'hofplein',
    vraag: 'Dagje Rotterdam?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Lijnbaan', tijd: '5 min.', richting: 219},
      {naar: 'De Doelen', tijd: '8 min.', richting: 229},
      {naar: 'Rotterdam Centraal', tijd: '9 min.', richting: 259},
      {naar: 'Markthal', tijd: '13 min.', richting: 138},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Lijnbaan 373 m (5,0 min); De Doelen 606 m (8,1 min); Rotterdam Centraal 692 m (9,3 min); Markthal 962 m (12,9 min).',
  },
  {
    slug: 'shopping-center',
    locatie: 'shopping-center',
    vraag: 'Shoppen in Alexandrium?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Winkels Alexandrium', tijd: '3 min.', richting: 203},
      {naar: 'Woonmall Alexandrium', tijd: '5 min.', richting: 82},
      {naar: 'Station Alexander', tijd: '6 min.', richting: 291},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Winkels Alexandrium: "op drie minuten lopen van de winkels" (locatiepagina); Woonmall Alexandrium 396 m (5,3 min); Station Alexander 455 m (6,1 min).',
  },
  {
    slug: 'europoint',
    locatie: 'europoint',
    vraag: 'Naar Rotterdam West?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Marconiplein', tijd: '4 min.', richting: 75},
      {naar: 'Dakpark', tijd: '11 min.', richting: 124},
      {naar: 'Keilepand', tijd: '12 min.', richting: 152},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Marconiplein 314 m (4,3 min); Dakpark 842 m (11,2 min); Keilepand 863 m (11,5 min).',
  },
  {
    slug: 'diergaarde-blijdorp',
    locatie: 'diergaarde-blijdorp',
    vraag: 'Dagje Blijdorp?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Diergaarde Blijdorp', tijd: '2 min.', richting: 104},
      {naar: 'Vroesenpark', tijd: '16 min.', richting: 62},
      {naar: 'Van Nellefabriek', tijd: '20 min.', richting: 204},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Diergaarde Blijdorp: "2 min tot Diergaarde Blijdorp" (locatiepagina); Vroesenpark 1175 m (15,7 min); Van Nellefabriek 1482 m (20,0 min).',
  },
  {
    slug: 'maashaven',
    locatie: 'maashaven',
    vraag: 'Naar de Maassilo?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Maassilo', tijd: '7 min.', richting: 69},
      {naar: 'Afrikaanderplein', tijd: '14 min.', richting: 59},
      {naar: 'Theater Zuidplein', tijd: '19 min.', richting: 185},
      {naar: 'Katendrecht', tijd: '23 min.', richting: 336},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Maassilo: "Zeven minuten van de Maassilo" (locatiepagina); Afrikaanderplein 1068 m (14,4 min); Theater Zuidplein 1424 m (19,1 min); Katendrecht 1751 m (23,4 min).',
  },
  {
    slug: 'td-gebouw',
    locatie: 'td-gebouw',
    vraag: 'Dagje Eindhoven?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Van Abbemuseum', tijd: '5 min.', richting: 69},
      {naar: 'Stratumseind', tijd: '9 min.', richting: 41},
      {naar: 'Markt', tijd: '12 min.', richting: 8},
      {naar: 'Philips Stadion', tijd: '19 min.', richting: 324},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Van Abbemuseum 389 m (5,2 min); Stratumseind 650 m (8,7 min); Markt 856 m (11,5 min); Philips Stadion 1429 m (19,4 min).',
  },
  {
    slug: 'philips-stadion',
    locatie: 'philips-stadion',
    vraag: 'Eindhoven ontdekken?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Philips Stadion', tijd: 'naast de deur', richting: 122},
      {naar: 'Strijp-S', tijd: '13 min.', richting: 322},
      {naar: 'Philips Museum', tijd: '14 min.', richting: 118},
      {naar: 'Markt', tijd: '17 min.', richting: 112},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Philips Stadion: de looputgang ligt tegen het stadion (Rick, 26-11-2026); Strijp-S 993 m (13,4 min); Philips Museum 1072 m (14,4 min); Markt 1278 m (17,3 min).',
  },
  {
    slug: 'philips-bedrijfsschool',
    locatie: 'philips-bedrijfsschool',
    vraag: 'Eindhoven op loopafstand?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Philips Stadion', tijd: '7 min.', richting: 109},
      {naar: 'Strijp-S', tijd: '12 min.', richting: 334},
      {naar: 'Philips Museum', tijd: '18 min.', richting: 113},
      {naar: 'Markt', tijd: '20 min.', richting: 109},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Philips Stadion 545 m (7,3 min); Strijp-S 912 m (12,3 min); Philips Museum 1300 m (17,5 min); Markt 1507 m (20,3 min).',
  },
  {
    slug: 'victoriapark',
    locatie: 'victoriapark',
    vraag: 'Avondje Eindhoven?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Philips Museum', tijd: '4 min.', richting: 111},
      {naar: 'Markt', tijd: '8 min.', richting: 99},
      {naar: 'Philips Stadion', tijd: '8 min.', richting: 299},
      {naar: 'Station Eindhoven', tijd: '10 min.', richting: 54},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Philips Museum 272 m (3,6 min); Markt 587 m (7,8 min); Philips Stadion 557 m (7,6 min); Station Eindhoven 740 m (9,9 min).',
  },
  {
    slug: 'dll-garage',
    locatie: 'dll-garage',
    vraag: 'Uit eten in Eindhoven?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Stratumseind', tijd: '7 min.', richting: 226},
      {naar: 'Effenaar', tijd: '9 min.', richting: 347},
      {naar: 'Van Abbemuseum', tijd: '9 min.', richting: 204},
      {naar: 'Markt', tijd: '10 min.', richting: 286},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Stratumseind 518 m (6,9 min); Effenaar 646 m (8,6 min); Van Abbemuseum 686 m (9,2 min); Markt 727 m (9,7 min).',
  },
  {
    slug: 'dll-parkeerdek',
    locatie: 'dll-parkeerdek',
    vraag: '\'s Avonds de stad in?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Stratumseind', tijd: '7 min.', richting: 226},
      {naar: 'Muziekgebouw', tijd: '8 min.', richting: 279},
      {naar: 'Markt', tijd: '10 min.', richting: 286},
      {naar: 'Station Eindhoven', tijd: '13 min.', richting: 327},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Stratumseind 518 m (6,9 min); Muziekgebouw 630 m (8,4 min); Markt 727 m (9,7 min); Station Eindhoven 961 m (12,8 min).',
  },
  {
    slug: 'evoluon',
    locatie: 'evoluon',
    vraag: 'Naar het Evoluon?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Evoluon', tijd: '2 min.', richting: 0},
      {naar: 'Strijp-S', tijd: '15 min.', richting: 50},
      {naar: 'Station Strijp-S', tijd: '16 min.', richting: 43},
      {naar: 'Philips Stadion', tijd: '23 min.', richting: 98},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Evoluon: "Vanaf je auto loop je in twee minuten naar de ingang" (locatiepagina); pijl omhoog want de parking ligt op het terrein zelf; Strijp-S 1083 m (14,8 min); Station Strijp-S 1152 m (15,6 min); Philips Stadion 1709 m (23,1 min).',
  },
  {
    slug: 'at-the-park',
    locatie: 'at-the-park',
    vraag: 'Naar Rijswijk?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Station Rijswijk', tijd: '7 min.', richting: 274},
      {naar: 'In de Bogaard', tijd: '13 min.', richting: 268},
      {naar: 'Rijswijkse Schouwburg', tijd: '19 min.', richting: 2},
      {naar: 'Wilhelminapark', tijd: '21 min.', richting: 167},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Station Rijswijk: "Je loopt vanaf de garage in zeven minuten naar het station" (locatiepagina); In de Bogaard 998 m (13,4 min); Rijswijkse Schouwburg 1458 m (19,4 min); Wilhelminapark 1588 m (21,2 min).',
  },
  {
    slug: 'stationsweg-ypenburg',
    locatie: 'stationsweg-ypenburg',
    vraag: 'Filmavond in Ypenburg?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Station Ypenburg', tijd: 'naast de deur', richting: 105},
      {naar: 'Pathé Ypenburg', tijd: '2 min.', richting: 286},
      {naar: 'Leidschenveen', tijd: '19 min.', richting: 42},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Station Ypenburg: "direct naast station Ypenburg" (locatiepagina); Pathé Ypenburg 143 m (1,9 min); Leidschenveen 1432 m (19,2 min).',
  },
  {
    slug: 'pr-schiedam-centrum',
    locatie: 'pr-schiedam-centrum',
    vraag: 'Dagje Schiedam?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Station Schiedam Centrum', tijd: '4 min.', richting: 137},
      {naar: 'Theater aan de Schie', tijd: '10 min.', richting: 189},
      {naar: 'Molen De Nieuwe Palmboom', tijd: '11 min.', richting: 227},
      {naar: 'Grote Markt', tijd: '13 min.', richting: 216},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Station Schiedam Centrum: "4 min. tot Schiedam Centraal" (locatiepagina); Theater aan de Schie 747 m (10,2 min); Molen De Nieuwe Palmboom 820 m (11,1 min); Grote Markt 959 m (13,1 min).',
  },
  {
    slug: 'heerhugowaard-p1-zuidtangent',
    locatie: 'heerhugowaard-p1-zuidtangent',
    vraag: 'Shoppen in Middenwaard?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Middenwaard', tijd: 'naast de deur', richting: 153},
      {naar: 'Gemeentehuis', tijd: '4 min.', richting: 177},
      {naar: 'Station Heerhugowaard', tijd: '9 min.', richting: 353},
      {naar: 'Cool Kunst en Cultuur', tijd: '9 min.', richting: 154},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Middenwaard: "Direct bij winkelcentrum" (locatiepagina); Gemeentehuis 285 m (3,8 min); Station Heerhugowaard 647 m (8,6 min); Cool Kunst en Cultuur 701 m (9,3 min).',
  },
  {
    slug: 'p2-middenwaard',
    locatie: 'p2-middenwaard',
    vraag: 'Dagje Heerhugowaard?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Middenwaard', tijd: 'naast de deur', richting: 230},
      {naar: 'Cool Kunst en Cultuur', tijd: '2 min.', richting: 270},
      {naar: 'Stadspark De Parel', tijd: '7 min.', richting: 241},
      {naar: 'Station Heerhugowaard', tijd: '18 min.', richting: 337},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Middenwaard: "Direct bij winkelcentrum" (locatiepagina); Cool Kunst en Cultuur 123 m (1,6 min); Stadspark De Parel 532 m (7,1 min); Station Heerhugowaard 1324 m (17,7 min).',
  },
  {
    slug: 'p1-belgielaan',
    locatie: 'p1-belgielaan',
    vraag: 'Shoppen in het Stadshart?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Stadshart', tijd: '2 min.', richting: 98},
      {naar: 'Stadhuis', tijd: '7 min.', richting: 104},
      {naar: 'Stadstheater', tijd: '8 min.', richting: 82},
      {naar: 'RandstadRail Centrum-West', tijd: '9 min.', richting: 244},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Stadshart: "2 min tot Stadshart" (locatiepagina); Stadhuis 534 m (7,1 min); Stadstheater 571 m (7,6 min); RandstadRail Centrum-West 647 m (8,6 min).',
  },
  {
    slug: 'p2-bovenlangs',
    locatie: 'p2-bovenlangs',
    vraag: 'Dagje Zoetermeer?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Stadshart', tijd: '2 min.', richting: 81},
      {naar: 'Stadhuis', tijd: '6 min.', richting: 92},
      {naar: 'Stadstheater', tijd: '7 min.', richting: 69},
      {naar: 'RandstadRail Centrum-West', tijd: '11 min.', richting: 264},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Stadshart: "2 min tot Stadshart" (locatiepagina); Stadhuis 477 m (6,4 min); Stadstheater 495 m (6,6 min); RandstadRail Centrum-West 834 m (11,1 min).',
  },
  {
    slug: 'p2-onderlangs',
    locatie: 'p2-onderlangs',
    vraag: 'Even naar het Stadshart?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Stadshart', tijd: '2 min.', richting: 74},
      {naar: 'Stadhuis', tijd: '7 min.', richting: 85},
      {naar: 'Stadstheater', tijd: '7 min.', richting: 65},
      {naar: 'RandstadRail Centrum-West', tijd: '11 min.', richting: 273},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Stadshart: "2 min tot Stadshart" (locatiepagina); Stadhuis 525 m (7,0 min); Stadstheater 542 m (7,2 min); RandstadRail Centrum-West 799 m (10,6 min).',
  },
  {
    slug: 'p4-luxemburglaan',
    locatie: 'p4-luxemburglaan',
    vraag: 'Dagje Zoetermeer?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Nationaal Videogame Museum', tijd: 'naast de deur', richting: 0},
      {naar: 'Stadshart', tijd: '2 min.', richting: 167},
      {naar: 'Stadstheater', tijd: '3 min.', richting: 112},
      {naar: 'Stadhuis', tijd: '4 min.', richting: 152},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Nationaal Videogame Museum: zelfde adres als de parking, Luxemburglaan 1 (OpenStreetMap); pijl omhoog; Stadshart: "2 min tot Stadshart" (locatiepagina); Stadstheater 237 m (3,2 min); Stadhuis 301 m (4,0 min).',
  },
  {
    slug: 'p5-amsterdamstraat',
    locatie: 'p5-amsterdamstraat',
    vraag: 'Shoppen in Zoetermeer?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Stadshart', tijd: '2 min.', richting: 65},
      {naar: 'Stadhuis', tijd: '4 min.', richting: 91},
      {naar: 'Stadstheater', tijd: '5 min.', richting: 55},
      {naar: 'RandstadRail Centrum-West', tijd: '12 min.', richting: 268},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Stadshart: "2 min tot Stadshart" (locatiepagina); Stadhuis 321 m (4,3 min); Stadstheater 401 m (5,4 min); RandstadRail Centrum-West 910 m (12,1 min).',
  },
  {
    slug: 'p8-nederlandlaan',
    locatie: 'p8-nederlandlaan',
    vraag: 'Snel naar het Stadshart?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Stadshart', tijd: '2 min.', richting: 84},
      {naar: 'RandstadRail Centrum-West', tijd: '10 min.', richting: 242},
      {naar: 'Stadhuis', tijd: '10 min.', richting: 90},
      {naar: 'Stadstheater', tijd: '11 min.', richting: 76},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Stadshart: "2 min tot Stadshart" (locatiepagina); RandstadRail Centrum-West 712 m (9,5 min); Stadhuis 768 m (10,2 min); Stadstheater 848 m (11,3 min).',
  },
  {
    slug: 'p9-duitslandlaan',
    locatie: 'p9-duitslandlaan',
    vraag: 'Middagje Stadshart?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Stadstheater', tijd: '1 min.', richting: 216},
      {naar: 'Stadshart', tijd: '2 min.', richting: 226},
      {naar: 'Stadhuis', tijd: '4 min.', richting: 196},
      {naar: 'RandstadRail Centrum-West', tijd: '15 min.', richting: 253},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Stadstheater 66 m (0,9 min); Stadshart: "2 min tot Stadshart" (locatiepagina); Stadhuis 274 m (3,6 min); RandstadRail Centrum-West 1156 m (15,4 min).',
  },
  {
    slug: 'p1-carlton-wtc',
    locatie: 'p1-carlton-wtc',
    vraag: 'Dagje Almere centrum?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Station Almere Centrum', tijd: '4 min.', richting: 117},
      {naar: 'Stadhuisplein', tijd: '9 min.', richting: 149},
      {naar: 'Citadel', tijd: '12 min.', richting: 165},
      {naar: 'Kunstlinie', tijd: '17 min.', richting: 169},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Station Almere Centrum 286 m (3,8 min); Stadhuisplein 694 m (9,2 min); Citadel 910 m (12,1 min); Kunstlinie 1280 m (17,1 min).',
  },
  {
    slug: 'p2-mandela-wtc',
    locatie: 'p2-mandela-wtc',
    vraag: 'Hele dag in Almere?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Station Almere Centrum', tijd: '3 min.', richting: 202},
      {naar: 'Stadhuisplein', tijd: '8 min.', richting: 175},
      {naar: 'Citadel', tijd: '12 min.', richting: 185},
      {naar: 'Kunstlinie', tijd: '17 min.', richting: 183},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Station Almere Centrum 187 m (2,5 min); Stadhuisplein 594 m (7,9 min); Citadel 878 m (11,7 min); Kunstlinie 1241 m (16,5 min).',
  },
  {
    slug: 'houthavenkade',
    locatie: 'houthavenkade',
    vraag: 'Dagje Zaandam?',
    sub: 'Vanaf hier loop je zo naar:',
    borden: [
      {naar: 'Czaar Peterhuisje', tijd: '3 min.', richting: 41},
      {naar: 'Gedempte Gracht', tijd: '6 min.', richting: 348},
      {naar: 'Zaantheater', tijd: '7 min.', richting: 45},
      {naar: 'Station Zaandam', tijd: '11 min.', richting: 289},
    ],
    bron: 'Looproutes OpenStreetMap (26-11-2026) vanaf het adres van de parking. Czaar Peterhuisje 216 m (2,9 min); Gedempte Gracht 458 m (6,1 min); Zaantheater 525 m (7,0 min); Station Zaandam 843 m (11,2 min).',
  },
];
