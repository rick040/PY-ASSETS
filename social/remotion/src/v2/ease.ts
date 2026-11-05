import { Easing, interpolate } from "remotion";

// Premium motion curves. Entrances decelerate hard (expo out), exits accelerate (expo in).
export const EASE_OUT = Easing.bezier(0.16, 1, 0.3, 1);
export const EASE_IN = Easing.bezier(0.7, 0, 0.84, 0);
export const EASE_IN_OUT = Easing.bezier(0.65, 0, 0.35, 1);

const clampOpts = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/** 0 -> 1 from `start` over `dur` frames with an expo-out curve. */
export const enter = (frame: number, start: number, dur = 18, easing = EASE_OUT) =>
  interpolate(frame, [start, start + dur], [0, 1], { ...clampOpts, easing });

/** 0 -> 1 as the scene ends: starts `dur` frames before `end`. */
export const leave = (frame: number, end: number, dur = 12, easing = EASE_IN) =>
  interpolate(frame, [end - dur, end], [0, 1], { ...clampOpts, easing });

export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
