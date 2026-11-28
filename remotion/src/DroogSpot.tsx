import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Fonts} from './components';
import {colors, font} from './theme';
import {ease, tween, useUbuntu} from './LocatieSpot';
import {CTA_GEO, EindCta, type ZoekFormaat} from './ZoekSpot';
import {RESERVEERBAAR, locaties} from './locaties';
import {AUTO_PAD, AUTO_VB} from './autoPad';
import type {Droog} from './droog';
import {Feiten, type FeitenGeo} from './Feiten';

// "Droog naar binnen": it pours outside (full screen, hook "Regent het?"), the camera pulls back and the rain turns out to be
// seen through the entrance of a garage. A car comes in out of the rain with its wipers going; inside they stop. Then three
// facts from the location page and the shared end screen. Meant to run with a rain trigger. 60 fps, 9:16 and 16:9.
// No box-shadows or blur, render in one tab (see LijstSpot).

type Rect = {x: number; y: number; w: number; h: number};
type Geo = {
  w: number;
  h: number;
  /** Final entrance opening, seen from inside the garage. */
  poort: Rect;
  /** Horizon of the street outside (frame coordinates). */
  horizon: number;
  hook: {y: number; size: number};
  /** Car: centre x, start y and width (far away), end y and width (inside). */
  auto: {x: number; y0: number; w0: number; y1: number; w1: number};
  feiten: FeitenGeo;
  regen: number;
  /** Depth (0 = frame edge, 1 = opening) of the ceiling lights, kept clear of the text. */
  lampen: number[];
};

const GEO: Record<ZoekFormaat, Geo> = {
  staand: {
    w: 1080,
    h: 1920,
    poort: {x: 160, y: 820, w: 760, h: 560},
    horizon: 1150,
    hook: {y: 330, size: 124},
    auto: {x: 540, y0: 1185, w0: 120, y1: 1560, w1: 860},
    feiten: {titelX: 70, titelY: 330, titelW: 940, titel: 96, align: 'center', x: 70, y: 820, w: 940, h: 190, gap: 34, tekst: 54, icoon: 120},
    regen: 150,
    lampen: [0.1, 0.9],
  },
  liggend: {
    w: 1920,
    h: 1080,
    poort: {x: 560, y: 340, w: 800, h: 500},
    horizon: 600,
    hook: {y: 46, size: 100},
    auto: {x: 960, y0: 630, w0: 110, y1: 880, w1: 640},
    feiten: {titelX: 100, titelY: 330, titelW: 700, titel: 96, align: 'left', x: 860, y: 240, w: 960, h: 170, gap: 30, tekst: 50, icoon: 110},
    regen: 170,
    lampen: [0.93],
  },
};

const T = {zoom: [150, 240], auto: [220, 400], binnen: 345, feiten: 470, cta: 700, duration: 870};
export const droogTimeline = () => T;

const hash = (i: number, k: number) => {
  const s = Math.sin(i * 12.9898 + k * 78.233) * 43758.5453;
  return s - Math.floor(s);
};
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

/** Rain, puddle rings and a street, in frame coordinates (drawn behind the entrance opening as a window). */
const Buiten: React.FC<{g: Geo; frame: number}> = ({g, frame}) => {
  const {w: W, h: H} = g;
  const streep = [];
  for (let i = 0; i < g.regen; i++) {
    const len = 50 + 60 * hash(i, 3);
    const v = (2000 + 1200 * hash(i, 2)) / 60;
    const y = ((hash(i, 4) * (H + 200) + frame * v) % (H + 200)) - 120;
    const x = hash(i, 1) * (W + 300) - 150 - y * 0.18;
    streep.push(<line key={i} x1={x} y1={y} x2={x - len * 0.18} y2={y + len} stroke="#FFFFFF" strokeWidth={3} strokeLinecap="round" opacity={0.22 + 0.38 * hash(i, 5)} />);
  }
  const ringen = [];
  for (let i = 0; i < 26; i++) {
    const p = 40 + Math.floor(hash(i, 6) * 30);
    const f = (frame + Math.floor(hash(i, 7) * p)) % p;
    const n = Math.floor((frame + Math.floor(hash(i, 7) * p)) / p);
    const t = f / p;
    const x = hash(i * 31 + n, 8) * W;
    const y = g.horizon + 30 + hash(i * 17 + n, 9) * (H - g.horizon - 30);
    const r = (18 + 40 * t) * (0.4 + (0.6 * (y - g.horizon)) / (H - g.horizon));
    ringen.push(<ellipse key={i} cx={x} cy={y} rx={r} ry={r * 0.32} fill="none" stroke="#FFFFFF" strokeWidth={2.5} opacity={0.45 * (1 - t)} />);
  }
  return (
    <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="lucht" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#24345F" />
          <stop offset="1" stopColor="#4A5E8C" />
        </linearGradient>
      </defs>
      <rect width={W} height={g.horizon} fill="url(#lucht)" />
      {/* Grey blocks of buildings on the horizon */}
      {Array.from({length: 9}, (_, i) => {
        const bw = W / 7;
        const bh = 80 + 140 * hash(i, 11);
        return <rect key={i} x={i * bw * 0.85 - 40} y={g.horizon - bh} width={bw * 0.8} height={bh} fill="#33467A" />;
      })}
      <rect y={g.horizon} width={W} height={H - g.horizon} fill="#1E2C55" />
      {/* Lane lines converging on the horizon, wet reflections */}
      {[-1, 1].map((s) => (
        <line key={s} x1={W / 2 + s * 30} y1={g.horizon} x2={W / 2 + s * W * 0.9} y2={H} stroke="#FFFFFF" strokeWidth={6} opacity={0.35} />
      ))}
      {Array.from({length: 6}, (_, i) => {
        const a = (i + ((frame / 40) % 1)) / 6;
        const y = g.horizon + (H - g.horizon) * a * a;
        return <rect key={i} x={W / 2 - 4 - 10 * a} y={y} width={8 + 20 * a} height={10 + 60 * a * a} fill="#FFFFFF" opacity={0.4} />;
      })}
      {ringen}
      {streep}
    </svg>
  );
};

