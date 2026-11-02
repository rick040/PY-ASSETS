import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors, font} from './theme';

/** Loads the Ubuntu files from the library. */
export const Fonts: React.FC = () => {
  const faces: [number, string, string][] = [
    [300, 'normal', 'Ubuntu-Light.ttf'],
    [400, 'normal', 'Ubuntu-Regular.ttf'],
    [500, 'normal', 'Ubuntu-Medium.ttf'],
    [700, 'normal', 'Ubuntu-Bold.ttf'],
  ];
  const css = faces
    .map(
      ([w, s, f]) =>
        `@font-face{font-family:'Ubuntu';font-weight:${w};font-style:${s};src:url(${staticFile(`fonts/${f}`)}) format('truetype');}`,
    )
    .join('\n');
  return <style>{css}</style>;
};

/** An atom SVG from svg/atom, scaled by width (height follows the viewBox). */
export const Atom: React.FC<{id: string; width: number; style?: React.CSSProperties}> = ({id, width, style}) => (
  <Img src={staticFile(`svg/atom/py-atom-${id}.svg`)} style={{width, display: 'block', ...style}} />
);

/** Spring 0 to 1, starting at `delay` frames. */
export const useSpring = (delay = 0, config: Partial<{damping: number; stiffness: number; mass: number}> = {}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: frame - delay, fps, config: {damping: 14, stiffness: 120, ...config}});
};

/** Rises from below with a fade, for text and small blocks. */
export const Rise: React.FC<{delay?: number; distance?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({
  delay = 0,
  distance = 60,
  children,
  style,
}) => {
  const p = useSpring(delay, {damping: 18, stiffness: 110});
  return (
    <div style={{opacity: Math.min(1, p * 1.6), transform: `translateY(${(1 - p) * distance}px)`, ...style}}>{children}</div>
  );
};

/** Fades out over the last frames of the story. */
export const useOutro = (total: number, length = 12) => {
  const frame = useCurrentFrame();
  return interpolate(frame, [total - length, total], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
};

/** Soft drifting circles for depth on a flat background. */
export const FloatingCircles: React.FC<{color: string; opacity?: number}> = ({color, opacity = 0.1}) => {
  const frame = useCurrentFrame();
  const defs = [
    {x: 140, y: 520, r: 160, s: 0.9},
    {x: 930, y: 760, r: 110, s: 1.3},
    {x: 820, y: 1320, r: 210, s: 0.7},
    {x: 120, y: 1500, r: 90, s: 1.1},
  ];
  return (
    <AbsoluteFill>
      {defs.map((d, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: d.x - d.r,
            top: d.y - d.r + Math.sin(frame / (28 / d.s) + i) * 26,
            width: d.r * 2,
            height: d.r * 2,
            borderRadius: '50%',
            background: color,
            opacity,
          }}
        />
      ))}
    </AbsoluteFill>
  );
};

/** Pill with live Ubuntu text (rounded like py-atom-shape-pill-solid). */
export const Pill: React.FC<{
  children: React.ReactNode;
  background: string;
  color?: string;
  size?: number;
  style?: React.CSSProperties;
}> = ({children, background, color = colors.wit, size = 48, style}) => (
  <div
    style={{
      display: 'inline-block',
      background,
      color,
      fontFamily: font,
      fontWeight: 700,
      fontSize: size,
      padding: `${size * 0.42}px ${size * 1.1}px`,
      borderRadius: 999,
      letterSpacing: 0.5,
      ...style,
    }}
  >
    {children}
  </div>
);

export const headline: React.CSSProperties = {
  fontFamily: font,
  fontWeight: 700,
  lineHeight: 1.05,
  letterSpacing: -1.5,
};
