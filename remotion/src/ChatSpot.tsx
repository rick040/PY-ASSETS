import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Fonts} from './components';
import {colors, font} from './theme';
import {clamp, ease, tween, useUbuntu, width, wrap} from './LocatieSpot';
import {CTA_GEO, EindCta, type ZoekFormaat} from './ZoekSpot';
import {RESERVEERBAAR, locaties, type Locatie} from './locaties';
import type {Chatgesprek} from './chatgesprekken';

// "Het appje": a chat in the house style. A question comes in (the hook), the answer is a location card
// and a short tip, a reply closes it, then the same end screen as the search spots. 60 fps, 9:16 and 16:9.
// No box-shadows or blur (they made Chrome drop layers in single frames) and render in one tab.

type Geo = {
  w: number;
  h: number;
  logo: {y: number; w: number};
  chat: {left: number; right: number; top: number; bottom: number};
  text: number;
  maxW: number;
  pad: number;
  gap: number;
  card: {w: number; photoH: number; name: number; pill: number};
};

const GEO: Record<ZoekFormaat, Geo> = {
  staand: {
    w: 1080,
    h: 1920,
    logo: {y: 250, w: 300},
    chat: {left: 70, right: 70, top: 470, bottom: 1580},
    text: 52,
    maxW: 800,
    pad: 34,
    gap: 26,
    card: {w: 780, photoH: 520, name: 66, pill: 38},
  },
  liggend: {
    w: 1920,
    h: 1080,
    logo: {y: 40, w: 250},
    chat: {left: 460, right: 460, top: 180, bottom: 1030},
    text: 42,
    maxW: 760,
    pad: 28,
    gap: 20,
    card: {w: 600, photoH: 380, name: 50, pill: 30},
  },
};

const TYPING = 34; // frames of typing dots before each message
const POP = 18;

/** When each message appears (after its typing dots), and when the CTA starts. */
export const chatTimeline = () => {
  const vraag = TYPING; // typing dots from frame 0, so the first frame is never empty
  const kaart = vraag + 70 + TYPING;
  const tip = kaart + 120 + TYPING;
  const reactie = tip + 100 + TYPING;
  const cta = reactie + 90;
  return {vraag, kaart, tip, reactie, cta, duration: cta + 170};
};

const vind = (slug: string): Locatie => {
  const l = locaties.find((x) => x.slug === slug);
  if (!l) throw new Error(`Onbekende locatie ${slug}`);
  return l;
};

const prijsTekst = (l: Locatie) =>
  l.prijs.bedrag === 'Gratis' ? `Gratis ${l.prijs.eenheid}` : `${l.prijs.vanaf ? 'vanaf ' : ''}${l.prijs.bedrag} ${l.prijs.eenheid}`;

const kenmerkTekst = (l: Locatie) => {
  const k = l.kenmerken.find(([a, b]) => /min\./.test(a) || /station|winkel/i.test(b)) ?? l.kenmerken[0];
  return k[0] ? `${k[0]} ${k[1]}` : k[1];
};

type Msg = {
  kant: 'in' | 'uit';
  at: number; // frame the message replaces its typing dots
  h: number; // full height
  render: (w: number) => React.ReactNode;
  w: number;
};

const Dots: React.FC<{size: number}> = ({size}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{display: 'flex', gap: size * 0.45, padding: `${size * 0.1}px 0`}}>
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          style={{
            width: size * 0.42,
            height: size * 0.42,
            borderRadius: '50%',
            background: colors.blauw,
            opacity: 0.35 + 0.65 * Math.max(0, Math.sin((frame / 7 - i * 0.9) % (Math.PI * 2))),
          }}
        />
      ))}
    </div>
  );
};

