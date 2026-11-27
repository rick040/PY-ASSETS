import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import {Fonts} from './components';
import {colors, font} from './theme';
import {ease, tween, useUbuntu, wrap} from './LocatieSpot';
import {CTA_GEO, EindCta, type ZoekFormaat} from './ZoekSpot';
import {RESERVEERBAAR, locaties, type Locatie} from './locaties';
import {lus} from './AmsterdamLight';
import {kaartjes} from './kaartjes';
import type {Rondje} from './rondjes';

// "Rondje zoeken of rondje lopen?": left a car keeps circling past full car parks and a stress meter rises; right a walker goes
// from our parking to the place over the real route on a real map. Then the question, the answer with the walking time and
// the shared end screen. 60 fps, 9:16 and 16:9. No box-shadows or blur, render in one tab (see LijstSpot).

const ROOD = '#E30613';
const WARM = '#FFC95C';
const ORANJE = '#F08300';
const mix = (a: string, b: string, t: number) => {
  const p = (c: string) => [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16));
  const [x, y] = [p(a), p(b)];
  return `rgb(${x.map((v, i) => Math.round(v + (y[i] - v) * Math.max(0, Math.min(1, t)))).join(',')})`;
};

type Geo = {
  w: number;
  h: number;
  split: number;
  kop: {y: number; size: number};
  lus: {cx: number; cy: number; hw: number; hh: number; rad: number};
  kaart: {x: number; y: number; w: number; h: number};
  meter: {y: number};
  vraag: {y: number; size: number};
};

const GEO: Record<ZoekFormaat, Geo> = {
  staand: {
    w: 1080,
    h: 1920,
    split: 540,
    kop: {y: 290, size: 52},
    lus: {cx: 270, cy: 960, hw: 170, hh: 260, rad: 70},
    kaart: {x: 565, y: 520, w: 490, h: 880},
    meter: {y: 1450},
    vraag: {y: 820, size: 68},
  },
  liggend: {
    w: 1920,
    h: 1080,
    split: 960,
    kop: {y: 70, size: 50},
    lus: {cx: 480, cy: 560, hw: 220, hh: 230, rad: 80},
    kaart: {x: 1010, y: 200, w: 860, h: 640},
    meter: {y: 900},
    vraag: {y: 400, size: 60},
  },
};

export const rondjeTimeline = () => ({vraag: 330, keuze: 430, cta: 500, duration: 670});

const vind = (slug: string): Locatie => {
  const l = locaties.find((x) => x.slug === slug);
  if (!l) throw new Error(`Onbekende locatie ${slug}`);
  return l;
};

const prijsTekst = (l: Locatie, override?: {bedrag: string; eenheid: string}) => {
  const p = override ?? l.prijs;
  return p.bedrag === 'Gratis' ? `Gratis ${p.eenheid}` : `${p.bedrag} ${p.eenheid}`;
};

