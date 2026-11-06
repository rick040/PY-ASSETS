import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { BRAND, FONT } from "../theme";
import { enter, EASE_OUT } from "./ease";
import { AssetImg } from "../components/AssetImg";

/** The arrow from the asset library: py-atom-arrow-right-circle (white circle, aqua arrow). */
const ArrowCircle: React.FC<{ size: number; pulse: number }> = ({ size, pulse }) => (
  <div style={{ width: size, height: size, flexShrink: 0, transform: `scale(${1 + pulse * 0.08})` }}>
    <AssetImg id="py-atom-arrow-right-circle" width={size} height={size} />
  </div>
);

/**
 * The "Reserveer online" button from the feed: aqua pill, white circle with arrow on the left.
 * Grows out of the circle, then a light sweep passes over it and the arrow nudges, as a tap invitation.
 * `variant="navy"` is the "Bekijk locaties" button: navy pill, arrow circle on the right.
 */
export const CtaPill: React.FC<{ text: string; start: number; height?: number; variant?: "aqua" | "navy" }> = ({ text, start, height = 124, variant = "aqua" }) => {
  const frame = useCurrentFrame();
  const grow = enter(frame, start, 22, EASE_OUT);
  const label = enter(frame, start + 8, 16);
  const sweep = interpolate(frame, [start + 26, start + 50], [-30, 130], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const pulse = frame > start + 30 ? Math.max(0, Math.sin((frame - start - 30) / 4.5)) : 0;
  const bg = variant === "aqua" ? "#5CC8DA" : "#14215E";
  const pad = height * 0.12;
  const right = variant === "navy";
  return (
    <div style={{ position: "relative", display: "inline-flex", flexDirection: right ? "row-reverse" : "row", alignItems: "center", gap: height * 0.26, height, padding: right ? `0 ${pad}px 0 ${height * 0.42}px` : `0 ${height * 0.42}px 0 ${pad}px`, borderRadius: height / 2, background: bg, overflow: "hidden", clipPath: `inset(0 ${(1 - grow) * 78}% 0 0 round ${height / 2}px)`, boxShadow: "0 18px 40px rgba(6,14,50,0.28)" }}>
      <ArrowCircle size={height - pad * 2} pulse={pulse} />
      <span style={{ fontFamily: FONT, fontWeight: 500, fontSize: height * 0.36, color: BRAND.wit, whiteSpace: "nowrap", opacity: label, transform: `translateX(${(1 - label) * -20}px)` }}>{text}</span>
      <div style={{ position: "absolute", top: 0, bottom: 0, left: `${sweep}%`, width: "22%", background: "linear-gradient(100deg, transparent, rgba(255,255,255,0.45), transparent)", transform: "skewX(-18deg)" }} />
    </div>
  );
};

/** "voordelig parkeren.nl" with the aqua chevron (py-comp-url-chevron): first part Bold, rest Light. */
export const UrlLine: React.FC<{ url: string; start: number; size?: number; color?: string }> = ({ url, start, size = 46, color = BRAND.wit }) => {
  const frame = useCurrentFrame();
  const p = enter(frame, start, 18);
  const m = url.match(/^(voordelig|parking|reserveer)(.*)$/i);
  const [a, b] = m ? [m[1], m[2]] : [url, ""];
  return (
    <div style={{ display: "inline-flex", alignItems: "center", gap: size * 0.3, fontFamily: FONT, fontSize: size, color, opacity: p, transform: `translateY(${(1 - p) * 16}px)` }}>
      <span><span style={{ fontWeight: 700 }}>{a}</span><span style={{ fontWeight: 300 }}>{b}</span></span>
      <svg width={size * 0.42} height={size * 0.62} viewBox="0 0 30 45"><path d="M7 0L0 7L15 22L0 37L7 45L30 22Z" fill="#69CADA" /></svg>
    </div>
  );
};
