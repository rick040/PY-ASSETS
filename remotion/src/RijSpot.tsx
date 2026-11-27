import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Fonts} from './components';
import {colors, font} from './theme';
import {clamp, ease, tween, useUbuntu, width, wrap} from './LocatieSpot';
import {CTA_GEO, EindCta, type ZoekFormaat} from './ZoekSpot';
import {RESERVEERBAAR, locaties, type Locatie} from './locaties';
import type {Rijroute} from './rijroutes';

// "Zo rijd je erin": a question ("Waar is de inrit?"), a real map with the last stretch to the garage entrance; a car drives
// it, the route fills in behind the car, each step (street, turn, entrance) appears as the car passes it, both on the map
// and as a row under it. Then the P at the entrance and the shared end screen. 60 fps, 9:16 and 16:9.
// No box-shadows or blur, render in one tab (see LijstSpot).

type Geo = {
  w: number;
  h: number;
  logo: {y: number; w: number};
  vraag: {x: number; y: number; w: number; size: number; sub: number; align: 'center' | 'left'};
  kaart: {x: number; y: number | null; w: number; h: number | null};
  rij: {x: number; w: number; h: number; gap: number; tekst: number; bodem: number | null};
  auto: number;
  label: number;
};

const GEO: Record<ZoekFormaat, Geo> = {
  staand: {
    w: 1080,
    h: 1920,
    logo: {y: 250, w: 300},
    vraag: {x: 60, y: 360, w: 960, size: 78, sub: 46, align: 'center'},
    kaart: {x: 60, y: null, w: 960, h: null},
    rij: {x: 60, w: 960, h: 104, gap: 12, tekst: 40, bodem: 1586},
    auto: 64,
    label: 30,
  },
  liggend: {
    w: 1920,
    h: 1080,
    logo: {y: 40, w: 250},
    vraag: {x: 110, y: 170, w: 760, size: 76, sub: 42, align: 'left'},
    kaart: {x: 960, y: 150, w: 850, h: 860},
    rij: {x: 110, w: 760, h: 100, gap: 14, tekst: 36, bodem: null},
    auto: 60,
    label: 28,
  },
};

const START = 60;
const RIJDEN = 300;

export const rijTimeline = () => {
  const aankomst = START + RIJDEN;
  const cta = aankomst + 130;
  return {start: START, aankomst, cta, duration: cta + 170};
};

const vind = (slug: string): Locatie => {
  const l = locaties.find((x) => x.slug === slug);
  if (!l) throw new Error(`Onbekende locatie ${slug}`);
  return l;
};

const PIJL = {rechtdoor: 0, rechts: 90, links: -90, inrit: 0};

