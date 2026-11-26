import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Fonts} from './components';
import {colors, font} from './theme';
import {clamp, ease, tween, useUbuntu, width, wrap} from './LocatieSpot';
import {CTA_GEO, EindCta, type ZoekFormaat} from './ZoekSpot';
import {PrijsRondje} from './LijstSpot';
import {RESERVEERBAAR, locaties, type Locatie} from './locaties';
import type {Bordje} from './borden';

// "Het bordje": a question, then a street sign builds up on two posts: the parking on top (aqua), four places below
// with an arrow and the walking time, each plank flipping down in turn. Then a price circle and the shared end screen.
// 60 fps, 9:16 and 16:9. No box-shadows or blur, render in one tab (see LijstSpot).

type Geo = {
  w: number;
  h: number;
  logo: {y: number; w: number};
  /** Question block: left edge, width and top (staand) or vertical centre (liggend). */
  vraag: {x: number; w: number; size: number; sub: number; top?: number; mid?: number; align: 'center' | 'left'};
  bord: {x: number; w: number; top?: number; header: number; row: number; gap: number; pad: number; naam: number; tijd: number; pijl: number; prijs: number};
  /** Posts reach down to this y. */
  paalEind: number;
};

const GEO: Record<ZoekFormaat, Geo> = {
  staand: {
    w: 1080,
    h: 1920,
    logo: {y: 250, w: 300},
    vraag: {x: 60, w: 960, size: 100, sub: 54, top: 400, align: 'center'},
    bord: {x: 90, w: 900, header: 170, row: 140, gap: 16, pad: 40, naam: 56, tijd: 40, pijl: 88, prijs: 230},
    paalEind: 1920,
  },
  liggend: {
    w: 1920,
    h: 1080,
    logo: {y: 40, w: 250},
    vraag: {x: 120, w: 780, size: 108, sub: 52, mid: 560, align: 'left'},
    bord: {x: 990, w: 820, header: 140, row: 122, gap: 14, pad: 34, naam: 48, tijd: 34, pijl: 74, prijs: 190},
    paalEind: 1080,
  },
};

const PLANK_START = 85;
const PLANK_GAP = 55;

/** Timing for a sign with n planks (3 or 4). */
export const bordTimeline = (n = 4) => {
  const header = 38;
  const planken = Array.from({length: n}, (_, i) => PLANK_START + i * PLANK_GAP);
  const prijs = planken[n - 1] + 70;
  const cta = prijs + 150;
  return {header, planken, prijs, cta, duration: cta + 170};
};

const vind = (slug: string): Locatie => {
  const l = locaties.find((x) => x.slug === slug);
  if (!l) throw new Error(`Onbekende locatie ${slug}`);
  return l;
};

/** Compass bearing to one of 8 arrow angles (up = north). */
const pijlHoek = (graden: number) => (Math.round(graden / 45) % 8) * 45;

/** A plank flips down from its top edge, with a small overshoot. */
const flip = (frame: number, at: number) => {
  const p = tween(frame, at, at + 26, ease(0.3, 1.45, 0.5, 1));
  return {
    opacity: frame < at ? 0 : 1,
    transform: `perspective(1400px) rotateX(${-95 * (1 - p)}deg)`,
    transformOrigin: '50% 0%',
  } as React.CSSProperties;
};

