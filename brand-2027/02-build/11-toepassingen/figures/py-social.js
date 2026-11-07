// ParkingYou 2027 social templates (post 4:5 and reel 9:16, u = 54 px). Needs py-fig.js and py-signs.js.
// PYSOC.post(type, fmt, opts) returns SVG markup for a 1080 x 1350 (post) or 1080 x 1920 (reel) frame.
// Types: 'aanbod' (het vak + een parkeerder), 'locatie' (de stem + de loper), 'evenement' (de stem + de danser).
const PYSOC = (() => {
  const u = 54, M = 108, W = 1080;
  const C = { navy: '#1A3580', aqua: '#32B9CD', white: '#FFFFFF', line: '#6F86C8', mine: '#2B4A9E' };
  const T = (x, y, s, size, o = {}) => `<text x="${x}" y="${y}" font-family="Ubuntu Sans" font-size="${size}" font-weight="${o.w || 400}" fill="${o.c || C.white}" ${o.anchor ? `text-anchor="${o.anchor}"` : ''} letter-spacing="${o.ls || 0}" style="font-variant-numeric:tabular-nums">${s}</text>`;
  const eyebrow = (x, y, s, c) => T(x, y, s.toUpperCase(), 24, { w: 700, c: c || C.aqua, ls: 1.9 });
  const logo = (x, y) => `<image href="../../kit/assets/logo-horizontal-reverse.svg" x="${x}" y="${y}" height="54" width="195.6"/>`;

  // Het vak on PY-Blauw: bays running in from the bottom edge (H) for len px; pitch 1.5u, line 0.05u; jouw vak at bay index k.
  function vak(H, len, k, figName, standY, o = {}) {
    const pitch = 1.5 * u, lw = 0.05 * u, top = H - len, light = !!o.light;
    const lineC = light ? '#DDE1E7' : C.line, mineC = light ? '#E3F6F9' : C.mine, ink = light ? C.navy : C.white;
    let s = `<g stroke="${lineC}" stroke-width="${lw}">`;
    for (let x = 27; x <= W; x += pitch) s += `<line x1="${x}" y1="${top}" x2="${x}" y2="${H}"/>`;
    s += `<line x1="0" y1="${top - 0.5 * u}" x2="${W}" y2="${top - 0.5 * u}" stroke-dasharray="${0.3 * u} ${0.25 * u}"/></g>`;
    const x0 = 27 + k * pitch;
    s += `<rect x="${x0}" y="${top}" width="${pitch}" height="${len}" fill="${mineC}"/>`;
    s += `<g stroke="${C.aqua}" stroke-width="${2 * lw}"><line x1="${x0}" y1="${top}" x2="${x0}" y2="${H}"/><line x1="${x0 + pitch}" y1="${top}" x2="${x0 + pitch}" y2="${H}"/></g>`;
    if (figName) {
      const h = 2.2 * u, fw = PYS.figW(figName, h);
      s += `<rect x="${x0 + 0.2 * u}" y="${standY}" width="${pitch - 0.4 * u}" height="${0.1 * u}" fill="${ink}"/>`;
      s += PYS.fig(figName, x0 + (pitch - fw) / 2, standY, h, ink, { flip: o.flip });
    }
    return s;
  }

  function guides(H, reel) {
    let s = '';
    if (reel) s += `<rect x="0" y="0" width="${W}" height="250" fill="#C4281C" opacity="0.28"/><rect x="0" y="${H - 340}" width="${W}" height="340" fill="#C4281C" opacity="0.28"/>`;
    s += `<rect x="${M}" y="${M}" width="${W - 2 * M}" height="${H - 2 * M}" fill="none" stroke="#32B9CD" stroke-width="4" stroke-dasharray="16 12"/>`;
    return s;
  }

  function post(type, fmt, o = {}) {
    const reel = fmt === 'reel', H = reel ? 1920 : 1350, dy = reel ? 162 : 0; // reel: key content starts at 5u (270) instead of 2u
    let s = `<rect width="${W}" height="${H}" fill="${C.navy}"/>`;
    if (type === 'aanbod') {
      const d = o.data || {}, t = dy + 60, light = d.ground !== 'navy';
      const ink = light ? C.navy : C.white, accent = light ? '#127C8C' : C.aqua;
      if (light) s = `<rect width="${W}" height="${H}" fill="#FFFFFF"/>`;
      s += light ? `<image href="../../kit/assets/logo-horizontal-color.svg" x="${M}" y="${M + dy}" height="54" width="195.6"/>` : logo(M, M + dy);
      s += eyebrow(M, 351 + t, d.eyebrow || 'Parking Hofplein', accent);
      s += T(M, 486 + t, d.l1 || 'Jouw vak', 117, { w: 700, c: ink });
      s += T(M, 608 + t, d.l2 || 'staat klaar.', 117, { c: ink });
      s += T(M, 748 + t, d.price || '€ 7,50', 78, { w: 800, c: ink }) + T(M + (d.priceW || 231), 748 + t, d.unit || 'per dag', 31, { c: ink });
      s += T(M, 806 + t, d.body || 'Midden in Rotterdam, de hele dag.', 31, { c: light ? '#1D1D1B' : C.white });
      s += T(M, 892 + t, d.cta || 'Reserveer je plek op parkingyou.nl', 31, { w: 700, c: ink });
      // jouw vak (k = 1) starts on the left margin, under the headline
      const k = d.k === undefined ? 1 : d.k;
      if (reel) s += vak(H, 340 + 4 * u, k, d.fig || 'cap-wave', 1566, { flip: d.flip, light });
      else s += vak(H, 4 * u, k, d.fig || 'cap-wave', 1296, { flip: d.flip, light });
    }
    if (type === 'locatie') {
      const ph = reel ? 918 : 648;
      s += `<image href="../../kit/photos/py-photo-philips-stadion.jpg" x="0" y="0" width="${W}" height="${ph}" preserveAspectRatio="xMidYMid slice"/>`;
      const b1 = ph + 132, b2 = b1 + 86, sh = 154;
      s += PYS.stem(M, b1 - 54 - 6, sh, C.aqua);
      const tx = M + PYS.stemW(sh) + 0.3 * sh;
      s += T(tx, b1, 'Philips Stadion', 78, { w: 700 }) + T(tx, b2, 'Eindhoven', 78);
      const f1 = b2 + 112, rule = f1 + 88;
      s += T(M, f1, '9 minuten lopen naar het centrum', 31) + T(M, f1 + 46, '700 plekken · doorrijhoogte 2,00 m', 31);
      s += `<rect x="${M}" y="${rule}" width="${W - 2 * M}" height="${0.1 * u}" fill="${C.white}"/>`;
      s += PYS.fig('walk', 972 - PYS.figW('walk', 3 * u) - 12, rule, 3 * u, C.white);
      const ly = reel ? 1512 : 1188;
      s += logo(M, ly) + T(972, ly + 44, 'parkingyou.nl', 31, { w: 700, anchor: 'end' });
    }
    if (type === 'evenement') {
      s += logo(M, M + dy);
      s += eyebrow(M, 351 + dy, 'Philips Stadion');
      const b1 = 500 + dy, lh = 96, sh = 3 * lh;
      s += PYS.stem(M, b1 - 62 - 12, sh, C.aqua);
      const tx = M + PYS.stemW(sh) + 0.3 * sh;
      s += T(tx, b1, 'Wedstrijddag?', 90, { w: 700 }) + T(tx, b1 + lh, 'Parkeer naast', 90) + T(tx, b1 + 2 * lh, 'het stadion.', 90);
      const rule = reel ? 1566 : 1242;
      s += `<rect x="${M}" y="${rule}" width="${W - 2 * M}" height="${0.1 * u}" fill="${C.white}"/>`;
      s += PYS.fig('dance', 972 - PYS.figW('dance', 6 * u), rule, 6 * u, C.white);
      s += T(M, rule - 92, '[za 14 nov] · aftrap [20:00]', 31, { w: 700 }) + T(M, rule - 46, 'Reserveer vooraf op parkingyou.nl', 31);
    }
    if (o.guides) s += guides(H, reel);
    return s;
  }
  return { post, vak, guides, T, logo, eyebrow, C, u, M, W };
})();
