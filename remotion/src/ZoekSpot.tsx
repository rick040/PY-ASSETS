import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Fonts} from './components';
import {colors, font} from './theme';
import {clamp, ease, tween, useUbuntu, width, wrap} from './LocatieSpot';
import {RESERVEERBAAR, locaties, type Locatie} from './locaties';
import type {Zoekopdracht} from './zoekopdrachten';

// Search spot, after the Jitter work in progress "IOS Stack": the question is typed in a search bar,
// the matching locations come in as a card carousel, and a CTA closes it. 60 fps, 9:16 and 16:9.
// No CSS blur filters: with them Chrome sometimes dropped layers in a frame (cards flickered away).
// 9:16 keeps logo, search and cards inside the 4:5 feed preview (y 285 to 1635).

export type ZoekFormaat = 'staand' | 'liggend';

type Geo = {
  w: number;
  h: number;
  logo: {y: number; w: number};
  pill: {w: number; h: number; y: number; yUp: number; scaleUp: number; text: number};
  card: {w: number; h: number; y: number; gap: number; name: number; pill: number; pad: number};
  dotsY: number;
  cta: {logoY: number; logoW: number; titleY: number; title: number; sub: number; buttonY: number; button: number};
};

const GEO: Record<ZoekFormaat, Geo> = {
  // Reel: key content between 250 px from the top and 330 px from the bottom.
  staand: {
    w: 1080,
    h: 1920,
    logo: {y: 320, w: 300},
    pill: {w: 960, h: 150, y: 900, yUp: 460, scaleUp: 0.86, text: 54},
    card: {w: 820, h: 972, y: 578, gap: 860, name: 74, pill: 40, pad: 52},
    dotsY: 1588,
    cta: {logoY: 520, logoW: 380, titleY: 1010, title: 104, sub: 60, buttonY: 1250, button: 58},
  },
  // YouTube: centred, neighbouring cards visible left and right.
  liggend: {
    w: 1920,
    h: 1080,
    logo: {y: 70, w: 250},
    pill: {w: 1100, h: 124, y: 500, yUp: 190, scaleUp: 0.8, text: 50},
    card: {w: 540, h: 640, y: 285, gap: 600, name: 52, pill: 30, pad: 36},
    dotsY: 958,
    cta: {logoY: 150, logoW: 300, titleY: 560, title: 96, sub: 52, buttonY: 790, button: 52},
  },
};

const HOLD = 140; // frames per card
const CTA_LEN = 170;

/** Parses "Avondje [PSV]?" into characters with a bold flag. */
const parse = (zoek: string) => {
  const out: {c: string; b: boolean}[] = [];
  let bold = false;
  for (const c of zoek) {
    if (c === '[') bold = true;
    else if (c === ']') bold = false;
    else out.push({c, b: bold});
  }
  return out;
};

/** All the moments of the spot, from the length of the question and the number of cards. */
export const timeline = (z: Zoekopdracht) => {
  const chars = parse(z.zoek).length;
  const typeStart = 15;
  const typeEnd = typeStart + Math.round(Math.min(110, Math.max(50, chars * 3.2)));
  const press = typeEnd + 18;
  const up = press + 16;
  const first = up + 18;
  const cards = z.locaties.map((_, i) => first + i * HOLD);
  const cta = first + z.locaties.length * HOLD;
  return {typeStart, typeEnd, press, up, first, cards, cta, duration: cta + CTA_LEN};
};

const vind = (slug: string): Locatie => {
  const l = locaties.find((x) => x.slug === slug);
  if (!l) throw new Error(`Onbekende locatie ${slug}`);
  return l;
};

const prijsTekst = (l: Locatie) =>
  l.prijs.bedrag === 'Gratis' ? `Gratis ${l.prijs.eenheid}` : `${l.prijs.vanaf ? 'vanaf ' : ''}${l.prijs.bedrag} ${l.prijs.eenheid}`;

