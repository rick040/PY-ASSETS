// Checklist spots (LijstSpot, "Het lijstje"): a question, four points that get ticked one by one,
// then the location (photo, name, price) and the shared CTA. One location per video.
// Every point must be on the location page (see locaties.ts `bron`). Text between [ ] is bold.

export type Lijstje = {
  slug: string;
  /** Location slug from locaties.ts. */
  locatie: string;
  /** Bold question at the top: the hook. */
  vraag: string;
  /** Light line under the question (default: "Hier parkeer je zonder zorgen:"). */
  sub?: string;
  /** Exactly four points, short enough for one line. */
  punten: [string, string, string, string];
  /** Source of the points, or what to check. */
  bron?: string;
};

export const lijstjes: Lijstje[] = [
  {
    slug: 'plantage',
    locatie: 'plantage',
    vraag: "Dagje Artis?",
    punten: ["Direct [naast Artis]", "[24/7] open", "[483] parkeerplaatsen", "Dagkaart Artis: [€17,50]"],
    bron: "Parking Plantage: \"direct naast Artis\", 483 plekken, 24/7 open, dagkaart bezoekers Artis €17,50.",
  },
  {
    slug: 'cruquius',
    locatie: 'cruquius',
    vraag: "Naar Amsterdam Oost?",
    punten: ["[24/7] open", "[Overdekte] garage", "Zondag [€1,30] per half uur", "[Lift] en rolstoeltoegang"],
    bron: "Cruquius: 24/7, overdekt, zondag €1,30 per 30 min, lift en rolstoeltoegang.",
  },
  {
    slug: 'zeeburgerkade',
    locatie: 'zeeburgerkade',
    vraag: "Dagje Amsterdam Oost?",
    punten: ["[Overdekte] garage", "[24/7] open", "[120] parkeerplaatsen", "Dagtarief vooraf: [€17,50]"],
    bron: "Zeeburgerkade: overdekt, 24 uur, 120 plaatsen, dagtarief vroegboekkorting €17,50.",
  },
  {
    slug: 'bos-en-lommerplantsoen',
    locatie: 'bos-en-lommerplantsoen',
    vraag: "Amsterdam zonder stress?",
    punten: ["[15 min.] tram naar centrum", "[24/7] open", "[168] parkeerplaatsen", "[Elektrisch] laden"],
    bron: "Bos en Lommerplantsoen: 15 min met de tram naar het centrum, 24/7, 168 plaatsen, laadpalen.",
  },
  {
    slug: 'b-amsterdam-b1',
    locatie: 'b-amsterdam-b1',
    vraag: "Naar B. Amsterdam?",
    punten: ["[853] parkeerplaatsen", "[24/7] open", "Max. [€15] per dag", "[Elektrisch] laden"],
    bron: "B1: 853 plaatsen, 24/7, max. dagtarief €15, laadpalen.",
  },
  {
    slug: 'hofplein',
    locatie: 'hofplein',
    vraag: "Dagje Rotterdam?",
    punten: ["[8 min.] van het centrum", "[24/7] open", "[Overdekte] garage", "Weekend max. [€15] per dag"],
    bron: "Hofplein: 8 min tot centrum, 24/7, overdekt, max. dagtarief za en zo €15.",
  },
  {
    slug: 'shopping-center',
    locatie: 'shopping-center',
    vraag: "Shoppen in Alexandrium?",
    punten: ["[3 min.] van het centrum", "[24/7] open", "[Overdekte] garage", "Dagtarief vooraf: [€9]"],
    bron: "Shopping Center: 3 min tot centrum, 24/7, overdekt, dagtarief vroegboekkorting €9.",
  },
  {
    slug: 'europoint',
    locatie: 'europoint',
    vraag: "Naar The Lee Towers?",
    punten: ["[24/7] open", "[Overdekte] garage", "Max. [€15] per dag", "[Cameratoezicht]"],
    bron: "Europoint: 24/7, overdekt, max. dagtarief €15, cameratoezicht.",
  },
  {
    slug: 'diergaarde-blijdorp',
    locatie: 'diergaarde-blijdorp',
    vraag: "Dagje Blijdorp?",
    punten: ["[2 min.] naar de dierentuin", "[1200] parkeerplaatsen", "[24/7] open", "[Elektrisch] laden"],
    bron: "Diergaarde Blijdorp: 2 min tot de dierentuin, 1200 plaatsen, 24/7, laadpalen.",
  },
  {
    slug: 'maashaven',
    locatie: 'maashaven',
    vraag: "Feestje in de Maassilo?",
    punten: ["[7 min.] naar de Maassilo", "[95] parkeerplaatsen", "Dagtarief vooraf: [€25]", "[Rolstoel]toegankelijk"],
    bron: "Maashaven: 7 min tot Maassilo, 95 plaatsen, dagtarief met reservering €25, rolstoeltoegankelijk.",
  },
  {
    slug: 'td-gebouw',
    locatie: 'td-gebouw',
    vraag: "Dagje Eindhoven?",
    punten: ["[10 min.] van het centrum", "[24/7] open", "[97] parkeerplaatsen", "Dagtarief vooraf: [€12]"],
    bron: "TD-gebouw: 10 min tot centrum, 24/7, 97 plaatsen, dagtarief vroegboekkorting €12.",
  },
  {
    slug: 'philips-stadion',
    locatie: 'philips-stadion',
    vraag: "Voordelig in Eindhoven?",
    punten: ["[700] parkeerplaatsen", "[9 min.] van het centrum", "[24/7] open", "Dagtarief vooraf: [€12,50]"],
    bron: "Philips Stadion: 700 plaatsen, 9 min tot centrum, 24/7, dagtarief met reservering €12,50. Niet bij wedstrijden en grote evenementen.",
  },
  {
    slug: 'philips-bedrijfsschool',
    locatie: 'philips-bedrijfsschool',
    vraag: "Eindhoven op loopafstand?",
    punten: ["[10 min.] van het centrum", "[176] parkeerplaatsen", "[24/7] open", "Na 21:00 [€0,65] / 20 min."],
    bron: "Philips Bedrijfsschool: 10 min tot centrum, 176 plaatsen, 24/7, 21-09u €0,65 per 20 min.",
  },
  {
    slug: 'victoriapark',
    locatie: 'victoriapark',
    vraag: "Avondje Eindhoven?",
    punten: ["[2 min.] van het centrum", "[24/7] open", "Max. [€5] per nacht", "[Elektrisch] laden"],
    bron: "Victoriapark: 2 min tot centrum, 24/7, nachttarief max. €5, laadpalen.",
  },
  {
    slug: 'dll-garage',
    locatie: 'dll-garage',
    vraag: "Uit eten in Eindhoven?",
    punten: ["[4 min.] van het centrum", "[Overdekte] garage", "Ma-vr open vanaf [17:00]", "[284] parkeerplaatsen"],
    bron: "DLL Garage: 4 min tot centrum, overdekt, ma-vr 17:00-06:00, 284 plaatsen.",
  },
  {
    slug: 'dll-parkeerdek',
    locatie: 'dll-parkeerdek',
    vraag: "'s Avonds de stad in?",
    punten: ["[4 min.] van het centrum", "[125] parkeerplaatsen", "Ma-vr open vanaf [17:00]", "Dagtarief vooraf: [€12]"],
    bron: "DLL parkeerdek: 4 min tot centrum, 125 plaatsen, ma-vr 17:00-06:00, dagtarief vroegboekkorting €12.",
  },
  {
    slug: 'evoluon',
    locatie: 'evoluon',
    vraag: "Naar het Evoluon?",
    punten: ["[2 min.] naar het Evoluon", "[350] parkeerplaatsen", "[24/7] open", "Dagtarief vooraf: [€9]"],
    bron: "Evoluon: 2 min tot Evoluon, 350 plaatsen, 24/7, dagtarief met reservering €9.",
  },
  {
    slug: 'at-the-park',
    locatie: 'at-the-park',
    vraag: "Naar Rijswijk?",
    punten: ["[7 min.] naar het station", "[24/7] open", "Dagtarief vooraf: [€7]", "[Elektrisch] laden"],
    bron: "At the Park: 7 min tot station, 24/7, dagtarief vroegboekkorting €7, laadpalen.",
  },
  {
    slug: 'stationsweg-ypenburg',
    locatie: 'stationsweg-ypenburg',
    vraag: "Filmavond in Ypenburg?",
    punten: ["Direct [naast Pathé]", "Filmbezoek: [4 uur €4,75]", "[425] parkeerplaatsen", "Direct [naast het station]"],
    bron: "Stationsweg Ypenburg: naast Pathé, Pathé-bezoekers 0-4 uur €4,75, 425 plaatsen, direct naast station. Pathé alleen als tekst.",
  },
  {
    slug: 'pr-schiedam-centrum',
    locatie: 'pr-schiedam-centrum',
    vraag: "Met de trein verder?",
    punten: ["[4 min.] naar het station", "[Overdekte] garage", "[Cameratoezicht]", "Max. [€23] per dag"],
    bron: "P+R Schiedam Centrum: 4 min tot Schiedam Centraal, overdekt, cameratoezicht, max. dagtarief €23.",
  },
  {
    slug: 'lentse-plas',
    locatie: 'lentse-plas',
    vraag: "Film of zwemmen in Nijmegen?",
    punten: ["Naast [Pathé Nijmegen]", "Filmbezoek: [4 uur €3,75]", "[24/7] open", "Max. [€21,50] per dag"],
    bron: "Lentse plas: naast Pathé Nijmegen, Pathé-bezoekers 0-4 uur €3,75, 24/7, max. €21,50 per dag. Check IG-024.",
  },
  {
    slug: 'pathe-ede',
    locatie: 'pathe-ede',
    vraag: "Naar de film in Ede?",
    punten: ["Direct [naast Pathé]", "Filmbezoek: [4 uur €4,50]", "Vlak bij de [A12]", "[Elke dag] open"],
    bron: "Pathé Ede: naast Pathé, Pathé-bezoekers max. 4 uur €4,50, bij de A12, elke dag open. Pathé alleen als tekst.",
  },
  {
    slug: 'heerhugowaard-p1-zuidtangent',
    locatie: 'heerhugowaard-p1-zuidtangent',
    vraag: "Shoppen in Middenwaard?",
    punten: ["Direct [bij de winkels]", "Max. [€9] per dag", "[Elektrisch] laden", "[Cameratoezicht]"],
    bron: "P1 Zuidtangent: direct bij winkelcentrum, max. dagtarief €9, laadpalen, cameratoezicht.",
  },
  {
    slug: 'p2-middenwaard',
    locatie: 'p2-middenwaard',
    vraag: "Dagje Heerhugowaard?",
    punten: ["Midden in het [centrum]", "[24/7] open", "Max. [€9] per dag", "[Elektrisch] laden"],
    bron: "P2 Middenwaard: centrum, 24/7, max. dagtarief €9, laadpalen.",
  },
  {
    slug: 'p1-belgielaan',
    locatie: 'p1-belgielaan',
    vraag: "Shoppen in het Stadshart?",
    punten: ["[2 min.] naar het Stadshart", "Daarna [€3] per uur", "Dagtarief [€16]", "[Elektrisch] laden"],
    bron: "P1 Belgielaan: 2 min tot Stadshart, eerste 2 uur gratis, daarna €3 per uur, dagtarief €16, laadpalen. Check IG-014: eerste 2 uur gratis bevestigen.",
  },
  {
    slug: 'p2-bovenlangs',
    locatie: 'p2-bovenlangs',
    vraag: "Dagje Zoetermeer?",
    punten: ["[2 min.] naar het Stadshart", "Daarna [€3] per uur", "Dagtarief [€16]", "[Elektrisch] laden"],
    bron: "P2 Bovenlangs: 2 min tot Stadshart, eerste 2 uur gratis, daarna €3 per uur, dagtarief €16, laadpalen. Check IG-014: eerste 2 uur gratis bevestigen.",
  },
  {
    slug: 'p2-onderlangs',
    locatie: 'p2-onderlangs',
    vraag: "Even naar het Stadshart?",
    punten: ["[2 min.] naar de winkels", "Daarna [€3] per uur", "Dagtarief [€16]", "[Elektrisch] laden"],
    bron: "P2 Onderlangs: 2 min tot Stadshart, eerste 2 uur gratis, daarna €3 per uur, dagtarief €16, laadpalen. Check IG-014: eerste 2 uur gratis bevestigen.",
  },
  {
    slug: 'p4-luxemburglaan',
    locatie: 'p4-luxemburglaan',
    vraag: "Boodschappen in Zoetermeer?",
    punten: ["[2 min.] naar het Stadshart", "Daarna [€3] per uur", "Dagtarief [€16]", "[Elektrisch] laden"],
    bron: "P4 Luxemburglaan: 2 min tot Stadshart, eerste 2 uur gratis, daarna €3 per uur, dagtarief €16, laadpalen. Check IG-014: eerste 2 uur gratis bevestigen.",
  },
  {
    slug: 'p5-amsterdamstraat',
    locatie: 'p5-amsterdamstraat',
    vraag: "Shoppen in Zoetermeer?",
    punten: ["[2 min.] naar het Stadshart", "Daarna [€3] per uur", "Dagtarief [€16]", "[Elektrisch] laden"],
    bron: "P5 Amsterdamstraat: 2 min tot Stadshart, eerste 2 uur gratis, daarna €3 per uur, dagtarief €16, laadpalen. Check IG-014: eerste 2 uur gratis bevestigen.",
  },
  {
    slug: 'p8-nederlandlaan',
    locatie: 'p8-nederlandlaan',
    vraag: "Snel naar het Stadshart?",
    punten: ["[2 min.] naar de winkels", "Daarna [€3] per uur", "Dagtarief [€16]", "Uitrijden [24/7]"],
    bron: "P8 Nederlandlaan: 2 min tot Stadshart, eerste 2 uur gratis, daarna €3 per uur, dagtarief €16, uitrijden 24/7. Check IG-014: eerste 2 uur gratis bevestigen.",
  },
  {
    slug: 'p9-duitslandlaan',
    locatie: 'p9-duitslandlaan',
    vraag: "Middagje Stadshart?",
    punten: ["[2 min.] naar de winkels", "Daarna [€3] per uur", "Dagtarief [€16]", "Uitrijden [24/7]"],
    bron: "P9 Duitslandlaan: 2 min tot Stadshart, eerste 2 uur gratis, daarna €3 per uur, dagtarief €16, uitrijden 24/7. Check IG-014: eerste 2 uur gratis bevestigen.",
  },
  {
    slug: 'p1-carlton-wtc',
    locatie: 'p1-carlton-wtc',
    vraag: "Dagje Almere centrum?",
    punten: ["[4 min.] van het centrum", "[Overdekte] garage", "[24/7] open", "[125] parkeerplaatsen"],
    bron: "P1 Carlton WTC: 4 min tot centrum, overdekt, 24/7, 125 plaatsen.",
  },
  {
    slug: 'p2-mandela-wtc',
    locatie: 'p2-mandela-wtc',
    vraag: "Hele dag in Almere?",
    punten: ["[4 min.] van het centrum", "[Overdekte] garage", "[24/7] open", "[250] parkeerplaatsen"],
    bron: "P2 Mandela WTC: 4 min tot centrum, overdekt, 24/7, 250 plaatsen. Prijs €6 per dag: check IG-013.",
  },
  {
    slug: 'houthavenkade',
    locatie: 'houthavenkade',
    vraag: "Dagje Zaandam?",
    punten: ["[6 min.] van het centrum", "[24/7] open", "Na 18:00 [€1] per uur", "[Elektrisch] laden"],
    bron: "Houthavenkade: 6 min tot centrum, 24/7, 18-09u €1 per uur, laadpalen.",
  },
];
