// ParkingYou 2027 social templates (post 4:5 and reel 9:16, u = 54 px). Needs py-fig.js and py-signs.js.
// PYSOC.post(type, fmt, opts) returns SVG markup for a 1080 x 1350 (post) or 1080 x 1920 (reel) frame.
// Types: 'aanbod' (het vak + een parkeerder), 'locatie' (de stem + de loper), 'evenement' (de stem + de danser).
const PYSOC = (() => {
  const u = 54, M = 108, W = 1080;
  const C = { navy: '#1A3580', aqua: '#32B9CD', white: '#FFFFFF', line: '#6F86C8', mine: '#2B4A9E' };
  const T = (x, y, s, size, o = {}) => `<text x="${x}" y="${y}" font-family="Ubuntu Sans" font-size="${size}" font-weight="${o.w || 400}" fill="${o.c || C.white}" ${o.anchor ? `text-anchor="${o.anchor}"` : ''} letter-spacing="${o.ls || 0}" style="font-variant-numeric:tabular-nums">${s}</text>`;
  const eyebrow = (x, y, s, c) => T(x, y, s.toUpperCase(), 24, { w: 700, c: c || C.aqua, ls: 1.9 });
  const logo = (x, y) => `<image href="../../kit/assets/logo-horizontal-reverse.svg" x="${x}" y="${y}" height="54" width="195.6"/>`;

  // Het vak (D40): a deck from above. Bays at a pitch of 4u, lines 0.05u, running in from the top edge for len (6u to 8u).
  // Jouw vak (index k from the first line at x0) is filled, has aqua side lines at double weight and an aqua stop line
  // at its open end; its parkeerder stands on that stop line. o: { u, W, x0, light, fig, figH, flip, pitch, lw, dash, gap }
  function vak(len, k, o = {}) {
    const uu = o.u || u, VW = o.W || W, pitch = o.pitch || 4 * uu, lw = o.lw || 0.05 * uu, x0 = o.x0 === undefined ? M : o.x0, light = !!o.light;
    const lineC = light ? '#DDE1E7' : C.line, mineC = light ? '#E3F6F9' : C.mine, ink = light ? C.navy : C.white;
    let s = `<g stroke="${lineC}" stroke-width="${lw}">`;
    let first = x0; while (first - pitch >= 0) first -= pitch;
    for (let x = first; x <= VW; x += pitch) s += `<line x1="${x}" y1="0" x2="${x}" y2="${len}"/>`;
    const laneY = len + (o.gap || 0.5 * uu);
    s += `<line x1="0" y1="${laneY}" x2="${VW}" y2="${laneY}" stroke-dasharray="${(o.dash || [0.3 * uu, 0.25 * uu]).join(' ')}"/></g>`;
    const xa = x0 + k * pitch;
    s += `<rect x="${xa}" y="0" width="${pitch}" height="${len}" fill="${mineC}"/>`;
    s += `<g stroke="${C.aqua}" stroke-width="${2 * lw}" stroke-linecap="square"><line x1="${xa}" y1="0" x2="${xa}" y2="${len}"/><line x1="${xa + pitch}" y1="0" x2="${xa + pitch}" y2="${len}"/><line x1="${xa}" y1="${len}" x2="${xa + pitch}" y2="${len}"/></g>`;
    if (o.fig) { const h = o.figH || 3 * uu, fw = PYS.figW(o.fig, h); s += PYS.fig(o.fig, xa + (pitch - fw) / 2, len - lw, h, ink, { flip: o.flip }); }
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
      // het vak runs in from the top (7u); jouw vak on the left margin with the gastheer on its stop line; logo at the foot
      const d = o.data || {}, light = d.ground === 'white';
      const ink = light ? C.navy : C.white, accent = light ? '#127C8C' : C.aqua;
      if (light) s = `<rect width="${W}" height="${H}" fill="#FFFFFF"/>`;
      const len = 7 * u, t = reel ? len + 0 : 0, figH = reel ? 3 * u : 5 * u;
      // reel: the bays end at 7u + 1u so the gastheer (3u) stands below the 250 px platform zone
      const L = reel ? 8 * u : len;
      s += vak(L, 0, { light, fig: d.fig || 'cap-wave', figH, flip: d.flip });
      const y0 = reel ? 560 : 540;
      s += eyebrow(M, y0, d.eyebrow || 'Parking Hofplein', accent);
      s += T(M, y0 + 140, d.l1 || 'Jouw vak', 117, { w: 800, c: ink });
      s += T(M, y0 + 262, d.l2 || 'staat klaar.', 117, { c: ink });
      s += T(M, y0 + 390, d.price || '€ 7,50', 78, { w: 800, c: ink }) + T(M + (d.priceW || 231), y0 + 390, d.unit || 'per dag', 31, { c: ink });
      s += T(M, y0 + 448, d.body || 'Midden in Rotterdam, de hele dag.', 31, { c: light ? '#1D1D1B' : C.white });
      s += T(M, y0 + 536, d.cta || 'Reserveer je plek op parkingyou.nl', 31, { w: 700, c: ink });
      const ly = reel ? 1512 : 1188;
      s += light ? `<image href="../../kit/assets/logo-horizontal-color.svg" x="${M}" y="${ly}" height="54" width="195.6"/>` : logo(M, ly);
    }
    if (type === 'locatie') {
      // white ground under the photo: de stem in PY-Aqua, the loper navy with aqua head
      s = `<rect width="${W}" height="${H}" fill="#FFFFFF"/>`;
      const ph = reel ? 918 : 648;
      s += `<image href="../../kit/photos/py-photo-philips-stadion.jpg" x="0" y="0" width="${W}" height="${ph}" preserveAspectRatio="xMidYMid slice"/>`;
      const lh = 78 * 50 / 48, b1 = ph + 140, b2 = b1 + lh, sh = 2 * lh;
      s += PYS.stem(M, b1 - lh + 12, sh, C.aqua);
      const tx = M + PYS.stemW(sh) + 0.3 * sh;
      s += T(tx, b1, 'Philips Stadion', 78, { w: 700, c: C.navy }) + T(tx, b2, 'Eindhoven', 78, { c: C.navy });
      const f1 = b2 + 112, rule = f1 + 88;
      s += T(M, f1, '9 minuten lopen naar het centrum', 31, { c: '#1D1D1B' }) + T(M, f1 + 46, '700 plekken · doorrijhoogte 2,00 m', 31, { c: '#1D1D1B' });
      s += `<rect x="${M}" y="${rule}" width="${W - 2 * M}" height="${0.1 * u}" fill="${C.navy}"/>`;
      s += PYS.fig('walk', 972 - PYS.figW('walk', 3 * u) - 12, rule, 3 * u, C.navy);
      const ly = reel ? 1512 : 1188;
      s += `<image href="../../kit/assets/logo-horizontal-color.svg" x="${M}" y="${ly}" height="54" width="195.6"/>` + T(972, ly + 44, 'parkingyou.nl', 31, { w: 700, anchor: 'end', c: C.navy });
    }
    if (type === 'evenement') {
      s += logo(M, M + dy);
      s += eyebrow(M, 351 + dy, 'Philips Stadion');
      const b1 = 500 + dy, lh = 90 * 50 / 48, sh = 3 * lh;
      s += PYS.stem(M, b1 - lh + 12, sh, C.aqua);
      const tx = M + PYS.stemW(sh) + 0.3 * sh;
      s += T(tx, b1, 'Wedstrijddag?', 90, { w: 800 }) + T(tx, b1 + lh, 'Parkeer naast', 90) + T(tx, b1 + 2 * lh, 'het stadion.', 90);
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