export const RijSpot: React.FC<{route: Rijroute; formaat?: ZoekFormaat}> = ({route: r, formaat = 'staand'}) => {
  const frame = useCurrentFrame();
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: colors.blauw}} />;
  const g = GEO[formaat];
  const t = rijTimeline();
  const l = vind(r.locatie);
  const staand = formaat === 'staand';
  const n = r.stappen.length;

  const vraagIn = interpolate(frame, [0, 22], [0.5, 1], {...clamp, easing: ease(0.2, 0.9, 0.3, 1)});
  const subIn = tween(frame, 12, 36, ease(0.2, 0.9, 0.3, 1));
  const kaartIn = tween(frame, 20, 50, ease(0.2, 0.9, 0.3, 1));
  const out = tween(frame, t.cta - 6, t.cta + 14);

  const vraagLines = wrap(r.vraag, g.vraag.size, '700', g.vraag.w);
  const subLines = wrap('Zo rijd je erin:', g.vraag.sub, '400', g.vraag.w);
  const vraagH = vraagLines.length * g.vraag.size * 1.1 + 10 + subLines.length * g.vraag.sub * 1.25;

  const rij = g.rij;
  const rijenH = n * rij.h + (n - 1) * rij.gap;
  const rijY = rij.bodem !== null ? rij.bodem - rijenH : g.vraag.y + vraagH + 50;
  const kaartY = g.kaart.y ?? g.vraag.y + vraagH + 30;
  const W = g.kaart.w;
  const H = g.kaart.h ?? rijY - 24 - kaartY;

  // Scale: the route and the entrance fill the card with room for the labels; north up, same scale both ways.
  const pad = 120;
  const xs = [0, ...r.route.map((p) => p[0])];
  const ys = [0, ...r.route.map((p) => p[1])];
  const [minX, maxX, minY, maxY] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
  const s = Math.min((W - 2 * pad) / Math.max(1, maxX - minX), (H - 2 * pad) / Math.max(1, maxY - minY), 2.4);
  const offX = (W - (maxX - minX) * s) / 2;
  const offY = (H - (maxY - minY) * s) / 2;
  const toX = (dx: number) => offX + (dx - minX) * s;
  const toY = (dy: number) => offY + (maxY - dy) * s;
  const pts = r.route.map(([x, y]) => ({x: toX(x), y: toY(y)}));

  // Distance along the route (screen px) for every vertex, and where each step sits on it.
  const cum = [0];
  for (let i = 1; i < pts.length; i++) cum.push(cum[i - 1] + Math.hypot(pts[i].x - pts[i - 1].x, pts[i].y - pts[i - 1].y));
  const total = cum[cum.length - 1];
  const stapD = r.stappen.map((st) => {
    const sx = toX(st.x), sy = toY(st.y);
    let best = 0, bd = Infinity;
    pts.forEach((p, i) => {
      const d = Math.hypot(p.x - sx, p.y - sy);
      if (d < bd) { bd = d; best = i; }
    });
    return cum[best];
  });

  const prog = tween(frame, t.start, t.aankomst, ease(0.42, 0, 0.5, 1));
  const afstand = total * prog;
  // Car position and heading.
  let ci = 0;
  while (ci < cum.length - 2 && cum[ci + 1] < afstand) ci++;
  const segL = Math.max(1e-6, cum[ci + 1] - cum[ci]);
  const f = Math.min(1, Math.max(0, (afstand - cum[ci]) / segL));
  const a = pts[ci], b = pts[ci + 1];
  const car = {x: a.x + (b.x - a.x) * f, y: a.y + (b.y - a.y) * f};
  const hoek = (Math.atan2(b.y - a.y, b.x - a.x) * 180) / Math.PI + 90;
  const gereden = [...pts.slice(0, ci + 1), car];
  const stapAt = (i: number) => t.start + Math.round(RIJDEN * (i === n - 1 ? 1 : Math.min(0.98, (stapD[i] / total) ** 0.95)));
  const pIn = tween(frame, t.aankomst, t.aankomst + 20, ease(0.3, 1.5, 0.5, 1));

  return (
    <AbsoluteFill style={{background: colors.blauw, fontFamily: font}}>
      <Fonts />
      <div style={{position: 'absolute', top: g.logo.y, width: '100%', display: 'flex', justifyContent: 'center', opacity: 1 - out}}>
        <Img src={staticFile('svg/atom/py-atom-logo-horizontal-white.svg')} style={{width: g.logo.w, display: 'block'}} />
      </div>
      <AbsoluteFill style={{opacity: 1 - out, transform: `translateY(${-80 * out}px)`}}>
        <div style={{position: 'absolute', left: g.vraag.x, top: g.vraag.y, width: g.vraag.w, color: colors.wit, textAlign: g.vraag.align}}>
          <div style={{fontSize: g.vraag.size, fontWeight: 700, lineHeight: 1.1, opacity: vraagIn, transform: `scale(${0.8 + 0.2 * vraagIn})`, transformOrigin: staand ? '50% 50%' : '0% 50%'}}>
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
        <div style={{position: 'absolute', left: g.kaart.x, top: kaartY, width: W, height: H, borderRadius: 40, overflow: 'hidden', border: `5px solid ${colors.wit}`, boxSizing: 'border-box', background: '#E7EBF3', opacity: kaartIn, transform: `scale(${0.94 + 0.06 * kaartIn})`}}>
          <Img src={staticFile(r.kaart.src)} decoding="sync" style={{position: 'absolute', left: toX(r.kaart.x0), top: toY(r.kaart.y0), width: r.kaart.w * s, height: r.kaart.h * s, maxWidth: 'none'}} />
          <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
            {/* The whole stretch faint, the driven part solid with a white edge */}
            <polyline points={pts.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ')} fill="none" stroke={colors.blauw} strokeOpacity={0.35} strokeWidth={8} strokeDasharray="2 16" strokeLinecap="round" strokeLinejoin="round" />
            {frame >= t.start ? (
              <>
                <polyline points={gereden.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ')} fill="none" stroke={colors.wit} strokeWidth={24} strokeLinecap="round" strokeLinejoin="round" />
                <polyline points={gereden.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ')} fill="none" stroke={colors.aqua} strokeWidth={14} strokeLinecap="round" strokeLinejoin="round" />
              </>
            ) : null}
          </svg>
          {/* Step labels on the map */}
          {r.stappen.slice(0, n - 1).map((st, i) => {
            const at = stapAt(i);
            if (frame < at) return null;
            const x = toX(st.x), y = toY(st.y);
            // A label close to the entrance makes way for the P when the car arrives.
            const dichtbij = Math.hypot(x - toX(0), y - toY(0)) < 220;
            const weg = dichtbij ? tween(frame, t.aankomst - 12, t.aankomst + 4) : 0;
            if (weg >= 1) return null;
            const v = tween(frame, at, at + 18, ease(0.3, 1.5, 0.5, 1)) * (1 - weg);
            const lw = width(st.label, g.label, '700') + g.label * 1.3;
            const shift = Math.min(Math.max(x - lw / 2, 14), W - 14 - lw) - (x - lw / 2);
            return (
              <div key={i} style={{position: 'absolute', left: x, top: y - g.label * 2.7, transform: `translateX(calc(-50% + ${shift}px)) scale(${v})`, padding: `${g.label * 0.3}px ${g.label * 0.65}px`, borderRadius: 999, background: colors.blauw, color: colors.wit, fontSize: g.label, fontWeight: 700, whiteSpace: 'nowrap'}}>
                {st.label}
              </div>
            );
          })}
          {/* The entrance */}
          {frame >= t.aankomst ? (
            <div style={{position: 'absolute', left: toX(0), top: toY(0), transform: `translate(-50%, -50%) scale(${pIn})`}}>
              <div style={{width: g.auto * 1.15, height: g.auto * 1.15, borderRadius: g.auto * 0.28, background: colors.aqua, border: `5px solid ${colors.wit}`, boxSizing: 'border-box', color: colors.wit, fontSize: g.auto * 0.7, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>P</div>
              <div style={{position: 'absolute', left: '50%', top: g.auto * 1.15 + 8, transform: 'translateX(-50%)', padding: `${g.label * 0.3}px ${g.label * 0.65}px`, borderRadius: 999, background: colors.aqua, color: colors.wit, fontSize: g.label, fontWeight: 700, whiteSpace: 'nowrap'}}>
                Inrit · Parking {l.naam}
              </div>
            </div>
          ) : null}
          {/* The car (top view) */}
          {frame < t.aankomst + 6 ? (
            <svg width={g.auto} height={g.auto * 1.7} viewBox="0 0 40 68" style={{position: 'absolute', left: car.x - g.auto / 2, top: car.y - g.auto * 0.85, transform: `rotate(${hoek}deg)`, opacity: 1 - tween(frame, t.aankomst, t.aankomst + 6)}}>
              <rect x={2} y={2} width={36} height={64} rx={12} fill={colors.blauw} stroke={colors.wit} strokeWidth={3} />
              <rect x={7} y={14} width={26} height={12} rx={4} fill="#9FD9E3" />
              <rect x={7} y={44} width={26} height={9} rx={3} fill="#9FD9E3" />
              <rect x={5} y={3} width={8} height={4} rx={2} fill="#FFE7AD" />
              <rect x={27} y={3} width={8} height={4} rx={2} fill="#FFE7AD" />
            </svg>
          ) : null}
          <div style={{position: 'absolute', right: 22, bottom: 16, fontSize: 18, color: colors.blauw, opacity: 0.7}}>© OpenStreetMap</div>
        </div>

        {/* Steps as rows */}
        {r.stappen.map((st, i) => {
          const at = stapAt(i);
          const v = tween(frame, at, at + 20, ease(0.2, 0.9, 0.3, 1));
          const inrit = st.pijl === 'inrit';
          return (
            <div key={i} style={{position: 'absolute', left: rij.x, top: rijY + i * (rij.h + rij.gap), width: rij.w, height: rij.h, borderRadius: 26, background: colors.wit, color: colors.blauw, border: `5px solid ${inrit && frame >= at ? colors.aqua : colors.wit}`, boxSizing: 'border-box', display: 'flex', alignItems: 'center', gap: 22, padding: '0 26px', opacity: 0.35 + 0.65 * v, transform: `translateX(${(1 - v) * 30}px)`}}>
              <div style={{flex: 'none', width: rij.h * 0.62, height: rij.h * 0.62, borderRadius: inrit ? rij.h * 0.14 : '50%', background: inrit ? colors.aqua : colors.blauw, display: 'flex', alignItems: 'center', justifyContent: 'center', color: colors.wit, fontSize: rij.h * 0.36, fontWeight: 700}}>
                {inrit ? 'P' : <Img src={staticFile('svg/atom/py-atom-arrow-up-plain.svg')} style={{width: rij.h * 0.32, height: rij.h * 0.32, display: 'block', filter: 'brightness(0) invert(1)', transform: `rotate(${PIJL[st.pijl]}deg)`}} />}
              </div>
              <div style={{fontSize: rij.tekst, fontWeight: inrit ? 700 : 500, lineHeight: 1.1}}>{st.tekst}</div>
            </div>
          );
        })}
      </AbsoluteFill>
      <EindCta start={t.cta} reserveer={RESERVEERBAAR.has(l.id)} k={CTA_GEO[formaat]} />
    </AbsoluteFill>
  );
};

export const RIJ_SIZE: Record<ZoekFormaat, {width: number; height: number}> = {
  staand: {width: 1080, height: 1920},
  liggend: {width: 1920, height: 1080},
};
