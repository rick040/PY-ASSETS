import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Fonts} from './components';
import {colors, font} from './theme';
import {clamp, ease, tween, useUbuntu, width, wrap} from './LocatieSpot';
import {CTA_GEO, EindCta, type ZoekFormaat} from './ZoekSpot';
import {locaties, type Locatie} from './locaties';
import type {Strippenkaart} from './strippenkaarten';

// "De strippenkaart": a question, a ParkingPass with 25 strips that get punched one by one while a day counter runs,
// then the price per day next to a loose day ticket (struck through) and the total saving; end screen "Bestel je ParkingPass".
// 60 fps, 9:16 and 16:9. No box-shadows or blur, render in one tab (see LijstSpot).

type Geo = {
  w: number;
  h: number;
  logo: {y: number; w: number};
  vraag: {x: number; y: number; w: number; size: number; sub: number; align: 'center' | 'left'};
  kaart: {x: number; y: number | null; w: number; strip: [number, number]; gap: number; pad: number; kop: number};
  prijs: {x: number; y: number | null; w: number; groot: number; tekst: number; align: 'center' | 'left'};
};

const GEO: Record<ZoekFormaat, Geo> = {
  staand: {
    w: 1080,
    h: 1920,
    logo: {y: 250, w: 300},
    vraag: {x: 60, y: 360, w: 960, size: 86, sub: 40, align: 'center'},
    kaart: {x: 70, y: null, w: 940, strip: [150, 66], gap: 16, pad: 44, kop: 48},
    prijs: {x: 60, y: null, w: 960, groot: 120, tekst: 44, align: 'center'},
  },
  liggend: {
    w: 1920,
    h: 1080,
    logo: {y: 40, w: 250},
    vraag: {x: 110, y: 170, w: 760, size: 80, sub: 38, align: 'left'},
    kaart: {x: 960, y: 190, w: 850, strip: [134, 58], gap: 14, pad: 38, kop: 42},
    prijs: {x: 110, y: null, w: 760, groot: 104, tekst: 40, align: 'left'},
  },
};

const STRIPS = 25;

export const stripTimeline = () => {
  const punch = Array.from({length: STRIPS}, (_, i) => 70 + i * 6);
  const prijs = punch[STRIPS - 1] + 26;
  const streep = prijs + 46;
  const badge = streep + 26;
  const cta = badge + 130;
  return {punch, prijs, streep, badge, cta, duration: cta + 170};
};

const vind = (slug: string): Locatie => {
  const l = locaties.find((x) => x.slug === slug);
  if (!l) throw new Error(`Onbekende locatie ${slug}`);
  return l;
};

const euro = (n: number) => (Number.isInteger(n) ? `€${n.toLocaleString('nl-NL')}` : `€${n.toFixed(2).replace('.', ',')}`);

