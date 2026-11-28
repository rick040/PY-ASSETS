// "Vraag het maar" (VraagSpot): the FAQ from the location page as an accordion that opens question by question. Every
// question and answer comes from the "Veelgestelde vragen" block of the location page; `kern` is the fact in the answer,
// shown big, `antwoord` the rest of the answer in short.

export type Vraag = {
  vraag: string;
  /** The fact, shown big, for example "€15" or "Ja, 24 uur". */
  kern: string;
  /** The rest of the answer, short; empty when the fact says it all. */
  antwoord?: string;
};

export type VraagSet = {
  slug: string;
  /** Location slug from locaties.ts. */
  locatie: string;
  /** Three questions from the page. */
  vragen: [Vraag, Vraag, Vraag];
  /** Leave the location photo out (TD-gebouw: the only photo shows an old price board). */
  zonderFoto?: boolean;
  bron: string;
};

export const vraagsets: VraagSet[] = [
  {
    slug: 'hofplein',
    locatie: 'hofplein',
    vragen: [
      {vraag: 'Wat kost parkeren in het weekend?', kern: '€15', antwoord: 'voor een hele dag, op zaterdag en zondag.'},
      {vraag: 'Hoeveel scheelt online reserveren?', kern: '€20 in plaats van €30', antwoord: 'voor een dagkaart op werkdagen als je vroeg boekt. Met reservering €25.'},
      {vraag: 'Is er een nachttarief?', kern: 'Ja, maximaal €15', antwoord: 'tussen 00.00 en 09.00 uur.'},
    ],
    bron:
      'Locatiepagina Hofplein, Veelgestelde vragen: weekend max. €15 per dag; werkdagen dagkaart €30 zonder, €25 met reservering, €20 bij vroeg boeken; nacht 00.00-09.00 max. €15.',
  },
  {
    slug: "plantage",
    locatie: "plantage",
    vragen: [
      {vraag: "Wat kost parkeren bij Artis?", kern: "€17,50", antwoord: "voor een dagkaart als Artis-bezoeker. Artis-leden betalen €15."},
      {vraag: "Hoe ver is het lopen naar de ingang van Artis?", kern: "Direct naast Artis", antwoord: "je staat vrijwel meteen bij de ingang."},
      {vraag: "Is er 's avonds een goedkoper tarief?", kern: "Ja, €22", antwoord: "tussen 18.00 en 09.00 uur, in plaats van het dagtarief."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "bos-en-lommerplantsoen",
    locatie: "bos-en-lommerplantsoen",
    vragen: [
      {vraag: "Hoe kom ik vanaf hier in het centrum?", kern: "In ongeveer 15 min.", antwoord: "met de tram, zonder overstappen."},
      {vraag: "Wat kost een dagkaart?", kern: "€14", antwoord: "als je ruim vooraf boekt. Met reservering €16, zonder €17,50."},
      {vraag: "Kan ik hier elektrisch laden?", kern: "Ja, er zijn laadpunten", antwoord: "voor elektrische auto's."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "b-amsterdam-b1",
    locatie: "b-amsterdam-b1",
    vragen: [
      {vraag: "Wat kost een dag parkeren?", kern: "Maximaal €15", antwoord: "per dag. Per uur betaal je €2,50."},
      {vraag: "Moet ik vooraf reserveren?", kern: "Nee, direct inrijden", antwoord: "je kenteken wordt bij de slagboom herkend."},
      {vraag: "Wat is de doorrijhoogte?", kern: "2,40 meter", antwoord: "geschikt voor bestelbussen, hoge SUV's en auto's met dakkoffer."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "shopping-center",
    locatie: "shopping-center",
    vragen: [
      {vraag: "Wat kost het eerste uur?", kern: "€1", antwoord: "daarna betaal je €1,25 per 30 minuten."},
      {vraag: "Hoe ver is het lopen naar Alexandrium?", kern: "Ongeveer 3 minuten", antwoord: "je loopt overdekt weg vanaf de garage."},
      {vraag: "Wat is de goedkoopste dagkaart?", kern: "€9", antwoord: "als je ruim vooraf boekt. Met reservering €11, zonder €12,50."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "europoint",
    locatie: "europoint",
    vragen: [
      {vraag: "Hoeveel parkeerplaatsen heeft Parking Europoint?", kern: "1.133 overdekte plaatsen", antwoord: "het is daarmee onze grootste garage."},
      {vraag: "Wat kost een dag parkeren?", kern: "€12", antwoord: "als je ruim vooraf boekt. Met reservering €14, zonder maximaal €15."},
      {vraag: "Ligt de garage dichter bij Rotterdam of bij Schiedam?", kern: "Tussen beide in", antwoord: "aan de westkant van Rotterdam, op korte afstand van Schiedam."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "maashaven",
    locatie: "maashaven",
    vragen: [
      {vraag: "Hoe ver is het lopen naar de Maassilo?", kern: "Ongeveer 7 minuten"},
      {vraag: "Tot hoe laat is de parking open?", kern: "Ma-vr tot 23.00 uur", antwoord: "op zaterdag tot 18.00 uur en op zondag tot 17.00 uur."},
      {vraag: "Moet ik reserveren?", kern: "Nee, direct inrijden", antwoord: "reserveer je online, dan betaal je €25 per dag."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "td-gebouw",
    locatie: "td-gebouw",
    zonderFoto: true,
    vragen: [
      {vraag: "Hoe ver is het lopen naar het Van Abbemuseum?", kern: "Ongeveer 6 minuten", antwoord: "het museum ligt aan de andere kant van het Anne Frankplantsoen."},
      {vraag: "Wat kost een uur parkeren?", kern: "€3 per uur", antwoord: "voor een hele dag is de dagkaart voordeliger: vanaf €12 bij vroeg boeken."},
      {vraag: "Is de parking 's nachts open?", kern: "Ja, 24 uur per dag", antwoord: "in- en uitrijden kan elke dag."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "philips-bedrijfsschool",
    locatie: "philips-bedrijfsschool",
    vragen: [
      {vraag: "Hoeveel parkeerplaatsen zijn er?", kern: "700 overdekte plaatsen", antwoord: "buiten wedstrijddagen is er bijna altijd plek."},
      {vraag: "Wat kost een dagkaart?", kern: "€12,50", antwoord: "als je online vooraf reserveert. Zonder reservering €15."},
      {vraag: "Is de garage 24 uur per dag open?", kern: "Ja, de klok rond", antwoord: "zeven dagen per week, behalve op dagen met een wedstrijd of groot evenement."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "dll-garage",
    locatie: "dll-garage",
    vragen: [
      {vraag: "Wanneer is de DLL-garage open?", kern: "Ma-vr vanaf 17.00 uur", antwoord: "tot 06.00 uur. Overdag is de garage voor medewerkers van het gebouw."},
      {vraag: "Wat kost een dag parkeren?", kern: "Vanaf €12", antwoord: "als je ruim vooraf boekt. Met reservering €14, zonder €15."},
      {vraag: "Hoe ver is het lopen naar het centrum?", kern: "Ongeveer 4 minuten", antwoord: "naar het Stadhuisplein en de uitgaansstraten."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "dll-parkeerdek",
    locatie: "dll-parkeerdek",
    vragen: [
      {vraag: "Kan ik hier met een bestelbus parkeren?", kern: "Ja, tot 2,50 meter", antwoord: "de meeste bestelbussen, hoge SUV's en auto's met dakkoffer passen."},
      {vraag: "Vanaf welk tijdstip kan ik inrijden?", kern: "Ma-vr vanaf 17.00 uur", antwoord: "tot 06.00 uur. Overdag parkeren hier medewerkers van het gebouw."},
      {vraag: "Sta ik hier overdekt?", kern: "Nee, in de open lucht", antwoord: "wil je overdekt staan, kies dan de DLL-garage op hetzelfde adres."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "evoluon",
    locatie: "evoluon",
    vragen: [
      {vraag: "Hoe ver is het lopen naar de ingang van het Evoluon?", kern: "Ongeveer 2 minuten", antwoord: "de parking ligt op het terrein van het Evoluon zelf."},
      {vraag: "Wat kost een dag parkeren bij het Evoluon?", kern: "€9", antwoord: "als je online vooraf reserveert. Zonder reservering €10."},
      {vraag: "Zijn er genoeg plaatsen tijdens een evenement?", kern: "350 plaatsen", antwoord: "bij grote evenementen reserveer je online, dan is je plek zeker."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "at-the-park",
    locatie: "at-the-park",
    vragen: [
      {vraag: "Wat is de goedkoopste manier om hier te parkeren?", kern: "Vanaf €7 per dag", antwoord: "met een dagkaart bij vroeg boeken. Of een ParkingPass: 10 dagen voor €80."},
      {vraag: "Hoe ver is het lopen naar het station?", kern: "Ongeveer 7 minuten", antwoord: "het centrum van Rijswijk ligt ook op loopafstand."},
      {vraag: "Kan ik hier elektrisch laden?", kern: "Ja, er zijn laadpunten", antwoord: "voor elektrische auto's."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "stationsweg-ypenburg",
    locatie: "stationsweg-ypenburg",
    vragen: [
      {vraag: "Wat kost parkeren als ik naar de bioscoop ga?", kern: "€4,75", antwoord: "voor de eerste vier uur."},
      {vraag: "Hoe ver is het lopen naar het station?", kern: "Naast de deur", antwoord: "de parking ligt direct naast station Ypenburg."},
      {vraag: "Tot hoe laat is de parking open?", kern: "Tot 01.00 uur", antwoord: "open vanaf 07.00 uur. Kom je later terug, dan haal je je auto vanaf 07.00 uur op."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "pr-schiedam-centrum",
    locatie: "pr-schiedam-centrum",
    vragen: [
      {vraag: "Wat kost P+R parkeren bij Schiedam Centraal?", kern: "€3,64 per dag", antwoord: "met OV-chipkaart, NS-Business Card of e-ticket. Ma-vr bij inrijden tussen 05.15 en 19.00 uur."},
      {vraag: "Hoe ver is het lopen naar het station?", kern: "Ongeveer 4 minuten", antwoord: "naar station Schiedam Centraal."},
      {vraag: "Tot hoe laat kan ik mijn auto ophalen?", kern: "Tot 01.00 uur", antwoord: "zondag tot en met donderdag. Op vrijdag en zaterdag tot 02.00 uur."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "lentse-plas",
    locatie: "lentse-plas",
    vragen: [
      {vraag: "Wat kost parkeren bij Pathé Nijmegen?", kern: "€3,75", antwoord: "voor de eerste vier uur. Je kaart waardeer je af in de bioscoop."},
      {vraag: "Wat is het dagtarief?", kern: "Maximaal €21,50", antwoord: "per dag. Je betaalt €1,10 per 20 minuten."},
      {vraag: "Is de parking 's nachts open?", kern: "Ja, 24 uur per dag", antwoord: "ook na een late voorstelling."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "heerhugowaard-p1-zuidtangent",
    locatie: "heerhugowaard-p1-zuidtangent",
    vragen: [
      {vraag: "Wat kost parkeren bij Middenwaard?", kern: "€1 per uur", antwoord: "met een maximum van €9 per dag."},
      {vraag: "Hoeveel parkeerplaatsen zijn er?", kern: "794 plaatsen", antwoord: "verdeeld over het terrein en de parkeerkelder."},
      {vraag: "Moet ik reserveren?", kern: "Nee, direct inrijden", antwoord: "het terrein is 24 uur per dag toegankelijk."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "p2-middenwaard",
    locatie: "p2-middenwaard",
    vragen: [
      {vraag: "Is P2 Middenwaard 24 uur per dag open?", kern: "Ja, de klok rond", antwoord: "in- en uitrijden kan altijd."},
      {vraag: "Wat is de doorrijhoogte?", kern: "2,10 meter", antwoord: "ruimer dan de 1,90 meter bij P1 Zuidtangent."},
      {vraag: "Wat kost een dag parkeren?", kern: "Maximaal €9", antwoord: "per dag. Je betaalt €1 per uur."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "p1-carlton-wtc",
    locatie: "p1-carlton-wtc",
    vragen: [
      {vraag: "Wat kost kort parkeren?", kern: "€1 per 20 minuten", antwoord: "voor een hele dag kies je P2 Mandela WTC om de hoek: €6 per dag."},
      {vraag: "Moet ik vooraf reserveren?", kern: "Nee, direct inrijden"},
      {vraag: "Hoe ver is het lopen naar het centrum?", kern: "Ongeveer 4 minuten"},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "p2-mandela-wtc",
    locatie: "p2-mandela-wtc",
    vragen: [
      {vraag: "Wat kost een dag parkeren in het centrum van Almere?", kern: "Maximaal €6", antwoord: "per dag. Tot dan betaal je €1 per 20 minuten."},
      {vraag: "Hoe ver is het lopen naar het centrum?", kern: "Ongeveer 4 minuten"},
      {vraag: "Is de garage 's nachts open?", kern: "Ja, 24 uur per dag", antwoord: "zeven dagen per week."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "p1-belgielaan",
    locatie: "p1-belgielaan",
    vragen: [
      {vraag: "Wat is de doorrijhoogte?", kern: "2,00 meter", antwoord: "samen met P2 Onderlangs de ruimste van het Stadshart."},
      {vraag: "Tot hoe laat kan ik inrijden bij P1?", kern: "Tot 19.00 uur", antwoord: "op vrijdag tot 21.00 uur. Uitrijden kan altijd."},
      {vraag: "Welke garage is 's avonds laat open?", kern: "P2, P4 en P9", antwoord: "P2 Bovenlangs, P2 Onderlangs, P4 Luxemburglaan en P9 Duitslandlaan zijn 24 uur per dag open."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "p2-bovenlangs",
    locatie: "p2-bovenlangs",
    vragen: [
      {vraag: "Is de garage 's nachts open?", kern: "Ja, 24 uur per dag", antwoord: "in- en uitrijden kan altijd."},
      {vraag: "Kan ik hier elektrisch laden?", kern: "Ja, er zijn laadpunten", antwoord: "voor elektrische auto's."},
      {vraag: "Wat is de doorrijhoogte bij P2 Bovenlangs?", kern: "1,95 meter", antwoord: "is je auto hoger, kies dan P2 Onderlangs of P1 Belgielaan met 2,00 meter."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "p2-onderlangs",
    locatie: "p2-onderlangs",
    vragen: [
      {vraag: "Moet ik vooraf reserveren?", kern: "Nee, direct inrijden"},
      {vraag: "Wat is de doorrijhoogte?", kern: "2,00 meter", antwoord: "iets ruimer dan bij P2 Bovenlangs, P4 en P5 in het Stadshart."},
      {vraag: "Hoeveel plaatsen zijn er?", kern: "287 plaatsen", antwoord: "de compactste garage van het Stadshart, dus je rijdt snel in en uit."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "p4-luxemburglaan",
    locatie: "p4-luxemburglaan",
    vragen: [
      {vraag: "Is P4 dag en nacht open?", kern: "Ja, 24 uur per dag", antwoord: "in- en uitrijden kan altijd."},
      {vraag: "Hoeveel plaatsen zijn er?", kern: "453 overdekte plaatsen"},
      {vraag: "Wat is de doorrijhoogte?", kern: "1,90 meter", antwoord: "rijd je hoger, kies dan P1 Belgielaan of P2 Onderlangs."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "p5-amsterdamstraat",
    locatie: "p5-amsterdamstraat",
    vragen: [
      {vraag: "Kan ik hier elektrisch laden?", kern: "Ja, er zijn laadpunten", antwoord: "voor elektrische auto's."},
      {vraag: "Tot hoe laat kan ik inrijden?", kern: "Tot 19.00 uur", antwoord: "op vrijdag tot 21.00 uur. Uitrijden kan 24 uur per dag."},
      {vraag: "Wat is de doorrijhoogte?", kern: "1,90 meter", antwoord: "rijd je hoger, kies dan P1 Belgielaan of P2 Onderlangs met 2,00 meter."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "p8-nederlandlaan",
    locatie: "p8-nederlandlaan",
    vragen: [
      {vraag: "Hoeveel plaatsen heeft P8?", kern: "659 overdekte plaatsen", antwoord: "de grootste garage van Stadshart Zoetermeer."},
      {vraag: "Tot hoe laat kan ik inrijden?", kern: "Tot 22.30 uur", antwoord: "inrijden kan vanaf 07.00 uur. Uitrijden kan 24 uur per dag."},
      {vraag: "Wie kan een winkelabonnement afnemen?", kern: "Winkeliers in het Stadshart", antwoord: "voor anderen is er het 24/7- of kantoorabonnement."},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
  {
    slug: "p9-duitslandlaan",
    locatie: "p9-duitslandlaan",
    vragen: [
      {vraag: "Is P9 dag en nacht open?", kern: "Ja, 24 uur per dag", antwoord: "dat geldt niet voor alle garages in het Stadshart."},
      {vraag: "Is er een lift?", kern: "Ja, er is een lift", antwoord: "handig met boodschappen, een kinderwagen of een rollator."},
      {vraag: "Wat is de doorrijhoogte?", kern: "2 meter"},
    ],
    bron: 'Locatiepagina, Veelgestelde vragen (opgehaald 27-11-2026).',
  },
];
