import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Fonts} from './components';
import {colors, font} from './theme';
import {clamp, ease, tween, useUbuntu, wrap} from './LocatieSpot';
import {CTA_GEO, EindCta} from './ZoekSpot';

// Amsterdam Light campaign: six Instagram ad animations (9:16, 60 fps, 6 to 12 s) for Parking Plantage.
// Shared kit: canal houses with windows that switch on, water with reflections and ripples, neon lines.
// Neon "glow" is stacked strokes, never blur or box-shadow (those made Chrome drop layers). Render in one tab.
// Key text stays inside the Instagram safe zones (top 250 px, bottom 330 px).

const W = 1080;
const H = 1920;
export const LIGHT_SIZE = {width: W, height: H};

const NACHT = '#0B1736';
const NACHT2 = '#13265C';
const WARM = '#FFC95C';
const WARM2 = '#FFE7AD';
const ORANJE = '#F08300';
const ROOD = '#E30613';

const pop = (frame: number, at: number, len = 18) => tween(frame, at, at + len, ease(0.3, 1.5, 0.5, 1));
const inn = (frame: number, at: number, len = 22) => tween(frame, at, at + len, ease(0.2, 0.9, 0.3, 1));
const mix = (a: string, b: string, t: number) => {
  const p = (c: string) => [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16));
  const [x, y] = [p(a), p(b)];
  return `rgb(${x.map((v, i) => Math.round(v + (y[i] - v) * Math.max(0, Math.min(1, t)))).join(',')})`;
};

/** Small deterministic random generator, so every render is the same. */
const rng = (seed: number) => () => {
  seed = (seed * 16807) % 2147483647;
  return (seed - 1) / 2147483646;
};

// ---------------------------------------------------------------- canal houses

type Huis = {x: number; w: number; body: number; gevel: number; type: number; tint: string; ramen: {x: number; y: number; w: number; h: number; rank: number}[]};

/** A row of canal houses standing on y = 0 (negative y is up), x from 0 to breedte. */
const maakHuizen = (seed: number, breedte: number, schaal = 1): Huis[] => {
  const r = rng(seed);
  const huizen: Huis[] = [];
  let x = -20 * schaal;
  const tints = ['#16285C', '#1B2F69', '#132354', '#1E3470'];
  while (x < breedte + 10) {
    const w = (105 + r() * 60) * schaal;
    const verd = 4 + Math.floor(r() * 2);
    const vh = (78 + r() * 14) * schaal;
    const body = verd * vh + 20 * schaal;
    const cols = w > 140 * schaal ? 3 : 2;
    const ramen: Huis['ramen'] = [];
    const m = 16 * schaal;
    const gap = 12 * schaal;
    const ww = (w - 2 * m - (cols - 1) * gap) / cols;
    for (let f = 0; f < verd; f++) {
      for (let c = 0; c < cols; c++) {
        ramen.push({x: m + c * (ww + gap), y: -body + 18 * schaal + f * vh, w: ww, h: vh * 0.6, rank: r()});
      }
    }
    huizen.push({x, w, body, gevel: (70 + r() * 60) * schaal, type: Math.floor(r() * 4), tint: tints[Math.floor(r() * tints.length)], ramen});
    x += w + 2 * schaal;
  }
  return huizen;
};

const gevelPad = (h: Huis) => {
  const {w, body: b, gevel: g} = h;
  const top = -b - g;
  switch (h.type) {
    case 0: {
      // step gable
      const s = w / 6;
      return `M0 0 L0 ${-b} L${s} ${-b} L${s} ${-b - g * 0.33} L${2 * s} ${-b - g * 0.33} L${2 * s} ${-b - g * 0.66} L${2.4 * s} ${-b - g * 0.66} L${2.4 * s} ${top} L${3.6 * s} ${top} L${3.6 * s} ${-b - g * 0.66} L${4 * s} ${-b - g * 0.66} L${4 * s} ${-b - g * 0.33} L${5 * s} ${-b - g * 0.33} L${5 * s} ${-b} L${w} ${-b} L${w} 0 Z`;
    }
    case 1:
      // neck gable with shoulders
      return `M0 0 L0 ${-b} Q${w * 0.18} ${-b} ${w * 0.28} ${-b - g * 0.45} L${w * 0.3} ${top} L${w * 0.7} ${top} L${w * 0.72} ${-b - g * 0.45} Q${w * 0.82} ${-b} ${w} ${-b} L${w} 0 Z`;
    case 2:
      // bell gable
      return `M0 0 L0 ${-b} C${w * 0.1} ${-b} ${w * 0.22} ${-b - g * 0.2} ${w * 0.25} ${-b - g * 0.6} C${w * 0.3} ${top - 6} ${w * 0.7} ${top - 6} ${w * 0.75} ${-b - g * 0.6} C${w * 0.78} ${-b - g * 0.2} ${w * 0.9} ${-b} ${w} ${-b} L${w} 0 Z`;
    default:
      // spout / point gable
      return `M0 0 L0 ${-b} L${w * 0.5} ${top} L${w} ${-b} L${w} 0 Z`;
  }
};

/** Canal houses on baseline y, with lit windows. `aan(rank)` returns 0..1 for a window with that random rank. */
const Huizen: React.FC<{huizen: Huis[]; y: number; aan: (rank: number) => number; spiegel?: boolean; dim?: number}> = ({huizen, y, aan, spiegel, dim = 0}) => (
  <g transform={spiegel ? `translate(0 ${y}) scale(1 -0.62)` : `translate(0 ${y})`} opacity={spiegel ? 0.3 : 1}>
    {huizen.map((h, i) => (
      <g key={i} transform={`translate(${h.x} 0)`}>
        <path d={gevelPad(h)} fill={mix(h.tint, '#24408A', dim)} />
        {h.ramen.map((r, j) => {
          const a = aan(r.rank);
          return (
            <g key={j}>
              {a > 0 ? <rect x={r.x - 7} y={r.y - 7} width={r.w + 14} height={r.h + 14} rx={6} fill={WARM} opacity={0.18 * a} /> : null}
              <rect x={r.x} y={r.y} width={r.w} height={r.h} rx={3} fill={mix('#0E1A3D', a > 0.5 ? WARM2 : WARM, a)} />
            </g>
          );
        })}
      </g>
    ))}
  </g>
);