/** The most useful second fact for a card: walking time if there is one, else the first fact. */
const kenmerkTekst = (l: Locatie) => {
  const k = l.kenmerken.find(([a, b]) => /min\./.test(a) || /station|winkel/i.test(b)) ?? l.kenmerken[0];
  return k[0] ? `${k[0]} ${k[1]}` : k[1];
};

// ---------------------------------------------------------------- search bar

const Search: React.FC<{z: Zoekopdracht; g: Geo}> = ({z, g}) => {
  const frame = useCurrentFrame();
  const t = timeline(z);
  const chars = parse(z.zoek);
  const p = g.pill;
  // The pill grows open from the middle, then the question is typed letter by letter.
  const open = tween(frame, 0, 14, ease(0.2, 0.9, 0.3, 1));
  const typed = Math.floor(interpolate(frame, [t.typeStart, t.typeEnd], [0, chars.length], clamp));
  const tap = interpolate(frame, [t.press, t.press + 5, t.press + 14], [1, 0.95, 1], clamp);
  const move = tween(frame, t.up, t.up + 30, ease(0.5, 0, 0, 1));
  const y = interpolate(move, [0, 1], [p.y, p.yUp]);
  const s = interpolate(move, [0, 1], [1, p.scaleUp]) * tap;
  const cursorOn = frame < t.press && Math.floor(frame / 18) % 2 === 0;
  const inner = p.w - p.h * 1.25;
  const full = chars.reduce((sum, ch) => sum + width(ch.c, p.text, ch.b ? '700' : '400'), 0);
  const size = Math.min(p.text, (p.text * inner) / full);
  const icon = p.h * 0.36;
  return (
    <div
      style={{
        position: 'absolute',
        left: (g.w - p.w) / 2,
        top: y - p.h / 2,
        width: p.w,
        height: p.h,
        transform: `scale(${s}) scaleX(${0.2 + 0.8 * open})`,
        opacity: Math.min(1, open * 3),
        borderRadius: p.h / 2,
        background: colors.wit,
        boxShadow: '0 18px 50px rgba(0,0,0,0.25)',
        display: 'flex',
        alignItems: 'center',
        paddingLeft: p.h * 0.36,
      }}
    >
      <svg width={icon} height={icon} viewBox="0 0 24 24" style={{flex: 'none', opacity: 0.55}}>
        <circle cx="10" cy="10" r="6.5" fill="none" stroke={colors.blauw} strokeWidth="2.4" />
        <path d="M15 15l5.5 5.5" stroke={colors.blauw} strokeWidth="2.6" strokeLinecap="round" />
      </svg>
      <div style={{marginLeft: p.h * 0.22, fontFamily: font, fontSize: size, color: colors.blauw, whiteSpace: 'pre', display: 'flex', alignItems: 'center'}}>
        {chars.slice(0, typed).map((ch, i) => (
          <span key={i} style={{fontWeight: ch.b ? 700 : 400}}>
            {ch.c}
          </span>
        ))}
        <span style={{display: 'inline-block', width: 4, height: size * 1.05, marginLeft: 3, background: colors.aqua, opacity: cursorOn ? 1 : 0}} />
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- cards

const Card: React.FC<{l: Locatie; g: Geo; active: number}> = ({l, g, active}) => {
  const frame = useCurrentFrame();
  const c = g.card;
  // Text and pills come in each time the card becomes the active one.
  const name = tween(frame, active + 4, active + 30, ease(0.2, 0.9, 0.3, 1));
  const pill1 = tween(frame, active + 16, active + 40, ease(0.2, 0.9, 0.3, 1));
  const pill2 = tween(frame, active + 24, active + 48, ease(0.2, 0.9, 0.3, 1));
  const lines = wrap(l.naam, c.name, '700', c.w - c.pad * 2);
  const pill = (text: string, t: number, bg: string, color: string) => (
    <div
      style={{
        display: 'inline-block',
        marginRight: 14,
        marginTop: 14,
        padding: `${c.pill * 0.32}px ${c.pill * 0.62}px`,
        borderRadius: 999,
        background: bg,
        color,
        fontWeight: 700,
        fontSize: c.pill,
        transform: `translateY(${(1 - t) * 24}px)`,
        opacity: t,
        whiteSpace: 'nowrap',
      }}
    >
      {text}
    </div>
  );
  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        borderRadius: c.w * 0.06,
        overflow: 'hidden',
        border: `${Math.round(c.w * 0.01)}px solid ${colors.wit}`,
        boxShadow: '0 30px 70px rgba(0,0,0,0.35)',
        background: colors.blauw,
      }}
    >
      <Img src={staticFile(l.foto)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover'}} />
      <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg, rgba(26,53,128,0) 38%, rgba(26,53,128,0.92) 82%)'}} />
      <div style={{position: 'absolute', left: c.pad, right: c.pad, bottom: c.pad * 0.8, fontFamily: font, color: colors.wit}}>
        <div style={{overflow: 'hidden', fontSize: c.name * 0.7, lineHeight: 1.15}}>
          <div style={{transform: `translateY(${(1 - name) * 110}%)`}}>{`Parking`}</div>
        </div>
        {lines.map((line, i) => (
          <div key={i} style={{overflow: 'hidden', fontSize: c.name, fontWeight: 700, lineHeight: 1.12}}>
            <div style={{transform: `translateY(${(1 - tween(frame, active + 8 + i * 4, active + 34 + i * 4, ease(0.2, 0.9, 0.3, 1))) * 110}%)`}}>{line}</div>
          </div>
        ))}
        <div>
          {pill(prijsTekst(l), pill1, colors.aqua, colors.wit)}
          {pill(kenmerkTekst(l), pill2, 'rgba(255,255,255,0.92)', colors.blauw)}
        </div>
      </div>
    </div>
  );
};