export const BordSpot: React.FC<{bordje: Bordje; formaat?: ZoekFormaat}> = ({bordje: s, formaat = 'staand'}) => {
  const frame = useCurrentFrame();
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: colors.blauw}} />;
  const g = GEO[formaat];
  const b = g.bord;
  const n = s.borden.length;
  const t = bordTimeline(n);
  const l = vind(s.locatie);
  const staand = formaat === 'staand';

  const vraagIn = interpolate(frame, [0, 22], [0.5, 1], {...clamp, easing: ease(0.2, 0.9, 0.3, 1)});
  const subIn = tween(frame, 12, 36, ease(0.2, 0.9, 0.3, 1));
  const paal = tween(frame, 18, 50, ease(0.3, 0, 0.2, 1));
  const out = tween(frame, t.cta - 6, t.cta + 14);

  // A single long word (for example "Heerhugowaard?") makes the question smaller instead of running into the sign.
  const breedsteWoord = Math.max(...s.vraag.split(' ').map((w) => width(w, g.vraag.size, '700')));
  const vraagSize = Math.min(g.vraag.size, (g.vraag.size * g.vraag.w) / breedsteWoord);
  const vraagLines = wrap(s.vraag, vraagSize, '700', g.vraag.w);
  const subLines = wrap(s.sub ?? 'Alles op loopafstand:', g.vraag.sub, '400', g.vraag.w);
  const vraagH = vraagLines.length * vraagSize * 1.1 + 12 + subLines.length * g.vraag.sub * 1.25;
  const vraagTop = g.vraag.top ?? (g.vraag.mid ?? 0) - vraagH / 2;

  // Header: "Parking" plus the name, wrapped next to the P and left of the price circle.
  const pMaat = b.header * 0.56;
  const naamMaat = b.naam * 1.08;
  const naamW = b.w - b.pad * 2 - pMaat - b.pad * 0.6 - b.prijs * 0.62;
  const naamLines = wrap(l.naam, naamMaat, '700', naamW);
  const headerH = Math.max(b.header, b.pad * 1.2 + naamMaat * 0.55 * 1.2 + naamLines.length * naamMaat * 1.08);
  // 9:16: the sign sits under the question and must end above the bottom safe zone (1590), so rows get lower if needed.
  const bordTop0 = staand ? vraagTop + vraagH + 56 : 0;
  const row = staand ? Math.min(b.row, (1585 - bordTop0 - headerH) / n - b.gap) : b.row;
  const bordH = headerH + n * (row + b.gap);
  const bordTop = b.top ?? (staand ? bordTop0 : (g.h - bordH) / 2 + 40);
  const naamMax = b.w - b.pad * 2 - b.pijl - b.pad * 0.7;
  const naamFit = (x: string) => Math.min(b.naam, (b.naam * naamMax) / width(x, b.naam, '700'));

  const paalX = [b.x + b.w * 0.2, b.x + b.w * 0.8];
  const paalW = staand ? 26 : 22;

  return (
    <AbsoluteFill style={{background: colors.blauw, fontFamily: font}}>
      <Fonts />
      <div style={{position: 'absolute', top: g.logo.y, width: '100%', display: 'flex', justifyContent: 'center', opacity: 1 - out}}>
        <Img src={staticFile('svg/atom/py-atom-logo-horizontal-white.svg')} style={{width: g.logo.w, display: 'block'}} />
      </div>

      <AbsoluteFill style={{opacity: 1 - out, transform: `translateY(${-80 * out}px)`}}>
        {/* Question */}
        <div style={{position: 'absolute', left: g.vraag.x, top: vraagTop, width: g.vraag.w, color: colors.wit, textAlign: g.vraag.align}}>
          <div style={{fontSize: vraagSize, fontWeight: 700, lineHeight: 1.1, opacity: vraagIn, transform: `scale(${0.8 + 0.2 * vraagIn})`, transformOrigin: staand ? '50% 50%' : '0% 50%'}}>
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

        {/* Posts, growing up from the bottom */}
        {paalX.map((x, i) => (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x - paalW / 2,
              top: bordTop + 30,
              width: paalW,
              height: g.paalEind - bordTop - 30,
              background: '#C9D1E3',
              borderRadius: `${paalW / 2}px ${paalW / 2}px 0 0`,
              transform: `scaleY(${paal})`,
              transformOrigin: '50% 100%',
            }}
          />
        ))}

        {/* Header plank: the parking */}
        <div
          style={{
            position: 'absolute',
            left: b.x,
            top: bordTop,
            width: b.w,
            height: headerH,
            borderRadius: 26,
            background: colors.aqua,
            color: colors.wit,
            display: 'flex',
            alignItems: 'center',
            gap: b.pad * 0.6,
            padding: `0 ${b.pad}px`,
            boxSizing: 'border-box',
            ...flip(frame, t.header),
          }}
        >
          <div
            style={{
              flex: 'none',
              width: pMaat,
              height: pMaat,
              borderRadius: pMaat * 0.2,
              background: colors.wit,
              color: colors.blauw,
              fontSize: pMaat * 0.78,
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              lineHeight: 1,
            }}
          >
            P
          </div>
          <div style={{lineHeight: 1.08}}>
            <div style={{fontSize: naamMaat * 0.55, lineHeight: 1.2}}>Parking</div>
            {naamLines.map((x, i) => (
              <div key={i} style={{fontSize: naamMaat, fontWeight: 700}}>
                {x}
              </div>
            ))}
          </div>
          <PrijsRondje l={l} d={b.prijs} at={t.prijs} pos={{right: -b.prijs * 0.22, top: (headerH - b.prijs) / 2}} licht />
        </div>

        {/* Destination planks */}
        {s.borden.map((d, i) => {
          const top = bordTop + headerH + b.gap + i * (row + b.gap);
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: b.x,
                top,
                width: b.w,
                height: row,
                borderRadius: 22,
                background: colors.wit,
                color: colors.blauw,
                display: 'flex',
                alignItems: 'center',
                gap: b.pad * 0.7,
                padding: `0 ${b.pad}px`,
                boxSizing: 'border-box',
                ...flip(frame, t.planken[i]),
              }}
            >
              <div
                style={{
                  flex: 'none',
                  width: b.pijl,
                  height: b.pijl,
                  borderRadius: '50%',
                  border: `${b.pijl * 0.07}px solid ${colors.aqua}`,
                  boxSizing: 'border-box',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <Img
                  src={staticFile('svg/atom/py-atom-arrow-up-plain.svg')}
                  style={{width: b.pijl * 0.5, height: b.pijl * 0.5, display: 'block', transform: `rotate(${pijlHoek(d.richting)}deg)`}}
                />
              </div>
              <div style={{lineHeight: 1.1}}>
                <div style={{fontSize: naamFit(d.naar), fontWeight: 700, whiteSpace: 'nowrap'}}>{d.naar}</div>
                <div style={{display: 'flex', alignItems: 'center', gap: b.tijd * 0.3, marginTop: b.tijd * 0.15, fontSize: b.tijd}}>
                  <Img src={staticFile('svg/atom/py-atom-figure-walk.svg')} style={{height: b.tijd * 1.05, display: 'block'}} />
                  <span>{d.tijd}</span>
                </div>
              </div>
            </div>
          );
        })}
      </AbsoluteFill>
      <EindCta start={t.cta} reserveer={RESERVEERBAAR.has(l.id)} k={CTA_GEO[formaat]} />
    </AbsoluteFill>
  );
};

export const BORD_SIZE: Record<ZoekFormaat, {width: number; height: number}> = {
  staand: {width: 1080, height: 1920},
  liggend: {width: 1920, height: 1080},
};
