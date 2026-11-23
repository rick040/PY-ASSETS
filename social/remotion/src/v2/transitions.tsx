import React from "react";
import { AbsoluteFill, useVideoConfig } from "remotion";
import type { TransitionPresentation, TransitionPresentationComponentProps } from "@remotion/transitions";
import { BUBBLE } from "../lib/paths";

type Empty = Record<string, never>;

/**
 * Vertical push with motion blur: the incoming scene rises in, the outgoing one moves up and away;
 * blur follows the speed (strongest mid-transition), which reads as smooth camera motion.
 */
const SlideBlur: React.FC<TransitionPresentationComponentProps<Empty>> = ({ children, presentationDirection, presentationProgress }) => {
  const p = presentationProgress;
  const speed = Math.sin(Math.PI * p); // 0 -> 1 -> 0
  const blur = speed * 14;
  const style: React.CSSProperties =
    presentationDirection === "entering"
      ? { transform: `translateY(${(1 - p) * 100}%)`, filter: `blur(${blur}px)` }
      : { transform: `translateY(${-p * 35}%) scale(${1 - p * 0.06})`, filter: `blur(${blur}px) brightness(${1 - p * 0.4})` };
  return <AbsoluteFill style={style}>{children}</AbsoluteFill>;
};
export const slideBlur = (): TransitionPresentation<Empty> => ({ component: SlideBlur, props: {} });

/** Alternate path through the bubble: every (x, y) pair is scaled by k and moved by (tx, ty). */
const placePath = (d: string, k: number, tx: number, ty: number) => {
  let i = 0;
  return d.replace(/-?\d*\.?\d+/g, (n) => {
    const v = parseFloat(n) * k + (i++ % 2 === 0 ? tx : ty);
    return v.toFixed(2);
  });
};

/** Brand transition: the next scene opens through the ParkingYou speech bubble growing from the centre. */
const BubbleReveal: React.FC<TransitionPresentationComponentProps<Empty>> = ({ children, presentationDirection, presentationProgress }) => {
  const { width, height } = useVideoConfig();
  if (presentationDirection === "exiting") {
    return <AbsoluteFill style={{ transform: `scale(${1 + presentationProgress * 0.08})`, filter: `brightness(${1 - presentationProgress * 0.35})` }}>{children}</AbsoluteFill>;
  }
  const p = presentationProgress;
  const cover = Math.hypot(width, height) / 2 / (BUBBLE.w / 2) * 1.25;
  const k = Math.max(0.001, p * p * cover + p * 2);
  const clip = `path('${placePath(BUBBLE.d, k, width / 2 - (BUBBLE.w / 2) * k, height / 2 - (BUBBLE.w / 2) * k)}')`;
  return <AbsoluteFill style={{ clipPath: clip, transform: `scale(${1.08 - 0.08 * p})` }}>{children}</AbsoluteFill>;
};
export const bubbleReveal = (): TransitionPresentation<Empty> => ({ component: BubbleReveal, props: {} });

/** Soft zoom-through: outgoing scene scales up and blurs away while the incoming one settles from 1.12. */
const ZoomThrough: React.FC<TransitionPresentationComponentProps<Empty>> = ({ children, presentationDirection, presentationProgress }) => {
  const p = presentationProgress;
  const style: React.CSSProperties =
    presentationDirection === "entering"
      ? { transform: `scale(${1.12 - 0.12 * p})`, opacity: Math.min(1, p * 1.6), filter: `blur(${(1 - p) * 12}px)` }
      : { transform: `scale(${1 + p * 0.25})`, opacity: 1 - p, filter: `blur(${p * 16}px)` };
  return <AbsoluteFill style={style}>{children}</AbsoluteFill>;
};
export const zoomThrough = (): TransitionPresentation<Empty> => ({ component: ZoomThrough, props: {} });
