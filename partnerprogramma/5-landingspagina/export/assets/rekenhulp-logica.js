/* Rekenlogica van de rekenhulp. Puur, zonder DOM, zodat ze los te testen is.
 * Brief: commissie per maand = bezoekers met auto x deel dat reserveert x gemiddelde boeking x percentage.
 * Werkt in de browser (window.PYRekenhulp) en in node (require). */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.PYRekenhulp = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var LIMIETEN = {
    bezoekers: { min: 10, max: 5000, stap: 10, standaard: 200 },
    deel: { min: 5, max: 60, stap: 1, standaard: 20 }
  };

  /* bezoekers: aantal per maand; deel en percentage in hele procenten (20 = 20%);
   * gemiddeldeBoeking: euro's of null als nog niet aangeleverd.
   * Geeft null terug zolang de gemiddelde boeking ontbreekt. Bedragen zijn hele euro's;
   * per jaar is de afgeronde maandwaarde keer 12, zodat de twee getallen op de pagina kloppen. */
  function berekenCommissie(inv) {
    var boeking = inv.gemiddeldeBoeking;
    if (boeking === null || boeking === undefined || isNaN(boeking)) return null;
    var maand = inv.bezoekers * (inv.deel / 100) * boeking * (inv.percentage / 100);
    var perMaand = Math.round(maand);
    return { perMaand: perMaand, perJaar: perMaand * 12 };
  }

  /* 1234567 -> "1.234.567" (nl-NL, zonder afhankelijkheid van ICU in de browser) */
  function formatEuro(n) {
    return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }

  function begrens(waarde, l) {
    var n = Math.round(Number(waarde));
    if (isNaN(n)) n = l.standaard;
    return Math.min(l.max, Math.max(l.min, n));
  }

  return { LIMIETEN: LIMIETEN, berekenCommissie: berekenCommissie, formatEuro: formatEuro, begrens: begrens };
});
