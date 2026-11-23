import React from "react";
import { random, useCurrentFrame, useVideoConfig } from "remotion";
import { evolvePath } from "@remotion/paths";
import { BRAND } from "../theme";
import { AssetImg } from "../components/AssetImg";
import { enter, EASE_OUT } from "./ease";

/** Rays around a big number ("13 nieuwe locaties"): they draw outwards with @remotion/paths and turn slowly. */
export const Sunburst: React.FC<{ start: number; size: number; color?: string; rays?: number; opacity?: number }> = ({ start, size, color = BRAND.wit, rays = 28, opacity = 0.55 }) => {
  const frame = useCurrentFrame();
  const r0 = size * 0.33;
  const rot = frame * 0.12;
  return (
    <svg width={size} height={size} viewBox={`${-size / 2} ${-size / 2} ${size} ${size}`} style={{ overflow: "visible", transform: `rotate(${rot}deg)`, opacity }}>
      {new Array(rays).fill(0).map((_, i) => {
        const a = (i / rays) * Math.PI * 2;
        const len = size * (0.1 + 0.07 * random(`ray${i}`));
        const d = `M ${Math.cos(a) * r0} ${Math.sin(a) * r0} L ${Math.cos(a) * (r0 + len)} ${Math.sin(a) * (r0 + len)}`;
        const p = enter(frame, start + (i % 7) * 1.5, 20, EASE_OUT);
        const { strokeDasharray, strokeDashoffset } = evolvePath(p, d);
        return <path key={i} d={d} stroke={color} strokeWidth={size * 0.012} strokeLinecap="round" fill="none" strokeDasharray={strokeDasharray} strokeDashoffset={strokeDashoffset} />;
      })}
    </svg>
  );
};

/** Orange, aqua and white confetti bursting from a point, then falling and turning (deterministic). */
export const Confetti: React.FC<{ start: number; count?: number; x?: number; y?: number; colors?: string[] }> = ({ start, count = 70, x = 0.5, y = 0.45, colors = [BRAND.oranje, BRAND.aqua, BRAND.wit, BRAND.oranje] }) => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const t = (frame - start) / fps;
  if (t < 0) return null;
  return (
    <svg width={width} height={height} style={{ position: "absolute", inset: 0, overflow: "visible", pointerEvents: "none" }}>
      {new Array(count).fill(0).map((_, i) => {
        const ang = random(`ca${i}`) * Math.PI * 2;
        const v = 900 + random(`cv${i}`) * 1300;
        const drag = 2.6;
        const k = (1 - Math.exp(-drag * t)) / drag;
        const px = x * width + Math.cos(ang) * v * k;
        const py = y * height + Math.sin(ang) * v * k * 0.8 + 520 * t * t * 0.5 + 120 * t;
        const w = 14 + random(`cw${i}`) * 16;
        const rot = random(`cr${i}`) * 360 + t * (200 + random(`cs${i}`) * 500);
        const flip = Math.abs(Math.cos(t * (6 + random(`cf${i}`) * 6)));
        const fade = Math.max(0, 1 - Math.max(0, t - 1.6) / 0.8);
        return <rect key={i} x={-w / 2} y={-w * 0.22} width={w} height={w * 0.44} rx={2} fill={colors[i % colors.length]} opacity={fade} transform={`translate(${px} ${py}) rotate(${rot}) scale(1 ${flip})`} />;
      })}
    </svg>
  );
};

/** White silhouettes of cars and people along the bottom, like the DLL carnaval post. They rise in, staggered. */
export const Skyline: React.FC<{ start: number; width: number; figures?: string[] }> = ({ start, width, figures = ["py-atom-picto-car", "py-atom-figure-dance", "py-atom-picto-car", "py-atom-figure-bags-cheer", "py-atom-figure-jump", "py-atom-picto-car"] }) => {
  const frame = useCurrentFrame();
  const slot = width / figures.length;
  return (
    <div style={{ position: "relative", width, height: slot * 1.1 }}>
      {figures.map((id, i) => {
        const p = enter(frame, start + i * 3, 20);
        const car = id.includes("car");
        const h = car ? slot * 0.62 : slot * 0.95;
        const bob = car ? 0 : -Math.abs(Math.sin((frame + i * 9) / 6)) * 10;
        return (
          <div key={i} style={{ position: "absolute", left: i * slot, bottom: 0, width: slot, display: "flex", justifyContent: "center", transform: `translateY(${(1 - p) * 140 + bob}px)`, opacity: p }}>
            <AssetImg id={id} height={h} tint="white" />
          </div>
        );
      })}
    </div>
  );
};

/** Twinkling points of light (light festivals, evenings): soft glow, each with its own noise-driven flicker. */
export const Sparkles: React.FC<{ count?: number; colors?: string[]; seed?: string; area?: { x: number; y: number; w: number; h: number } }> = ({ count = 46, colors = ["#FFFFFF", BRAND.aqua, "#FFD38A"], seed = "sp", area }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const A = area ?? { x: 0, y: 0, w: width, h: height };
  return (
    <svg width={width} height={height} style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
      <defs>
        {colors.map((c, i) => (
          <radialGradient key={i} id={`${seed}g${i}`}>
            <stop offset="0%" stopColor={c} stopOpacity={1} />
            <stop offset="35%" stopColor={c} stopOpacity={0.5} />
            <stop offset="100%" stopColor={c} stopOpacity={0} />
          </radialGradient>
        ))}
      </defs>
      {new Array(count).fill(0).map((_, i) => {
        const x = A.x + random(`${seed}x${i}`) * A.w;
        const y = A.y + random(`${seed}y${i}`) * A.h;
        const r = 10 + random(`${seed}r${i}`) * 34;
        const tw = 0.5 + 0.5 * Math.sin(frame / (6 + random(`${seed}s${i}`) * 10) + random(`${seed}p${i}`) * 6.28);
        return <circle key={i} cx={x} cy={y + Math.sin(frame / 40 + i) * 6} r={r * (0.7 + 0.3 * tw)} fill={`url(#${seed}g${i % colors.length})`} opacity={0.25 + 0.75 * tw} />;
      })}
    </svg>
  );
};
