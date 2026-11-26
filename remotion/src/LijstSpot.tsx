import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Fonts} from './components';
import {colors, font} from './theme';
import {clamp, ease, tween, useUbuntu, width, wrap} from './LocatieSpot';
import {CTA_GEO, EindCta, type ZoekFormaat} from './ZoekSpot';
import {RESERVEERBAAR, locaties, type Locatie} from './locaties';
import type {Lijstje} from './lijstjes';

// "Het lijstje": a question, a white card with four points that get a tick one by one, then the card opens
// to show the location (photo, name, price) and the shared end screen. 60 fps, 9:16 and 16:9.
// No box-shadows or blur (they made Chrome drop layers in single frames) and render in one tab.

type Geo = {
  w: number;
  h: number;
  logo: {y: number; w: number};
  area: {top: number; bottom: number};
  vraag: number;
  sub: number;
  /** Column (photo above the list) or row (photo left of the list). */
  richting: 'column' | 'row';
  card: {w: number; pad: number; row: number; text: number; box: number; foto: number; naam: number; prijs: number};
};

const GEO: Record<ZoekFormaat, Geo> = {
  staand: {
    w: 1080,
    h: 1920,
    logo: {y: 250, w: 300},
    area: {top: 400, bottom: 1590},
    vraag: 112,
    sub: 56,
    richting: 'column',
    card: {w: 960, pad: 50, row: 146, text: 60, box: 76, foto: 380, naam: 78, prijs: 250},
  },
  liggend: {
    w: 1920,
    h: 1080,
    logo: {y: 40, w: 250},
    area: {top: 150, bottom: 1040},
    vraag: 80,
    sub: 44,
    richting: 'row',
    card: {w: 900, pad: 44, row: 122, text: 52, box: 66, foto: 640, naam: 66, prijs: 220},
  },
};

const CHECK_START = 75;
const CHECK_GAP = 55;

export const lijstTimeline = () => {
  const checks = [0, 1, 2, 3].map((i) => CHECK_START + i * CHECK_GAP);
  const open = checks[3] + 60;
  const prijs = open + 45;
  const cta = prijs + 135;
  return {checks, open, prijs, cta, duration: cta + 170};
};

const vind = (slug: string): Locatie => {
  const l = locaties.find((x) => x.slug === slug);
  if (!l) throw new Error(`Onbekende locatie ${slug}`);
  return l;
};

/** "Direct [naast Artis]" -> light and bold parts. */
const delen = (s: string) => s.split(/(\[[^\]]*\])/).filter(Boolean).map((x) => (x.startsWith('[') ? {t: x.slice(1, -1), vet: true} : {t: x, vet: false}));

const Rich: React.FC<{text: string}> = ({text}) => (
  <>
    {delen(text).map((d, i) => (
      <span key={i} style={{fontWeight: d.vet ? 700 : 400}}>
        {d.t}
      </span>
    ))}
  </>
);

const Vinkje: React.FC<{at: number; size: number}> = ({at, size}) => {
  const frame = useCurrentFrame();
  const fill = tween(frame, at, at + 10, ease(0.2, 0.9, 0.3, 1));
  const pop = interpolate(frame, [at, at + 7, at + 16], [1, 1.18, 1], clamp);
  const draw = tween(frame, at + 4, at + 18, ease(0.3, 0, 0.2, 1));
  return (
    <div
      style={{
        position: 'relative',
        flex: 'none',
        width: size,
        height: size,
        borderRadius: size * 0.28,
        border: `${size * 0.075}px solid ${colors.aqua}`,
        background: fill > 0 ? colors.aqua : 'transparent',
        opacity: 1,
        transform: `scale(${pop})`,
        boxSizing: 'border-box',
      }}
    >
      <svg viewBox="0 0 26 26" width={size * 0.85} height={size * 0.85} style={{position: 'absolute', left: size * 0.0, top: size * 0.0}}>
        <path d="M6 13.5 L11 18.5 L20.5 8" fill="none" stroke={colors.wit} strokeWidth={3.6} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
      </svg>
    </div>
  );
};

