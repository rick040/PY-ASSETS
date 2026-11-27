import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Fonts} from './components';
import {colors, font} from './theme';
import {clamp, ease, tween, useUbuntu, width, wrap} from './LocatieSpot';
import {CTA_GEO, EindCta, type ZoekFormaat} from './ZoekSpot';
import {RESERVEERBAAR, locaties, type Locatie} from './locaties';
import type {Vroegboek} from './vroegboeken';

// "Vroeg boeken loont": a question, three parking tickets with the day rates (without booking, with booking, booked early)
// drop in, the first two are struck through, the early one wins with the saving, then the shared end screen.
// 60 fps, 9:16 and 16:9. No box-shadows or blur, render in one tab (see LijstSpot).

type Geo = {
  w: number;
  h: number;
  logo: {y: number; w: number};
  vraag: {x: number; y: number; w: number; size: number; sub: number; align: 'center' | 'left'};
  ticket: {x: number; y: number; w: number; h: number; gap: number; label: number; prijs: number};
  /** The closing line: under the tickets (staand) or under the question (liggend). */
  slot: {x: number; y: number | null; w: number; size: number; align: 'center' | 'left'};
};

const GEO: Record<ZoekFormaat, Geo> = {
  staand: {
    w: 1080,
    h: 1920,
    logo: {y: 250, w: 300},
    vraag: {x: 60, y: 370, w: 960, size: 86, sub: 42, align: 'center'},
    ticket: {x: 110, y: 600, w: 860, h: 200, gap: 40, label: 40, prijs: 104},
    slot: {x: 80, y: 1410, w: 920, size: 58, align: 'center'},
  },
  liggend: {
    w: 1920,
    h: 1080,
    logo: {y: 40, w: 250},
    vraag: {x: 110, y: 210, w: 740, size: 84, sub: 40, align: 'left'},
    ticket: {x: 940, y: 190, w: 860, h: 196, gap: 44, label: 38, prijs: 100},
    slot: {x: 110, y: null, w: 740, size: 54, align: 'left'},
  },
};

export const vroegTimeline = () => {
  const tickets = [40, 78, 116];
  const streep = [176, 204];
  const winnaar = 236;
  const slot = 290;
  const cta = 440;
  return {tickets, streep, winnaar, slot, cta, duration: cta + 170};
};

const vind = (slug: string): Locatie => {
  const l = locaties.find((x) => x.slug === slug);
  if (!l) throw new Error(`Onbekende locatie ${slug}`);
  return l;
};

const euro = (n: number) => (Number.isInteger(n) ? `€${n}` : `€${n.toFixed(2).replace('.', ',')}`);

