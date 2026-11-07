// 09-ui figure helpers. Runs on load before the renderer takes the screenshot.
// 1. <i data-i="search" data-s="24"></i>  -> inline outline icon (24 grid, 2 px stroke, round caps and joins)
// 2. <span class="bub" data-size="64" data-fill="orange">content</span> -> the bubble (path from kit/assets/bubble.svg, never redrawn)
// 3. <div class="qr" data-size="132"></div> -> placeholder QR pattern (not a real code)
// Icons are placeholders in the B3 drawing logic until B3 picks the UI icon set.
(function () {
  const P = {
    search: '<circle cx="11" cy="11" r="7"/><path d="M16.5 16.5L21 21"/>',
    pin: '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    car: '<path d="M5 17H4a1 1 0 0 1-1-1v-4l2.2-5.1A2 2 0 0 1 7 5.7h10a2 2 0 0 1 1.8 1.2L21 12v4a1 1 0 0 1-1 1h-1"/><path d="M3 12h18M9.5 17h5"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/>',
    'chevron-left': '<path d="M15 18l-6-6 6-6"/>',
    'chevron-right': '<path d="M9 6l6 6-6 6"/>',
    'chevron-down': '<path d="M6 9l6 6 6-6"/>',
    check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    x: '<path d="M6 6l12 12M18 6L6 18"/>',
    alert: '<circle cx="12" cy="12" r="9"/><path d="M12 7.5V13M12 16.5h.01"/>',
    warning: '<path d="M12 3.5L2.8 19.5a1 1 0 0 0 .9 1.5h16.6a1 1 0 0 0 .9-1.5z"/><path d="M12 10v4M12 17.5h.01"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.5h.01"/>',
    'check-circle': '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.7 2.7L16 9.5"/>',
    'minus-circle': '<circle cx="12" cy="12" r="9"/><path d="M8 12h8"/>',
    lock: '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    user: '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    ticket: '<path d="M4 6h16a1 1 0 0 1 1 1v3a2 2 0 0 0 0 4v3a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-3a2 2 0 0 0 0-4V7a1 1 0 0 1 1-1z"/><path d="M14 6v2M14 11v2M14 16v2"/>',
    route: '<path d="M3 11l18-8-8 18-2-8z"/>',
    walk: '<circle cx="13" cy="4.5" r="1.8"/><path d="M9 21l3-7 3 3v4M7.5 12l2.5-4h4l2.5 3.5M12 14l1-6"/>',
    height: '<path d="M4 3h16M4 21h16M12 7v10M9 9.5L12 6.5l3 3M9 14.5l3 3 3-3"/>',
    menu: '<path d="M4 7h16M4 12h16M4 17h16"/>',
    card: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18M7 15h3"/>',
    mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    ev: '<path d="M9 3v5M15 3v5M6 8h12v3a6 6 0 0 1-12 0zM12 17v4"/>',
    home: '<path d="M4 11l8-7 8 7v9a1 1 0 0 1-1 1h-4v-6H9v6H5a1 1 0 0 1-1-1z"/>',
    arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
    edit: '<path d="M4 20h4L19 9l-4-4L4 16z"/>',
    garage: '<path d="M3 21V9l9-5 9 5v12"/><path d="M7 21v-8h10v8M7 17h10"/>',
    'calendar-plus': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4M12 13v5M9.5 15.5h5"/>',
    sliders: '<path d="M4 7h10M18 7h2M4 17h2M10 17h10"/><circle cx="16" cy="7" r="2"/><circle cx="8" cy="17" r="2"/>',
    spinner: '<path d="M12 3a9 9 0 1 0 9 9"/>',
    share: '<path d="M12 3v12M7 8l5-5 5 5M5 13v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/>',
    eye: '<path d="M2.5 12S6 5 12 5s9.5 7 9.5 7-3.5 7-9.5 7-9.5-7-9.5-7z"/><circle cx="12" cy="12" r="3"/>'
  };
  document.querySelectorAll('i[data-i]').forEach(el => {
    const s = el.dataset.s || 24;
    const cls = 'ic' + (el.className ? ' ' + el.className : '');
    const st = el.getAttribute('style') || '';
    el.outerHTML = `<svg class="${cls}" style="${st}" width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${P[el.dataset.i] || ''}</svg>`;
  });

  const BP = 'M18 0C8.059 0 0 8.058 0 17.999C0 34.701 16.691 43.074 16.691 43.074C17.264 43.423 18 43.006 18 42.335L18 35.997C27.941 35.997 36 27.939 36 17.999C36 8.058 27.941 0 18 0Z';
  const FILL = { navy: 'var(--py-bubble-navy)', aqua: 'var(--py-bubble-aqua)', orange: 'var(--py-bubble-orange)', white: 'var(--py-bubble-white)' };
  const INK = { navy: 'var(--py-text-on-brand)', aqua: 'var(--py-task-walk-fg)', orange: 'var(--py-task-pay-fg)', white: 'var(--py-surface-brand)' };
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
})();
