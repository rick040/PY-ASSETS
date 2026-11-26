import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Fonts} from './components';
import {colors, font} from './theme';
import {clamp, ease, tween, useUbuntu, width, wrap} from './LocatieSpot';
import {CTA_GEO, EindCta, type ZoekFormaat} from './ZoekSpot';
import {RESERVEERBAAR, locaties, type Locatie, type Prijs} from './locaties';
import type {Kaartje} from './kaartjes';

// "Het kaartje": a question about a well-known place, a real map (OpenStreetMap data in the house colours) with an aqua pin
// on the place; our nearest parkings drop in and the real walking route draws from the pin to each one. Then a card per
// parking in the style of the search-spot cards (photo, "Parking" + name, price pill, walking-time pill), nearest marked,
// and the shared end screen. 60 fps, 9:16 and 16:9. No box-shadows or blur, render in one tab (see LijstSpot).

type Geo = {
  w: number;
  h: number;
  logo: {y: number; w: number};
  vraag: {x: number; y: number; w: number; size: number; sub: number; align: 'center' | 'left'};
  /** Map card. staand: from under the question to above the cards. */
  kaart: {x: number; y: number | null; w: number; h: number | null};
  /** Parking cards. staand: bottom edge at `bodem`; liggend: under the question. */
  rij: {x: number; w: number; h: number; gap: number; naam: number; pill: number; pad: number; bodem: number | null};
  marker: number;
  pin: number;
  label: number;
};

const GEO: Record<ZoekFormaat, Geo> = {
  staand: {
    w: 1080,
    h: 1920,
    logo: {y: 250, w: 300},
    vraag: {x: 60, y: 360, w: 960, size: 80, sub: 46, align: 'center'},
    kaart: {x: 60, y: null, w: 960, h: null},
    rij: {x: 60, w: 960, h: 124, gap: 14, naam: 44, pill: 27, pad: 30, bodem: 1586},
    marker: 66,
    pin: 74,
    label: 30,
  },
  liggend: {
    w: 1920,
    h: 1080,
    logo: {y: 40, w: 250},
    vraag: {x: 110, y: 170, w: 760, size: 84, sub: 46, align: 'left'},
    kaart: {x: 960, y: 150, w: 850, h: 860},
    rij: {x: 110, w: 760, h: 136, gap: 16, naam: 42, pill: 26, pad: 28, bodem: null},
    marker: 66,
    pin: 78,
    label: 30,
  },
};

const MARKER_START = 80;
const MARKER_GAP = 55;

export const kaartTimeline = (n = 3) => {
  const markers = Array.from({length: n}, (_, i) => MARKER_START + i * MARKER_GAP);
  const rijen = Array.from({length: n}, (_, i) => markers[n - 1] + 60 + i * 22);
  const dichtst = rijen[n - 1] + 40;
  const cta = dichtst + 130;
  return {markers, rijen, dichtst, cta, duration: cta + 170};
};

const vind = (slug: string): Locatie => {
  const l = locaties.find((x) => x.slug === slug);
  if (!l) throw new Error(`Onbekende locatie ${slug}`);
  return l;
};

const pop = (frame: number, at: number, len = 18) => tween(frame, at, at + len, ease(0.3, 1.5, 0.5, 1));

const prijsTekst = (pr: Prijs) => (pr.bedrag === 'Gratis' ? `Gratis ${pr.eenheid}` : `${pr.vanaf ? 'vanaf ' : ''}${pr.bedrag} ${pr.eenheid}`);

/** The first part of a polyline, up to fraction p of its length. */
const deel = (pts: {x: number; y: number}[], p: number) => {
  if (p >= 1) return pts;
  const seg = pts.slice(1).map((q, i) => Math.hypot(q.x - pts[i].x, q.y - pts[i].y));
  let rest = seg.reduce((a, b) => a + b, 0) * Math.max(0, p);
  const out = [pts[0]];
  for (let i = 0; i < seg.length; i++) {
    if (rest >= seg[i]) {
      out.push(pts[i + 1]);
      rest -= seg[i];
    } else {
      const f = seg[i] ? rest / seg[i] : 0;
      out.push({x: pts[i].x + (pts[i + 1].x - pts[i].x) * f, y: pts[i].y + (pts[i + 1].y - pts[i].y) * f});
      break;
    }
  }
  return out;
};

