import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import {Fonts} from './components';
import {colors, font} from './theme';
import {ease, tween, useUbuntu, wrap} from './LocatieSpot';
import {CTA_GEO, EindCta, type ZoekFormaat} from './ZoekSpot';
import {RESERVEERBAAR, locaties} from './locaties';
import {AUTO_PAD, AUTO_VB} from './autoPad';
import {Feiten, type FeitenGeo} from './Feiten';
import type {Laden} from './laden';

// "Stekker erin": an almost empty battery blinks ("Elektrisch rijden?"), a car drives up to a charging post, the cable
// is drawn and clicks in, energy runs along it and the battery fills while the text says "Je auto laadt, terwijl jij in
// Artis bent." Then three facts and the shared end screen. No percentages or charging times: the pages do not give them.
// 60 fps, 9:16 and 16:9. No box-shadows or blur, render in one tab (see LijstSpot).

type Geo = {
  w: number;
  h: number;
  tekst: {x: number; y: number; w: number; size: number; align: 'center' | 'left'};
  /** Battery: centre and outer size. */
  accu: {cx: number; cy: number; w: number; h: number};
  /** Ground line, charging post (left edge, width, height) and car (centre x, width, start x off screen). */
  grond: number;
  paal: {x: number; w: number; h: number};
  auto: {x: number; w: number; x0: number};
  feiten: FeitenGeo;
};

const GEO: Record<ZoekFormaat, Geo> = {
  staand: {
    w: 1080,
    h: 1920,
    tekst: {x: 70, y: 300, w: 940, size: 100, align: 'center'},
    accu: {cx: 540, cy: 860, w: 560, h: 250},
    grond: 1620,
    paal: {x: 130, w: 170, h: 420},
    auto: {x: 680, w: 600, x0: 1500},
    feiten: {titelX: 70, titelY: 330, titelW: 940, titel: 96, align: 'center', x: 70, y: 820, w: 940, h: 190, gap: 34, tekst: 54, icoon: 120},
  },
  liggend: {
    w: 1920,
    h: 1080,
    tekst: {x: 100, y: 150, w: 800, size: 92, align: 'left'},
    accu: {cx: 420, cy: 760, w: 520, h: 230},
    grond: 960,
    paal: {x: 1050, w: 150, h: 380},
    auto: {x: 1500, w: 560, x0: 2400},
    feiten: {titelX: 100, titelY: 330, titelW: 700, titel: 96, align: 'left', x: 860, y: 240, w: 960, h: 170, gap: 30, tekst: 50, icoon: 110},
  },
};

const T = {inrijden: [110, 210], kabel: [225, 285], klik: 285, laden: [300, 600], tekst2: 300, feiten: 640, cta: 830, duration: 1000};
export const laadTimeline = () => T;

const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const bez = (p: number[][], t: number) => {
  const u = 1 - t;
  return [0, 1].map((k) => u * u * u * p[0][k] + 3 * u * u * t * p[1][k] + 3 * u * t * t * p[2][k] + t * t * t * p[3][k]);
};

/** Battery outline with the aqua fill (`niveau` 0..1) and a lightning bolt while it charges. */
const Accu: React.FC<{g: Geo; niveau: number; bliksem: number; knipper: number}> = ({g, niveau, bliksem, knipper}) => {
  const {cx, cy, w, h} = g.accu;
  const rand = 16;
  const pad = 18;
  const binnenW = w - 2 * rand - 2 * pad;
  return (
    <svg width={w + 60} height={h} style={{position: 'absolute', left: cx - w / 2, top: cy - h / 2, overflow: 'visible'}}>
      <rect x={rand / 2} y={rand / 2} width={w - rand} height={h - rand} rx={40} fill="none" stroke={colors.wit} strokeWidth={rand} />
      <rect x={w + 4} y={h * 0.3} width={34} height={h * 0.4} rx={12} fill={colors.wit} />
      <rect x={rand + pad} y={rand + pad} width={Math.max(0, binnenW * niveau)} height={h - 2 * rand - 2 * pad} rx={20} fill={colors.aqua} opacity={knipper} />
      <g transform={`translate(${w / 2} ${h / 2}) scale(${(h / 200) * (0.85 + 0.15 * bliksem)})`} opacity={bliksem}>
        <path d="M14 -78 L-44 12 L-6 12 L-18 78 L44 -14 L6 -14 Z" fill={colors.wit} stroke={colors.blauw} strokeWidth={8} strokeLinejoin="round" />
      </g>
    </svg>
  );
};

