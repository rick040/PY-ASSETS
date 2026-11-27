import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Fonts} from './components';
import {colors, font} from './theme';
import {clamp, ease, tween, useUbuntu, wrap} from './LocatieSpot';
import {CTA_GEO, EindCta, type ZoekFormaat} from './ZoekSpot';
import {RESERVEERBAAR, locaties, type Locatie} from './locaties';
import type {Overstap} from './overstappen';

// "Parkeer en stap over": a question, then a line map like a metro map. A car pulls into the parking stop, a walker follows
// the line to the station, a train pulls in and the departure board fills with the places the location page names; the train
// leaves and the shared end screen follows. 60 fps, 9:16 (vertical line) and 16:9 (horizontal line).
// No box-shadows or blur, render in one tab (see LijstSpot).

type Geo = {
  w: number;
  h: number;
  logo: {y: number; w: number};
  vraag: {x: number; y: number; w: number; size: number; sub: number; align: 'center' | 'left'};
  /** Stop positions: parking, walk (label only), station. */
  stops: [number, number][];
  richting: 'v' | 'h';
  bord: {x: number; y: number; w: number; rij: number; tekst: number};
  label: number;
  stip: number;
};

const GEO: Record<ZoekFormaat, Geo> = {
  staand: {
    w: 1080,
    h: 1920,
    logo: {y: 250, w: 300},
    vraag: {x: 60, y: 360, w: 960, size: 84, sub: 46, align: 'center'},
    stops: [
      [170, 720],
      [170, 950],
      [170, 1180],
    ],
    richting: 'v',
    bord: {x: 120, y: 1285, w: 840, rij: 78, tekst: 44},
    label: 50,
    stip: 96,
  },
  liggend: {
    w: 1920,
    h: 1080,
    logo: {y: 40, w: 250},
    vraag: {x: 110, y: 170, w: 1100, size: 80, sub: 44, align: 'left'},
    stops: [
      [230, 560],
      [690, 560],
      [1150, 560],
    ],
    richting: 'h',
    bord: {x: 1340, y: 430, w: 470, rij: 84, tekst: 42},
    label: 44,
    stip: 92,
  },
};

export const overstapTimeline = () => {
  const auto = 40;
  const lopen = 110;
  const station = 230;
  const trein = 250;
  const bord = 300;
  const weg = 420;
  const cta = 470;
  return {auto, lopen, station, trein, bord, weg, cta, duration: cta + 170};
};

const vind = (slug: string): Locatie => {
  const l = locaties.find((x) => x.slug === slug);
  if (!l) throw new Error(`Onbekende locatie ${slug}`);
  return l;
};

const Trein: React.FC<{breed: number; vervoer: 'trein' | 'metro'}> = ({breed, vervoer}) => (
  <svg width={breed} height={breed * 0.36} viewBox="0 0 200 72" style={{display: 'block'}}>
    <path d="M6 10 Q6 4 12 4 L168 4 Q194 4 196 40 L196 56 Q196 64 188 64 L12 64 Q6 64 6 58 Z" fill={colors.wit} stroke={colors.blauw} strokeWidth={4} />
    <rect x={6} y={44} width={190} height={8} fill={vervoer === 'metro' ? colors.blauw : colors.aqua} />
    {[18, 50, 82, 114].map((x) => (
      <rect key={x} x={x} y={14} width={24} height={20} rx={4} fill={colors.blauw} />
    ))}
    <path d="M150 14 L170 14 Q184 16 186 34 L150 34 Z" fill={colors.blauw} />
    <circle cx={40} cy={68} r={4} fill={colors.blauw} />
    <circle cx={160} cy={68} r={4} fill={colors.blauw} />
  </svg>
);

const Auto: React.FC<{breed: number}> = ({breed}) => (
  <svg width={breed} height={breed * 0.5} viewBox="0 0 120 60" style={{display: 'block'}}>
    <path d="M8 40 Q8 30 18 28 L34 26 L46 12 Q50 8 58 8 L84 8 Q92 8 96 14 L106 28 Q114 30 114 40 L114 46 Q114 50 110 50 L12 50 Q8 50 8 46 Z" fill={colors.wit} stroke={colors.blauw} strokeWidth={4} />
    <path d="M50 14 L60 14 L60 26 L40 26 Z M66 14 L84 14 Q88 14 90 18 L96 26 L66 26 Z" fill={colors.blauw} />
    <circle cx={32} cy={50} r={9} fill={colors.blauw} stroke={colors.wit} strokeWidth={3} />
    <circle cx={92} cy={50} r={9} fill={colors.blauw} stroke={colors.wit} strokeWidth={3} />
  </svg>
);