/** Water under the houses: dark gradient, the mirrored houses and moving ripple lines. */
const Water: React.FC<{huizen: Huis[]; y: number; breedte: number; hoogte: number; aan: (rank: number) => number; frame: number}> = ({huizen, y, breedte, hoogte, aan, frame}) => {
  const lijnen = [];
  for (let k = 0; k < 16; k++) {
    const yy = y + 14 + k * (hoogte / 16);
    const shift = ((frame * (0.6 + (k % 3) * 0.25) + k * 37) % 120) - 120;
    lijnen.push(<line key={k} x1={shift} y1={yy} x2={breedte + 120} y2={yy} stroke={NACHT} strokeWidth={5 + (k % 3) * 2} strokeDasharray={`${50 + (k % 4) * 20} ${22 + (k % 3) * 10}`} opacity={0.9} />);
  }
  return (
    <g>
      <rect x={0} y={y} width={breedte} height={hoogte} fill="#0D1C45" />
      <Huizen huizen={huizen} y={y} aan={aan} spiegel />
      {lijnen}
      <rect x={0} y={y} width={breedte} height={6} fill="#24408A" />
    </g>
  );
};

/** One line of "neon": stacked strokes from wide and faint to thin and white. */
const Neon: React.FC<{d: string; kleur?: string; dash?: string; offset?: number; schaal?: number; opacity?: number}> = ({d, kleur = colors.aqua, dash, offset, schaal = 1, opacity = 1}) => (
  <g fill="none" strokeLinecap="round" strokeLinejoin="round" opacity={opacity}>
    {[
      [30, 0.07],
      [18, 0.14],
      [10, 0.35],
      [5, 1],
    ].map(([w, o], i) => (
      <path key={i} d={d} stroke={kleur} strokeWidth={w * schaal} opacity={o} pathLength={1} strokeDasharray={dash} strokeDashoffset={offset} />
    ))}
    <path d={d} stroke={colors.wit} strokeWidth={1.8 * schaal} opacity={0.9} pathLength={1} strokeDasharray={dash} strokeDashoffset={offset} />
  </g>
);

/** A few light-art pieces over the water: neon arches and rings that switch on. */
const Lichtkunst: React.FC<{frame: number; at: number; y: number; breedte?: number}> = ({frame, at, y, breedte = W}) => {
  const stukken = [
    {d: `M${breedte * 0.1} ${y} Q${breedte * 0.25} ${y - 260} ${breedte * 0.4} ${y}`, k: colors.aqua, t: 0},
    {d: `M${breedte * 0.55} ${y - 140} m-70 0 a70 70 0 1 0 140 0 a70 70 0 1 0 -140 0`, k: '#B79CFF', t: 18},
    {d: `M${breedte * 0.7} ${y} Q${breedte * 0.82} ${y - 200} ${breedte * 0.95} ${y}`, k: WARM, t: 34},
  ];
  return (
    <g>
      {stukken.map((s, i) => {
        const v = tween(frame, at + s.t, at + s.t + 30, ease(0.3, 0, 0.2, 1));
        if (v <= 0) return null;
        const flick = 0.85 + 0.15 * Math.sin((frame + i * 20) / 6);
        return <Neon key={i} d={s.d} kleur={s.k} dash="1 1" offset={1 - v} opacity={flick} />;
      })}
    </g>
  );
};

/** Strings of bulbs hanging between two points, switching on left to right. */
const Lampjes: React.FC<{frame: number; at: number; y: number; breedte?: number}> = ({frame, at, y, breedte = W}) => {
  const bollen = [];
  const n = 18;
  for (let i = 0; i <= n; i++) {
    const t = i / n;
    const x = breedte * t;
    const yy = y + Math.sin(t * Math.PI * 3) ** 2 * 50;
    const a = tween(frame, at + i * 3, at + i * 3 + 8);
    bollen.push(
      <g key={i}>
        <circle cx={x} cy={yy} r={14} fill={WARM} opacity={0.2 * a} />
        <circle cx={x} cy={yy} r={6} fill={mix('#33437A', WARM2, a)} />
      </g>,
    );
  }
  const pad = Array.from({length: 61}, (_, i) => {
    const t = i / 60;
    return `${i ? 'L' : 'M'}${(breedte * t).toFixed(1)} ${(y + Math.sin(t * Math.PI * 3) ** 2 * 50).toFixed(1)}`;
  }).join(' ');
  return (
    <g>
      <path d={pad} stroke="#33437A" strokeWidth={2} fill="none" />
      {bollen}
    </g>
  );
};

/** Big bold text block that rises in; wraps to the width. */
const Kop: React.FC<{tekst: string; at: number; y: number; size?: number; sub?: string; color?: string; uit?: number}> = ({tekst, at, y, size = 92, sub, color = colors.wit, uit}) => {
  const frame = useCurrentFrame();
  // A heading that starts at frame 0 is already half visible, so the first frame is never empty.
  const v = at === 0 ? interpolate(frame, [0, 22], [0.5, 1], {...clamp, easing: ease(0.2, 0.9, 0.3, 1)}) : inn(frame, at, 26);
  const s = sub ? inn(frame, at + 12, 26) : 0;
  const o = uit !== undefined ? 1 - tween(frame, uit, uit + 16) : 1;
  if (frame < at) return null;
  return (
    <div style={{position: 'absolute', left: 70, right: 70, top: y, textAlign: 'center', color, opacity: o}}>
      <div style={{fontSize: size, fontWeight: 700, lineHeight: 1.08, opacity: v, transform: `translateY(${(1 - v) * 50}px)`}}>
        {wrap(tekst, size, '700', W - 140).map((l, i) => (
          <div key={i}>{l}</div>
        ))}
      </div>
      {sub ? <div style={{fontSize: size * 0.5, lineHeight: 1.25, marginTop: 14, opacity: s, transform: `translateY(${(1 - s) * 30}px)`}}>{sub}</div> : null}
    </div>
  );
};

