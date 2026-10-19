# QR-test

Na elke export worden de PDF's gerasterd (300, 150 en 100 dpi) en de codes teruggelezen met twee onafhankelijke decoders (zxing-cpp en OpenCV).
Een kaart slaagt als op elke resolutie het verwachte aantal codes gelezen wordt en elke code precies de verwachte URL is.

| PDF | Verwacht | Codes | Module | Code | Rustzone | Resultaat |
|---|---|---|---|---|---|---|
| 2-balie-qr-kaart/export/HOF-HOTELVB/parkingyou-kaart-a6-HOF-HOTELVB.pdf | https://parkingyou.nl/p/HOF-HOTELVB | 1 | 33x33 (v4, Q) | 30 mm | 3.6 mm | gelezen |
| 2-balie-qr-kaart/export/HOF-HOTELVB/parkingyou-tafelstandaard-a6-HOF-HOTELVB.pdf | https://parkingyou.nl/p/HOF-HOTELVB | 2 | 33x33 (v4, Q) | 30 mm | 3.6 mm | gelezen |
| 2-balie-qr-kaart/export/PLA-THEATERVB/parkingyou-kaart-a6-PLA-THEATERVB.pdf | https://parkingyou.nl/p/PLA-THEATERVB | 1 | 33x33 (v4, Q) | 30 mm | 3.6 mm | gelezen |
| 2-balie-qr-kaart/export/PLA-THEATERVB/parkingyou-tafelstandaard-a6-PLA-THEATERVB.pdf | https://parkingyou.nl/p/PLA-THEATERVB | 2 | 33x33 (v4, Q) | 30 mm | 3.6 mm | gelezen |