const Pill: React.FC<{bg: string; color: string; size: number; children: React.ReactNode}> = ({bg, color, size, children}) => (
  <div
    style={{
      display: 'flex',
      alignItems: 'center',
      gap: size * 0.3,
      padding: `${size * 0.32}px ${size * 0.62}px`,
      borderRadius: 999,
      background: bg,
      color,
      fontWeight: 700,
      fontSize: size,
      lineHeight: 1.1,
      whiteSpace: 'nowrap',
    }}
  >
    {children}
  </div>
);

export const KaartSpot: React.FC<{kaartje: Kaartje; formaat?: ZoekFormaat}> = ({kaartje: k, formaat = 'staand'}) => {
  const frame = useCurrentFrame();
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: colors.blauw}} />;
  const g = GEO[formaat];
  const staand = formaat === 'staand';
  const n = k.parkings.length;
  const t = kaartTimeline(n);
  const ps = k.parkings.map((p) => ({...p, l: vind(p.locatie)}));
  const r = g.rij;

  const vraagIn = interpolate(frame, [0, 22], [0.5, 1], {...clamp, easing: ease(0.2, 0.9, 0.3, 1)});
  const subIn = tween(frame, 12, 36, ease(0.2, 0.9, 0.3, 1));
  const kaartIn = tween(frame, 20, 50, ease(0.2, 0.9, 0.3, 1));
  const zoom = tween(frame, 20, t.rijen[0], ease(0.4, 0, 0.2, 1));
  const pinIn = pop(frame, 44, 20);
  const out = tween(frame, t.cta - 6, t.cta + 14);
  const dichtstIn = tween(frame, t.dichtst, t.dichtst + 16);

  const breedsteWoord = Math.max(...k.vraag.split(' ').map((x) => width(x, g.vraag.size, '700')));
  const vraagSize = Math.min(g.vraag.size, (g.vraag.size * g.vraag.w) / breedsteWoord);
  const vraagLines = wrap(k.vraag, vraagSize, '700', g.vraag.w);
  const subLines = wrap(k.sub ?? 'Parkeer op loopafstand:', g.vraag.sub, '400', g.vraag.w);
  const vraagH = vraagLines.length * vraagSize * 1.1 + 10 + subLines.length * g.vraag.sub * 1.25;

  // Cards: 9:16 stacked above the bottom safe zone, 16:9 under the question.
  const rijenH = n * r.h + (n - 1) * r.gap;
  const rijY = r.bodem !== null ? r.bodem - rijenH : g.vraag.y + vraagH + 56;
  const kaartY = g.kaart.y ?? g.vraag.y + vraagH + 34;
  const W = g.kaart.w;
  const H = g.kaart.h ?? rijY - 26 - kaartY;

  // Map scale: the pin and all parkings fill the card, with room for the labels; same scale both ways (north up).
  const padX = 200;
  const padTop = 170;
  const padBot = 100;
  const xs = [0, ...ps.map((p) => p.dx)];
  const ys = [0, ...ps.map((p) => p.dy)];
  const [minX, maxX, minY, maxY] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
  const s = Math.min((W - 2 * padX) / Math.max(1, maxX - minX), (H - padTop - padBot) / Math.max(1, maxY - minY), 1.4);
  const offX = (W - (maxX - minX) * s) / 2;
  const offY = padTop + (H - padTop - padBot - (maxY - minY) * s) / 2;
  const toX = (dx: number) => offX + (dx - minX) * s;
  const toY = (dy: number) => offY + (maxY - dy) * s;
  const cx = toX(0);
  const cy = toY(0);
  const pos = ps.map((p) => ({x: toX(p.dx), y: toY(p.dy)}));

  // Label placement: every label above or below its point, whichever is free, and kept inside the card.
  type Box = {x1: number; y1: number; x2: number; y2: number};
  const raakt = (a: Box, b: Box) => a.x1 < b.x2 && b.x1 < a.x2 && a.y1 < b.y2 && b.y1 < a.y2;
  const binnen = (x: number, w: number) => Math.min(Math.max(x - w / 2, 14), W - 14 - w) - (x - w / 2);
  const m = g.marker;
  const pinH = g.pin * 1.32;
  const pinSize = g.label * 1.12;
  const pinW = width(k.plek, pinSize, '700') + pinSize * 1.24;
  const pinLH = pinSize * 1.1 + pinSize * 0.64;
  const markerBoxes: Box[] = pos.map((q) => ({x1: q.x - m / 2 - 6, y1: q.y - m / 2 - 6, x2: q.x + m / 2 + 6, y2: q.y + m / 2 + 6}));
  const pinBody: Box = {x1: cx - g.pin / 2, y1: cy - pinH, x2: cx + g.pin / 2, y2: cy};
  const pinShift = binnen(cx, pinW);
  const pinBoven: Box = {x1: cx - pinW / 2 + pinShift, y1: cy - pinH - 10 - pinLH, x2: cx + pinW / 2 + pinShift, y2: cy - pinH - 10};
  const pinOnderBox: Box = {x1: pinBoven.x1, y1: cy + 12, x2: pinBoven.x2, y2: cy + 12 + pinLH};
  const pinOnder = pinBoven.y1 < 8 || markerBoxes.some((b) => raakt(b, pinBoven));
  const bezet: Box[] = [pinOnder ? pinOnderBox : pinBoven, pinBody, ...markerBoxes];
  const mSize = g.label * 0.82;
  const labels = pos.map((q, i) => {
    const lw = width(`${ps[i].l.naam} · ${ps[i].tijd}`, mSize, '700') + mSize * 1.6;
    const lh = mSize * 1.1 + mSize * 0.64;
    const shift = binnen(q.x, lw);
    const onderBox: Box = {x1: q.x - lw / 2 + shift, y1: q.y + m / 2 + 8, x2: q.x + lw / 2 + shift, y2: q.y + m / 2 + 8 + lh};
    const bovenBox: Box = {x1: onderBox.x1, y1: q.y - m / 2 - 8 - lh, x2: onderBox.x2, y2: q.y - m / 2 - 8};
    const eigen = markerBoxes.filter((_, j) => j !== i);
    const vrij = (b: Box) => b.y1 > 6 && b.y2 < H - 6 && !bezet.filter((x) => !eigen.includes(x) || true).some((x) => x !== markerBoxes[i] && raakt(x, b));
    const onder = vrij(onderBox) || !vrij(bovenBox);
    bezet.push(onder ? onderBox : bovenBox);
    return {onder, shift};
  });
  // A slow push-in on the map while the parkings come in (around the pin, so nothing jumps).
  const z = 1.06 - 0.06 * zoom;

  return (
    <AbsoluteFill style={{background: colors.blauw, fontFamily: font}}>
      <Fonts />
      <div style={{position: 'absolute', top: g.logo.y, width: '100%', display: 'flex', justifyContent: 'center', opacity: 1 - out}}>
        <Img src={staticFile('svg/atom/py-atom-logo-horizontal-white.svg')} style={{width: g.logo.w, display: 'block'}} />
      </div>

      <AbsoluteFill style={{opacity: 1 - out, transform: `translateY(${-80 * out}px)`}}>
        {/* Question */}
        <div style={{position: 'absolute', left: g.vraag.x, top: g.vraag.y, width: g.vraag.w, color: colors.wit, textAlign: g.vraag.align}}>
          <div style={{fontSize: vraagSize, fontWeight: 700, lineHeight: 1.1, opacity: vraagIn, transform: `scale(${0.8 + 0.2 * vraagIn})`, transformOrigin: staand ? '50% 50%' : '0% 50%'}}>
            {vraagLines.map((x, i) => (
              <div key={i}>{x}</div>
            ))}
          </div>
          <div style={{fontSize: g.vraag.sub, lineHeight: 1.25, marginTop: 10, opacity: subIn, transform: `translateY(${(1 - subIn) * 30}px)`}}>
            {subLines.map((x, i) => (
              <div key={i}>{x}</div>
            ))}
          </div>
        </div>

        {/* Map card */}
        <div
          style={{
            position: 'absolute',
            left: g.kaart.x,
            top: kaartY,
            width: W,
            height: H,
            borderRadius: 40,
            overflow: 'hidden',
            border: `5px solid ${colors.wit}`,
            boxSizing: 'border-box',
            background: '#E7EBF3',
            opacity: kaartIn,
            transform: `scale(${0.94 + 0.06 * kaartIn})`,
          }}
        >
          <div style={{position: 'absolute', inset: 0, transform: `scale(${z})`, transformOrigin: `${cx}px ${cy}px`}}>
            <Img
              src={staticFile(k.kaart.src)}
              decoding="sync"
              style={{position: 'absolute', left: toX(k.kaart.x0), top: toY(k.kaart.y0), width: k.kaart.w * s, height: k.kaart.h * s, maxWidth: 'none'}}
            />
            {/* Walking routes, drawn from the pin out to each parking */}
            <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
              {ps.map((p, i) => {
                const d = tween(frame, t.markers[i] - 4, t.markers[i] + 26, ease(0.3, 0, 0.2, 1));
                if (d <= 0) return null;
                const pts = deel(
                  [...p.route].reverse().map(([x, y]) => ({x: toX(x), y: toY(y)})),
                  d,
                );
                return (
                  <polyline
                    key={i}
                    points={pts.map((q) => `${q.x.toFixed(1)},${q.y.toFixed(1)}`).join(' ')}
                    fill="none"
                    stroke={colors.blauw}
                    strokeWidth={9}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeDasharray="0.1 19"
                  />
                );
              })}
            </svg>

            {/* Parking markers with name and walking time */}
            {pos.map((q, i) => {
              const at = t.markers[i] + 22;
              if (frame < at) return null;
              const v = pop(frame, at);
              const m = g.marker;
              const {onder, shift} = labels[i];
              const eerste = i === 0;
              return (
                <div key={`m${i}`} style={{position: 'absolute', left: q.x, top: q.y, transform: `translate(-50%, -50%) scale(${v})`}}>
                  <div
                    style={{
                      width: m,
                      height: m,
                      borderRadius: m * 0.24,
                      background: eerste && dichtstIn > 0 ? colors.aqua : colors.blauw,
                      border: `5px solid ${colors.wit}`,
                      boxSizing: 'border-box',
                      color: colors.wit,
                      fontSize: m * 0.6,
                      fontWeight: 700,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      lineHeight: 1,
                    }}
                  >
                    P
                  </div>
                  <div style={{position: 'absolute', left: '50%', top: onder ? m + 8 : -(mSize * 1.74) - 8, transform: `translateX(calc(-50% + ${shift}px))`}}>
                    <Pill bg={colors.blauw} color={colors.wit} size={g.label * 0.82}>
                      {ps[i].l.naam}
                      <span style={{fontWeight: 400}}>· {ps[i].tijd}</span>
                    </Pill>
                  </div>
                </div>
              );
            })}

            {/* The place: aqua pin with its name */}
            <div style={{position: 'absolute', left: cx, top: cy, transform: `translate(-50%, -100%) scale(${pinIn})`, transformOrigin: '50% 100%', opacity: frame < 44 ? 0 : 1}}>
              <div style={{position: 'absolute', left: '50%', ...(pinOnder ? {top: pinH + 12} : {bottom: pinH + 10}), transform: `translateX(calc(-50% + ${pinShift}px))`}}>
                <Pill bg={colors.aqua} color={colors.wit} size={g.label * 1.12}>
                  {k.plek}
                </Pill>
              </div>
              <svg width={g.pin} height={g.pin * 1.32} viewBox="0 0 60 80" style={{display: 'block'}}>
                <path d="M30 78 C30 78 4 46 4 28 A26 26 0 1 1 56 28 C56 46 30 78 30 78 Z" fill={colors.aqua} stroke={colors.wit} strokeWidth={4} />
                <circle cx={30} cy={28} r={10} fill={colors.wit} />
              </svg>
            </div>
          </div>
          {/* Map data credit (ODbL) */}
          <div style={{position: 'absolute', right: 22, bottom: 16, fontSize: 18, color: colors.blauw, opacity: 0.7}}>© OpenStreetMap</div>
        </div>

        {/* Parking cards in the style of the search-spot cards */}
        {ps.map((p, i) => {
          const v = tween(frame, t.rijen[i], t.rijen[i] + 20, ease(0.2, 0.9, 0.3, 1));
          const eerste = i === 0;
          const naamMax = r.w - r.pad * 2 - 330;
          const naamSize = Math.min(r.naam, (r.naam * naamMax) / width(p.l.naam, r.naam, '700'));
          return (
            <div
              key={`r${i}`}
              style={{
                position: 'absolute',
                left: r.x,
                top: rijY + i * (r.h + r.gap),
                width: r.w,
                height: r.h,
                borderRadius: 30,
                overflow: 'hidden',
                border: `5px solid ${eerste && dichtstIn > 0 ? colors.aqua : colors.wit}`,
                boxSizing: 'border-box',
                background: colors.blauw,
                opacity: v,
                transform: `translateY(${(1 - v) * 40}px)`,
              }}
            >
              <Img src={staticFile(p.l.foto)} decoding="sync" style={{position: 'absolute', right: 0, top: 0, width: '62%', height: '100%', objectFit: 'cover'}} />
              <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(90deg, rgba(26,53,128,1) 38%, rgba(26,53,128,0.82) 62%, rgba(26,53,128,0.25) 100%)'}} />
              <div style={{position: 'absolute', left: r.pad, top: 0, bottom: 0, display: 'flex', flexDirection: 'column', justifyContent: 'center', color: colors.wit}}>
                <div style={{display: 'flex', alignItems: 'center', gap: 12, fontSize: r.naam * 0.62, lineHeight: 1.2}}>
                  Parking
                  {eerste ? (
                    <span style={{opacity: dichtstIn, fontSize: r.pill * 0.8, fontWeight: 700, padding: '3px 12px', borderRadius: 999, background: colors.aqua}}>dichtstbij</span>
                  ) : null}
                </div>
                <div style={{fontSize: naamSize, fontWeight: 700, lineHeight: 1.1, whiteSpace: 'nowrap'}}>{p.l.naam}</div>
              </div>
              <div style={{position: 'absolute', right: r.pad * 0.8, top: 0, bottom: 0, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'flex-end', gap: 10}}>
                <Pill bg={colors.aqua} color={colors.wit} size={r.pill}>
                  {prijsTekst(p.prijs ?? p.l.prijs)}
                </Pill>
                <Pill bg="rgba(255,255,255,0.94)" color={colors.blauw} size={r.pill}>
                  <Img src={staticFile('svg/atom/py-atom-figure-walk.svg')} style={{height: r.pill * 1.05, display: 'block'}} />
                  {p.tijd} lopen
                </Pill>
              </div>
            </div>
          );
        })}
      </AbsoluteFill>
      <EindCta start={t.cta} reserveer={ps.every((p) => RESERVEERBAAR.has(p.l.id))} k={CTA_GEO[formaat]} />
    </AbsoluteFill>
  );
};

export const KAART_SIZE: Record<ZoekFormaat, {width: number; height: number}> = {
  staand: {width: 1080, height: 1920},
  liggend: {width: 1920, height: 1080},
};