const PrijsRondje: React.FC<{l: Locatie; d: number; at: number}> = ({l, d, at}) => {
  const frame = useCurrentFrame();
  const p = tween(frame, at, at + 30, ease(0.2, 1.4, 0.4, 1));
  if (frame < at) return null;
  const m = l.prijs.bedrag.match(/^(€\d+),(\d\d)$/);
  const main = m ? `${m[1]},` : l.prijs.bedrag;
  const big = d * (m ? (m[1].length > 3 ? 0.26 : 0.3) : 0.2);
  return (
    <div
      style={{
        position: 'absolute',
        right: d * 0.12,
        top: d * 0.12,
        width: d,
        height: d,
        borderRadius: '50%',
        background: colors.aqua,
        color: colors.wit,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        transform: `scale(${p}) rotate(${-30 * (1 - p)}deg)`,
        lineHeight: 1,
      }}
    >
      {l.prijs.vanaf ? <div style={{fontSize: d * 0.1, marginBottom: d * 0.02}}>vanaf</div> : null}
      <div style={{fontSize: big, fontWeight: 700, whiteSpace: 'nowrap'}}>
        {main}
        {m ? <span style={{fontSize: big * 0.6, verticalAlign: 'top', position: 'relative', top: big * 0.05}}>{m[2]}</span> : null}
      </div>
      <div style={{fontSize: d * 0.12, marginTop: d * 0.03}}>{l.prijs.eenheid}</div>
    </div>
  );
};

