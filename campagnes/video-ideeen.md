# Video-ideeën voor bulkproductie (per locatie of per bestemming)

Elke serie wordt een Remotion-template dat uit data rendert, in 9:16 en 16:9. Data alleen van de locatiepagina's op
parkingyou.nl of gemeten via OpenStreetMap; aantallen locaties geteld op de pagina's van 27-11-2026.

## Gemaakt

| Serie | Locaties | Map in `remotion/out/` |
|---|---|---|
| Locatiespot en reel | 34 | `locaties`, `reels` |
| Zoekvideo | 13 zoekopdrachten | `zoek` |
| Het appje | 34 + 2 Maashaven | `chat` |
| Het lijstje | 34 | `lijstje` |
| Het bordje | 32 + 1 Maashaven | `bordje` |
| Het kaartje (bekende plekken, echte kaart) | 20 + 3 Maashaven | `kaartje` |
| Vroeg boeken loont | 10 + Maashaven | `vroegboeken` |
| De strippenkaart (ParkingPass) | 11 | `strippenkaart` |
| Amsterdam Light (Plantage) | 8 video's | `amsterdam-light` |
| Zo rijd je erin | 6 | `rijroute` |
| Parkeer en stap over | 6 | `overstap` |
| Rondje zoeken per locatie | 23 | `rondje` |
| Vraag het maar | 27 | `vraag` |

## Ronde 1, nog te maken

| # | Serie | Data | Locaties |
|---|---|---|---|
| 1 | ~~Past mijn auto? (doorrijhoogte)~~ afgewezen | doorrijhoogte | 24 |
| 2 | Droog naar binnen (overdekt, inzetten met regentrigger) | overdekte garage | 21 |
| 3 | Stekker erin (elektrisch laden) | laadpunten | 19 |
| 4 | De klok rond (dag- en avondtarief, openingstijden) | avond- of nachttarief | 22 |
| 5 | Vraag het maar (veelgestelde vragen) | FAQ op de pagina | 27 |
| 6 | De plekkenteller | aantal plaatsen | 32 |
| 7 | Slagboom gaat vanzelf open (kenteken) | kentekenherkenning | 17 |
| 8 | Het momentje (koopzondag, kerst, feestdagen) | kalender + tarief | winkellocaties |

## Ronde 2, nieuw

| # | Serie | Zo werkt het | Data | Locaties |
|---|---|---|---|---|
| 11 | De maandrekening | Een maandkalender vult zich met werkdagen; de losse dagkaarten tellen op tegen het abonnement per maand. "Elke dag hier? Dan is dit goedkoper." | abonnementen (24/7, Office, Winkel, Bewoner) en dagtarief | 26 |
| 12 | Parkeer en stap over | Auto rijdt de garage in, stippellijn naar het station of de metro met looptijd, dan een trein of metro die vertrekt. "Zonder file de stad in." | station, metro of P+R op de pagina, looptijd uit pagina of OSM | 10 |
| 13 | Zonder trappen | Pictogrammen klikken één voor één aan: rolstoeltoegang, lift, gehandicaptenplekken. Voor wie slecht ter been is, of voor mantelzorgers. | faciliteiten | 21 (lift: 17) |
| 14 | Veilig geparkeerd | Nachtscène, het camerabord uit de bibliotheek zwenkt, "Cameratoezicht" en de openingstijden komen in beeld. | cameratoezicht | 12 |
| 15 | Raad de prijs | Quizvorm voor Instagram: "Wat kost een dag parkeren naast Artis?" Drie antwoorden, het goede licht op (€17,50 met Artis-dagkaart). Lokt reacties uit. | tarieven | 34 |
| 16 | Rondje zoeken per locatie | De split-screen uit de Light-campagne als bulkversie: links een auto die rondjes rijdt, rechts iemand die vanaf onze parking naar een bekende plek loopt (route uit Het kaartje). | kaartjes-data | 20+ |
| 17 | Zo rijd je erin | Echte kaart, de autoroute van de laatste kilometer naar de inrit wordt getekend (OpenStreetMap, autoprofiel), met de straatnaam van de inrit. Neemt de spanning weg van "waar moet ik naar binnen?". | adres, inrit op de pagina | 34 (inrit benoemd: 8) |
| 18 | Het weerbericht | Uitbreiding van Droog naar binnen: drie varianten (regen, vorst met ruiten krabben, hitte met een koele auto). Inzetten met een weertrigger. | overdekte garage | 21 |
| 19 | Uitgaansagenda | Het kaartje met een datum: "Za 14 dec, concert in De Doelen? Parkeer bij Hofplein." Alleen in de dagen ervoor inzetten. | lijst met evenementen per plek (input nodig) | 20 plekken |
| 20 | Wat parkeerders zeggen | Een echte recensie in beeld met sterren en de locatie, daarna de feiten en de CTA. Recensies doen het meestal sterk in advertenties. | echte recensies, bijvoorbeeld Google (input nodig) | per locatie met recensies |

## Spelregels voor alle series

- Prijzen en feiten alleen van de locatiepagina; na 1 februari alle prijsvideo's opnieuw renderen.
- "Reserveer" alleen bij de 15 boekbare locaties.
- Partnernamen (Artis, PSV, Pathé) alleen als tekst.
- Geen schaduwen of blur, renderen in één tab, iedere video op flikkering controleren.
- Openingstijden meenemen waar ze het verhaal raken (Maashaven, DLL).
