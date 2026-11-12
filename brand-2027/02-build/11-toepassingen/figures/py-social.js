// ParkingYou 2027 social templates (post 4:5 and reel 9:16, u = 54 px). Needs py-fig.js and py-signs.js.
// PYSOC.post(type, fmt, opts) returns SVG markup for a 1080 x 1350 (post) or 1080 x 1920 (reel) frame.
// Types: 'aanbod' (de stem + de gastheer zwaait), 'locatie' (de stem + de loper), 'evenement' (de stem + de danser).
// Grounds are flat PY-Blauw or white (D44). Per frame the logo plus at most two elements.
const PYSOC = (() => {
  const u = 54, M = 108, W = 1080;
  const C = { navy: '#1A3580', aqua: '#32B9CD', white: '#FFFFFF' };
  const T = (x, y, s, size, o = {}) => `<text x="${x}" y="${y}" font-family="Ubuntu Sans" font-size="${size}" font-weight="${o.w || 400}" fill="${o.c || C.white}" ${o.anchor ? `text-anchor="${o.anchor}"` : ''} letter-spacing="${o.ls || 0}" style="font-variant-numeric:tabular-nums">${s}</text>`;
  const eyebrow = (x, y, s, c) => T(x, y, s.toUpperCase(), 24, { w: 700, c: c || C.aqua, ls: 1.9 });
  const logo = (x, y) => `<image href="../../kit/assets/logo-horizontal-reverse.svg" x="${x}" y="${y}" height="54" width="195.6"/>`;

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
      // Flat ground. Logo on the top margin, de stem opens the key line, price as plain text,
      // the gastheer zwaait (mirrored, faces the text) stands on a short 0.1u line on the bottom margin.
      const d = o.data || {}, light = d.ground === 'white';
      const ink = light ? C.navy : C.white, accent = light ? '#127C8C' : C.aqua;
      if (light) s = `<rect width="${W}" height="${H}" fill="#FFFFFF"/>`;
      const top = reel ? 5 * u : M, foot = reel ? 29 * u : H - M; // reel: key content between 5u and 29u (D16)
      s += light ? `<image href="../../kit/assets/logo-horizontal-color.svg" x="${M}" y="${top}" height="54" width="195.6"/>` : logo(M, top);
      const e = top + 6 * u;                       // eyebrow 6u under the logo
      s += eyebrow(M, e, d.eyebrow || 'Parking Hofplein', accent);
      const lh = 117 * 50 / 48, b1 = e + 2.5 * u, b2 = b1 + lh, sh = 2 * lh;
      s += PYS.stem(M, b1 - lh + 12, sh, C.aqua);
      const tx = M + PYS.stemW(sh) + 0.3 * sh;
      s += T(tx, b1, d.l1 || 'Jouw plek', 117, { w: 800, c: ink }) + T(tx, b2, d.l2 || 'staat klaar.', 117, { c: ink });
      const pb = b2 + 3 * u;
      s += T(M, pb, d.price || '€ 7,50', 78, { w: 800, c: ink }) + T(M + (d.priceW || 231), pb, d.unit || 'per dag', 31, { c: ink });
      s += T(M, pb + 58, d.body || 'Midden in Rotterdam, de hele dag.', 31, { c: light ? '#1D1D1B' : C.white });
      // the gastheer 7u on a short line of 0.1u (figure width plus 1u on the open side), feet on the bottom margin
      const fn = d.fig || 'cap-wave', fh = 7 * u, fw = PYS.figW(fn, fh), fx = W - M - fw;
      s += `<rect x="${fx - u}" y="${foot - 0.1 * u}" width="${fw + u}" height="${0.1 * u}" fill="${ink}"/>`;
      s += PYS.fig(fn, fx, foot - 0.1 * u, fh, ink, { flip: d.flip === undefined ? true : d.flip });
      s += T(M, foot - 6, d.cta || 'Reserveer je plek op parkingyou.nl', 31, { w: 700, c: ink });
    }
    if (type === 'locatie') {
      // white ground under the photo: de stem in PY-Aqua, the loper in navy
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
  return { post, guides, T, logo, eyebrow, C, u, M, W };
})();
