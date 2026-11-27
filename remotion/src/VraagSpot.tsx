import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import {Fonts} from './components';
import {colors, font} from './theme';
import {ease, tween, useUbuntu, wrap} from './LocatieSpot';
import {CTA_GEO, EindCta, type ZoekFormaat} from './ZoekSpot';
import {RESERVEERBAAR, locaties} from './locaties';
import type {VraagSet} from './vragen';

// "Vraag het maar": the FAQ of the location page as an accordion. Three questions are visible from the first frame; one by
// one a tap opens a question and the answer folds out with the fact big in aqua, the previous one closes. Then the shared
// end screen. 60 fps, 9:16 and 16:9. No box-shadows or blur, render in one tab (see LijstSpot).

type Geo = {
  w: number;
  h: number;
  titel: {x: number; y: number; w: number; size: number; align: 'center' | 'left'};
  lijst: {x: number; y: number; w: number; pad: number; gap: number; q: number; a: number; kern: number; knop: number};
  foto: {x: number; y: number; w: number; h: number};
};

const GEO: Record<ZoekFormaat, Geo> = {
  staand: {
    w: 1080,
    h: 1920,
    titel: {x: 70, y: 270, w: 940, size: 80, align: 'center'},
    lijst: {x: 70, y: 480, w: 940, pad: 38, gap: 22, q: 46, a: 38, kern: 84, knop: 66},
    foto: {x: 70, y: 1190, w: 940, h: 390},
  },
  liggend: {
    w: 1920,
    h: 1080,
    titel: {x: 100, y: 150, w: 660, size: 84, align: 'left'},
    lijst: {x: 860, y: 110, w: 960, pad: 32, gap: 20, q: 40, a: 34, kern: 72, knop: 58},
    foto: {x: 100, y: 470, w: 660, h: 440},
  },
};

const OPEN = [80, 300, 520];
export const vraagTimeline = () => ({open: OPEN, cta: 760, duration: 930});

