// 09-ui figure helpers. Runs on load before the renderer takes the screenshot.
// 1. <i data-i="search" data-s="24"></i>  -> inline UI icon (Tabler logic: 24 grid, 2 px stroke, round caps and joins)
// 2. <i data-pijl="right"></i>            -> de hoekige pijl (path from kit/assets/arrow-plain-navy.svg), never a chevron or Tabler arrow.
//    Default size = the cap height of the surrounding text (0.693 em), sitting on the baseline. data-s sets a fixed size in px.
//    Directions: right, down, left, up (45 degree steps: downright, upright, upleft), downleft uses arrow-downleft.
// 3. <span class="bub" data-size="64" data-fill="navy">content</span> -> the bubble (path from kit/assets/bubble.svg, never redrawn, never rotated)
// 4. <div class="voice"><div class="voice__text">...</div></div> -> de stem (kit/assets/arc.svg) left of the text block:
//    height = text block, stroke = 1/25 of the height (at least 1.5 px), gap = 0.3 x the height.
// 5. <div class="vak" data-ground="brand|light" data-h="144" data-shift="0">one bubble or one figure</div> -> het vak
//    (bay pitch 72, line 2 px, jouw vak filled with aqua side lines at double weight, lines run in from the top edge)
// 6. <div class="qr" data-size="132"></div> -> placeholder QR pattern (not a real code)
(function () {
  const P = {
    search: '<circle cx="10" cy="10" r="7"/><path d="M21 21l-6-6"/>',
    pin: '<path d="M9 11a3 3 0 1 0 6 0a3 3 0 0 0 -6 0"/><path d="M17.657 16.657l-4.243 4.243a2 2 0 0 1 -2.827 0l-4.244 -4.243a8 8 0 1 1 11.314 0z"/>',
    calendar: '<rect x="4" y="5" width="16" height="16" rx="2"/><path d="M16 3v4M8 3v4M4 11h16"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
    car: '<circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M5 17h-2v-6l2 -5h9l4 5h1a2 2 0 0 1 2 2v4h-2m-4 0h-6m-6 -6h15m-6 0v-5"/>',
    check: '<path d="M5 12l5 5l10 -10"/>',
    x: '<path d="M18 6l-12 12M6 6l12 12"/>',
    alert: '<circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/>',
    warning: '<path d="M12 9v4M10.363 3.591l-8.106 13.534a1.914 1.914 0 0 0 1.636 2.871h16.214a1.914 1.914 0 0 0 1.636 -2.87l-8.106 -13.536a1.914 1.914 0 0 0 -3.274 0zM12 16h.01"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v4h1"/>',
    'check-circle': '<circle cx="12" cy="12" r="9"/><path d="M9 12l2 2l4 -4"/>',
    'minus-circle': '<circle cx="12" cy="12" r="9"/><path d="M9 12h6"/>',
    lock: '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11v-4a4 4 0 1 1 8 0v4"/>',
    user: '<circle cx="12" cy="7" r="4"/><path d="M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2"/>',
    ticket: '<path d="M15 5v2M15 11v2M15 17v2M5 5h14a2 2 0 0 1 2 2v3a2 2 0 0 0 0 4v3a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-3a2 2 0 0 0 0 -4v-3a2 2 0 0 1 2 -2"/>',
    map: '<path d="M3 7l6 -3l6 3l6 -3v13l-6 3l-6 -3l-6 3v-13M9 4v13M15 7v13"/>',
    walk: '<circle cx="13" cy="4" r="1"/><path d="M7 21l3 -4M16 21l-2 -4l-3 -3l1 -6M6 12l2 -3l4 -1l3 3l3 1"/>',
    height: '<path d="M4 4h16M4 20h16M12 7v10M9 7h6M9 17h6"/>',
    menu: '<path d="M4 6h16M4 12h16M4 18h16"/>',
    card: '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M3 10h18M7 15h.01M11 15h2"/>',
    mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6l9 -6"/>',
    phone: '<path d="M5 4h4l2 5l-2.5 1.5a11 11 0 0 0 5 5l1.5 -2.5l5 2v4a2 2 0 0 1 -2 2a16 16 0 0 1 -15 -15a2 2 0 0 1 2 -2"/>',
    ev: '<path d="M9.785 6l8.215 8.215l-2.054 2.054a5.81 5.81 0 1 1 -8.215 -8.215l2.054 -2.054zM4 20l3.5 -3.5M15 4l-3.5 3.5M20 9l-3.5 3.5"/>',
    garage: '<path d="M3 21v-12l9 -5l9 5v12"/><path d="M7 21v-8h10v8M7 17h10"/>',
    'calendar-plus': '<path d="M12.5 21h-6.5a2 2 0 0 1 -2 -2v-12a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v5M16 3v4M8 3v4M4 11h16M16 19h6M19 16v6"/>',
    spinner: '<path d="M12 3a9 9 0 1 0 9 9"/>',
    share: '<circle cx="6" cy="12" r="3"/><circle cx="18" cy="6" r="3"/><circle cx="18" cy="18" r="3"/><path d="M8.7 10.7l6.6 -3.4M8.7 13.3l6.6 3.4"/>',
    wifi: '<path d="M12 18h.01M9.172 15.172a4 4 0 0 1 5.656 0M6.343 12.343a8 8 0 0 1 11.314 0M3.515 9.515c4.686 -4.687 12.284 -4.687 17 0"/>'
  };
  document.querySelectorAll('i[data-i]').forEach(el => {
    const s = el.dataset.s || 24;
    const cls = 'ic' + (el.className ? ' ' + el.className : '');
    const st = el.getAttribute('style') || '';
    el.outerHTML = `<svg class="${cls}" style="${st}" width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${P[el.dataset.i] || ''}</svg>`;
  });

  // De hoekige pijl: kit/assets/arrow-plain-navy.svg (py-atom-arrow-right-plain) and arrow-downleft-navy.svg, fill = currentColor.
  const AR = 'M161.762 0L125 19.794L174.279 102.376L0 102.376L0 147.059L174.618 147.059L125 230.205L161.762 249.999L249.999 125L161.762 0';
  const ADL = '<path d="M0 37.848L36.389 26.93L63.683 135.013L171.771 162.311L160.852 198.7L23.654 175.047L0 37.848"/><path d="M199.064 28.751L66.752 161.064L38 132.313L170.313 0L199.064 28.751"/>';
  const ROT = { right: 0, downright: 45, down: 90, downleft: 135, left: 180, upleft: 225, up: 270, upright: 315 };
  document.querySelectorAll('i[data-pijl]').forEach(el => {
    const d = el.dataset.pijl || 'right';
    const size = el.dataset.s ? el.dataset.s + 'px' : '0.693em';
    const st = el.getAttribute('style') || '';
    const cls = 'pijl' + (el.className ? ' ' + el.className : '');
    const body = d === 'downleft'
      ? `<svg viewBox="0 0 199.064 198.7" fill="currentColor">${ADL}</svg>`
      : `<svg viewBox="0 0 250 250" fill="currentColor"><path d="${AR}" transform="rotate(${ROT[d] || 0} 125 125)"/></svg>`;
    el.outerHTML = body.replace('<svg ', `<svg class="${cls}" aria-hidden="true" style="width:${size};height:${size};${st}" `);
  });

  const BP = 'M18 0C8.059 0 0 8.058 0 17.999C0 34.701 16.691 43.074 16.691 43.074C17.264 43.423 18 43.006 18 42.335L18 35.997C27.941 35.997 36 27.939 36 17.999C36 8.058 27.941 0 18 0Z';
  const FILL = { navy: 'var(--py-bubble-navy)', aqua: 'var(--py-bubble-aqua)', white: 'var(--py-bubble-white)' };
  const INK = { navy: 'var(--py-text-on-brand)', aqua: 'var(--py-task-walk-fg)', white: 'var(--py-surface-brand)' };
  document.querySelectorAll('.bub').forEach(el => {
    const w = +el.dataset.size, h = w * 43.423 / 36, f = el.dataset.fill || 'navy';
    const inner = el.innerHTML;
    const outline = f === 'white' && el.dataset.outline !== 'no';
    const vb = outline ? '-0.6 -0.6 37.2 44.623' : '0 0 36 43.423';
    const stroke = outline ? 'stroke:var(--py-surface-brand);stroke-width:1.2;' : '';
    el.style.cssText += `;position:relative;display:inline-block;flex:none;width:${w}px;height:${h.toFixed(1)}px;color:${INK[f]}`;
    el.innerHTML = `<svg viewBox="${vb}" width="${w}" height="${h.toFixed(1)}" style="position:absolute;left:0;top:0" aria-hidden="true"><path d="${BP}" style="fill:${FILL[f]};${stroke}"/></svg>` +
      `<span class="bub__c" style="position:absolute;left:0;top:0;width:${w}px;height:${w}px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">${inner}</span>`;
  });

  // Het vak: bay lines from the top edge, pitch 72, line 2 px; jouw vak filled, side lines aqua at 4 px; content centred in jouw vak.
  document.querySelectorAll('.vak').forEach(el => {
    const W = el.offsetWidth, H = +(el.dataset.h || 144), pitch = 72, brand = el.dataset.ground === 'brand';
    const line = brand ? 'var(--py-vak-line-on-brand)' : 'var(--py-vak-line)';
    const mine = brand ? 'var(--py-vak-mine-on-brand)' : 'var(--py-vak-mine)';
    const x0 = ((W / 2 - pitch / 2) % pitch + pitch) % pitch;
    const m = Math.round((W / 2 - pitch / 2 - x0) / pitch) + (+(el.dataset.shift || 0));
    const mx = x0 + m * pitch;
    let s = `<rect x="${mx}" y="0" width="${pitch}" height="${H}" fill="${mine}"/>`;
    for (let x = x0; x <= W; x += pitch) {
      const isEdge = Math.abs(x - mx) < 1 || Math.abs(x - mx - pitch) < 1;
      s += isEdge ? '' : `<rect x="${x - 1}" y="0" width="2" height="${H}" fill="${line}"/>`;
    }
    s += `<rect x="${mx - 2}" y="0" width="4" height="${H}" fill="var(--py-vak-mine-edge)"/><rect x="${mx + pitch - 2}" y="0" width="4" height="${H}" fill="var(--py-vak-mine-edge)"/>`;
    const inner = el.innerHTML;
    el.style.cssText += `;position:relative;height:${H}px;flex:none`;
    el.innerHTML = `<svg width="${W}" height="${H}" style="position:absolute;left:0;top:0" aria-hidden="true">${s}</svg>` +
      `<div style="position:absolute;left:${mx}px;top:0;width:${pitch}px;height:${H}px;display:flex;align-items:center;justify-content:center">${inner}</div>`;
  });

  document.querySelectorAll('.qr').forEach(el => {
    const n = 25, s = +(el.dataset.size || 132), m = s / (n + 2);
    let seed = 7; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
    let r = '';
    const inF = (x, y) => (x < 8 && y < 8) || (x > n - 9 && y < 8) || (x < 8 && y > n - 9);
    for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) if (!inF(x, y) && rnd() > 0.52) r += `<rect x="${(x + 1) * m}" y="${(y + 1) * m}" width="${m}" height="${m}"/>`;
    [[0, 0], [n - 7, 0], [0, n - 7]].forEach(([x, y]) => {
      r += `<rect x="${(x + 1.5) * m}" y="${(y + 1.5) * m}" width="${6 * m}" height="${6 * m}" fill="none" stroke="currentColor" stroke-width="${m}"/>`;
      r += `<rect x="${(x + 3) * m}" y="${(y + 3) * m}" width="${3 * m}" height="${3 * m}"/>`;
    });
    el.innerHTML = `<svg width="${s}" height="${s}" viewBox="0 0 ${s} ${s}" fill="currentColor" aria-label="QR-code (voorbeeld)">${r}</svg>`;
  });

  // De stem: sized after the fonts are in, so the text block has its final height.
  const ARC = 'M9.393 0.453C6.631 3.303 4.396 6.696 2.852 10.463C1.307 14.231 0.453 18.373 0.453 22.721C0.453 27.069 1.307 31.211 2.852 34.978C4.396 38.746 6.631 42.139 9.393 44.988';
  const stems = () => document.querySelectorAll('.voice').forEach(el => {
    const t = el.querySelector('.voice__text'); if (!t || el.querySelector('.voice__arc')) return;
    const h = t.getBoundingClientRect().height, w = h * 10 / 45.44, sw = Math.max(1.5, h / 25);
    const svg = `<svg class="voice__arc" aria-hidden="true" viewBox="0 0 10 45.44" preserveAspectRatio="none" width="${w.toFixed(1)}" height="${h.toFixed(1)}" style="flex:none;overflow:visible;margin-right:${(0.3 * h).toFixed(1)}px"><path d="${ARC}" fill="none" stroke="var(--py-voice-arc)" stroke-width="${sw.toFixed(2)}" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>`;
    t.insertAdjacentHTML('beforebegin', svg);
  });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(stems); else stems();
})();