export const OverstapSpot: React.FC<{overstap: Overstap; formaat?: ZoekFormaat}> = ({overstap: o, formaat = 'staand'}) => {
  const frame = useCurrentFrame();
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: colors.blauw}} />;
  const g = GEO[formaat];
  const t = overstapTimeline();
  const l = vind(o.locatie);
  const staand = formaat === 'staand';
  const [A, B, C] = g.stops;
  const v = g.richting === 'v';

  const vraagIn = interpolate(frame, [0, 22], [0.5, 1], {...clamp, easing: ease(0.2, 0.9, 0.3, 1)});
  const subIn = tween(frame, 12, 36, ease(0.2, 0.9, 0.3, 1));
  const out = tween(frame, t.cta - 6, t.cta + 14);
  const vraagLines = wrap(o.vraag, g.vraag.size, '700', g.vraag.w);
  const subLines = wrap(o.sub, g.vraag.sub, '400', g.vraag.w);

  const pop = (at: number) => tween(frame, at, at + 18, ease(0.3, 1.6, 0.5, 1));
  const inn = (at: number, len = 22) => tween(frame, at, at + len, ease(0.2, 0.9, 0.3, 1));
  // The line from parking to station is drawn as the walker goes.
  const lijn = tween(frame, t.lopen, t.station, ease(0.4, 0, 0.5, 1));
  const end = [A[0] + (C[0] - A[0]) * lijn, A[1] + (C[1] - A[1]) * lijn];
  const loper = frame >= t.lopen && frame < t.station + 10;
  const stap = Math.abs(Math.sin(frame / 5)) * 6;
  // Car: slides in towards the parking stop and fades into it.
  const autoV = tween(frame, t.auto - 30, t.auto + 26, ease(0.2, 0.8, 0.3, 1));
  const autoUit = tween(frame, t.auto + 26, t.auto + 40);
  // Train: pulls in at the station, leaves later.
  const treinIn = tween(frame, t.trein, t.trein + 40, ease(0.2, 0.9, 0.3, 1));
  const treinUit = tween(frame, t.weg, t.weg + 30, ease(0.6, 0, 0.9, 0.5));
  const tb = staand ? 300 : 260;
  const stip = g.stip;
  const labelStyle: React.CSSProperties = {position: 'absolute', color: colors.wit, lineHeight: 1.15};

  return (
    <AbsoluteFill style={{background: colors.blauw, fontFamily: font, overflow: 'hidden'}}>
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

        {/* The line: faint full track, aqua drawn part */}
        <svg width={g.w} height={g.h} style={{position: 'absolute', left: 0, top: 0}}>
          <line x1={A[0]} y1={A[1]} x2={C[0]} y2={C[1]} stroke={colors.wit} strokeOpacity={0.18} strokeWidth={18} strokeLinecap="round" />
          {lijn > 0 ? <line x1={A[0]} y1={A[1]} x2={end[0]} y2={end[1]} stroke={colors.aqua} strokeWidth={18} strokeLinecap="round" /> : null}
          {/* walk stop: small ring */}
          <circle cx={B[0]} cy={B[1]} r={18} fill={colors.blauw} stroke={frame >= t.lopen + 50 ? colors.aqua : 'rgba(255,255,255,0.3)'} strokeWidth={8} />
        </svg>

        {/* Stop 1: parking */}
        <div style={{position: 'absolute', left: A[0] - stip / 2, top: A[1] - stip / 2, width: stip, height: stip, borderRadius: stip * 0.24, background: colors.aqua, border: `6px solid ${colors.wit}`, boxSizing: 'border-box', color: colors.wit, fontSize: stip * 0.56, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${0.6 + 0.4 * pop(t.auto + 10)})`}}>P</div>
        {frame < t.auto + 40 ? (
          <div style={{position: 'absolute', left: v ? A[0] - 340 + 280 * autoV : A[0] - 60 - 300 * (1 - autoV), top: v ? A[1] - 40 : A[1] - 130, opacity: Math.min(1, autoV * 2) * (1 - autoUit)}}>
            <Auto breed={150} />
          </div>
        ) : null}
        <div style={{...labelStyle, ...(v ? {left: A[0] + stip * 0.8, top: A[1] - g.label * 0.75} : {left: A[0] - 160, top: A[1] + stip * 0.75, width: 340, textAlign: 'center'}), opacity: inn(t.auto + 16)}}>
          <div style={{fontSize: g.label * 0.62, opacity: 0.85}}>Parkeer bij</div>
          <div style={{fontSize: g.label, fontWeight: 700}}>{l.naam}</div>
          <div style={{display: 'inline-block', marginTop: 10, padding: `${g.label * 0.18}px ${g.label * 0.5}px`, borderRadius: 999, background: colors.aqua, fontSize: g.label * 0.62, fontWeight: 700, transform: `scale(${pop(t.auto + 40)})`}}>{o.prijs}</div>
          {o.voorwaarde ? <div style={{fontSize: g.label * 0.45, marginTop: 6, opacity: 0.8}}>{o.voorwaarde}</div> : null}
        </div>

        {/* Stop 2: walking */}
        {loper ? (
          <div style={{position: 'absolute', left: end[0] - (v ? 90 : 30), top: end[1] - (v ? 50 : 150) - stap}}>
            <Img src={staticFile('svg/atom/py-atom-figure-walk.svg')} style={{height: 96, display: 'block', filter: 'brightness(0) invert(1)'}} />
          </div>
        ) : null}
        <div style={{...labelStyle, ...(v ? {left: B[0] + stip * 0.8, top: B[1] - g.label * 0.6} : {left: B[0] - 160, top: B[1] + stip * 0.6, width: 320, textAlign: 'center'}), display: 'flex', alignItems: 'center', justifyContent: v ? 'flex-start' : 'center', gap: 14, fontSize: g.label * 0.85, opacity: inn(t.lopen + 50)}}>
          <Img src={staticFile('svg/atom/py-atom-figure-walk.svg')} style={{height: g.label * 0.95, display: 'block', filter: 'brightness(0) invert(1)'}} />
          {o.lopen === 'naast de deur' ? 'Station naast de deur' : `${o.lopen} lopen`}
        </div>

        {/* Stop 3: station */}
        <div style={{position: 'absolute', left: C[0] - stip / 2, top: C[1] - stip / 2, width: stip, height: stip, borderRadius: '50%', background: frame >= t.station ? colors.wit : colors.blauw, border: `8px solid ${frame >= t.station ? colors.aqua : 'rgba(255,255,255,0.3)'}`, boxSizing: 'border-box', transform: `scale(${frame >= t.station ? 0.7 + 0.3 * pop(t.station) : 0.7})`, display: 'flex', alignItems: 'center', justifyContent: 'center', color: colors.blauw, fontSize: stip * 0.42, fontWeight: 700}}>
          {o.vervoer === 'metro' ? 'M' : null}
        </div>
        <div style={{...labelStyle, ...(v ? {left: C[0] + stip * 0.8, top: C[1] - g.label * 0.6} : {left: C[0] - 170, top: C[1] + stip * 0.75, width: 340, textAlign: 'center'}), opacity: inn(t.station + 6)}}>
          <div style={{fontSize: g.label, fontWeight: 700}}>{o.station}</div>
          <div style={{fontSize: g.label * 0.62, opacity: 0.85}}>en stap in de {o.vervoer}</div>
        </div>
        {/* Train pulls in beside the station stop and leaves */}
        {frame >= t.trein ? (
          <div style={{position: 'absolute', left: (v ? 620 : C[0] - tb / 2) - 700 * (1 - treinIn) + 1100 * treinUit, top: v ? C[1] - 160 : C[1] - 170, opacity: treinIn}}>
            <Trein breed={tb} vervoer={o.vervoer} />
          </div>
        ) : null}

        {/* Departure board */}
        <div style={{position: 'absolute', left: g.bord.x, top: g.bord.y, width: g.bord.w, borderRadius: 26, overflow: 'hidden', background: colors.wit, color: colors.blauw, opacity: inn(t.bord - 10), transform: `translateY(${(1 - inn(t.bord - 10)) * 30}px)`}}>
          <div style={{padding: '14px 26px', background: colors.aqua, color: colors.wit, fontSize: g.bord.tekst * 0.7, fontWeight: 700}}>Met de {o.vervoer} naar</div>
          {o.naar.map((n, i) => {
            const at = t.bord + i * 22;
            const k = tween(frame, at, at + 14, ease(0.3, 0, 0.2, 1));
            return (
              <div key={n} style={{height: g.bord.rij, display: 'flex', alignItems: 'center', gap: 18, padding: '0 26px', borderTop: i ? '2px solid rgba(26,53,128,0.1)' : 'none', fontSize: g.bord.tekst, fontWeight: 700, overflow: 'hidden'}}>
                <div style={{transform: `rotateX(${90 * (1 - k)}deg)`, opacity: frame >= at ? 1 : 0}}>{n}</div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
      <EindCta start={t.cta} reserveer={RESERVEERBAAR.has(l.id)} k={CTA_GEO[formaat]} />
    </AbsoluteFill>
  );
};

export const OVERSTAP_SIZE: Record<ZoekFormaat, {width: number; height: number}> = {
  staand: {width: 1080, height: 1920},
  liggend: {width: 1920, height: 1080},
};