export const LaadSpot: React.FC<{laden: Laden; formaat?: ZoekFormaat}> = ({laden: d, formaat = 'staand'}) => {
  const frame = useCurrentFrame();
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: colors.blauw}} />;
  const g = GEO[formaat];
  const l = locaties.find((x) => x.slug === d.slug);
  if (!l) throw new Error(`Onbekende locatie ${d.slug}`);
  const uit = ease(0.2, 0.9, 0.3, 1);

  // Battery: low and blinking until the plug clicks in, then it fills.
  const laad = tween(frame, T.laden[0], T.laden[1], ease(0.4, 0, 0.6, 1));
  const niveau = lerp(0.1, 1, laad);
  const knipper = frame < T.klik ? (Math.floor(frame / 20) % 2 === 0 ? 1 : 0.25) : 1;
  const bliksem = tween(frame, T.klik, T.klik + 16) * (0.8 + 0.2 * Math.sin(frame * 0.25)) * (1 - tween(frame, T.laden[1], T.laden[1] + 20));

  // Car drives in from the right and stops beside the post.
  const rij = tween(frame, T.inrijden[0], T.inrijden[1], ease(0.15, 0.6, 0.3, 1));
  const autoX = lerp(g.auto.x0, g.auto.x, rij);
  const s = g.auto.w / AUTO_VB.w;
  const autoH = AUTO_VB.h * s;
  const veer = frame > T.inrijden[1] && frame < T.inrijden[1] + 24 ? Math.sin(((frame - T.inrijden[1]) / 24) * Math.PI) * 8 : 0;

  // Cable from the post's socket to the left front of the car, drawn in, then a click and energy dots running along it.
  const P = g.paal;
  const paalTop = g.grond - P.h;
  const van = [P.x + P.w * 0.5, paalTop + P.h * 0.55];
  const naar = [g.auto.x - g.auto.w * 0.44, g.grond - autoH * 0.4];
  const zak = Math.max(van[1], naar[1]) + (formaat === 'staand' ? 150 : 110);
  const pts = [van, [van[0] + 40, zak], [naar[0] - 80, zak], naar];
  const kabel = tween(frame, T.kabel[0], T.kabel[1], ease(0.4, 0, 0.3, 1));
  const N = 40;
  const lijn = Array.from({length: N + 1}, (_, i) => bez(pts, (i / N) * kabel));
  const klik = frame >= T.klik && frame < T.klik + 30 ? tween(frame, T.klik, T.klik + 30) : -1;
  const stroom = frame > T.klik && frame < T.laden[1];

  // Text: hook, then "Je auto laadt, terwijl jij ...".
  const X = g.tekst;
  const hook = tween(frame, 6, 30, uit) * (1 - tween(frame, T.tekst2 - 30, T.tekst2 - 10));
  const weg = 1 - tween(frame, T.feiten - 24, T.feiten - 4);
  const tekst2 = tween(frame, T.tekst2, T.tekst2 + 24, uit) * weg;
  const tekst3 = tween(frame, T.tekst2 + 40, T.tekst2 + 64, uit) * weg;
  const zin = `terwijl jij ${d.terwijl}.`;
  const zinRegels = wrap(zin, X.size * 0.62, '400', X.w);
  const dim = tween(frame, T.feiten - 20, T.feiten + 10);
  const rise = (v: number): React.CSSProperties => ({opacity: v, transform: `translateY(${(1 - v) * 40}px)`});

  return (
    <AbsoluteFill style={{background: colors.blauw, fontFamily: font, overflow: 'hidden'}}>
      <Fonts />
      {/* Ground */}
      <div style={{position: 'absolute', left: 0, top: g.grond, width: g.w, height: g.h - g.grond, background: '#14275F'}} />
      <div style={{position: 'absolute', left: 0, top: g.grond, width: g.w, height: 8, background: colors.aqua, opacity: 0.6}} />

      {/* Charging post */}
      <div style={{position: 'absolute', left: P.x, top: paalTop, width: P.w, height: P.h, borderRadius: '36px 36px 10px 10px', background: colors.wit}}>
        <div style={{position: 'absolute', left: P.w * 0.15, top: P.w * 0.15, width: P.w * 0.7, height: P.w * 0.7, borderRadius: 22, background: stroom ? colors.aqua : '#E3F5F8', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <Img src={staticFile('svg/atom/py-atom-picto-ev.svg')} style={{width: P.w * 0.46, height: P.w * 0.46, display: 'block'}} />
        </div>
        <div style={{position: 'absolute', left: P.w * 0.5 - 22, top: P.h * 0.55 - 22, width: 44, height: 44, borderRadius: '50%', background: colors.blauw}} />
      </div>

      {/* Cable */}
      <svg width={g.w} height={g.h} style={{position: 'absolute', left: 0, top: 0}}>
        {kabel > 0 ? <polyline points={lijn.map((p) => p.join(',')).join(' ')} fill="none" stroke="#0E1B45" strokeWidth={18} strokeLinecap="round" strokeLinejoin="round" /> : null}
        {kabel > 0 ? <polyline points={lijn.map((p) => p.join(',')).join(' ')} fill="none" stroke={colors.wit} strokeWidth={10} strokeLinecap="round" strokeLinejoin="round" /> : null}
        {stroom
          ? Array.from({length: 5}, (_, i) => {
              const t = ((frame - T.klik) / 50 + i / 5) % 1;
              const [x, y] = bez(pts, t);
              return <circle key={i} cx={x} cy={y} r={11} fill={colors.aqua} />;
            })
          : null}
        {klik >= 0 ? <circle cx={naar[0]} cy={naar[1]} r={20 + 60 * klik} fill="none" stroke={colors.aqua} strokeWidth={6} opacity={1 - klik} /> : null}
        {kabel >= 1 ? <rect x={naar[0] - 18} y={naar[1] - 14} width={36} height={28} rx={8} fill={colors.blauw} stroke={colors.wit} strokeWidth={5} /> : null}
      </svg>

      {/* Car */}
      <svg width={g.auto.w} height={autoH} viewBox={`0 0 ${AUTO_VB.w} ${AUTO_VB.h}`} style={{position: 'absolute', left: autoX - g.auto.w / 2, top: g.grond - autoH + veer * 0.3}}>
        <path d={AUTO_PAD} fill={colors.wit} />
      </svg>

      <Accu g={g} niveau={niveau} bliksem={bliksem} knipper={knipper} />

      {/* Hook, then the charging sentence */}
      <div style={{position: 'absolute', left: X.x, top: X.y, width: X.w, textAlign: X.align, color: colors.wit, ...rise(hook)}}>
        <div style={{fontSize: X.size, fontWeight: 700, lineHeight: 1.05}}>Elektrisch rijden?</div>
        <div style={{fontSize: X.size * 0.44, fontWeight: 400, marginTop: 18}}>
          <span>Laad bij Parking </span>
          <span style={{fontWeight: 700}}>{l.naam}</span>
        </div>
      </div>
      <div style={{position: 'absolute', left: X.x, top: X.y, width: X.w, textAlign: X.align, color: colors.wit}}>
        <div style={{fontSize: X.size, fontWeight: 700, lineHeight: 1.05, ...rise(tekst2)}}>Je auto laadt,</div>
        <div style={{fontSize: X.size * 0.62, fontWeight: 400, lineHeight: 1.2, marginTop: 14, ...rise(tekst3)}}>
          {zinRegels.map((r, i) => (
            <div key={i}>{r}</div>
          ))}
        </div>
      </div>

      <AbsoluteFill style={{background: colors.blauw, opacity: 0.96 * dim}} />
      <Feiten frame={frame} start={T.feiten} F={g.feiten} kicker="Elektrisch laden" naam={l.naam} stad={l.stad} feiten={d.feiten} />

      <AbsoluteFill style={{background: colors.blauw, opacity: 0.94 * tween(frame, T.cta - 10, T.cta + 16)}} />
      <EindCta start={T.cta} reserveer={RESERVEERBAAR.has(l.id)} k={CTA_GEO[formaat]} />
    </AbsoluteFill>
  );
};

export const LAAD_SIZE: Record<ZoekFormaat, {width: number; height: number}> = {
  staand: {width: 1080, height: 1920},
  liggend: {width: 1920, height: 1080},
};
