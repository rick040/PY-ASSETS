import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Fonts} from './components';
import {colors, font} from './theme';
import {clamp, ease, tween, useUbuntu, wrap} from './LocatieSpot';
import {CTA_GEO, EindCta, type ZoekFormaat} from './ZoekSpot';
import {RESERVEERBAAR, locaties, type Locatie} from './locaties';
import type {Kaartje} from './kaartjes';

// "Het kaartje": a question, a drawn map with a pin on a well-known place, our parkings drop in around it with a dotted
// line and the walking time, then a row per parking with its price (nearest marked) and the shared end screen.
// 60 fps, 9:16 and 16:9. No box-shadows or blur, render in one tab (see LijstSpot).

type Geo = {
  w: number;
  h: number;
  logo: {y: number; w: number};
  vraag: {x: number; y: number; w: number; size: number; sub: number; align: 'center' | 'left'};
  /** Map card; y is the top (staand: placed under the question when null). */
  kaart: {x: number; y: number | null; w: number; h: number};
  /** Rows with the parkings and prices; y null = under the map. */
  rij: {x: number; y: number | null; w: number; h: number; gap: number; naam: number};
  marker: number;
  pin: number;
  label: number;
};

const GEO: Record<ZoekFormaat, Geo> = {
  staand: {
    w: 1080,
    h: 1920,
    logo: {y: 250, w: 300},
    vraag: {x: 60, y: 390, w: 960, size: 92, sub: 50, align: 'center'},
    kaart: {x: 60, y: null, w: 960, h: 570},
    rij: {x: 60, y: null, w: 960, h: 86, gap: 10, naam: 42},
    marker: 70,
    pin: 74,
    label: 34,
  },
  liggend: {
    w: 1920,
    h: 1080,
    logo: {y: 40, w: 250},
    vraag: {x: 110, y: 200, w: 760, size: 88, sub: 46, align: 'left'},
    kaart: {x: 960, y: 150, w: 850, h: 860},
    rij: {x: 110, y: null, w: 760, h: 100, gap: 14, naam: 42},
    marker: 74,
    pin: 80,
    label: 34,
  },
};

const MARKER_START = 80;
const MARKER_GAP = 55;

export const kaartTimeline = (n = 3) => {
  const markers = Array.from({length: n}, (_, i) => MARKER_START + i * MARKER_GAP);
  const rijen = Array.from({length: n}, (_, i) => markers[n - 1] + 60 + i * 22);
  const dichtst = rijen[n - 1] + 40;
  const cta = dichtst + 120;
  return {markers, rijen, dichtst, cta, duration: cta + 170};
};

const vind = (slug: string): Locatie => {
  const l = locaties.find((x) => x.slug === slug);
  if (!l) throw new Error(`Onbekende locatie ${slug}`);
  return l;
};

const pop = (frame: number, at: number, len = 18) => tween(frame, at, at + len, ease(0.3, 1.5, 0.5, 1));

/** Decorative streets: a slightly turned grid with a few wide roads, the same on every map. */
const Straten: React.FC<{w: number; h: number}> = ({w, h}) => {
  const lijnen: React.ReactNode[] = [];
  const stap = 150;
  for (let i = -6; i <= 12; i++) {
    const breed = i % 3 === 0;
    lijnen.push(<line key={`a${i}`} x1={-200 + i * stap} y1={-200} x2={-200 + i * stap + 260} y2={h + 200} stroke="#FFFFFF" strokeWidth={breed ? 18 : 9} />);
    lijnen.push(<line key={`b${i}`} x1={-200} y1={-120 + i * stap} x2={w + 200} y2={-120 + i * stap - 200} stroke="#FFFFFF" strokeWidth={breed ? 18 : 9} />);
  }
  return (
    <svg width={w} height={h} style={{position: 'absolute', left: 0, top: 0}}>
      <rect width={w} height={h} fill="#E4E9F4" />
      {/* a park block for some colour */}
      <rect x={w * 0.62} y={h * 0.12} width={w * 0.2} height={h * 0.16} rx={24} fill="#D3EFE3" transform={`rotate(-8 ${w * 0.72} ${h * 0.2})`} />
      {lijnen}
    </svg>
  );
};

const prijsDelen = (l: Locatie) =>
  l.prijs.bedrag === 'Gratis' ? {groot: 'Gratis', klein: l.prijs.eenheid} : {groot: `${l.prijs.vanaf ? 'vanaf ' : ''}${l.prijs.bedrag}`, klein: l.prijs.eenheid};