/** Darkens the scene before the end screen so the CTA reads well. */
const Dim: React.FC<{at: number}> = ({at}) => {
  const frame = useCurrentFrame();
  const v = tween(frame, at - 10, at + 16);
  return <AbsoluteFill style={{background: NACHT, opacity: 0.88 * v}} />;
};

const Logo: React.FC<{uit: number; y?: number}> = ({uit, y = 250}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{position: 'absolute', top: y, width: '100%', display: 'flex', justifyContent: 'center', opacity: 1 - tween(frame, uit - 10, uit + 6)}}>
      <Img src={staticFile('svg/atom/py-atom-logo-horizontal-white.svg')} style={{width: 300, display: 'block'}} />
    </div>
  );
};

const Basis: React.FC<{children: React.ReactNode; bg?: string}> = ({children, bg = NACHT}) => {
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: bg}} />;
  return (
    <AbsoluteFill style={{background: bg, fontFamily: font, overflow: 'hidden'}}>
      <Fonts />
      {children}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- 1. Lichten aan om 16:30

export const LICHTEN_DUUR = 560;

export const LichtenAan: React.FC = () => {
  const frame = useCurrentFrame();
  const huizen = React.useMemo(() => maakHuizen(7, W), []);
  const KLAAR = 112; // the clock reaches 16:30
  const CTA = 400;
  // Clock: 16:25 -> 16:30 in the first KLAAR frames, seconds hand spinning, then the windows cascade on.
  const p = tween(frame, 0, KLAAR, ease(0.5, 0, 0.6, 1));
  const minuten = 25 + 5 * p;
  const sec = (frame < KLAAR ? p * 5 * 360 : 0) % 360;
  const aan = (rank: number) => (rank > 0.9 ? 0 : tween(frame, KLAAR + 10 + rank * 150, KLAAR + 22 + rank * 150));
  const klokUit = tween(frame, 240, 262);
  const ring = tween(frame, KLAAR, KLAAR + 40);
  const lucht = tween(frame, KLAAR, KLAAR + 160);
  const digitaal = frame < KLAAR ? `16:${String(Math.min(29, Math.floor(minuten))).padStart(2, '0')}` : '16:30';
  const B = 1360;
  return (
    <Basis>
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${NACHT} 0%, ${mix(NACHT, NACHT2, lucht)} 60%, ${mix('#101F4C', '#2A3F86', lucht)} 100%)`}} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <Water huizen={huizen} y={B} breedte={W} hoogte={H - B} aan={aan} frame={frame} />
        <Lichtkunst frame={frame} at={KLAAR + 120} y={B + 300} />
        <Huizen huizen={huizen} y={B} aan={aan} />
        <Lampjes frame={frame} at={KLAAR + 60} y={B - 110} />
      </svg>
      {/* Clock */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 330, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: 1 - klokUit, transform: `translateY(${-60 * klokUit}px)`}}>
        <svg width={300} height={300} viewBox="-150 -150 300 300" style={{overflow: 'visible'}}>
          {ring > 0 && ring < 1 ? <circle r={140 + 80 * ring} fill="none" stroke={colors.aqua} strokeWidth={8 * (1 - ring)} opacity={1 - ring} /> : null}
          <circle r={140} fill={NACHT2} stroke={colors.wit} strokeWidth={8} />
          {Array.from({length: 12}, (_, i) => (
            <line key={i} x1={0} y1={-118} x2={0} y2={i % 3 === 0 ? -96 : -106} stroke={colors.wit} strokeWidth={i % 3 === 0 ? 7 : 4} strokeLinecap="round" transform={`rotate(${i * 30})`} />
          ))}
          <line x1={0} y1={12} x2={0} y2={-62} stroke={colors.wit} strokeWidth={11} strokeLinecap="round" transform={`rotate(${(4 + minuten / 60) * 30})`} />
          <line x1={0} y1={14} x2={0} y2={-100} stroke={colors.wit} strokeWidth={7} strokeLinecap="round" transform={`rotate(${minuten * 6})`} />
          <line x1={0} y1={20} x2={0} y2={-108} stroke={colors.aqua} strokeWidth={3} strokeLinecap="round" transform={`rotate(${sec})`} />
          <circle r={9} fill={colors.aqua} />
        </svg>
        <div style={{marginTop: 26, fontSize: 96, fontWeight: 700, color: frame >= KLAAR ? WARM : colors.wit, letterSpacing: 2}}>{digitaal}</div>
        <div style={{fontSize: 44, color: colors.wit, opacity: inn(frame, KLAAR + 6)}}>Lichten aan</div>
      </div>
      <Kop tekst="Je plek staat al klaar." sub="Parking Plantage, in hartje Amsterdam" at={262} y={360} size={80} uit={CTA - 10} />
      <Dim at={CTA} />
      <EindCta start={CTA} reserveer k={CTA_GEO.staand} />
    </Basis>
  );
};

// ---------------------------------------------------------------- 2. Eén lichtlijn

export const LIJN_DUUR = 480;

// Logo mark outline (24 x 28.95 units) traced from the tip, scaled into place.
const LOGO_S = 13;
const LOGO_X = 540 - 12 * LOGO_S;
const LOGO_Y = 560;
const lp = (x: number, y: number) => `${(LOGO_X + x * LOGO_S).toFixed(1)} ${(LOGO_Y + y * LOGO_S).toFixed(1)}`;
const LOGO_PAD =
  `L${lp(11.127, 28.716)} C${lp(11.509, 28.949)} ${lp(12, 28.671)} ${lp(12, 28.223)} L${lp(12, 23.998)} ` +
  `C${lp(18.627, 23.998)} ${lp(24, 18.626)} ${lp(24, 11.999)} C${lp(24, 5.372)} ${lp(18.627, 0)} ${lp(12, 0)} ` +
  `C${lp(5.373, 0)} ${lp(0, 5.372)} ${lp(0, 11.999)} C${lp(0, 23.134)} ${lp(11.127, 28.716)} ${lp(11.127, 28.716)}`;
const BINNEN = `M${lp(12, 4.8)} C${lp(15.977, 4.8)} ${lp(19.2, 8.024)} ${lp(19.2, 12)} C${lp(19.2, 15.976)} ${lp(15.977, 19.2)} ${lp(12, 19.2)} C${lp(8.024, 19.2)} ${lp(4.8, 15.976)} ${lp(4.8, 12)} C${lp(4.8, 8.024)} ${lp(8.024, 4.8)} ${lp(12, 4.8)}`;
// From the barrier arm, down the exit ramp, out of the garage, along the canal (waves), up to the tip of the mark.
const LIJN_PAD =
  `M160 1250 L330 1250 Q360 1250 380 1275 L440 1350 Q460 1375 500 1375 L620 1375 Q680 1375 680 1435 Q680 1500 740 1500 ` +
  `C780 1480 800 1520 840 1500 C880 1480 900 1520 940 1500 Q990 1500 990 1440 L990 1120 Q990 1000 870 1000 ` +
  `L${(LOGO_X + 11.127 * LOGO_S + 40).toFixed(1)} 1000 Q${lp(11.127, 30.5)} ${lp(11.127, 28.716)} ` +
  LOGO_PAD;

export const LichtLijn: React.FC = () => {
  const frame = useCurrentFrame();
  // 0..20 still; 20..300 the line draws; 300..340 the inner ring and dot; hold; 390..465 the line runs out from its start;
  // the mark and wordmark fade so frame 480 matches frame 0 (seamless loop).
  const kop = tween(frame, 20, 300, ease(0.45, 0, 0.55, 1));
  const staart = tween(frame, 390, 465, ease(0.45, 0, 0.55, 1));
  const binnen = tween(frame, 296, 336, ease(0.3, 0, 0.2, 1));
  const vul = tween(frame, 330, 360) * (1 - tween(frame, 420, 462));
  const woord = inn(frame, 340) * (1 - tween(frame, 420, 462));
  const lengte = kop - staart;
  const glans = 0.9 + 0.1 * Math.sin(frame / 7);
  return (
    <Basis>
      <AbsoluteFill style={{background: `radial-gradient(circle at 50% 45%, ${NACHT2} 0%, ${NACHT} 70%)`}} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        {/* Faint scene: garage box, barrier post and arm, canal edge */}
        <g stroke="#2B3F7E" strokeWidth={4} fill="none" opacity={0.9}>
          <path d="M90 1440 L90 1150 L620 1150 L620 1300 M90 1440 L560 1440" />
          <rect x={130} y={1226} width={26} height={56} rx={6} fill="#2B3F7E" />
          <line x1={156} y1={1250} x2={330} y2={1250} strokeWidth={10} strokeLinecap="round" />
          <path d="M560 1560 L1040 1560 M600 1600 L1040 1600" strokeDasharray="26 18" />
        </g>
        <text x={110} y={1132} fill="#2B3F7E" fontSize={44} fontWeight={700} fontFamily="Ubuntu">P</text>
        {lengte > 0 ? <Neon d={LIJN_PAD} dash={`${lengte} 2`} offset={-staart} opacity={glans} /> : null}
        {binnen > 0 ? <Neon d={BINNEN} dash="1 1" offset={1 - binnen} opacity={glans * (1 - tween(frame, 420, 462))} /> : null}
        {/* Filled mark */}
        <g opacity={vul}>
          <path d={`M${LOGO_PAD.slice(1)} Z ${BINNEN}`} fill={colors.wit} fillRule="evenodd" />
          <circle cx={LOGO_X + 12 * LOGO_S} cy={LOGO_Y + 12 * LOGO_S} r={2.28 * LOGO_S} fill={colors.wit} />
        </g>
      </svg>
      <div style={{position: 'absolute', top: 1050, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: woord, transform: `translateY(${(1 - woord) * 30}px)`}}>
        <Img src={staticFile('svg/atom/py-atom-logo-wordmark-white.svg')} style={{width: 520, display: 'block'}} />
        <div style={{marginTop: 30, fontSize: 46, color: colors.wit}}>Je plek in hartje Amsterdam</div>
      </div>
    </Basis>
  );
};

// ---------------------------------------------------------------- 3. Kies je rondje

export const RONDJE_DUUR = 660;

/** Point and heading on a rounded rectangle loop, t in 0..1. */
export const lus = (t: number, cx: number, cy: number, hw: number, hh: number, rad: number) => {
  const segs: {len: number; at: (u: number) => [number, number, number]}[] = [];
  const line = (x1: number, y1: number, x2: number, y2: number) =>
    segs.push({len: Math.hypot(x2 - x1, y2 - y1), at: (u) => [x1 + (x2 - x1) * u, y1 + (y2 - y1) * u, Math.atan2(y2 - y1, x2 - x1)]});
  const arc = (ox: number, oy: number, a0: number) =>
    segs.push({len: (Math.PI / 2) * rad, at: (u) => {
      const a = a0 + (u * Math.PI) / 2;
      return [ox + rad * Math.cos(a), oy + rad * Math.sin(a), a + Math.PI / 2];
    }});
  const [l, r, tp, b] = [cx - hw, cx + hw, cy - hh, cy + hh];
  line(l + rad, tp, r - rad, tp);
  arc(r - rad, tp + rad, -Math.PI / 2);
  line(r, tp + rad, r, b - rad);
  arc(r - rad, b - rad, 0);
  line(r - rad, b, l + rad, b);
  arc(l + rad, b - rad, Math.PI / 2);
  line(l, b - rad, l, tp + rad);
  arc(l + rad, tp + rad, Math.PI);
  const total = segs.reduce((a, s) => a + s.len, 0);
  let d = (((t % 1) + 1) % 1) * total;
  for (const s of segs) {
    if (d <= s.len) return s.at(d / s.len);
    d -= s.len;
  }
  return segs[0].at(0);
};

export const KiesRondje: React.FC = () => {
  const frame = useCurrentFrame();
  const huizen = React.useMemo(() => maakHuizen(21, 540, 0.62), []);
  const VRAAG = 330;
  const KEUZE = 430;
  const CTA = 500;
  const stress = tween(frame, 30, VRAAG, ease(0.4, 0, 0.6, 1));
  const ronde = (frame - 20) / 150;
  const [carX, carY, hoek] = lus(Math.max(0, ronde), 270, 980, 170, 250, 70);
  const rondjes = Math.max(1, Math.min(9, Math.floor(Math.max(0, ronde)) + 1));
  const keuze = tween(frame, KEUZE, KEUZE + 30, ease(0.4, 0, 0.2, 1));
  const aan = (rank: number) => (rank > 0.85 ? 0 : 1);
  const loop = (frame % 40) / 40;
  const walkX = 600 + (frame / RONDJE_DUUR) * 280;
  return (
    <Basis>
      {/* Left: searching */}
      <div style={{position: 'absolute', left: 0, top: 0, width: 540, height: H, background: '#0F1D45', overflow: 'hidden', opacity: 1 - 0.6 * keuze}}>
        <svg width={540} height={H} style={{position: 'absolute', inset: 0}}>
          {/* city blocks */}
          {[
            [160, 790, 220, 380],
            [10, 560, 150, 130],
            [380, 560, 150, 130],
            [10, 1300, 150, 140],
            [380, 1300, 150, 140],
          ].map(([x, y, w, h], i) => (
            <rect key={i} x={x} y={y} width={w} height={h} rx={18} fill="#1A2C63" />
          ))}
          <path d="M100 730 l0 0" />
          <rect x={100} y={730} width={340} height={500} rx={70} fill="none" stroke="#2A3F7E" strokeWidth={76} />
          {/* full car parks */}
          {[
            [270, 880],
            [470, 760],
            [70, 1100],
          ].map(([x, y], i) => (
            <g key={i} transform={`translate(${x} ${y})`} opacity={inn(frame, 40 + i * 50)}>
              <rect x={-34} y={-34} width={68} height={68} rx={14} fill={colors.blauw} stroke={colors.wit} strokeWidth={4} />
              <text x={0} y={14} fill={colors.wit} fontSize={42} fontWeight={700} textAnchor="middle" fontFamily="Ubuntu">P</text>
              <rect x={-38} y={40} width={76} height={34} rx={8} fill={ROOD} />
              <text x={0} y={66} fill={colors.wit} fontSize={24} fontWeight={700} textAnchor="middle" fontFamily="Ubuntu">VOL</text>
            </g>
          ))}
          {/* the car */}
          <g transform={`translate(${carX} ${carY}) rotate(${(hoek * 180) / Math.PI + 90})`}>
            <rect x={-24} y={-44} width={48} height={88} rx={14} fill={colors.wit} />
            <rect x={-18} y={-30} width={36} height={18} rx={5} fill="#0F1D45" />
            <rect x={-18} y={16} width={36} height={14} rx={5} fill="#0F1D45" />
            <rect x={-20} y={-46} width={12} height={6} rx={3} fill={WARM} />
            <rect x={8} y={-46} width={12} height={6} rx={3} fill={WARM} />
          </g>
        </svg>
        <div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center', color: colors.wit}}>
          <div style={{fontSize: 52, fontWeight: 700}}>Rondje zoeken</div>
          <div style={{fontSize: 36, marginTop: 8, opacity: 0.85}}>rondje {rondjes}</div>
        </div>
        {/* stress meter */}
        <div style={{position: 'absolute', left: 60, right: 60, top: 1500, color: colors.wit, fontSize: 32, fontWeight: 700}}>
          <div style={{marginBottom: 10}}>Stress</div>
          <div style={{height: 34, borderRadius: 999, background: '#24356E', overflow: 'hidden'}}>
            <div style={{width: `${8 + 92 * stress}%`, height: '100%', borderRadius: 999, background: stress < 0.5 ? mix(colors.aqua, WARM, stress * 2) : mix(WARM, ORANJE, (stress - 0.5) * 2)}} />
          </div>
        </div>
      </div>
      {/* Right: looking */}
      <div style={{position: 'absolute', left: 540, top: 0, width: 540, height: H, background: `linear-gradient(180deg, ${NACHT} 0%, ${NACHT2} 100%)`, overflow: 'hidden'}}>
        <svg width={540} height={H} style={{position: 'absolute', inset: 0}}>
          <Water huizen={huizen} y={1180} breedte={540} hoogte={H - 1180} aan={aan} frame={frame} />
          <Lichtkunst frame={frame} at={30} y={1440} breedte={540} />
          <Huizen huizen={huizen} y={1180} aan={aan} />
          <Lampjes frame={frame} at={10} y={760} breedte={540} />
          <rect x={0} y={1180} width={540} height={26} fill="#2A3F86" />
        </svg>
        <div style={{position: 'absolute', left: walkX - 540, top: 1040 + Math.abs(Math.sin(loop * Math.PI * 2)) * -6}}>
          <Img src={staticFile('svg/atom/py-atom-figure-walk.svg')} style={{height: 140, display: 'block', filter: 'brightness(0) invert(1)'}} />
        </div>
        <div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center', color: colors.wit}}>
          <div style={{fontSize: 52, fontWeight: 700}}>Rondje kijken</div>
          <div style={{fontSize: 36, marginTop: 8, opacity: 0.85}}>langs de grachten</div>
        </div>
      </div>
      <div style={{position: 'absolute', left: 538, top: 0, width: 4, height: H, background: colors.wit, opacity: 1 - keuze}} />
      {/* Question, then the answer */}
      <div style={{position: 'absolute', left: 50, right: 50, top: 1260, textAlign: 'center', opacity: inn(frame, VRAAG) * (1 - tween(frame, KEUZE - 6, KEUZE + 10))}}>
        <div style={{display: 'inline-block', padding: '26px 40px', borderRadius: 40, background: colors.blauw, border: `5px solid ${colors.wit}`, color: colors.wit, fontSize: 72, fontWeight: 700, lineHeight: 1.1}}>
          Rondje zoeken of
          <br />
          rondje kijken?
        </div>
      </div>
      <div style={{position: 'absolute', left: 50, right: 50, top: 1250, textAlign: 'center', opacity: inn(frame, KEUZE + 6) * (1 - tween(frame, CTA - 10, CTA + 6))}}>
        <div style={{display: 'inline-block', padding: '26px 40px', borderRadius: 40, background: colors.aqua, color: colors.wit, fontSize: 64, fontWeight: 700, lineHeight: 1.12}}>
          Parkeer bij Plantage
          <br />
          en loop zo de stad in.
        </div>
      </div>
      <Dim at={CTA} />
      <EindCta start={CTA} reserveer k={CTA_GEO.staand} />
    </Basis>
  );
};

// ---------------------------------------------------------------- 4. Light Nights (date versions)

export const NACHT_DUUR = 600;

export type LightNight = {slug: string; dag: string; datum: string; start: [number, number, number, number]};
export const LIGHT_NIGHTS: LightNight[] = [
  {slug: '26-nov', dag: 'Do', datum: '26 nov', start: [2, 18, 42, 10]},
  {slug: '12-dec', dag: 'Za', datum: '12 dec', start: [3, 6, 15, 40]},
  {slug: '19-dec', dag: 'Za', datum: '19 dec', start: [3, 6, 15, 40]},
];

const Flip: React.FC<{waarde: number; label: string}> = ({waarde, label}) => (
  <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12}}>
    <div style={{position: 'relative', width: 186, height: 200, borderRadius: 26, background: colors.wit, color: colors.blauw, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 120, fontWeight: 700, overflow: 'hidden'}}>
      {String(waarde).padStart(2, '0')}
      <div style={{position: 'absolute', left: 0, right: 0, top: 99, height: 3, background: colors.blauw, opacity: 0.25}} />
    </div>
    <div style={{fontSize: 32, color: colors.wit}}>{label}</div>
  </div>
);

export const LightNightSpot: React.FC<{nacht: LightNight}> = ({nacht}) => {
  const frame = useCurrentFrame();
  const huizen = React.useMemo(() => maakHuizen(33, W), []);
  const NUL = 300;
  const CTA = 440;
  // Countdown runs from the start value to zero, accelerating, then the city lights up.
  const p = tween(frame, 60, NUL, ease(0.55, 0, 0.9, 0.6));
  const [d0, u0, m0, s0] = nacht.start;
  const totaal = ((d0 * 24 + u0) * 60 + m0) * 60 + s0;
  const rest = Math.max(0, Math.round(totaal * (1 - p)));
  const vals = [Math.floor(rest / 86400), Math.floor((rest % 86400) / 3600), Math.floor((rest % 3600) / 60), rest % 60];
  const aan = (rank: number) => (rank > 0.92 ? 0 : tween(frame, NUL + rank * 50, NUL + 10 + rank * 50));
  const burst = tween(frame, NUL, NUL + 50, ease(0.2, 0.9, 0.3, 1));
  const B = 1500;
  return (
    <Basis>
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${NACHT} 0%, ${NACHT2} 75%)`}} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        {burst > 0 && burst < 1
          ? [0, 1, 2].map((i) => {
              const v = Math.max(0, Math.min(1, burst * 1.4 - i * 0.2));
              return <circle key={i} cx={540} cy={760} r={120 + v * 700} fill="none" stroke={[colors.aqua, WARM, '#B79CFF'][i]} strokeWidth={14 * (1 - v)} opacity={1 - v} />;
            })
          : null}
        <Water huizen={huizen} y={B} breedte={W} hoogte={H - B} aan={aan} frame={frame} />
        <Lichtkunst frame={frame} at={NUL + 10} y={B + 300} />
        <Huizen huizen={huizen} y={B} aan={aan} />
      </svg>
      {/* Date card */}
      <div style={{position: 'absolute', top: 290, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', color: colors.wit}}>
        <div style={{fontSize: 60, fontWeight: 700, color: colors.aqua, letterSpacing: 4, opacity: interpolate(frame, [0, 20], [0.5, 1], clamp)}}>LIGHT NIGHT</div>
        <div style={{marginTop: 14, padding: '14px 44px', borderRadius: 999, background: colors.wit, color: colors.blauw, fontSize: 84, fontWeight: 700, transform: `scale(${0.7 + 0.3 * pop(frame, 6, 24)})`}}>
          {nacht.dag} {nacht.datum}
        </div>
      </div>
      {/* Countdown */}
      <div style={{position: 'absolute', top: 620, width: '100%', display: 'flex', justifyContent: 'center', gap: 22, opacity: inn(frame, 24) * (1 - tween(frame, NUL + 6, NUL + 24))}}>
        <Flip waarde={vals[0]} label="dagen" />
        <Flip waarde={vals[1]} label="uur" />
        <Flip waarde={vals[2]} label="min" />
        <Flip waarde={vals[3]} label="sec" />
      </div>
      <Kop tekst="Dan gaan alle lichten aan" at={NUL + 30} y={660} size={72} uit={CTA - 10} />
      <Kop tekst="Reserveer nu je plek" sub="Parking Plantage, in hartje Amsterdam" at={NUL + 60} y={930} size={72} uit={CTA - 10} />
      <Dim at={CTA} />
      <EindCta start={CTA} reserveer k={CTA_GEO.staand} />
    </Basis>
  );
};

