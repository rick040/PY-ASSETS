import React from "react";
import { random, useCurrentFrame } from "remotion";

/** Thin falling lines; deterministic per seed so every render is identical. */
export const Rain: React.FC<{ width: number; height: number; color: string; count?: number; opacity?: number }> = ({ width, height, color, count = 70, opacity = 0.45 }) => {
  const frame = useCurrentFrame();
  return (
    <svg width={width} height={height} style={{ position: "absolute", inset: 0 }}>
      {new Array(count).fill(0).map((_, i) => {
        const x = random(`x${i}`) * width;
        const speed = 28 + random(`s${i}`) * 22;
        const len = 40 + random(`l${i}`) * 50;
        const y = ((random(`y${i}`) * height + frame * speed) % (height + len)) - len;
        return <line key={i} x1={x} y1={y} x2={x - len * 0.18} y2={y + len} stroke={color} strokeWidth={4} strokeLinecap="round" opacity={opacity * (0.5 + random(`o${i}`) * 0.5)} />;
      })}
    </svg>
  );
};