export const KaartSpot: React.FC<{kaartje: Kaartje; formaat?: ZoekFormaat}> = ({kaartje: k, formaat = 'staand'}) => {
  const frame = useCurrentFrame();
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: colors.blauw}} />;
  const g = GEO[formaat];
  const staand = formaat === 'staand';
  const n = k.parkings.length;
  const t = kaartTimeline(n);
  const ps = k.parkings.map((p) => ({...p, l: vind(p.locatie)}));

  const vraagIn = interpolate(frame, [0, 22], [0.5, 1], {...clamp, easing: ease(0.2, 0.9, 0.3, 1)});
  const subIn = tween(frame, 12, 36, ease(0.2, 0.9, 0.3, 1));
  const kaartIn = tween(frame, 20, 50, ease(0.2, 0.9, 0.3, 1));
  const pinIn = pop(frame, 44, 20);
  const out = tween(frame, t.cta - 6, t.cta + 14);

  const vraagLines = wrap(k.vraag, g.vraag.size, '700', g.vraag.w);
  const subLines = wrap(k.sub ?? 'Parkeer op loopafstand:', g.vraag.sub, '400', g.vraag.w);
  const vraagH = vraagLines.length * g.vraag.size * 1.1 + 10 + subLines.length * g.vraag.sub * 1.25;

  const kaartY = g.kaart.y ?? g.vraag.y + vraagH + 40;
  const rijY = g.rij.y ?? (staand ? kaartY + g.kaart.h + 24 : g.vraag.y + vraagH + 50);
  const W = g.kaart.w;
  const H = g.kaart.h;

  // Map scale: the pin and all parkings together fill the card, with room for the labels (pin label above,
  // parking labels below). Same scale in both directions, so the directions stay true.
  const padX = 190;
  const padTop = 150;
  const padBot = 110;
  const xs = [0, ...ps.map((p) => p.dx)];
  const ys = [0, ...ps.map((p) => p.dy)];
  const [minX, maxX, minY, maxY] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
  const s = Math.min((W - 2 * padX) / Math.max(1, maxX - minX), (H - padTop - padBot) / Math.max(1, maxY - minY), 1.2);
  const offX = (W - (maxX - minX) * s) / 2;
  const offY = padTop + (H - padTop - padBot - (maxY - minY) * s) / 2;
  const toX = (dx: number) => offX + (dx - minX) * s;
  const toY = (dy: number) => offY + (maxY - dy) * s;
  const cx = toX(0);
  const cy = toY(0);
  const pos = ps.map((p) => ({x: toX(p.dx), y: toY(p.dy)}));
  const dichtstIn = tween(frame, t.dichtst, t.dichtst + 16);

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
          <div style={{fontSize: g.vraag.sub, lineHeight: 1.25, marginTop: 10, opacity: subIn, transform: `translateY(${(1 - subIn) * 30}px)`}}>
            {subLines.map((x, i) => (
              <div key={i}>{x}</div>
            ))}
          </div>
        </div>

        {/* Map */}
        <div
          style={{
            position: 'absolute',
            left: g.kaart.x,
            top: kaartY,
            width: W,
            height: H,
            borderRadius: 40,
            overflow: 'hidden',
            opacity: kaartIn,
            transform: `scale(${0.92 + 0.08 * kaartIn})`,
          }}
        >
          <Straten w={W} h={H} />
          {/* Dotted walking lines, drawn from the pin to each parking */}
          <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
            {pos.map((q, i) => {
              const d = tween(frame, t.markers[i] + 8, t.markers[i] + 30, ease(0.3, 0, 0.2, 1));
              if (d <= 0) return null;
              return (
                <line
                  key={i}
                  x1={cx}
                  y1={cy}
                  x2={cx + (q.x - cx) * d}
                  y2={cy + (q.y - cy) * d}
                  stroke={colors.blauw}
                  strokeWidth={9}
                  strokeLinecap="round"
                  strokeDasharray="0.1 20"
                />
              );
            })}
          </svg>

          {/* Parking markers with their name */}
          {pos.map((q, i) => {
            const v = pop(frame, t.markers[i]);
            if (frame < t.markers[i]) return null;
            const m = g.marker;
            const onder = q.y < H - m - 60;
            return (
              <div key={`m${i}`} style={{position: 'absolute', left: q.x, top: q.y, transform: `translate(-50%, -50%) scale(${v})`}}>
                <div
                  style={{
                    width: m,
                    height: m,
                    borderRadius: m * 0.22,
                    background: colors.blauw,
                    border: `5px solid ${colors.wit}`,
                    boxSizing: 'border-box',
                    color: colors.wit,
                    fontSize: m * 0.62,
                    fontWeight: 700,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    lineHeight: 1,
                  }}
                >
                  P
                </div>
                <div
                  style={{
                    position: 'absolute',
                    left: '50%',
                    top: onder ? m + 6 : -g.label * 1.6 - 6,
                    transform: 'translateX(-50%)',
                    padding: '4px 14px',
                    borderRadius: 12,
                    background: colors.blauw,
                    color: colors.wit,
                    fontSize: g.label * 0.85,
                    fontWeight: 700,
                    whiteSpace: 'nowrap',
                  }}
                >
                  {ps[i].l.naam}
                  <span style={{fontWeight: 400}}> · {ps[i].tijd}</span>
                </div>
              </div>
            );
          })}

          {/* The place: aqua pin with its name */}
          <div style={{position: 'absolute', left: cx, top: cy, transform: `translate(-50%, -100%) scale(${pinIn})`, transformOrigin: '50% 100%', opacity: frame < 44 ? 0 : 1}}>
            <div
              style={{
                position: 'absolute',
                left: '50%',
                bottom: g.pin * 1.32 + 10,
                transform: 'translateX(-50%)',
                padding: '10px 22px',
                borderRadius: 16,
                background: colors.aqua,
                color: colors.wit,
                fontSize: g.label * 1.15,
                fontWeight: 700,
                whiteSpace: 'nowrap',
              }}
            >
              {k.plek}
            </div>
            <svg width={g.pin} height={g.pin * 1.32} viewBox="0 0 60 80" style={{display: 'block'}}>
              <path d="M30 78 C30 78 4 46 4 28 A26 26 0 1 1 56 28 C56 46 30 78 30 78 Z" fill={colors.aqua} stroke={colors.wit} strokeWidth={4} />
              <circle cx={30} cy={28} r={10} fill={colors.wit} />
            </svg>
          </div>
        </div>

        {/* Rows: parking, walking time, price; nearest one marked */}
        {ps.map((p, i) => {
          const v = tween(frame, t.rijen[i], t.rijen[i] + 18, ease(0.2, 0.9, 0.3, 1));
          const r = g.rij;
          const eerste = i === 0;
          const pr = prijsDelen(p.l);
          return (
            <div
              key={`r${i}`}
              style={{
                position: 'absolute',
                left: r.x,
                top: rijY + i * (r.h + r.gap),
                width: r.w,
                height: r.h,
                borderRadius: 24,
                background: colors.wit,
                color: colors.blauw,
                border: `5px solid ${eerste && dichtstIn > 0 ? colors.aqua : colors.wit}`,
                boxSizing: 'border-box',
                display: 'flex',
                alignItems: 'center',
                gap: 18,
                padding: '0 24px',
                opacity: v,
                transform: `translateY(${(1 - v) * 40}px)`,
              }}
            >
              <div
                style={{
                  flex: 'none',
                  width: r.h * 0.56,
                  height: r.h * 0.56,
                  borderRadius: 12,
                  background: colors.blauw,
                  color: colors.wit,
                  fontSize: r.h * 0.36,
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                P
              </div>
              <div style={{flex: 1, minWidth: 0, lineHeight: 1.05}}>
                <div style={{fontSize: r.naam * 0.62, opacity: 0.8}}>
                  {p.tijd} lopen{eerste ? <span style={{opacity: dichtstIn, fontWeight: 700, color: colors.aqua}}> · dichtstbij</span> : null}
                </div>
                <div style={{fontSize: r.naam, fontWeight: 700, whiteSpace: 'nowrap'}}>{p.l.naam}</div>
              </div>
              <div style={{flex: 'none', textAlign: 'right', lineHeight: 1.05}}>
                <div style={{fontSize: r.naam, fontWeight: 700}}>{pr.groot}</div>
                <div style={{fontSize: r.naam * 0.55}}>{pr.klein}</div>
              </div>
            </div>
          );
        })}
      </AbsoluteFill>
      <EindCta start={t.cta} reserveer={ps.every((p) => RESERVEERBAAR.has(p.l.id))} k={CTA_GEO[formaat]} />
    </AbsoluteFill>
  );
};

export const KAART_SIZE: Record<ZoekFormaat, {width: number; height: number}> = {
  staand: {width: 1080, height: 1920},
  liggend: {width: 1920, height: 1080},
};
