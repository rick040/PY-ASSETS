import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Easing, Img, continueRender, delayRender, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {measureText} from '@remotion/layout-utils';
import {Fonts} from './components';
import {colors, font} from './theme';
import type {Locatie} from './locaties';

// Rebuild of the Jitter animation "Plantage" (1920x1080, 60 fps, 395 frames), plus a 9:16 reel version.
// Frame numbers below are the keyframes of the Jitter export, so the timing matches the original.

export const SPOT = {width: 1920, height: 1080, fps: 60, duration: 395};
// 9:16 reel: same timing, plus an end card (logo and parkingyou.nl) from frame 372.
export const REEL = {width: 1080, height: 1920, fps: 60, duration: 500};

export type Formaat = 'liggend' | 'staand';

type Rect = {x: number; y: number; w: number; h: number};
type Geo = {
  w: number;
  h: number;
  panel: Rect & {ox: number; oy: number};
  photo: Rect & {ox: number; oy: number};
  hook: {size: number; maxW: number; subMax: number; step: number; top: (lines: number) => number; subY: (lines: number) => number};
  title: {left: number; size: number; line: number; max: number};
  layout: (lines: number) => {top: number; rowTop: number; rowStep: number};
  rows: {left: number; max: number};
  logo: {right: number; bottom: number};
  bubble: {ax: number; ay: number};
  endCard: boolean;
};

// Landscape: the Jitter file. Blue panel on the left (1010 px), photo on the right.
const LIGGEND: Geo = {
  w: 1920,
  h: 1080,
  panel: {x: 0, y: 0, w: 1010, h: 1080, ox: 505, oy: 566},
  photo: {x: 1010, y: 0, w: 910, h: 1080, ox: 1396 - 1010, oy: 679.5},
  hook: {size: 150, maxW: 1500, subMax: 1600, step: 180, top: (n) => (n === 1 ? 320 : 230), subY: () => 770},
  title: {left: 115, size: 88, line: 101, max: 1010 - 115 - 25},
  layout: (n) =>
    n === 1 ? {top: 130, rowTop: 423, rowStep: 138} : n === 2 ? {top: 85, rowTop: 423, rowStep: 138} : {top: 62, rowTop: 504, rowStep: 126},
  rows: {left: 113, max: 1010 - 218 - 50},
  logo: {right: 1920 - 1863, bottom: 1080 - 1016},
  bubble: {ax: 1752, ay: 218},
  endCard: false,
};

// Portrait reel: photo on top (760 px), blue panel below. Key content stays out of the
// Instagram and TikTok UI (top 250 px, bottom 330 px).
const STAAND: Geo = {
  w: 1080,
  h: 1920,
  panel: {x: 0, y: 760, w: 1080, h: 1160, ox: 540, oy: 1340},
  photo: {x: 0, y: 0, w: 1080, h: 760, ox: 540, oy: 380},
  hook: {
    size: 108,
    maxW: 960,
    subMax: 960,
    step: 130,
    top: (n) => 920 - (n * 130 + 80 + 110) / 2,
    subY: (n) => 920 - (n * 130 + 80 + 110) / 2 + n * 130 + 80,
  },
  title: {left: 90, size: 92, line: 106, max: 1080 - 90 - 60},
  layout: (n) => {
    const top = n >= 3 ? 805 : 830;
    const rowTop = top + n * 106 + (n >= 3 ? 80 : 95);
    return {top, rowTop, rowStep: Math.min(128, (1540 - rowTop) / 3)};
  },
  rows: {left: 88, max: 1080 - 88 - 105 - 60},
  logo: {right: 40, bottom: 1920 - 730},
  bubble: {ax: 907, ay: 440},
  endCard: true,
};

export const GEO: Record<Formaat, Geo> = {liggend: LIGGEND, staand: STAAND};
const ease = (a: number, b: number, c: number, d: number) => Easing.bezier(a, b, c, d);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/** 0 to 1 between two frames with an easing. */
const tween = (frame: number, from: number, to: number, easing = (t: number) => t) =>
  interpolate(frame, [from, to], [0, 1], {...clamp, easing});

