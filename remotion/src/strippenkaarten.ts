// "De strippenkaart" (StripSpot): the ParkingPass of a location (one strip = one day), 25 strips punched one by one,
// then the price per day next to a loose day ticket (without booking) and the total saving.
// Data from the ParkingPass and Tarieven blocks of each location page (parkingyou.nl, 27-11-2026).
// DLL garage and deck are left out (closed on weekdays during office hours; the garage sells only 25 strips).

export type Strippenkaart = {
  slug: string;
  /** Location slug from locaties.ts. */
  locatie: string;
  vraag: string;
  /** Price of 10 and 25 strips (one strip = one day). */
  tien: number;
  vijfentwintig: number;
  /** Loose day ticket without booking, to compare with. */
  dag: number;
  /** How the day ticket is named on the page, when it is not the plain "losse dagkaart". */
  dagLabel?: string;
  bron: string;
};

export const strippenkaarten: Strippenkaart[] = [
  {slug: 'plantage', locatie: 'plantage', vraag: 'Vaak in Amsterdam?', tien: 350, vijfentwintig: 750, dag: 45, dagLabel: 'Losse dagkaart (09-18 uur)', bron: '10 strippen €350, 25 strippen €750; 09-18u zonder reservering €45.'},
  {slug: 'cruquius', locatie: 'cruquius', vraag: 'Vaak in Amsterdam Oost?', tien: 190, vijfentwintig: 450, dag: 25, bron: '10 strippen €190, 25 strippen €450; dagtarief zonder reservering €25.'},
  {slug: 'zeeburgerkade', locatie: 'zeeburgerkade', vraag: 'Vaak in Amsterdam?', tien: 190, vijfentwintig: 450, dag: 25, bron: '10 strippen €190, 25 strippen €450; dagtarief zonder reservering €25.'},
  {slug: 'bos-en-lommerplantsoen', locatie: 'bos-en-lommerplantsoen', vraag: 'Vaak in Amsterdam West?', tien: 150, vijfentwintig: 350, dag: 17.5, bron: '10 strippen €150, 25 strippen €350; dagtarief zonder reservering €17,50.'},
  {slug: 'hofplein', locatie: 'hofplein', vraag: 'Vaak in Rotterdam?', tien: 200, vijfentwintig: 437.5, dag: 30, dagLabel: 'Losse dagkaart (ma-vr)', bron: '10 strippen €200, 25 strippen €437,50; dagtarief zonder reservering ma t/m vrij €30.'},
  {slug: 'shopping-center', locatie: 'shopping-center', vraag: 'Vaak bij Alexandrium?', tien: 100, vijfentwintig: 225, dag: 12.5, bron: '10 strippen €100, 25 strippen €225; dagtarief zonder reservering €12,50.'},
  {slug: 'europoint', locatie: 'europoint', vraag: 'Vaak in Rotterdam West?', tien: 100, vijfentwintig: 225, dag: 15, dagLabel: 'Maximaal dagtarief', bron: '10 strippen €100, 25 strippen €225; max. dagtarief €15.'},
  {slug: 'td-gebouw', locatie: 'td-gebouw', vraag: 'Vaak in Eindhoven?', tien: 100, vijfentwintig: 200, dag: 15, bron: '10 strippen €100, 25 strippen €200; dagtarief zonder reservering €15.'},
  {slug: 'philips-bedrijfsschool', locatie: 'philips-bedrijfsschool', vraag: 'Vaak in Eindhoven?', tien: 90, vijfentwintig: 200, dag: 15, bron: '10 strippen €90, 25 strippen €200; dagtarief zonder reservering €15. Niet tijdens wedstrijden en grote evenementen.'},
  {slug: 'evoluon', locatie: 'evoluon', vraag: 'Vaak bij het Evoluon?', tien: 100, vijfentwintig: 200, dag: 10, bron: '10 strippen €100, 25 strippen €200; dagtarief zonder reservering €10 (10 strippen geeft hier geen voordeel per dag).'},
  {slug: 'at-the-park', locatie: 'at-the-park', vraag: 'Vaak in Rijswijk?', tien: 80, vijfentwintig: 175, dag: 12, bron: '10 strippen €80, 25 strippen €175; dagtarief zonder reservering €12.'},
];
