/* Rekenhulp en aanmeldformulier. Vanilla JS; de formule zit in rekenhulp-logica.js. */
(function () {
  "use strict";
  var R = window.PYRekenhulp;

  /* ---------- rekenhulp ---------- */
  function rekenhulp(form) {
    var bez = form.querySelector("#rh-bezoekers");
    var deel = form.querySelector("#rh-deel");
    var bezUit = form.querySelector("#rh-bezoekers-waarde");
    var deelUit = form.querySelector("#rh-deel-waarde");
    var bedrag = form.querySelector("[data-bedrag]");
    var live = form.querySelector("[data-live]");
    var timer = null;

    function vul(slider) {
      var l = (Number(slider.value) - Number(slider.min)) / (Number(slider.max) - Number(slider.min));
      slider.style.setProperty("--vul", (l * 100).toFixed(1) + "%");
    }

    function getal(n) { var s = document.createElement("span"); s.className = "getal"; s.textContent = n; return s; }
    function ph(tekst) { var s = document.createElement("span"); s.className = "placeholder"; s.textContent = tekst; return s; }

    function toon() {
      var b = R.begrens(bez.value, R.LIMIETEN.bezoekers);
      var d = R.begrens(deel.value, R.LIMIETEN.deel);
      var garage = form.querySelector('input[name="garage"]:checked');
      var niveau = form.querySelector('input[name="niveau"]:checked');
      var boekingTxt = garage ? garage.getAttribute("data-boeking") : "";
      var boeking = boekingTxt === "" || boekingTxt === null ? null : Number(boekingTxt);

      bezUit.textContent = R.formatEuro(b);
      deelUit.textContent = d + "%";
      bez.setAttribute("aria-valuetext", form.getAttribute("data-tpl-bezoekers").replace("{n}", R.formatEuro(b)));
      deel.setAttribute("aria-valuetext", form.getAttribute("data-tpl-deel").replace("{n}", d));
      vul(bez); vul(deel);

      var uit = R.berekenCommissie({ bezoekers: b, deel: d, gemiddeldeBoeking: boeking, percentage: Number(niveau.getAttribute("data-percentage")) });
      var voor = form.getAttribute("data-voor"), maand = form.getAttribute("data-maand"), jaar = form.getAttribute("data-jaar");
      var plek = form.getAttribute("data-placeholder");
      var tekst;
      bedrag.textContent = "";
      bedrag.appendChild(document.createTextNode(voor + "€"));
      if (uit) {
        bedrag.appendChild(getal(R.formatEuro(uit.perMaand)));
        bedrag.appendChild(document.createTextNode(maand + "€"));
        bedrag.appendChild(getal(R.formatEuro(uit.perJaar)));
        tekst = voor + "€" + R.formatEuro(uit.perMaand) + maand + "€" + R.formatEuro(uit.perJaar) + jaar;
      } else {
        bedrag.appendChild(ph(plek));
        bedrag.appendChild(document.createTextNode(maand + "€"));
        bedrag.appendChild(ph(plek));
        tekst = voor + "€" + plek + maand + "€" + plek + jaar;
      }
      bedrag.appendChild(document.createTextNode(jaar));
      // schermlezer: pas na een korte pauze voorlezen, niet bij elke stap van de schuif
      clearTimeout(timer);
      timer = setTimeout(function () { live.textContent = tekst + " " + form.querySelector(".disclaimer").textContent; }, 500);
    }

    form.addEventListener("input", toon);
    form.addEventListener("change", toon);
    toon();
  }

  /* ---------- aanmeldformulier ---------- */
  var MELDINGEN = JSON.parse(document.getElementById("meldingen").textContent);

  var REGELS = {
    kvk: function (w) { return /^\d{8}$/.test(w.replace(/\s/g, "")) ? "" : MELDINGEN.kvk; },
    email: function (w) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(w) ? "" : MELDINGEN.email; },
    telefoon: function (w) { return /^[+\d][\d\s().-]*$/.test(w) && w.replace(/\D/g, "").length >= 10 ? "" : MELDINGEN.telefoon; }
  };

  function controleer(veld) {
    var naam = veld.getAttribute("data-veld");
    var el = veld.querySelector("input, select, textarea");
    var fout = veld.querySelector(".fout");
    var melding = "";
    if (el.type === "checkbox") {
      if (!el.checked) melding = MELDINGEN.akkoord;
    } else {
      var w = el.value.trim();
      if (el.required && w === "") melding = el.tagName === "SELECT" ? MELDINGEN.keuze : MELDINGEN.verplicht;
      else if (w !== "" && REGELS[naam]) melding = REGELS[naam](w);
    }
    fout.textContent = melding;
    fout.hidden = melding === "";
    if (melding) { veld.setAttribute("data-fout", ""); el.setAttribute("aria-invalid", "true"); }
    else { veld.removeAttribute("data-fout"); el.removeAttribute("aria-invalid"); }
    return melding === "";
  }

  function formulier(form) {
    var velden = [].slice.call(form.querySelectorAll("[data-veld]"));
    var samenvatting = form.querySelector(".samenvatting");
    var bevestiging = document.querySelector("[data-bevestiging]");

    velden.forEach(function (v) {
      var el = v.querySelector("input, select, textarea");
      el.addEventListener("blur", function () { if (el.value !== "" || v.hasAttribute("data-fout")) controleer(v); });
      el.addEventListener("input", function () { if (v.hasAttribute("data-fout")) controleer(v); });
      el.addEventListener("change", function () { if (v.hasAttribute("data-fout")) controleer(v); });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var eerste = null;
      velden.forEach(function (v) { if (!controleer(v) && !eerste) eerste = v; });
      if (eerste) {
        samenvatting.textContent = samenvatting.getAttribute("data-melding");
        samenvatting.hidden = false;
        eerste.querySelector("input, select, textarea").focus();
        return;
      }
      samenvatting.hidden = true;
      var gegevens = {};
      velden.forEach(function (v) {
        var el = v.querySelector("input, select, textarea");
        gegevens[el.name] = el.type === "checkbox" ? el.checked : el.value.trim();
      });
      // Prototype: er wordt niets verstuurd. Payload hangt hier op de gebeurtenis of vervangt dit blok door de form-builder.
      form.dispatchEvent(new CustomEvent("partner-aanmelding", { bubbles: true, detail: { endpoint: form.getAttribute("data-endpoint"), gegevens: gegevens } }));
      form.hidden = true;
      bevestiging.hidden = false;
      bevestiging.focus();
    });
  }

  var rh = document.querySelector("[data-rekenhulp]");
  if (rh) rekenhulp(rh);
  var fm = document.querySelector("[data-aanmeldform]");
  if (fm) formulier(fm);
})();