export const ChatSpot: React.FC<{gesprek: Chatgesprek; formaat?: ZoekFormaat}> = ({gesprek: c, formaat = 'staand'}) => {
  const frame = useCurrentFrame();
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: colors.blauw}} />;
  const g = GEO[formaat];
  const t = chatTimeline();
  const l = vind(c.locatie);
  const lineH = g.text * 1.25;

  // Text bubbles are measured so the chat can scroll like a real one.
  const textMsg = (kant: Msg['kant'], at: number, text: string): Msg => {
    // Wrap a little narrower than the bubble and add slack: the measured width can come out a few % under the render.
    const lines = wrap(text, g.text, '400', g.maxW - g.pad * 2 - 48);
    const w = Math.min(g.maxW, Math.max(...lines.map((x) => width(x, g.text, '400'))) * 1.05 + g.pad * 2 + 4);
    const h = lines.length * lineH + g.pad * 1.3;
    return {
      kant,
      at,
      h,
      w,
      render: () => (
        <div style={{fontSize: g.text, lineHeight: `${lineH}px`, padding: `${g.pad * 0.65}px ${g.pad}px`}}>
          {lines.map((x, i) => (
            <div key={i}>{x}</div>
          ))}
        </div>
      ),
    };
  };

  const k = g.card;
  const nameLines = wrap(l.naam, k.name, '700', k.w - g.pad * 2);
  // Two pills side by side when they fit, else the second goes to its own row (and the card grows).
  const pillW = (text: string) => width(text, k.pill, '700') + k.pill * 1.2 + 12;
  const pillRows = pillW(prijsTekst(l)) + pillW(c.kenmerk ?? kenmerkTekst(l)) > k.w - g.pad * 2 ? 2 : 1;
  const cardH = k.photoH + g.pad * 0.8 + k.name * 0.75 + nameLines.length * k.name * 1.12 + pillRows * k.pill * 1.9 + g.pad;
  const pill = (text: string, bg: string, color: string) => (
    <div style={{display: 'inline-block', marginRight: 12, marginTop: 12, padding: `${k.pill * 0.3}px ${k.pill * 0.6}px`, borderRadius: 999, background: bg, color, fontWeight: 700, fontSize: k.pill, whiteSpace: 'nowrap'}}>
      {text}
    </div>
  );
  const cardMsg: Msg = {
    kant: 'uit',
    at: t.kaart,
    h: cardH,
    w: k.w,
    render: () => (
      <div>
        <Img src={staticFile(`locaties/staand/${l.id}.jpg`)} style={{display: 'block', width: k.w, height: k.photoH, objectFit: 'cover'}} />
        <div style={{padding: `${g.pad * 0.8}px ${g.pad}px ${g.pad}px`, color: colors.blauw}}>
          <div style={{fontSize: k.name * 0.7, lineHeight: 1.1}}>Parking</div>
          {nameLines.map((x, i) => (
            <div key={i} style={{fontSize: k.name, fontWeight: 700, lineHeight: 1.12}}>
              {x}
            </div>
          ))}
          <div>
            {pill(prijsTekst(l), colors.aqua, colors.wit)}
            {pill(c.kenmerk ?? kenmerkTekst(l), 'rgba(26,53,128,0.1)', colors.blauw)}
          </div>
        </div>
      </div>
    ),
  };

  const msgs: Msg[] = [textMsg('in', t.vraag, c.vraag), cardMsg, textMsg('uit', t.tip, c.tip), textMsg('in', t.reactie, c.reactie)];
  const dotsH = g.text * 0.42 + g.pad * 1.3 + g.text * 0.2;
  const dotsW = g.text * 2.2 + g.pad * 2;

  // Each slot: typing dots from (at - TYPING), then the message grows in.
  const slots = msgs
    .map((m) => {
      const start = m.at - TYPING;
      if (frame < start) return null;
      const typing = frame < m.at;
      const p = tween(frame, m.at, m.at + POP, ease(0.2, 0.9, 0.3, 1));
      const h = typing ? dotsH * tween(frame, start, start + 10, ease(0.2, 0.9, 0.3, 1)) : dotsH + (m.h - dotsH) * p;
      return {m, typing, p, h};
    })
    .filter((x): x is NonNullable<typeof x> => x !== null);

  // Stack from the bottom of the chat area, newest at the bottom; older messages scroll up and out.
  const out = tween(frame, t.cta - 6, t.cta + 14);
  const area = g.chat;
  const bottom = area.bottom;
  const total = slots.reduce((sum, s) => sum + s.h + g.gap, 0);
  const contentH = area.bottom - area.top;
  // Until the chat is full, messages start at the top like a real chat; after that it scrolls up.
  let y = Math.min(area.top, bottom - total);

  return (
    <AbsoluteFill style={{background: colors.blauw}}>
      <Fonts />
      <div style={{position: 'absolute', top: g.logo.y, width: '100%', display: 'flex', justifyContent: 'center', opacity: 1 - out}}>
        <Img src={staticFile('svg/atom/py-atom-logo-horizontal-white.svg')} style={{width: g.logo.w, display: 'block'}} />
      </div>
      <div
        style={{
          position: 'absolute',
          left: 0,
          top: area.top - 150,
          width: g.w,
          height: contentH + 150,
          overflow: 'hidden',
          opacity: 1 - out,
          transform: `translateY(${-80 * out}px)`,
          // Scrolled-up messages are gone before they reach the logo.
          WebkitMaskImage: 'linear-gradient(180deg, transparent 0, transparent 120px, #000 150px)',
          maskImage: 'linear-gradient(180deg, transparent 0, transparent 120px, #000 150px)',
        }}
      >
        {slots.map((s, i) => {
          const top = y - (area.top - 150);
          y += s.h + g.gap;
          const uit = s.m.kant === 'uit';
          const w = s.typing ? dotsW : dotsW + (s.m.w - dotsW) * s.p;
          const isCard = s.m === cardMsg;
          const r = g.text * 0.75;
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                top,
                left: uit ? undefined : area.left,
                right: uit ? area.right : undefined,
                width: w,
                height: s.h,
                borderRadius: uit ? `${r}px ${r}px ${r * 0.25}px ${r}px` : `${r}px ${r}px ${r}px ${r * 0.25}px`,
                background: uit && !isCard ? colors.aqua : colors.wit,
                color: uit && !isCard ? colors.wit : colors.blauw,
                fontFamily: font,
                overflow: 'hidden',
              }}
            >
              {s.typing ? (
                <div style={{padding: `${g.pad * 0.65}px ${g.pad}px`}}>
                  <Dots size={g.text} />
                </div>
              ) : (
                <div style={{width: s.m.w, opacity: interpolate(s.p, [0.3, 1], [0, 1], clamp)}}>{s.m.render(s.m.w)}</div>
              )}
            </div>
          );
        })}
      </div>
      <EindCta start={t.cta} reserveer={RESERVEERBAAR.has(l.id)} k={CTA_GEO[formaat]} />
    </AbsoluteFill>
  );
};

export const CHAT_SIZE: Record<ZoekFormaat, {width: number; height: number}> = {
  staand: {width: 1080, height: 1920},
  liggend: {width: 1920, height: 1080},
};