/** The garage seen from inside: ceiling with lights, side walls and a floor with markings, around the opening `p`. */
const Binnen: React.FC<{g: Geo; p: Rect}> = ({g, p}) => {
  const {w: W, h: H} = g;
  const pt = (x: number, y: number) => `${x},${y}`;
  const lampen = g.lampen.map((t) => {
    const y = lerp(0, p.y, t) + 20 * (1 - t);
    const hw = lerp(W * 0.32, p.w * 0.3, t);
    const hh = lerp(26, 10, t);
    return <rect key={t} x={W / 2 - hw} y={y} width={2 * hw} height={hh} rx={hh / 2} fill="#FFFFFF" opacity={0.95} />;
  });
  const vakken = [0.3, 0.55, 0.8].flatMap((t) =>
    [-1, 1].map((s) => {
      const y = lerp(H, p.y + p.h, 1 - t);
      const xIn = lerp(W / 2 + s * W * 0.22, W / 2 + s * p.w * 0.25, 1 - t);
      const xUit = lerp(s < 0 ? 0 : W, s < 0 ? p.x : p.x + p.w, 1 - t);
      return <line key={`${t}${s}`} x1={xIn} y1={y} x2={xUit} y2={y} stroke="#FFFFFF" strokeWidth={5} opacity={0.3} />;
    }),
  );
  return (
    <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
      <polygon points={[pt(0, 0), pt(W, 0), pt(p.x + p.w, p.y), pt(p.x, p.y)].join(' ')} fill="#24387A" />
      <polygon points={[pt(0, 0), pt(p.x, p.y), pt(p.x, p.y + p.h), pt(0, H)].join(' ')} fill="#1A2C66" />
      <polygon points={[pt(W, 0), pt(p.x + p.w, p.y), pt(p.x + p.w, p.y + p.h), pt(W, H)].join(' ')} fill="#1A2C66" />
      <polygon points={[pt(0, H), pt(p.x, p.y + p.h), pt(p.x + p.w, p.y + p.h), pt(W, H)].join(' ')} fill="#14234F" />
      {lampen}
      {vakken}
      <line x1={W / 2} y1={H} x2={W / 2} y2={p.y + p.h} stroke={colors.aqua} strokeWidth={8} strokeDasharray="40 30" opacity={0.8} />
      {/* Frame around the opening */}
      <rect x={p.x - 10} y={p.y - 10} width={p.w + 20} height={p.h + 10} fill="none" stroke="#3A519A" strokeWidth={20} />
    </svg>
  );
};

/** Front view of the car (picto-car), with wipers and headlights. */
const Auto: React.FC<{cx: number; cy: number; w: number; frame: number; wissen: number}> = ({cx, cy, w, frame, wissen}) => {
  const s = w / AUTO_VB.w;
  const h = AUTO_VB.h * s;
  const hoek = wissen * 38 * Math.sin(frame * 0.2);
  return (
    <svg width={w} height={h} viewBox={`0 0 ${AUTO_VB.w} ${AUTO_VB.h}`} style={{position: 'absolute', left: cx - w / 2, top: cy - h, overflow: 'visible'}}>
      <path d={AUTO_PAD} fill={colors.wit} />
      {[9.6, 18.4].map((px, i) => (
        <line
          key={px}
          x1={px}
          y1={7.4}
          x2={px + (i === 0 ? -4.6 : -4.6)}
          y2={7.4}
          stroke={colors.blauw}
          strokeWidth={0.45}
          strokeLinecap="round"
          transform={`rotate(${i === 0 ? hoek + 30 : hoek + 30} ${px} 7.4)`}
          opacity={wissen > 0.01 ? 1 : 0}
        />
      ))}
    </svg>
  );
};