export const VraagSpot: React.FC<{set: VraagSet; formaat?: ZoekFormaat}> = ({set, formaat = 'staand'}) => {
  const frame = useCurrentFrame();
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: colors.blauw}} />;
  const g = GEO[formaat];
  const L = g.lijst;
  const t = vraagTimeline();
  const l = locaties.find((x) => x.slug === set.locatie);
  if (!l) throw new Error(`Onbekende locatie ${set.locatie}`);
  const zacht = ease(0.65, 0, 0.35, 1);
  const tekstW = L.w - 2 * L.pad - L.knop - 24;

  // Accordion: item i opens at OPEN[i] and closes when the next one opens (the last stays open).
  const rijen = set.vragen.map((v, i) => {
    const open = tween(frame, OPEN[i], OPEN[i] + 30, zacht) * (i < 2 ? 1 - tween(frame, OPEN[i + 1], OPEN[i + 1] + 30, zacht) : 1);
    const qLines = wrap(v.vraag, L.q, '700', tekstW);
    const kernLines = wrap(v.kern, L.kern, '700', L.w - 2 * L.pad);
    const aLines = wrap(v.antwoord, L.a, '400', L.w - 2 * L.pad);
    const dicht = 2 * L.pad + qLines.length * L.q * 1.18;
    const extra = 26 + kernLines.length * L.kern * 1.08 + 8 + aLines.length * L.a * 1.3;
    return {v, i, open, qLines, kernLines, aLines, dicht, extra, hoogte: dicht + extra * open};
  });
  let y = L.y;
  const posities = rijen.map((r) => {
    const top = y;
    y += r.hoogte + L.gap;
    return top;
  });

  const T = g.titel;
  const binnen = (i: number) => 0.5 + 0.5 * tween(frame, i * 6, i * 6 + 24, ease(0.2, 0.9, 0.3, 1));

  return (
    <AbsoluteFill style={{background: colors.blauw, fontFamily: font, overflow: 'hidden'}}>
      <Fonts />
      <div style={{position: 'absolute', left: T.x, top: T.y, width: T.w, textAlign: T.align, color: colors.wit, opacity: binnen(0)}}>
        <div style={{fontSize: T.size, fontWeight: 700, lineHeight: 1.05}}>Vraag het maar</div>
        <div style={{fontSize: T.size * 0.5, marginTop: 14, lineHeight: 1.25}}>
          <span style={{fontWeight: 300}}>Parking </span>
          <span style={{fontWeight: 700}}>{l.naam}</span>
          <span style={{fontWeight: 300}}>, {l.stad}</span>
        </div>
      </div>

      <div style={{position: 'absolute', left: g.foto.x, top: g.foto.y, width: g.foto.w, height: g.foto.h, borderRadius: 32, overflow: 'hidden', border: `5px solid ${colors.wit}`, boxSizing: 'border-box', opacity: binnen(4)}}>
        <Img src={staticFile(l.foto)} decoding="sync" style={{width: '100%', height: '100%', objectFit: 'cover', display: 'block'}} />
      </div>

      {rijen.map((r, n) => {
        const tik = frame - OPEN[r.i];
        const ring = tik > -4 && tik < 26 ? tween(frame, OPEN[r.i] - 4, OPEN[r.i] + 26) : -1;
        const druk = 1 - 0.025 * (tik > -8 && tik < 10 ? Math.sin(((tik + 8) / 18) * Math.PI) : 0);
        const inhoud = tween(frame, OPEN[r.i] + 12, OPEN[r.i] + 34) * (r.open > 0.6 ? 1 : r.open / 0.6);
        return (
          <div
            key={r.i}
            style={{
              position: 'absolute',
              left: L.x,
              top: posities[n],
              width: L.w,
              height: r.hoogte,
              borderRadius: 30,
              background: colors.wit,
              overflow: 'hidden',
              transform: `scale(${druk})`,
              opacity: binnen(n + 1),
            }}
          >
            <div style={{position: 'absolute', left: L.pad, top: L.pad, width: tekstW, color: colors.blauw, fontSize: L.q, fontWeight: 700, lineHeight: 1.18}}>
              {r.qLines.map((x, i) => (
                <div key={i}>{x}</div>
              ))}
            </div>
            {/* Plus that turns into a minus */}
            <div style={{position: 'absolute', right: L.pad, top: (r.dicht - L.knop) / 2, width: L.knop, height: L.knop}}>
              {ring >= 0 ? (
                <div style={{position: 'absolute', left: L.knop / 2 - (L.knop / 2) * (1 + ring), top: L.knop / 2 - (L.knop / 2) * (1 + ring), width: L.knop * (1 + ring), height: L.knop * (1 + ring), borderRadius: '50%', border: `4px solid ${colors.aqua}`, boxSizing: 'border-box', opacity: 1 - ring}} />
              ) : null}
              <div style={{position: 'absolute', inset: 0, borderRadius: '50%', background: r.open > 0.5 ? colors.aqua : colors.blauw}} />
              <div style={{position: 'absolute', left: L.knop * 0.27, top: L.knop / 2 - 3.5, width: L.knop * 0.46, height: 7, borderRadius: 4, background: colors.wit}} />
              <div style={{position: 'absolute', left: L.knop / 2 - 3.5, top: L.knop * 0.27, width: 7, height: L.knop * 0.46, borderRadius: 4, background: colors.wit, transform: `rotate(${90 * r.open}deg) scaleY(${1 - r.open})`}} />
            </div>
            <div style={{position: 'absolute', left: L.pad, right: L.pad, top: r.dicht - 6, height: 3, borderRadius: 2, background: colors.aqua, opacity: 0.35 * inhoud}} />
            <div style={{position: 'absolute', left: L.pad, width: L.w - 2 * L.pad, top: r.dicht + 20, opacity: inhoud, transform: `translateY(${(1 - inhoud) * 16}px)`}}>
              <div style={{color: colors.aqua, fontSize: L.kern, fontWeight: 700, lineHeight: 1.08}}>
                {r.kernLines.map((x, i) => (
                  <div key={i}>{x}</div>
                ))}
              </div>
              <div style={{marginTop: 8, color: colors.blauw, fontSize: L.a, fontWeight: 400, lineHeight: 1.3}}>
                {r.aLines.map((x, i) => (
                  <div key={i}>{x}</div>
                ))}
              </div>
            </div>
          </div>
        );
      })}

      <AbsoluteFill style={{background: colors.blauw, opacity: 0.92 * tween(frame, t.cta - 10, t.cta + 16)}} />
      <EindCta start={t.cta} reserveer={RESERVEERBAAR.has(l.id)} k={CTA_GEO[formaat]} />
    </AbsoluteFill>
  );
};

export const VRAAG_SIZE: Record<ZoekFormaat, {width: number; height: number}> = {
  staand: {width: 1080, height: 1920},
  liggend: {width: 1920, height: 1080},
};