const Carousel: React.FC<{z: Zoekopdracht; g: Geo}> = ({z, g}) => {
  const frame = useCurrentFrame();
  const t = timeline(z);
  const c = g.card;
  const items = z.locaties.map(vind);
  // Position in the carousel as a float: 0 is the first card, each swipe adds one.
  const pos = t.cards.slice(1).reduce((sum, start) => sum + tween(frame, start - 26, start + 4, ease(0.6, 0, 0.2, 1)), 0);
  const enter = tween(frame, t.first, t.first + 32, ease(0.2, 0.9, 0.3, 1));
  const leave = tween(frame, t.cta - 6, t.cta + 20, ease(0.5, 0, 0.8, 0.4));
  if (frame < t.first) return null;
  return (
    <AbsoluteFill style={{opacity: 1 - leave, transform: `translateY(${-120 * leave}px)`}}>
      {items.map((l, i) => {
        const d = i - pos;
        const ad = Math.min(Math.abs(d), 1.5);
        const x = g.w / 2 - c.w / 2 + d * c.gap;
        const scale = (1 - 0.14 * Math.min(ad, 1)) * (0.88 + 0.12 * enter);
        const opacity = (1 - 0.5 * Math.min(ad, 1)) * enter;
        return (
          <div
            key={l.slug}
            style={{
              position: 'absolute',
              left: x,
              top: c.y + 180 * (1 - enter),
              width: c.w,
              height: c.h,
              transform: `scale(${scale})`,
              opacity,
              zIndex: 10 - Math.round(ad * 2),
            }}
          >
            <Card l={l} g={g} active={t.cards[i]} />
          </div>
        );
      })}
      {items.length > 1 ? (
        <div style={{position: 'absolute', top: g.dotsY, left: 0, width: g.w, display: 'flex', justifyContent: 'center', gap: 18, opacity: enter}}>
          {items.map((_, i) => {
            const on = Math.max(0, 1 - Math.abs(i - pos));
            return <div key={i} style={{width: 18 + 26 * on, height: 18, borderRadius: 9, background: on > 0.5 ? colors.aqua : 'rgba(255,255,255,0.45)'}} />;
          })}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- CTA

const Cta: React.FC<{z: Zoekopdracht; g: Geo}> = ({z, g}) => {
  const frame = useCurrentFrame();
  const t = timeline(z);
  const reserveer = z.locaties.every((s) => RESERVEERBAAR.has(vind(s).id));
  const k = g.cta;
  const logo = tween(frame, t.cta + 8, t.cta + 38, ease(0.2, 0.9, 0.3, 1.15));
  const title = tween(frame, t.cta + 18, t.cta + 44, ease(0.2, 0.9, 0.3, 1));
  const sub = tween(frame, t.cta + 26, t.cta + 52, ease(0.2, 0.9, 0.3, 1));
  const button = tween(frame, t.cta + 36, t.cta + 62, ease(0.2, 1.3, 0.4, 1));
  const tap = interpolate(frame, [t.cta + 100, t.cta + 106, t.cta + 118], [1, 0.93, 1], clamp);
  const glow = tween(frame, t.cta + 100, t.cta + 140);
  if (frame < t.cta) return null;
  const rise = (v: number): React.CSSProperties => ({opacity: v, transform: `translateY(${(1 - v) * 50}px)`});
  return (
    <AbsoluteFill style={{fontFamily: font, color: colors.wit}}>
      <div style={{position: 'absolute', top: k.logoY, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <div style={{transform: `scale(${logo})`, opacity: Math.min(1, logo * 2)}}>
          <Img src={staticFile('svg/atom/py-atom-logo-stacked-white.svg')} style={{width: k.logoW, display: 'block'}} />
        </div>
      </div>
      <div style={{position: 'absolute', top: k.titleY, width: '100%', textAlign: 'center', fontSize: k.title, fontWeight: 700, lineHeight: 1.05, ...rise(title)}}>
        {reserveer ? 'Reserveer online' : 'Bekijk alle locaties'}
      </div>
      <div style={{position: 'absolute', top: k.titleY + k.title * 1.2, width: '100%', textAlign: 'center', fontSize: k.sub, lineHeight: 1.2, ...rise(sub)}}>
        {reserveer ? 'en sta zeker van je plek' : 'met tarieven en openingstijden'}
      </div>
      <div style={{position: 'absolute', top: k.buttonY, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <div
          style={{
            padding: `${k.button * 0.45}px ${k.button * 1.1}px`,
            borderRadius: 999,
            background: colors.wit,
            color: colors.blauw,
            fontSize: k.button,
            fontWeight: 700,
            transform: `scale(${button * tap})`,
            opacity: Math.min(1, button * 2),
            boxShadow: `0 0 0 ${glow * 26}px rgba(50,185,205,${0.5 * (1 - glow)})`,
          }}
        >
          parkingyou.nl
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- composition

const Header: React.FC<{z: Zoekopdracht; g: Geo}> = ({z, g}) => {
  const frame = useCurrentFrame();
  const t = timeline(z);
  const out = tween(frame, t.cta - 6, t.cta + 14);
  return (
    <div style={{position: 'absolute', top: g.logo.y, width: '100%', display: 'flex', justifyContent: 'center', opacity: 1 - out}}>
      <Img src={staticFile('svg/atom/py-atom-logo-horizontal-white.svg')} style={{width: g.logo.w, display: 'block'}} />
    </div>
  );
};

export const ZoekSpot: React.FC<{zoekopdracht: Zoekopdracht; formaat?: ZoekFormaat}> = ({zoekopdracht: z, formaat = 'staand'}) => {
  const frame = useCurrentFrame();
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: colors.blauw}} />;
  const g = GEO[formaat];
  const t = timeline(z);
  const searchOut = tween(frame, t.cta - 6, t.cta + 14);
  return (
    <AbsoluteFill style={{background: colors.blauw}}>
      <Fonts />
      <Header z={z} g={g} />
      <div style={{opacity: 1 - searchOut}}>
        <Search z={z} g={g} />
      </div>
      <Carousel z={z} g={g} />
      <Cta z={z} g={g} />
    </AbsoluteFill>
  );
};

export const ZOEK_SIZE: Record<ZoekFormaat, {width: number; height: number}> = {
  staand: {width: 1080, height: 1920},
  liggend: {width: 1920, height: 1080},
};