export const RondjeSpot: React.FC<{rondje: Rondje; formaat?: ZoekFormaat}> = ({rondje: r, formaat = 'staand'}) => {
  const frame = useCurrentFrame();
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: colors.blauw}} />;
  const g = GEO[formaat];
  const t = rondjeTimeline();
  const k = kaartjes.find((x) => x.slug === r.kaartje);
  if (!k) throw new Error(`Onbekend kaartje ${r.kaartje}`);
  const p = k.parkings[0];
  const l = vind(p.locatie);
  const L = g.lus;
  const inn = (at: number, len = 22) => tween(frame, at, at + len, ease(0.2, 0.9, 0.3, 1));

  // Left: car on the loop, stress rising.
  const stress = tween(frame, 30, t.vraag, ease(0.4, 0, 0.6, 1));
  const ronde = Math.max(0, (frame - 20) / 150);
  const [carX, carY, hoek] = lus(ronde, L.cx, L.cy, L.hw, L.hh, L.rad);
  const rondjes = Math.max(1, Math.min(9, Math.floor(ronde) + 1));
  const keuze = tween(frame, t.keuze, t.keuze + 30, ease(0.4, 0, 0.2, 1));

  // Right: real map with the walking route; scale to fit route and place.
  const M = g.kaart;
  const pad = 70;
  const route = [...p.route].reverse().reverse(); // parking -> place
  const xs = [0, ...route.map((q) => q[0])];
  const ys = [0, ...route.map((q) => q[1])];
  const [minX, maxX, minY, maxY] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
  const s = Math.min((M.w - 2 * pad) / Math.max(1, maxX - minX), (M.h - 2 * pad - 60) / Math.max(1, maxY - minY), 1.6);
  const offX = (M.w - (maxX - minX) * s) / 2;
  const offY = 60 + (M.h - 60 - (maxY - minY) * s) / 2;
  const toX = (dx: number) => offX + (dx - minX) * s;
  const toY = (dy: number) => offY + (maxY - dy) * s;
  const pts = route.map(([x, y]) => ({x: toX(x), y: toY(y)}));
  const cum = [0];
  for (let i = 1; i < pts.length; i++) cum.push(cum[i - 1] + Math.hypot(pts[i].x - pts[i - 1].x, pts[i].y - pts[i - 1].y));
  const total = cum[cum.length - 1];
  const loop = tween(frame, 50, 300, ease(0.3, 0, 0.6, 1));
  const afstand = total * loop;
  let ci = 0;
  while (ci < cum.length - 2 && cum[ci + 1] < afstand) ci++;
  const f = Math.min(1, Math.max(0, (afstand - cum[ci]) / Math.max(1e-6, cum[ci + 1] - cum[ci])));
  const loper = {x: pts[ci].x + (pts[ci + 1].x - pts[ci].x) * f, y: pts[ci].y + (pts[ci + 1].y - pts[ci].y) * f};
  const gelopen = [...pts.slice(0, ci + 1), loper];
  const aan = frame >= 300;

  const kopStyle: React.CSSProperties = {position: 'absolute', top: g.kop.y, width: '100%', textAlign: 'center', color: colors.wit};
  const antwoord = `Zet je auto ${r.wanneer ? r.wanneer + ' ' : ''}in ${r.bij ?? `Parking ${l.naam}`} en loop in ${p.tijd.replace(" ", "\u00a0")} naar ${r.naar}.`;
  const antwoordLines = wrap(antwoord, g.vraag.size * 0.9, '700', g.w - 220);

  return (
    <AbsoluteFill style={{background: colors.blauw, fontFamily: font, overflow: 'hidden'}}>
      <Fonts />
      {/* Left: searching */}
      <div style={{position: 'absolute', left: 0, top: 0, width: g.split, height: g.h, background: '#0F1D45', overflow: 'hidden', opacity: 1 - 0.6 * keuze}}>
        <svg width={g.split} height={g.h} style={{position: 'absolute', inset: 0}}>
          <rect x={L.cx - L.hw + 70} y={L.cy - L.hh + 70} width={2 * L.hw - 140} height={2 * L.hh - 140} rx={18} fill="#1A2C63" />
          {[
            [L.cx - L.hw - 160, L.cy - L.hh - 150],
            [L.cx + L.hw + 50, L.cy - L.hh - 150],
            [L.cx - L.hw - 160, L.cy + L.hh + 50],
            [L.cx + L.hw + 50, L.cy + L.hh + 50],
          ]
            .filter(([x]) => x >= 10 && x + 110 <= g.split - 10)
            .map(([x, y], i) => (
              <rect key={i} x={x} y={y} width={110} height={100} rx={18} fill="#1A2C63" />
            ))}
          <rect x={L.cx - L.hw} y={L.cy - L.hh} width={2 * L.hw} height={2 * L.hh} rx={L.rad} fill="none" stroke="#2A3F7E" strokeWidth={76} />
          {[
            [L.cx, L.cy - 100],
            [L.cx + L.hw + 30, L.cy - L.hh + 120],
            [L.cx - L.hw - 30, L.cy + L.hh - 140],
          ].map(([x, y], i) => (
            <g key={i} transform={`translate(${x} ${y})`} opacity={inn(40 + i * 50)}>
              <rect x={-34} y={-34} width={68} height={68} rx={14} fill={colors.blauw} stroke={colors.wit} strokeWidth={4} />
              <text x={0} y={14} fill={colors.wit} fontSize={42} fontWeight={700} textAnchor="middle" fontFamily="Ubuntu">P</text>
              <rect x={-38} y={40} width={76} height={34} rx={8} fill={ROOD} />
              <text x={0} y={66} fill={colors.wit} fontSize={24} fontWeight={700} textAnchor="middle" fontFamily="Ubuntu">VOL</text>
            </g>
          ))}
          <g transform={`translate(${carX} ${carY}) rotate(${(hoek * 180) / Math.PI + 90})`}>
            <rect x={-24} y={-44} width={48} height={88} rx={14} fill={colors.wit} />
            <rect x={-18} y={-30} width={36} height={18} rx={5} fill="#0F1D45" />
            <rect x={-18} y={16} width={36} height={14} rx={5} fill="#0F1D45" />
            <rect x={-20} y={-46} width={12} height={6} rx={3} fill={WARM} />
            <rect x={8} y={-46} width={12} height={6} rx={3} fill={WARM} />
          </g>
        </svg>
        <div style={kopStyle}>
          <div style={{fontSize: g.kop.size, fontWeight: 700}}>Rondje zoeken</div>
          <div style={{fontSize: g.kop.size * 0.7, marginTop: 6, opacity: 0.85}}>rondje {rondjes}</div>
        </div>
        <div style={{position: 'absolute', left: 60, right: 60, top: g.meter.y, color: colors.wit, fontSize: 32, fontWeight: 700}}>
          <div style={{marginBottom: 10}}>Stress</div>
          <div style={{height: 34, borderRadius: 999, background: '#24356E', overflow: 'hidden'}}>
            <div style={{width: `${8 + 92 * stress}%`, height: '100%', borderRadius: 999, background: stress < 0.5 ? mix(colors.aqua, WARM, stress * 2) : mix(WARM, ORANJE, (stress - 0.5) * 2)}} />
          </div>
        </div>
      </div>

      {/* Right: walking from our parking on the real map */}
      <div style={{position: 'absolute', left: g.split, top: 0, width: g.w - g.split, height: g.h, background: colors.blauw}}>
        <div style={{...kopStyle, top: g.kop.y}}>
          <div style={{fontSize: g.kop.size, fontWeight: 700}}>Rondje lopen</div>
          <div style={{fontSize: g.kop.size * 0.7, marginTop: 6, opacity: 0.85}}>naar {r.naar}</div>
        </div>
      </div>
      <div style={{position: 'absolute', left: M.x, top: M.y, width: M.w, height: M.h, borderRadius: 32, overflow: 'hidden', border: `5px solid ${colors.wit}`, boxSizing: 'border-box', background: '#E7EBF3'}}>
        <Img src={staticFile(k.kaart.src)} decoding="sync" style={{position: 'absolute', left: toX(k.kaart.x0), top: toY(k.kaart.y0), width: k.kaart.w * s, height: k.kaart.h * s, maxWidth: 'none'}} />
        <svg width={M.w} height={M.h} style={{position: 'absolute', left: 0, top: 0}}>
          <polyline points={pts.map((q) => `${q.x.toFixed(1)},${q.y.toFixed(1)}`).join(' ')} fill="none" stroke={colors.blauw} strokeOpacity={0.3} strokeWidth={7} strokeDasharray="0.1 16" strokeLinecap="round" />
          <polyline points={gelopen.map((q) => `${q.x.toFixed(1)},${q.y.toFixed(1)}`).join(' ')} fill="none" stroke={colors.blauw} strokeWidth={9} strokeDasharray="0.1 16" strokeLinecap="round" />
        </svg>
        {/* Parking at the start */}
        <div style={{position: 'absolute', left: pts[0].x - 30, top: pts[0].y - 30, width: 60, height: 60, borderRadius: 14, background: colors.blauw, border: `5px solid ${colors.wit}`, boxSizing: 'border-box', color: colors.wit, fontSize: 34, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>P</div>
        {/* The place */}
        <div style={{position: 'absolute', left: toX(0), top: toY(0), transform: 'translate(-50%, -100%)'}}>
          <svg width={56} height={74} viewBox="0 0 60 80" style={{display: 'block'}}>
            <path d="M30 78 C30 78 4 46 4 28 A26 26 0 1 1 56 28 C56 46 30 78 30 78 Z" fill={colors.aqua} stroke={colors.wit} strokeWidth={4} />
            <circle cx={30} cy={28} r={10} fill={colors.wit} />
          </svg>
        </div>
        {/* Walker */}
        {!aan ? (
          <div style={{position: 'absolute', left: loper.x - 22, top: loper.y - 64 - Math.abs(Math.sin(frame / 5)) * 5}}>
            <Img src={staticFile('svg/atom/py-atom-figure-walk.svg')} style={{height: 64, display: 'block'}} />
          </div>
        ) : null}
        <div style={{position: 'absolute', right: 16, bottom: 12, fontSize: 16, color: colors.blauw, opacity: 0.7}}>© OpenStreetMap</div>
      </div>
      <div style={{position: 'absolute', left: g.split + 30, right: 30, top: M.y + M.h + 24, display: 'flex', flexWrap: 'wrap', gap: 12, justifyContent: 'center', opacity: inn(60)}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 10, padding: '10px 22px', borderRadius: 999, background: colors.wit, color: colors.blauw, fontSize: 30, fontWeight: 700}}>
          <Img src={staticFile('svg/atom/py-atom-figure-walk.svg')} style={{height: 30, display: 'block'}} />
          {p.tijd} lopen
        </div>
        <div style={{padding: '10px 22px', borderRadius: 999, background: colors.aqua, color: colors.wit, fontSize: 30, fontWeight: 700}}>{prijsTekst(l, p.prijs)}</div>
      </div>
      <div style={{position: 'absolute', left: g.split - 2, top: 0, width: 4, height: g.h, background: colors.wit, opacity: 1 - keuze}} />

      {/* Question, then the answer, over a dimmed scene */}
      <AbsoluteFill style={{background: '#0F1D45', opacity: 0.6 * inn(t.vraag - 10, 26)}} />
      <div style={{position: 'absolute', left: 40, right: 40, top: g.vraag.y, textAlign: 'center', opacity: inn(t.vraag) * (1 - tween(frame, t.keuze - 6, t.keuze + 10))}}>
        <div style={{display: 'inline-block', padding: '24px 40px', borderRadius: 40, background: colors.blauw, border: `5px solid ${colors.wit}`, color: colors.wit, fontSize: g.vraag.size, fontWeight: 700, lineHeight: 1.1}}>
          Rondje zoeken of
          <br />
          rondje lopen?
        </div>
      </div>
      <div style={{position: 'absolute', left: 50, right: 50, top: g.vraag.y - 10, textAlign: 'center', opacity: inn(t.keuze + 6) * (1 - tween(frame, t.cta - 10, t.cta + 6))}}>
        <div style={{display: 'inline-block', padding: '24px 40px', borderRadius: 40, background: colors.aqua, color: colors.wit, fontSize: g.vraag.size * 0.9, fontWeight: 700, lineHeight: 1.12}}>
          {antwoordLines.map((x, i) => (
            <div key={i}>{x}</div>
          ))}
        </div>
      </div>
      <AbsoluteFill style={{background: colors.blauw, opacity: 0.9 * tween(frame, t.cta - 10, t.cta + 16)}} />
      <EindCta start={t.cta} reserveer={RESERVEERBAAR.has(l.id)} k={CTA_GEO[formaat]} />
    </AbsoluteFill>
  );
};

export const RONDJE_SIZE: Record<ZoekFormaat, {width: number; height: number}> = {
  staand: {width: 1080, height: 1920},
  liggend: {width: 1920, height: 1080},
};
