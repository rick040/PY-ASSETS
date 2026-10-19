/* node partnerprogramma/5-landingspagina/test-rekenhulp.js */
"use strict";
const assert = require("assert");
const R = require("./rekenhulp-logica.js");

// standaardwaarden uit de brief
assert.deepStrictEqual(R.LIMIETEN.bezoekers, { min: 10, max: 5000, stap: 10, standaard: 200 });
assert.deepStrictEqual(R.LIMIETEN.deel, { min: 5, max: 60, stap: 1, standaard: 20 });

// zolang de gemiddelde boeking ontbreekt: geen bedrag
assert.strictEqual(R.berekenCommissie({ bezoekers: 200, deel: 20, gemiddeldeBoeking: null, percentage: 6 }), null);
assert.strictEqual(R.berekenCommissie({ bezoekers: 200, deel: 20, gemiddeldeBoeking: undefined, percentage: 6 }), null);

// 200 x 20% x 50 x 6% = 120 per maand, 1440 per jaar
let r = R.berekenCommissie({ bezoekers: 200, deel: 20, gemiddeldeBoeking: 50, percentage: 6 });
assert.deepStrictEqual(r, { perMaand: 120, perJaar: 1440 });

// per niveau, zelfde invoer: 4, 6 en 9 procent
[[4, 80], [6, 120], [9, 180]].forEach(([p, verwacht]) =>
  assert.strictEqual(R.berekenCommissie({ bezoekers: 200, deel: 20, gemiddeldeBoeking: 50, percentage: p }).perMaand, verwacht));

// uiterste waarden
assert.strictEqual(R.berekenCommissie({ bezoekers: 5000, deel: 60, gemiddeldeBoeking: 50, percentage: 9 }).perMaand, 13500);
assert.strictEqual(R.berekenCommissie({ bezoekers: 10, deel: 5, gemiddeldeBoeking: 50, percentage: 4 }).perMaand, 1);

// afronden op hele euro's, jaar is 12 x de afgeronde maand
r = R.berekenCommissie({ bezoekers: 130, deel: 17, gemiddeldeBoeking: 23.5, percentage: 6 }); // 31,16 -> 31
assert.deepStrictEqual(r, { perMaand: 31, perJaar: 372 });

// nl-NL opmaak
assert.strictEqual(R.formatEuro(0), "0");
assert.strictEqual(R.formatEuro(999), "999");
assert.strictEqual(R.formatEuro(1000), "1.000");
assert.strictEqual(R.formatEuro(162000), "162.000");
assert.strictEqual(R.formatEuro(1234567.4), "1.234.567");

// begrenzen
assert.strictEqual(R.begrens(1, R.LIMIETEN.bezoekers), 10);
assert.strictEqual(R.begrens(99999, R.LIMIETEN.bezoekers), 5000);
assert.strictEqual(R.begrens("abc", R.LIMIETEN.deel), 20);

console.log("rekenhulp: alle tests geslaagd");