export const StripSpot: React.FC<{strip: Strippenkaart; formaat?: ZoekFormaat}> = ({strip: s, formaat = 'staand'}) => {
  const frame = useCurrentFrame();
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: colors.blauw}} />;
  const g = GEO[formaat];
  const k = g.kaart;
  const p = g.prijs;
  const t = stripTimeline();
  const l = vind(s.locatie);
  const staand = formaat === 'staand';

  const vraagIn = interpolate(frame, [0, 22], [0.5, 1], {...clamp, easing: ease(0.2, 0.9, 0.3, 1)});
  const subIn = tween(frame, 12, 36, ease(0.2, 0.9, 0.3, 1));
  const kaartIn = tween(frame, 26, 58, ease(0.2, 0.9, 0.3, 1));
  const out = tween(frame, t.cta - 6, t.cta + 14);
  const geknipt = t.punch.filter((at) => frame >= at).length;
  const tel = frame >= t.punch[0] ? geknipt : 0;

  const vraagLines = wrap(s.vraag, g.vraag.size, '700', g.vraag.w);
  const subLines = wrap(`Parking ${l.naam} · 1 strip is 1 dag`, g.vraag.sub, '400', g.vraag.w);
  const vraagH = vraagLines.length * g.vraag.size * 1.1 + 12 + subLines.length * g.vraag.sub * 1.25;

  const kop = k.kop * 2.3;
  const gridH = 5 * k.strip[1] + 4 * k.gap;
  const kaartH = k.pad + kop + gridH + k.pad;
  const kaartY = k.y ?? g.vraag.y + vraagH + 44;
  const prijsY = p.y ?? (staand ? kaartY + kaartH + 44 : g.vraag.y + vraagH + 50);

  const perDag = s.vijfentwintig / STRIPS;
  const besparing = Math.round((STRIPS * s.dag - s.vijfentwintig) * 100) / 100;
  const r1 = tween(frame, t.prijs, t.prijs + 22, ease(0.2, 0.9, 0.3, 1));
  const r2 = tween(frame, t.prijs + 10, t.prijs + 34, ease(0.3, 1.4, 0.5, 1));
  const r3 = tween(frame, t.prijs + 24, t.prijs + 46, ease(0.2, 0.9, 0.3, 1));
  const streep = tween(frame, t.streep, t.streep + 16, ease(0.4, 0, 0.2, 1));
  const badge = tween(frame, t.badge, t.badge + 22, ease(0.3, 1.6, 0.5, 1));
  const dagTekst = euro(s.dag);
  const dagW = width(dagTekst, p.tekst, '700');
  const rij = (v: number): React.CSSProperties => ({opacity: v, transform: `translateY(${(1 - v) * 30}px)`});

  return (
    <AbsoluteFill style={{background: colors.blauw, fontFamily: font}}>
      <Fonts />
      <div style={{position: 'absolute', top: g.logo.y, width: '100%', display: 'flex', justifyContent: 'center', opacity: 1 - out}}>
        <Img src={staticFile('svg/atom/py-atom-logo-horizontal-white.svg')} style={{width: g.logo.w, display: 'block'}} />
      </div>
      <AbsoluteFill style={{opacity: 1 - out, transform: `translateY(${-80 * out}px)`}}>
        {/* Question */}
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

        {/* The ParkingPass */}
        <div
          style={{
            position: 'absolute',
            left: k.x,
            top: kaartY,
            width: k.w,
            height: kaartH,
            borderRadius: 34,
            background: colors.wit,
            color: colors.blauw,
            opacity: kaartIn,
            transform: `translateY(${(1 - kaartIn) * 80}px) rotate(${(1 - kaartIn) * -3}deg)`,
          }}
        >
          <div style={{position: 'absolute', left: k.pad, top: k.pad, right: k.pad, height: kop, display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
            <div style={{display: 'flex', alignItems: 'center', gap: 18}}>
              <div style={{width: kop * 0.8, height: kop * 0.8, borderRadius: kop * 0.18, background: colors.blauw, color: colors.wit, fontSize: kop * 0.56, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>P</div>
              <div style={{lineHeight: 1.1}}>
                <div style={{fontSize: k.kop, fontWeight: 700}}>ParkingPass</div>
                <div style={{fontSize: k.kop * 0.62, opacity: 0.75}}>Parking {l.naam}</div>
              </div>
            </div>
            <div style={{textAlign: 'right', lineHeight: 1}}>
              <div style={{fontSize: k.kop * 0.6, opacity: 0.75}}>dag</div>
              <div style={{fontSize: k.kop * 1.5, fontWeight: 700, color: colors.aqua, fontVariantNumeric: 'tabular-nums'}}>
                {tel}
                <span style={{fontSize: k.kop * 0.6, color: colors.blauw, fontWeight: 400}}> / {STRIPS}</span>
              </div>
            </div>
          </div>
          {/* 25 strips: each one is punched (aqua, with a hole) on its day */}
          <div style={{position: 'absolute', left: k.pad, right: k.pad, top: k.pad + kop + k.pad * 0.6, display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: k.gap}}>
            {t.punch.map((at, i) => {
              const v = tween(frame, at, at + 10, ease(0.3, 1.6, 0.5, 1));
              const aan = frame >= at;
              return (
                <div
                  key={i}
                  style={{
                    position: 'relative',
                    height: k.strip[1],
                    borderRadius: 14,
                    background: aan ? colors.aqua : '#E8EDF7',
                    color: aan ? colors.wit : colors.blauw,
                    display: 'flex',
                    alignItems: 'center',
                    paddingLeft: 16,
                    fontSize: k.strip[1] * 0.42,
                    fontWeight: 700,
                    transform: `scale(${aan ? 1 + 0.12 * (1 - Math.abs(2 * v - 1)) : 1})`,
                  }}
                >
                  {i + 1}
                  {aan ? (
                    <div style={{position: 'absolute', right: 14, top: '50%', width: k.strip[1] * 0.5 * v, height: k.strip[1] * 0.5 * v, marginTop: -k.strip[1] * 0.25 * v, borderRadius: '50%', background: colors.blauw}} />
                  ) : null}
                </div>
              );
            })}
          </div>
        </div>

        {/* Price per day, the loose day ticket struck through, the saving */}
        <div style={{position: 'absolute', left: p.x, top: prijsY, width: p.w, color: colors.wit, textAlign: p.align}}>
          <div style={{fontSize: p.tekst, ...rij(r1)}}>
            {STRIPS} dagen voor <b>{euro(s.vijfentwintig)}</b>
          </div>
          <div style={{fontSize: p.groot, fontWeight: 700, lineHeight: 1.05, color: colors.aqua, ...rij(r2), transform: `scale(${0.7 + 0.3 * r2})`, transformOrigin: staand ? '50% 50%' : '0% 50%'}}>
            {euro(perDag)} <span style={{fontSize: p.groot * 0.45, color: colors.wit}}>per dag</span>
          </div>
          <div style={{fontSize: p.tekst * 0.9, marginTop: 6, ...rij(r3)}}>
            {s.dagLabel ?? 'Losse dagkaart'}{' '}
            <span style={{position: 'relative', fontWeight: 700}}>
              {dagTekst}
              {streep > 0 ? <span style={{position: 'absolute', left: -6, top: '52%', height: 6, width: (dagW * 0.9 + 12) * streep, borderRadius: 3, background: colors.aqua, transform: 'rotate(-8deg)', transformOrigin: '0 50%'}} /> : null}
            </span>
          </div>
          {badge > 0 ? (
            <div style={{display: 'inline-block', marginTop: 22, padding: `${p.tekst * 0.36}px ${p.tekst * 0.8}px`, borderRadius: 999, background: colors.wit, color: colors.blauw, fontSize: p.tekst * 0.95, fontWeight: 700, transform: `scale(${badge})`}}>
              Je bespaart {euro(besparing)} op {STRIPS} dagen
            </div>
          ) : null}
        </div>
      </AbsoluteFill>
      <EindCta start={t.cta} reserveer k={CTA_GEO[formaat]} titel="Bestel je ParkingPass" sub="en parkeer voordeliger, dag na dag" />
    </AbsoluteFill>
  );
};

export const STRIP_SIZE: Record<ZoekFormaat, {width: number; height: number}> = {
  staand: {width: 1080, height: 1920},
  liggend: {width: 1920, height: 1080},
};
