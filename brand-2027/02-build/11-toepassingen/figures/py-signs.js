// ParkingYou 2027 sign builders for chapter Toepassingen. Needs py-fig.js first (PY_ASSETS, pyBuild).
// All builders return SVG markup in millimetres (1 user unit = 1 mm). Call PYS.mount(id, markup) before DOMContentLoaded.
const PYS = (() => {
  const C = { navy: '#1A3580', aqua: '#32B9CD', orange: '#F08300', diep: '#0D142E', white: '#FFFFFF' };
  const aspect = n => { const v = PY_ASSETS[n].vb.split(' ').map(parseFloat); return v[2] / v[3]; };
  // de stem: height h, stroke 1/25 of h (built into the asset), width from the asset
  const stem = (x, y, h, col) => `<svg data-p="arc" x="${x}" y="${y}" width="${(h * aspect('arc')).toFixed(2)}" height="${h}" color="${col}"></svg>`;
  const stemW = h => h * aspect('arc');
  // de hoekige pijl in a square box of size s, rotated in 45 degree steps (0 = right, -90 = up)
  const arrow = (x, y, s, deg, col) => { const cx = x + s / 2, cy = y + s / 2;
    return `<g transform="rotate(${deg} ${cx} ${cy})"><svg data-p="arrow" x="${x}" y="${y}" width="${s}" height="${s}" color="${col}"></svg></g>`; };
  const picto = (n, x, y, s, col) => `<svg data-p="${n}" data-anchor="center" x="${x}" y="${y}" width="${s}" height="${s}" style="color:${col}"></svg>`;
  // a parkeerder standing with its feet on y (baseline); head colour default aqua; mono = one colour
  const fig = (n, x, base, h, col, o = {}) => { const w = h * aspect('fig-' + n);
    return `<svg data-p="fig-${n}" ${o.flip ? 'data-flip="1"' : ''} ${o.head ? `data-head="${o.head}"` : ''} x="${x}" y="${base - h}" width="${w.toFixed(2)}" height="${h}" color="${col}"></svg>`; };
  const figW = (n, h) => h * aspect('fig-' + n);
  const text = (x, y, s, size, col, o = {}) => `<text x="${x}" y="${y}" font-family="Ubuntu Sans" font-weight="${o.w || 700}" font-size="${size}" letter-spacing="${(size * 0.01).toFixed(2)}" fill="${col}" ${o.anchor ? `text-anchor="${o.anchor}"` : ''} style="font-variant-numeric:tabular-nums">${s}</text>`;

  // Route board: pill 200 high, u = 10, cap 70. Arrow and pictogram in a 2k box (2 x cap = 140, decision D37).
  // De stem is as high as that box, with 0.3 x its height of air on each side.
  // left: modules from the left end; right: modules from the right end. Module: ['picto',name] ['text',str] ['arrow',deg] ['stem'] ['fig',name,{flip}]
  function board(o) {
    const H = 200, w = o.w, u = 10, cap = 70, box = 2 * cap, y0 = (H - box) / 2, font = 101, x0 = 40, base = 100 + cap / 2;
    const fg = o.fg, stemCol = o.stem || fg;
    let s = `<rect width="${w}" height="${H}" rx="100" fill="${o.fill}"/>`;
    const place = (m, x) => {
      if (m[0] === 'picto') return [picto(m[1], x, y0, box, fg), box];
      if (m[0] === 'arrow') return [arrow(x, y0, box, m[1], fg), box];
      if (m[0] === 'stem') return [stem(x + 0.3 * box, y0, box, stemCol), stemW(box) + 0.6 * box];
      if (m[0] === 'gap') return ['', m[1]];
      if (m[0] === 'fig') { const h = base - 20; return [fig(m[1], x, base, h, fg, Object.assign({ head: o.head }, m[2] || {})), figW(m[1], h)]; }
      if (m[0] === 'text') return [text(x, base, m[1], font, fg), 0];
    };
    let x = x0;
    for (const m of (o.left || [])) { const [mk, mw] = place(m, x); s += mk; x += mw + (m[0] === 'stem' || m[0] === 'gap' ? 0 : (m[0] === 'fig' ? 2 * u : 0)); }
    x = w - x0;
    for (const m of (o.right || []).slice().reverse()) {
      const wdt = m[0] === 'stem' ? stemW(box) + 0.6 * box : (m[0] === 'gap' ? m[1] : box);
      x -= wdt; s += place(m, x)[0];
    }
    return s;
  }

  // Entrance lightbox face 1000 x 1000, u = 50, margin 100. kind: 'car' or 'walk'.
  function entrance(kind, name) {
    let s = `<rect width="1000" height="1000" fill="${C.navy}"/>`;
    s += `<image href="../../kit/assets/logo-horizontal-reverse.svg" x="100" y="100" height="200" width="724.4" preserveAspectRatio="xMinYMin meet"/>`;
    if (kind === 'car') {
      // P met dak 400 (8u) | stem 200 | pijl 200 (2k) linksonder
      s += `<svg data-p="p-roof" x="100" y="350" width="312" height="400" style="color:#FFFFFF"></svg>`;
      // arrow 2k = 200 (cap 100, decision D37), drawn as the straight arrow rotated 135 degrees so its length stays 200;
      // stem as high as the arrow module (200), 0.3 x 200 = 60 air on each side
      s += stem(472, 450, 200, C.aqua);
      s += arrow(472 + stemW(200) + 60 + 30, 450, 200, 135, '#FFFFFF');
      s += text(100, 900, name, 144.3, '#FFFFFF');
    } else {
      // loper 540 hoog (54 procent van de face) op de basislijn van de tekst | pijl 2k = 200
      s += fig('walk', 110, 900, 540, '#FFFFFF');
      s += arrow(620, 430, 200, 0, '#FFFFFF');
      s += text(430, 900, name, 144.3, '#FFFFFF');
    }
    return s;
  }

  function mount(id, markup) { document.getElementById(id).insertAdjacentHTML('beforeend', markup); }
  return { C, stem, stemW, arrow, picto, fig, figW, text, board, entrance, mount };
})();
