import { interpolate, spring, SpringConfig } from "remotion";

export const springs: Record<"pop" | "smooth" | "bouncy", Partial<SpringConfig>> = {
  pop: { damping: 14, stiffness: 180, mass: 0.7 },
  smooth: { damping: 200 },
  bouncy: { damping: 9, stiffness: 160, mass: 0.8 },
};

/** Spring from 0 to 1 starting at `delay` (frames). A negative delay means "already done at frame 0". */
export const pop = (frame: number, fps: number, delay = 0, config = springs.pop) =>
  spring({ frame: frame - delay, fps, config });

export const clamp01 = (x: number) => Math.min(1, Math.max(0, x));

export const fadeIn = (frame: number, start: number, length = 10) =>
  interpolate(frame, [start, start + length], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

export const mix = (a: number, b: number, t: number) => a + (b - a) * t;
