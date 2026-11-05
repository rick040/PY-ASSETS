import React from "react";
import { AbsoluteFill, Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { noise2D } from "@remotion/noise";
import { BRAND } from "../theme";

export type BackdropKind = "navy" | "glow" | "light" | "photo";

/** Soft light that drifts slowly (noise driven), so a background is never static. */
const Light: React.FC<{ seed: string; color: string; size: number; x: number; y: number; opacity: number }> = ({ seed, color, size, x, y, opacity }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const dx = noise2D(seed + "x", frame / 160, 0) * width * 0.12;
  const dy = noise2D(seed + "y", 0, frame / 160) * height * 0.08;
  return (
    <div style={{ position: "absolute", left: x * width + dx - size / 2, top: y * height + dy - size / 2, width: size, height: size, borderRadius: "50%", background: `radial-gradient(circle, ${color} 0%, transparent 68%)`, opacity, mixBlendMode: "screen" }} />
  );
};

/** Fine film grain: keeps flat colour areas from banding and gives a filmic finish. */
export const Grain: React.FC<{ opacity?: number }> = ({ opacity = 0.06 }) => {
  const frame = useCurrentFrame();
  const seed = Math.floor(frame / 2) % 8; // re-seed every other frame, subtle
  return (
    <AbsoluteFill style={{ opacity, mixBlendMode: "overlay", pointerEvents: "none" }}>
      <svg width="100%" height="100%">
        <filter id={`grain${seed}`}>
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={seed} stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter={`url(#grain${seed})`} />
      </svg>
    </AbsoluteFill>
  );
};

/**
 * Backgrounds from the current feed: flat navy with drifting light, the cyan-to-blue GLOW gradient,
 * the pale Easter-post blue, or a photo/video with a slow Ken Burns move and a dark gradient for legible text.
 */
export const Backdrop: React.FC<{ kind: BackdropKind; media?: string; mediaType?: "image" | "video"; children?: React.ReactNode; seed?: string }> = ({ kind, media, mediaType = "image", children, seed = "bg" }) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const zoom = interpolate(frame, [0, durationInFrames], [1.06, 1.16]);
  const pan = interpolate(frame, [0, durationInFrames], [-1.5, 1.5]);
  return (
    <AbsoluteFill style={{ backgroundColor: kind === "light" ? "#E4EEF4" : BRAND.blauw, overflow: "hidden" }}>
      {kind === "glow" && (
        <>
          <AbsoluteFill style={{ background: `linear-gradient(150deg, #39D3E6 0%, ${BRAND.aqua} 22%, #1B7FD0 58%, #2340B8 82%, ${BRAND.blauw} 100%)` }} />
          <Light seed={seed + "a"} color="#9FF3FF" size={width * 1.3} x={0.15} y={0.18} opacity={0.55} />
          <Light seed={seed + "b"} color="#4E7BFF" size={width * 1.4} x={0.9} y={0.85} opacity={0.5} />
        </>
      )}
      {kind === "navy" && (
        <>
          <Light seed={seed + "a"} color="#3B5BD0" size={width * 1.5} x={0.2} y={0.15} opacity={0.55} />
          <Light seed={seed + "b"} color={BRAND.aqua} size={width * 1.1} x={0.95} y={0.95} opacity={0.22} />
        </>
      )}
      {kind === "light" && <Light seed={seed + "a"} color="#FFFFFF" size={width * 1.4} x={0.5} y={0.25} opacity={0.9} />}
      {kind === "photo" && media && (
        <AbsoluteFill style={{ transform: `scale(${zoom}) translateX(${pan}%)` }}>
          {mediaType === "video" ? (
            <OffthreadVideo src={staticFile(media)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          ) : (
            <Img src={staticFile(media)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          )}
        </AbsoluteFill>
      )}
      {kind === "photo" && <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(14,24,66,0.70) 0%, rgba(14,24,66,0.15) 38%, rgba(14,24,66,0.25) 62%, rgba(14,24,66,0.85) 100%)" }} />}
      {/* vignette */}
      {kind !== "light" && <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, transparent 55%, rgba(8,14,46,0.45) 100%)" }} />}
      {children}
      <Grain opacity={kind === "light" ? 0.04 : 0.07} />
    </AbsoluteFill>
  );
};