export const DroogSpot: React.FC<{droog: Droog; formaat?: ZoekFormaat}> = ({droog: d, formaat = 'staand'}) => {
  const frame = useCurrentFrame();
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: colors.blauw}} />;
  const g = GEO[formaat];
  const l = locaties.find((x) => x.slug === d.slug);
  if (!l) throw new Error(`Onbekende locatie ${d.slug}`);
  const zacht = ease(0.65, 0, 0.35, 1);

  // Camera pulls back: the window on the rain shrinks from the full frame to the entrance opening.
  const z = tween(frame, T.zoom[0], T.zoom[1], zacht);
  const p: Rect = {x: lerp(0, g.poort.x, z), y: lerp(0, g.poort.y, z), w: lerp(g.w, g.poort.w, z), h: lerp(g.h, g.poort.h, z)};

  // Car drives in: slow far away, faster as it comes near.
  const a = tween(frame, T.auto[0], T.auto[1], ease(0.5, 0, 0.6, 1));
  const autoW = g.auto.w0 * Math.pow(g.auto.w1 / g.auto.w0, a);
  const autoY = lerp(g.auto.y0, g.auto.y1, (autoW - g.auto.w0) / (g.auto.w1 - g.auto.w0));
  const wissen = 1 - tween(frame, T.binnen, T.binnen + 20);
  // Drips fall off the car once it is inside.
  const druppels = frame > T.binnen && frame < T.binnen + 60;

  const hook = tween(frame, 6, 30, ease(0.2, 0.9, 0.3, 1)) * (1 - tween(frame, T.binnen - 40, T.binnen - 20));
  const droogTekst = tween(frame, T.binnen - 16, T.binnen + 10, ease(0.2, 0.9, 0.3, 1)) * (1 - tween(frame, T.feiten - 20, T.feiten));
  const dim = tween(frame, T.feiten - 20, T.feiten + 10);
  const F = g.feiten;

  return (
    <AbsoluteFill style={{background: colors.blauw, fontFamily: font, overflow: 'hidden'}}>
      <Fonts />
      <Binnen g={g} p={p} />
      <div style={{position: 'absolute', left: p.x, top: p.y, width: p.w, height: p.h, overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: -p.x, top: -p.y, width: g.w, height: g.h}}>
          <Buiten g={g} frame={frame} />
        </div>
      </div>
      {frame >= T.auto[0] - 1 ? <Auto cx={g.auto.x} cy={autoY} w={autoW} frame={frame} wissen={wissen} /> : null}
      {druppels
        ? [0.12, 0.3, 0.52, 0.7, 0.88].map((fx, i) => {
            const t = (frame - T.binnen - i * 7) / 30;
            if (t < 0 || t > 1) return null;
            const s = autoW / AUTO_VB.w;
            return <div key={i} style={{position: 'absolute', left: g.auto.x - autoW / 2 + fx * autoW, top: autoY - 3 * s + t * t * 2.5 * s, width: 12, height: 18, borderRadius: '50% 50% 50% 50% / 60% 60% 40% 40%', background: colors.aqua, opacity: 1 - t}} />;
          })
        : null}

      {/* Hook on the rain, then "Droog naar binnen." */}
      <div style={{position: 'absolute', top: g.hook.y, width: '100%', textAlign: 'center', color: colors.wit, opacity: hook, transform: `translateY(${(1 - Math.min(1, hook * 1.4)) * 40}px)`}}>
        <div style={{fontSize: g.hook.size, fontWeight: 700, lineHeight: 1.05}}>Regent het?</div>
        <div style={{fontSize: g.hook.size * 0.44, fontWeight: 400, marginTop: 18}}>Parkeer droog in {l.stad}</div>
      </div>
      <div style={{position: 'absolute', top: g.hook.y, width: '100%', textAlign: 'center', color: colors.wit, opacity: droogTekst, transform: `translateY(${(1 - Math.min(1, droogTekst * 1.4)) * 40}px)`}}>
        <div style={{fontSize: g.hook.size, fontWeight: 700, lineHeight: 1.05}}>Droog naar binnen.</div>
        <div style={{fontSize: g.hook.size * 0.44, fontWeight: 400, marginTop: 18}}>
          <span style={{fontWeight: 300}}>Parking </span>
          <span style={{fontWeight: 700}}>{l.naam}</span>
        </div>
      </div>

      {/* Facts */}
      <AbsoluteFill style={{background: colors.blauw, opacity: 0.96 * dim}} />
      <Feiten frame={frame} start={T.feiten} F={F} kicker="Overdekt parkeren" naam={l.naam} stad={l.stad} feiten={d.feiten} />

      <AbsoluteFill style={{background: colors.blauw, opacity: 0.94 * tween(frame, T.cta - 10, T.cta + 16)}} />
      <EindCta start={T.cta} reserveer={RESERVEERBAAR.has(l.id)} k={CTA_GEO[formaat]} />
    </AbsoluteFill>
  );
};

export const DROOG_SIZE: Record<ZoekFormaat, {width: number; height: number}> = {
  staand: {width: 1080, height: 1920},
  liggend: {width: 1920, height: 1080},
};