const Ticket: React.FC<{
  g: Geo;
  i: number;
  label: string;
  bedrag: number;
  besparing?: number;
  top: number;
}> = ({g, i, label, bedrag, besparing, top}) => {
  const frame = useCurrentFrame();
  const t = vroegTimeline();
  const k = g.ticket;
  const at = t.tickets[i];
  const inv = tween(frame, at, at + 26, ease(0.3, 1.35, 0.5, 1));
  const streep = i < 2 ? tween(frame, t.streep[i], t.streep[i] + 16, ease(0.4, 0, 0.2, 1)) : 0;
  const win = i === 2 ? tween(frame, t.winnaar, t.winnaar + 24, ease(0.3, 1.5, 0.5, 1)) : 0;
  const badge = i === 2 ? tween(frame, t.winnaar + 18, t.winnaar + 40, ease(0.3, 1.6, 0.5, 1)) : 0;
  const stub = k.h * 0.82;
  const prijsW = width(euro(bedrag), k.prijs, '700');
  if (frame < at) return null;
  return (
    <div
      style={{
        position: 'absolute',
        left: k.x,
        top: top + i * (k.h + k.gap),
        width: k.w,
        height: k.h,
        opacity: Math.min(1, inv * 1.5) * (1 - 0.45 * streep),
        transform: `translateY(${(1 - inv) * -70}px) rotate(${(1 - inv) * (i % 2 ? 4 : -4)}deg) scale(${1 + 0.05 * win})`,
      }}
    >
      <div
        style={{
          position: 'absolute',
          inset: 0,
          borderRadius: 30,
          background: colors.wit,
          border: `${8 * win}px solid ${colors.aqua}`,
          boxSizing: 'border-box',
          display: 'flex',
          alignItems: 'center',
          color: colors.blauw,
          overflow: 'hidden',
        }}
      >
        {/* Stub with the P, perforation to the body */}
        <div style={{width: stub, height: '100%', flex: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRight: `5px dashed rgba(26,53,128,0.22)`, boxSizing: 'border-box'}}>
          <div style={{width: stub * 0.52, height: stub * 0.52, borderRadius: stub * 0.12, background: win > 0.5 ? colors.aqua : colors.blauw, color: colors.wit, fontSize: stub * 0.36, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>P</div>
        </div>
        <div style={{paddingLeft: 40, lineHeight: 1.05}}>
          <div style={{fontSize: k.label, opacity: 0.75}}>{label}</div>
          <div style={{position: 'relative', display: 'inline-block', fontSize: k.prijs, fontWeight: 700}}>
            {euro(bedrag)}
            {streep > 0 ? <div style={{position: 'absolute', left: -8, top: '54%', height: 10, width: (prijsW + 16) * streep, borderRadius: 5, background: colors.blauw, transform: 'rotate(-8deg)', transformOrigin: '0 50%'}} /> : null}
          </div>
        </div>
      </div>
      {/* Notches in the perforation (background colour circles) */}
      {[-1, 1].map((s) => (
        <div key={s} style={{position: 'absolute', left: stub - 20, top: s < 0 ? -20 : k.h - 20, width: 40, height: 40, borderRadius: '50%', background: colors.blauw}} />
      ))}
      {besparing && badge > 0 ? (
        <div
          style={{
            position: 'absolute',
            right: 22,
            top: -k.h * 0.52,
            transform: `scale(${badge}) rotate(${-6 * badge}deg)`,
            padding: `${k.label * 0.42}px ${k.label * 0.8}px`,
            borderRadius: 999,
            background: colors.aqua,
            color: colors.wit,
            fontSize: k.label * 0.95,
            fontWeight: 700,
            lineHeight: 1.05,
            textAlign: 'center',
          }}
        >
          Je bespaart
          <br />
          <span style={{fontSize: k.label * 1.4}}>{euro(besparing)}</span>
        </div>
      ) : null}
    </div>
  );
};

export const VroegSpot: React.FC<{vroeg: Vroegboek; formaat?: ZoekFormaat}> = ({vroeg: v, formaat = 'staand'}) => {
  const frame = useCurrentFrame();
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: colors.blauw}} />;
  const g = GEO[formaat];
  const t = vroegTimeline();
  const l = vind(v.locatie);
  const staand = formaat === 'staand';

  const vraagIn = interpolate(frame, [0, 22], [0.5, 1], {...clamp, easing: ease(0.2, 0.9, 0.3, 1)});
  const subIn = tween(frame, 12, 36, ease(0.2, 0.9, 0.3, 1));
  const slotIn = tween(frame, t.slot, t.slot + 26, ease(0.2, 0.9, 0.3, 1));
  const out = tween(frame, t.cta - 6, t.cta + 14);

  const vraagLines = wrap(v.vraag, g.vraag.size, '700', g.vraag.w);
  const subLines = wrap(`Parking ${l.naam} · ${v.wat}`, g.vraag.sub, '400', g.vraag.w);
  const vraagH = vraagLines.length * g.vraag.size * 1.1 + 12 + subLines.length * g.vraag.sub * 1.25;
  const vroeg = v.tarieven[2].bedrag;
  const besparing = Math.round((v.tarieven[0].bedrag - vroeg) * 100) / 100;
  const slotTekst = `Boek ruim vooraf en betaal ${euro(vroeg)}.`;
  const slotLines = wrap(slotTekst, g.slot.size, '700', g.slot.w);
  const slotY = g.slot.y ?? g.vraag.y + vraagH + 60;
  // 9:16: the tickets sit under the question, with room for the badge on the last one.
  const ticketY = staand ? Math.max(g.ticket.y, g.vraag.y + vraagH + 50) : g.ticket.y;
  const slotYStaand = ticketY + 3 * g.ticket.h + 2 * g.ticket.gap + 60;

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
          <div style={{fontSize: g.vraag.sub, lineHeight: 1.25, marginTop: 12, opacity: subIn, transform: `translateY(${(1 - subIn) * 30}px)`}}>
            {subLines.map((x, i) => (
              <div key={i}>{x}</div>
            ))}
          </div>
        </div>
        {v.tarieven.map((tr, i) => (
          <Ticket key={i} g={g} i={i} label={tr.label} bedrag={tr.bedrag} besparing={i === 2 ? besparing : undefined} top={ticketY} />
        ))}
        <div style={{position: 'absolute', left: g.slot.x, top: staand ? slotYStaand : slotY, width: g.slot.w, textAlign: g.slot.align, color: colors.wit, fontSize: g.slot.size, fontWeight: 700, lineHeight: 1.12, opacity: slotIn, transform: `translateY(${(1 - slotIn) * 40}px)`}}>
          {slotLines.map((x, i) => (
            <div key={i}>{x}</div>
          ))}
        </div>
      </AbsoluteFill>
      <EindCta start={t.cta} reserveer={RESERVEERBAAR.has(l.id)} k={CTA_GEO[formaat]} />
    </AbsoluteFill>
  );
};

export const VROEG_SIZE: Record<ZoekFormaat, {width: number; height: number}> = {
  staand: {width: 1080, height: 1920},
  liggend: {width: 1920, height: 1080},
};