/** Greedy line wrap with real Ubuntu metrics. */
const wrap = (text: string, fontSize: number, fontWeight: string, maxWidth: number) => {
  const lines: string[] = [];
  let line = '';
  for (const word of text.split(' ')) {
    const test = line ? `${line} ${word}` : word;
    if (line && measureText({text: test, fontFamily: 'Ubuntu', fontSize, fontWeight}).width > maxWidth) {
      lines.push(line);
      line = word;
    } else line = test;
  }
  if (line) lines.push(line);
  return lines;
};

const width = (text: string, fontSize: number, fontWeight: string) =>
  measureText({text, fontFamily: 'Ubuntu', fontSize, fontWeight}).width;

// ---------------------------------------------------------------- hook screen

const Hook: React.FC<{hook: string; subhook: string; g: Geo}> = ({hook, subhook, g}) => {
  const frame = useCurrentFrame();
  const HOOK_SIZE = g.hook.size;
  const lines = wrap(hook, HOOK_SIZE, '700', g.hook.maxW);
  const subSize = Math.min(HOOK_SIZE, (HOOK_SIZE * g.hook.subMax) / width(subhook, HOOK_SIZE, '400'));
  // Each line slides 84 px to the left (strong ease-in) and is gone at the end, top line first.
  const rows = [...lines.map((l) => ({text: l, weight: 700, size: HOOK_SIZE})), {text: subhook, weight: 400, size: subSize}];
  const top = g.hook.top(lines.length);
  return (
    <AbsoluteFill>
      {rows.map((r, i) => {
        const start = 67.8 + i * 1.25;
        const t = tween(frame, start, start + 7.1, ease(1, 0, 1, 1));
        const gone = frame >= start + 7.1;
        const y = i < lines.length ? top + i * g.hook.step : g.hook.subY(lines.length);
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              top: y - r.size * 0.21,
              left: 0,
              width: '100%',
              textAlign: 'center',
              fontFamily: font,
              fontWeight: r.weight,
              fontSize: r.size,
              lineHeight: 1.2,
              color: colors.wit,
              whiteSpace: 'nowrap',
              transform: `translateX(${-84 * t}px)`,
              opacity: gone ? 0 : 1,
            }}
          >
            {r.text}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- photo panel

const Photo: React.FC<{src: string; g: Geo}> = ({src, g}) => {
  const frame = useCurrentFrame();
  const s = interpolate(frame, [91.8, 394.8], [1, 1.1], clamp);
  const p = g.photo;
  return (
    <div style={{position: 'absolute', left: p.x, top: p.y, width: p.w, height: p.h, overflow: 'hidden'}}>
      <Img
        src={staticFile(src)}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `scale(${s})`,
          transformOrigin: `${p.ox}px ${p.oy}px`,
        }}
      />
    </div>
  );
};

// ---------------------------------------------------------------- title

// One size for every title. A name that does not fit next to "Parking" goes to its own line,
// and a name that is too wide for one line wraps at a space (for example "Bos en" / "Lommerplantsoen").

/** Title lines: the first is always "Parking" (with the name after it when it fits). */
const titleLines = (naam: string, g: Geo): {text: string; bold: boolean}[][] => {
  const {size, max} = g.title;
  const one = width('Parking ', size, '400') + width(naam, size, '700');
  if (one <= max) return [[{text: 'Parking ', bold: false}, {text: naam, bold: true}]];
  return [[{text: 'Parking', bold: false}], ...wrap(naam, size, '700', max).map((l) => [{text: l, bold: true}])];
};

const Title: React.FC<{naam: string; g: Geo}> = ({naam, g}) => {
  const frame = useCurrentFrame();
  const lines = titleLines(naam, g);
  const {top} = g.layout(lines.length);
  const {left, size, line} = g.title;
  // Words come up out of a mask: "Parking" first, the name a frame later and slower (Jitter timing).
  const timing = (bold: boolean, li: number) => (bold ? [93 + (li - 1) * 4, 130.8 + (li - 1) * 4] : [91.8, 104.5]);
  return (
    <div style={{position: 'absolute', left, top, fontFamily: font, fontSize: size, color: colors.wit, whiteSpace: 'nowrap'}}>
      {lines.map((parts, li) => (
        <div key={li} style={{height: line, lineHeight: `${line}px`, overflow: 'hidden'}}>
          {parts.map((part, pi) => {
            const [from, to] = timing(part.bold, li);
            const t = tween(frame, from, to, ease(0.2, 0.9, 0.3, 1));
            return (
              <span key={pi} style={{display: 'inline-block', whiteSpace: 'pre', fontWeight: part.bold ? 700 : 400, transform: `translateY(${(1 - t) * 110}%)`}}>
                {part.text}
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};

// ---------------------------------------------------------------- check rows

// Overshoot of the check circle (Jitter values), one step every ~13 frames.
const BOUNCE = [0, 1.3731, 0.8681, 1.0466, 0.9835, 1];
const bounce = (frame: number, start: number, step = 13) =>
  interpolate(
    frame,
    BOUNCE.map((_, i) => start + i * step),
    BOUNCE,
    {...clamp, easing: ease(0.3, 0, 0.54, 1)},
  );

const ROWS = [
  {slide: [116.4, 192.6], circle: 136.2, check: 147.7, out: 341.9},
  {slide: [147.7, 214.3], circle: 165.1, check: 175.0, out: 344.8},
  {slide: [169.2, 229.2], circle: 184.8, check: 193.8, out: 346.8},
  {slide: [197.4, 248.8], circle: 210.8, check: 218.5, out: 349.4},
];
const ROW_SIZE = 64;

const Check: React.FC<{size: number}> = ({size}) => (
  <svg width={size} height={size} viewBox="0 0 24 24">
    <path d="M6.5 12.5l3.6 3.6 7.4-7.6" fill="none" stroke={colors.wit} strokeWidth={1.9} strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const Rows: React.FC<{kenmerken: Locatie['kenmerken']; naam: string; g: Geo}> = ({kenmerken, naam, g}) => {
  const {rowTop, rowStep} = g.layout(titleLines(naam, g).length);
  const frame = useCurrentFrame();
  return (
    <>
      {kenmerken.map(([licht, vet], i) => {
        const r = ROWS[i];
        const t = tween(frame, r.slide[0], r.slide[1], ease(0, 0, 0, 1));
        const opacity = interpolate(frame, r.slide, [0, 1], clamp);
        const out = 1 - tween(frame, r.out, 364.8, ease(0.33, 0, 0.67, 1));
        const circle = bounce(frame, r.circle) * out;
        const check = bounce(frame, r.check) * out;
        const text = licht ? `${licht} ${vet}` : vet;
        const size = Math.min(ROW_SIZE, (ROW_SIZE * g.rows.max) / width(text, ROW_SIZE, '700'));
        const cy = rowTop + i * rowStep;
        return (
          <div key={i} style={{position: 'absolute', left: g.rows.left, top: cy - 41, height: 82, opacity, transform: `translateX(${-41 * (1 - t)}px)`}}>
            <div
              style={{
                position: 'absolute',
                left: 0,
                top: 0,
                width: 82,
                height: 82,
                borderRadius: '50%',
                background: colors.aqua,
                transform: `scale(${circle})`,
              }}
            />
            <div style={{position: 'absolute', left: 9, top: 9, transform: `scale(${check})`}}>
              <Check size={64} />
            </div>
            <div
              style={{
                position: 'absolute',
                left: 105,
                top: 41 - size * 0.62,
                fontFamily: font,
                fontSize: size,
                lineHeight: 1.2,
                color: colors.wit,
                whiteSpace: 'nowrap',
              }}
            >
              {licht ? <span style={{fontWeight: 400}}>{licht} </span> : null}
              <span style={{fontWeight: 700}}>{vet}</span>
            </div>
          </div>
        );
      })}
    </>
  );
};

// ---------------------------------------------------------------- price bubble

// py-atom-shape-bubble-solid, mirrored so the tail points to the bottom right as in the Jitter file.
const BUBBLE_PATH =
  'M18 0C8.059 0 0 8.058 0 17.998C0 34.701 16.691 43.073 16.691 43.073C17.264 43.423 18 43.006 18 42.335L18 35.997C27.941 35.997 36 27.939 36 17.998C36 8.058 27.941 0 18 0';

const Bubble: React.FC<{prijs: Locatie['prijs']; g: Geo}> = ({prijs, g}) => {
  const frame = useCurrentFrame();
  const t = tween(frame, 224.3, 314.3, ease(0.5, 0, 0, 1));
  const R = 133; // circle radius in px
  const k = (2 * R) / 36;
  const m = prijs.bedrag.match(/^(€\d+),(\d\d)$/);
  const blue = colors.blauw;
  const main = m ? `${m[1]},` : prijs.bedrag;
  const mainSize = m ? (m[1].length > 3 ? 92 : 112) : 84;
  return (
    <div
      style={{
        position: 'absolute',
        left: g.bubble.ax - R,
        top: g.bubble.ay - 160,
        width: 36 * k,
        height: 43.423 * k,
        transform: `scale(${t}) rotate(${-45 * (1 - t)}deg)`,
        transformOrigin: `${R}px 160px`,
      }}
    >
      <svg width={36 * k} height={43.423 * k} viewBox="0 0 36 43.423" style={{position: 'absolute', transform: 'scaleX(-1)'}}>
        <path d={BUBBLE_PATH} fill={colors.wit} />
      </svg>
      <div
        style={{
          position: 'absolute',
          left: 0,
          top: 0,
          width: 2 * R,
          height: 2 * R,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: font,
          color: blue,
          transform: 'rotate(-12deg)',
        }}
      >
        {prijs.vanaf ? <div style={{fontSize: 34, fontWeight: 400, lineHeight: 1, marginBottom: 2}}>vanaf</div> : null}
        <div style={{display: 'flex', alignItems: 'flex-start', fontWeight: 700, lineHeight: 1, letterSpacing: -2}}>
          <span style={{fontSize: mainSize}}>{main}</span>
          {m ? <span style={{fontSize: mainSize * 0.5, marginTop: mainSize * 0.02, letterSpacing: 0}}>{m[2]}</span> : null}
        </div>
        <div style={{fontSize: prijs.eenheid.length > 10 ? 34 : 44, fontWeight: 400, lineHeight: 1.1, marginTop: 4}}>{prijs.eenheid}</div>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- logo

const Logo: React.FC<{g: Geo}> = ({g}) => {
  const frame = useCurrentFrame();
  const pop = tween(frame, 97.8, 115.8, ease(0.25, 0.25, 0.25, 1));
  const slide = tween(frame, 110.4, 146.4, ease(0.25, 0, 0.25, 1));
  const reveal = tween(frame, 116.4, 155.4, ease(0, 0, 0.4, 1));
  const pinH = 50;
  const pinW = (24 / 28.949) * pinH;
  const markW = 246;
  const total = pinW + 14 + markW;
  // The pin starts in the middle of the logo and moves to its place while the wordmark appears behind it.
  const pinX = (1 - slide) * (total / 2 - pinW / 2);
  const edge = reveal * 120;
  return (
    <div style={{position: 'absolute', right: g.logo.right, bottom: g.logo.bottom, width: total, height: pinH}}>
      <div
        style={{
          position: 'absolute',
          left: pinW + 14,
          top: (pinH - (markW * 14.964) / 73.76) / 2 + 2,
          width: markW,
          WebkitMaskImage: `linear-gradient(90deg, #000 ${edge - 20}%, transparent ${edge}%)`,
          maskImage: `linear-gradient(90deg, #000 ${edge - 20}%, transparent ${edge}%)`,
        }}
      >
        <Img src={staticFile('svg/atom/py-atom-logo-wordmark-white.svg')} style={{width: markW, display: 'block'}} />
      </div>
      <div style={{position: 'absolute', left: pinX, top: 0, transform: `scale(${pop})`, opacity: pop}}>
        <Img src={staticFile('svg/atom/py-atom-logo-beeldmerk-white.svg')} style={{width: pinW, display: 'block'}} />
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- composition

/** Text is measured for wrapping and fitting, so Ubuntu has to be loaded before the first frame. */
const useUbuntu = () => {
  const [handle] = useState(() => delayRender('Ubuntu laden'));
  const [ready, setReady] = useState(false);
  useEffect(() => {
    const faces = [
      ['400', 'Ubuntu-Regular.ttf'],
      ['700', 'Ubuntu-Bold.ttf'],
    ].map(([weight, file]) => new FontFace('Ubuntu', `url(${staticFile(`fonts/${file}`)})`, {weight}));
    Promise.all(faces.map((f) => f.load()))
      .then((loaded) => {
        loaded.forEach((f) => document.fonts.add(f));
        setReady(true);
        continueRender(handle);
      })
      .catch((err) => {
        console.error(err);
        continueRender(handle);
      });
  }, [handle]);
  return ready;
};

/** Reel end card: the blue panel grows back over everything, then the stacked logo and the web address. */
const EndCard: React.FC<{g: Geo}> = ({g}) => {
  const frame = useCurrentFrame();
  const cover = interpolate(frame, [372, 410], [1, 3], {...clamp, easing: ease(0.5, 0, 0, 1)});
  const logo = tween(frame, 400, 430, ease(0.2, 0.9, 0.3, 1.2));
  const url = tween(frame, 415, 445, ease(0.2, 0.9, 0.3, 1));
  if (frame < 372) return null;
  const p = g.panel;
  return (
    <>
      <div
        style={{
          position: 'absolute',
          left: p.x,
          top: p.y,
          width: p.w,
          height: p.h,
          background: colors.blauw,
          transform: `scale(${cover})`,
          transformOrigin: `${p.ox}px ${p.oy - p.y}px`,
        }}
      />
      <div style={{position: 'absolute', left: 0, top: 700, width: g.w, display: 'flex', justifyContent: 'center'}}>
        <div style={{transform: `scale(${logo})`, opacity: Math.min(1, logo * 2)}}>
          <Img src={staticFile('svg/atom/py-atom-logo-stacked-white.svg')} style={{width: 460, display: 'block'}} />
        </div>
      </div>
      <div
        style={{
          position: 'absolute',
          left: 0,
          top: 1150,
          width: g.w,
          textAlign: 'center',
          fontFamily: font,
          fontWeight: 700,
          fontSize: 76,
          color: colors.wit,
          opacity: url,
          transform: `translateY(${(1 - url) * 40}px)`,
        }}
      >
        parkingyou.nl
      </div>
    </>
  );
};

export const LocatieSpot: React.FC<{locatie: Locatie; formaat?: Formaat}> = ({locatie, formaat = 'liggend'}) => {
  const frame = useCurrentFrame();
  const ready = useUbuntu();
  if (!ready) return <AbsoluteFill style={{background: colors.blauw}} />;
  const g = GEO[formaat];
  const p = g.panel;
  // The blue panel starts at 300 percent (covers the frame) and settles to its place.
  const panel = interpolate(frame, [67.8, 115.8], [3, 1], {...clamp, easing: ease(0.5, 0, 0, 1)});
  const foto = formaat === 'staand' ? `locaties/staand/${locatie.id}.jpg` : locatie.foto;
  return (
    <AbsoluteFill style={{background: colors.blauw}}>
      <Fonts />
      <Photo src={foto} g={g} />
      <div
        style={{
          position: 'absolute',
          left: p.x,
          top: p.y,
          width: p.w,
          height: p.h,
          background: colors.blauw,
          transform: `scale(${panel})`,
          transformOrigin: `${p.ox}px ${p.oy - p.y}px`,
        }}
      />
      {frame < 78 ? <Hook hook={locatie.hook} subhook={locatie.subhook} g={g} /> : null}
      <Title naam={locatie.naam} g={g} />
      <Rows kenmerken={locatie.kenmerken} naam={locatie.naam} g={g} />
      <Logo g={g} />
      <Bubble prijs={locatie.prijs} g={g} />
      {g.endCard ? <EndCard g={g} /> : null}
    </AbsoluteFill>
  );
};