// ---------------------------------------------------------------- 5. Reserveren in 3 tikken

export const TIKKEN_DUUR = 640;

const Tik: React.FC<{x: number; y: number; at: number}> = ({x, y, at}) => {
  const frame = useCurrentFrame();
  const v = tween(frame, at, at + 26);
  if (frame < at - 8 || v >= 1) return null;
  const vinger = 1 - tween(frame, at - 8, at);
  return (
    <div style={{position: 'absolute', left: x, top: y}}>
      <div style={{position: 'absolute', left: -30 - 40 * v, top: -30 - 40 * v, width: 60 + 80 * v, height: 60 + 80 * v, borderRadius: '50%', border: `${6 * (1 - v)}px solid ${colors.aqua}`, opacity: 1 - v, boxSizing: 'border-box'}} />
      <div style={{position: 'absolute', left: -26, top: -26, width: 52, height: 52, borderRadius: '50%', background: colors.blauw, opacity: 0.35 * (1 - v) * (1 - vinger * 0.5)}} />
    </div>
  );
};

export const DrieTikken: React.FC = () => {
  const frame = useCurrentFrame();
  const T1 = 100;
  const T2 = 200;
  const T3 = 300;
  const CTA = 470;
  const PX = 270;
  const PY = 520;
  const PW = 540;
  const PH = 1000;
  const scherm = frame < T1 + 30 ? 0 : frame < T2 + 20 ? 1 : 2;
  const s2 = inn(frame, T1 + 30);
  const s3 = inn(frame, T2 + 20);
  const check = tween(frame, T2 + 30, T2 + 60, ease(0.3, 0, 0.2, 1));
  const ticket = inn(frame, T3 + 10, 30);
  const gloei = frame > T3 + 20 ? 0.5 + 0.5 * Math.sin((frame - T3) / 9) : 0;
  const stap = frame < T1 ? 1 : frame < T2 ? 2 : 3;
  // December 2026 starts on a Tuesday: the grid starts on Monday, so index 1 is the 1st.
  const dagen = Array.from({length: 35}, (_, i) => i);
  return (
    <Basis bg={colors.blauw}>
      <Kop tekst="Reserveren in 3 tikken" at={0} y={290} size={84} uit={CTA - 10} />
      <div style={{position: 'absolute', top: 410, width: '100%', display: 'flex', justifyContent: 'center', gap: 16, opacity: 1 - tween(frame, CTA - 10, CTA + 6)}}>
        {['Datum', 'Bevestigd', 'Ticket'].map((t, i) => (
          <div key={t} style={{padding: '10px 26px', borderRadius: 999, fontSize: 32, fontWeight: 700, background: stap > i ? colors.aqua : 'rgba(255,255,255,0.15)', color: colors.wit}}>
            {i + 1}. {t}
          </div>
        ))}
      </div>
      {/* Phone */}
      <div style={{position: 'absolute', left: PX, top: PY, width: PW, height: PH, borderRadius: 70, background: '#0B1736', border: `10px solid ${colors.wit}`, boxSizing: 'border-box', overflow: 'hidden', opacity: 1 - tween(frame, CTA - 10, CTA + 6), transform: `translateY(${(1 - inn(frame, 0, 30)) * 80}px)`}}>
        <div style={{position: 'absolute', inset: 0, background: '#F3F6FB', color: colors.blauw, fontFamily: font}}>
          <div style={{height: 150, background: colors.blauw, color: colors.wit, padding: '56px 36px 0', boxSizing: 'border-box'}}>
            <div style={{fontSize: 24, opacity: 0.8}}>Parking</div>
            <div style={{fontSize: 40, fontWeight: 700}}>Plantage</div>
          </div>
          {/* Screen 1: date */}
          {scherm === 0 ? (
            <div style={{padding: 30}}>
              <div style={{fontSize: 38, fontWeight: 700, marginBottom: 6}}>Kies je datum</div>
              <div style={{fontSize: 28, marginBottom: 20, opacity: 0.7}}>December 2026</div>
              <div style={{display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: 8, fontSize: 26, textAlign: 'center'}}>
                {['ma', 'di', 'wo', 'do', 'vr', 'za', 'zo'].map((d) => (
                  <div key={d} style={{opacity: 0.55}}>{d}</div>
                ))}
                {dagen.map((d, i) => {
                  const kies = d === 12 && frame >= T1;
                  return (
                    <div key={i} style={{height: 56, lineHeight: '56px', borderRadius: 14, background: kies ? colors.aqua : d > 0 && d <= 31 ? colors.wit : 'transparent', color: kies ? colors.wit : colors.blauw, fontWeight: kies ? 700 : 400}}>
                      {d > 0 && d <= 31 ? d : ''}
                    </div>
                  );
                })}
              </div>
            </div>
          ) : null}
          {/* Screen 2: confirmed */}
          {scherm === 1 ? (
            <div style={{padding: 30, opacity: s2, transform: `translateX(${(1 - s2) * 60}px)`}}>
              <div style={{fontSize: 38, fontWeight: 700}}>Za 12 dec</div>
              <div style={{fontSize: 28, opacity: 0.7, marginBottom: 30}}>Parking Plantage</div>
              <div style={{borderRadius: 24, background: colors.wit, padding: 28}}>
                <div style={{fontSize: 30, marginBottom: 10}}>Rijd in op kenteken</div>
                <div style={{fontSize: 30}}>Plek voor je vastgezet</div>
              </div>
              <div style={{marginTop: 300, height: 96, borderRadius: 999, background: colors.aqua, color: colors.wit, fontSize: 36, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>Reserveer</div>
            </div>
          ) : null}
          {/* Screen 3: confirmed + ticket */}
          {scherm === 2 ? (
            <div style={{padding: 30, opacity: s3}}>
              <div style={{display: 'flex', alignItems: 'center', gap: 18, marginBottom: 26}}>
                <svg width={84} height={84} viewBox="0 0 84 84">
                  <circle cx={42} cy={42} r={38} fill={colors.aqua} />
                  <path d="M24 43 L37 56 L61 30" fill="none" stroke={colors.wit} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - check} />
                </svg>
                <div style={{fontSize: 40, fontWeight: 700}}>Plek bevestigd</div>
              </div>
              <div style={{position: 'relative', opacity: frame >= T3 ? ticket : 0.0001, transform: `scale(${0.85 + 0.15 * ticket})`}}>
                {[40, 26, 14].map((pad, i) => (
                  <div key={i} style={{position: 'absolute', inset: -pad * gloei, borderRadius: 30 + pad, background: colors.aqua, opacity: [0.08, 0.14, 0.25][i] * gloei}} />
                ))}
                <div style={{position: 'relative', borderRadius: 30, background: colors.blauw, color: colors.wit, padding: 34}}>
                  <div style={{fontSize: 26, opacity: 0.8}}>Ticket</div>
                  <div style={{fontSize: 44, fontWeight: 700}}>Parking Plantage</div>
                  <div style={{fontSize: 32, marginTop: 6}}>Za 12 dec</div>
                  <div style={{marginTop: 26, padding: '14px 20px', borderRadius: 16, background: colors.wit, color: colors.blauw, fontSize: 30, fontWeight: 700, textAlign: 'center'}}>Je kenteken is je ticket</div>
                </div>
              </div>
              {frame < T3 ? <div style={{marginTop: 120, height: 96, borderRadius: 999, background: colors.blauw, color: colors.wit, fontSize: 36, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>Toon ticket</div> : null}
            </div>
          ) : null}
        </div>
      </div>
      <Tik x={PX + 674 - 270} y={PY + 421} at={T1} />
      <Tik x={PX + PW / 2} y={PY + 150 + 30 + 46 + 34 + 30 + 160 + 300 + 48} at={T2} />
      <Tik x={PX + PW / 2} y={PY + 150 + 30 + 110 + 120 + 48} at={T3} />
      <EindCta start={CTA} reserveer k={CTA_GEO.staand} />
    </Basis>
  );
};

// ---------------------------------------------------------------- 6. Dagje Artis, avondje licht

export const ARTIS_DUUR = 660;

const Giraf: React.FC<{x: number; y: number; frame: number}> = ({x, y, frame}) => {
  const z = Math.sin(frame / 8) * 10;
  return (
    <g transform={`translate(${x} ${y})`} fill={colors.blauw}>
      <rect x={-62} y={-30} width={14} height={110} rx={7} transform={`rotate(${z} -55 -30)`} />
      <rect x={-34} y={-30} width={14} height={110} rx={7} transform={`rotate(${-z} -27 -30)`} />
      <rect x={30} y={-30} width={14} height={110} rx={7} transform={`rotate(${-z} 37 -30)`} />
      <rect x={56} y={-30} width={14} height={110} rx={7} transform={`rotate(${z} 63 -30)`} />
      <ellipse cx={0} cy={-50} rx={84} ry={48} />
      <path d="M44 -70 L96 -250 L124 -240 L84 -54 Z" />
      <ellipse cx={122} cy={-262} rx={42} ry={22} transform="rotate(-20 122 -262)" />
      <rect x={100} y={-306} width={8} height={26} rx={4} />
      <rect x={116} y={-310} width={8} height={26} rx={4} />
      {[
        [-30, -60],
        [10, -40],
        [40, -66],
        [-50, -36],
        [80, -150],
        [92, -200],
      ].map(([cx, cy], i) => (
        <circle key={i} cx={cx} cy={cy} r={11} fill={colors.aqua} />
      ))}
    </g>
  );
};

const Olifant: React.FC<{x: number; y: number; frame: number}> = ({x, y, frame}) => {
  const z = Math.sin(frame / 9 + 1) * 8;
  const slurf = Math.sin(frame / 14) * 10;
  return (
    <g transform={`translate(${x} ${y})`} fill={colors.blauw}>
      <rect x={-70} y={-40} width={34} height={100} rx={14} transform={`rotate(${z} -53 -40)`} />
      <rect x={-20} y={-40} width={34} height={100} rx={14} transform={`rotate(${-z} -3 -40)`} />
      <rect x={30} y={-40} width={34} height={100} rx={14} transform={`rotate(${z} 47 -40)`} />
      <ellipse cx={0} cy={-80} rx={110} ry={80} />
      <circle cx={-110} cy={-110} r={58} />
      <ellipse cx={-80} cy={-112} rx={36} ry={52} fill="#24408A" />
      <path d={`M-160 -100 Q-${190 + slurf} -40 -${168 + slurf} 30`} stroke={colors.blauw} strokeWidth={26} strokeLinecap="round" fill="none" />
      <circle cx={-128} cy={-128} r={7} fill={colors.wit} />
    </g>
  );
};

export const ArtisLicht: React.FC = () => {
  const frame = useCurrentFrame();
  const huizen = React.useMemo(() => maakHuizen(44, W), []);
  const AVOND = 250;
  const CTA = 500;
  const nacht = tween(frame, AVOND, AVOND + 110, ease(0.45, 0, 0.55, 1));
  const zon = tween(frame, AVOND - 40, AVOND + 80, ease(0.5, 0, 0.6, 1));
  const dieren = 1 - tween(frame, AVOND + 10, AVOND + 70);
  const stad = tween(frame, AVOND + 40, AVOND + 110, ease(0.2, 0.9, 0.3, 1));
  const aan = (rank: number) => (rank > 0.9 ? 0 : tween(frame, AVOND + 90 + rank * 90, AVOND + 100 + rank * 90));
  const loopX = (frame / ARTIS_DUUR) * 200;
  const B = 1380;
  return (
    <Basis>
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${mix('#BFEAF2', NACHT, nacht)} 0%, ${mix('#E9F8FB', NACHT2, nacht)} 70%)`}} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        {/* Sun going down */}
        <circle cx={800} cy={620 + zon * 700} r={90} fill={WARM} opacity={1 - nacht * 0.9} />
        {/* Day: trees, ground and animals */}
        <g opacity={dieren}>
          <rect x={0} y={B - 20} width={W} height={H - B + 20} fill="#BFE7D9" />
          {[
            [120, B - 20, 110],
            [930, B - 20, 130],
            [520, B - 20, 80],
          ].map(([x, y, r], i) => (
            <g key={i}>
              <rect x={x - 12} y={y - r * 1.2} width={24} height={r * 1.2} fill="#5E8C8F" />
              <circle cx={x} cy={y - r * 1.5} r={r} fill={colors.aqua} opacity={0.85} />
            </g>
          ))}
          <Giraf x={300 + loopX} y={B + 60} frame={frame} />
          <Olifant x={820 - loopX * 0.6} y={B + 120} frame={frame} />
        </g>
        {/* Evening: canal houses, water and light art */}
        <g opacity={stad} transform={`translate(0 ${(1 - stad) * 200})`}>
          <Water huizen={huizen} y={B} breedte={W} hoogte={H - B} aan={aan} frame={frame} />
          <Lichtkunst frame={frame} at={AVOND + 120} y={B + 300} />
          <Huizen huizen={huizen} y={B} aan={aan} />
          <Lampjes frame={frame} at={AVOND + 130} y={B - 110} />
        </g>
      </svg>
      <Kop tekst="Overdag naar Artis" at={0} y={330} size={92} color={colors.blauw} uit={AVOND - 10} />
      <Kop tekst="'s Avonds lichtkunst" at={AVOND + 20} y={330} size={92} uit={AVOND + 170} />
      <Kop tekst="Eén keer parkeren, de hele dag Amsterdam." sub="Parking Plantage, direct naast Artis" at={AVOND + 186} y={330} size={84} uit={CTA - 10} />
      <Dim at={CTA} />
      <EindCta start={CTA} reserveer k={CTA_GEO.staand} />
    </Basis>
  );
};