export const LijstSpot: React.FC<{lijstje: Lijstje; formaat?: ZoekFormaat}> = ({lijstje: s, formaat = 'staand'}) => {
  const frame = useCurrentFrame();
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: colors.blauw}} />;
  const g = GEO[formaat];
  const k = g.card;
  const t = lijstTimeline();
  const l = vind(s.locatie);
  const kolom = g.richting === 'column';

  // Question: there from frame 0 (never an empty first frame), it gives way when the card opens.
  const vraagIn = interpolate(frame, [0, 22], [0.5, 1], {...clamp, easing: ease(0.2, 0.9, 0.3, 1)});
  const subIn = tween(frame, 12, 36, ease(0.2, 0.9, 0.3, 1));
  const cardIn = tween(frame, 24, 56, ease(0.2, 0.9, 0.3, 1));
  const open = tween(frame, t.open, t.open + 45, ease(0.6, 0, 0.2, 1));
  const out = tween(frame, t.cta - 6, t.cta + 14);

  const vraagLines = wrap(s.vraag, g.vraag, '700', g.w - 160);
  const subLines = wrap(s.sub ?? 'Hier parkeer je zonder zorgen:', g.sub, '400', g.w - 160);
  const vraagH = vraagLines.length * g.vraag * 1.1 + subLines.length * g.sub * 1.25 + (kolom ? 70 : 40);

  const naamLines = wrap(l.naam, k.naam, '700', k.w - k.pad * 2);
  const naamH = k.pad * 0.9 + k.naam * 0.62 * 1.2 + naamLines.length * k.naam * 1.1 + k.pad * 0.2;
  const lijstH = 4 * k.row + k.pad * 0.6;
  const kaartH = naamH + lijstH;

  const fotoMaat = k.foto * open; // height (column) or width (row) of the photo
  const naamMaat = naamH * open;

  return (
    <AbsoluteFill style={{background: colors.blauw, fontFamily: font}}>
      <Fonts />
      <div style={{position: 'absolute', top: g.logo.y, width: '100%', display: 'flex', justifyContent: 'center', opacity: 1 - out}}>
        <Img src={staticFile('svg/atom/py-atom-logo-horizontal-white.svg')} style={{width: g.logo.w, display: 'block'}} />
      </div>
      <div
        style={{
          position: 'absolute',
          left: 0,
          top: g.area.top,
          width: g.w,
          height: g.area.bottom - g.area.top,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          opacity: 1 - out,
          transform: `translateY(${-80 * out}px)`,
        }}
      >
        {/* Question */}
        <div style={{height: vraagH * (1 - open), overflow: 'hidden', flex: 'none', width: '100%', textAlign: 'center', color: colors.wit, opacity: 1 - open * 1.6}}>
          <div style={{fontSize: g.vraag, fontWeight: 700, lineHeight: 1.1, opacity: vraagIn, transform: `scale(${0.8 + 0.2 * vraagIn})`}}>
            {vraagLines.map((x, i) => (
              <div key={i}>{x}</div>
            ))}
          </div>
          <div style={{fontSize: g.sub, lineHeight: 1.25, marginTop: 10, opacity: subIn, transform: `translateY(${(1 - subIn) * 30}px)`}}>
            {subLines.map((x, i) => (
              <div key={i}>{x}</div>
            ))}
          </div>
        </div>

        {/* Card */}
        <div
          style={{
            flex: 'none',
            display: 'flex',
            flexDirection: g.richting,
            background: colors.wit,
            borderRadius: 44,
            overflow: 'hidden',
            opacity: cardIn,
            transform: `translateY(${(1 - cardIn) * 160}px)`,
            color: colors.blauw,
          }}
        >
          <div style={{position: 'relative', flex: 'none', overflow: 'hidden', [kolom ? 'height' : 'width']: fotoMaat, [kolom ? 'width' : 'height']: kolom ? k.w : lijstH + naamMaat}}>
            <Img
              src={staticFile(`locaties/staand/${l.id}.jpg`)}
              decoding="sync"
              style={{position: 'absolute', left: 0, top: 0, width: kolom ? k.w : k.foto, height: kolom ? k.foto : kaartH, objectFit: 'cover', display: 'block'}}
            />
            <PrijsRondje l={l} d={k.prijs} at={t.prijs} />
          </div>
          <div style={{width: k.w, flex: 'none'}}>
            <div style={{height: naamMaat, overflow: 'hidden'}}>
              <div style={{padding: `${k.pad * 0.9}px ${k.pad}px 0`}}>
                <div style={{fontSize: k.naam * 0.62, lineHeight: 1.2}}>Parking</div>
                {naamLines.map((x, i) => (
                  <div key={i} style={{fontSize: k.naam, fontWeight: 700, lineHeight: 1.1}}>
                    {x}
                  </div>
                ))}
              </div>
            </div>
            <div style={{padding: `${k.pad * 0.3}px 0`}}>
              {s.punten.map((p, i) => {
                const at = t.checks[i];
                const aan = tween(frame, at, at + 12);
                return (
                  <div
                    key={i}
                    style={{
                      height: k.row,
                      display: 'flex',
                      alignItems: 'center',
                      gap: k.box * 0.45,
                      padding: `0 ${k.pad}px`,
                      borderTop: i === 0 && open === 0 ? 'none' : `2px solid rgba(26,53,128,0.1)`,
                      fontSize: k.text,
                      whiteSpace: 'nowrap',
                    }}
                  >
                    <Vinkje at={at} size={k.box} />
                    <div style={{opacity: 0.45 + 0.55 * aan}}>
                      <Rich text={p} />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
      <EindCta start={t.cta} reserveer={RESERVEERBAAR.has(l.id)} k={CTA_GEO[formaat]} />
    </AbsoluteFill>
  );
};

export const LIJST_SIZE: Record<ZoekFormaat, {width: number; height: number}> = {
  staand: {width: 1080, height: 1920},
  liggend: {width: 1920, height: 1080},
};

/** Widest point in px at the card's text size, to check that every point fits on one line. */
export const puntBreedte = (p: string, formaat: ZoekFormaat) =>
  delen(p).reduce((sum, d) => sum + width(d.t, GEO[formaat].card.text, d.vet ? '700' : '400'), 0);
