import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { noise2D } from "@remotion/noise";
import { BRAND, FONT } from "../theme";
import { AssetImg } from "../components/AssetImg";
import { enter } from "./ease";
import { useBackdrop } from "./Backdrop";

/** Splits 7.5 into "€7" and ",50"; whole numbers stay "€15". */
const split = (n: number) => {
  if (Number.isInteger(n)) return { main: `€${n}`, cents: "" };
  const [e, c] = n.toFixed(2).split(".");
  return { main: `€${e}`, cents: `,${c}` };
};

/**
 * Round price badge from the feed (white with navy text, or aqua with white text): pops in with one soft
 * overshoot, then floats a little. Cents are set small and raised, as on the Hofplein post.
 */
export const PriceBadge: React.FC<{ amount: number; label: string; start: number; size?: number; tone?: "white" | "aqua"; rotate?: number; float?: boolean }> = ({ amount, label, start, size = 420, tone = "white", rotate = -8, float = true }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - start, fps, config: { damping: 13, stiffness: 120, mass: 0.9 } });
  const fy = float ? noise2D("pb", frame / 50, 0) * 10 : 0;
  const fr = float ? noise2D("pr", 0, frame / 60) * 2 : 0;
  const { main, cents } = split(amount);
  const bg = tone === "white" ? BRAND.wit : BRAND.aqua;
  const fg = tone === "white" ? BRAND.blauw : BRAND.wit;
  const fs = size * (main.length > 3 ? 0.34 : 0.4);
  return (
    <div style={{ width: size, height: size, borderRadius: size / 2, background: bg, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", transform: `translateY(${fy}px) scale(${s}) rotate(${rotate + fr + (1 - s) * -20}deg)`, boxShadow: "0 24px 60px rgba(6,14,50,0.30)", fontFamily: FONT, color: fg }}>
      <div style={{ display: "flex", alignItems: "flex-start", fontWeight: 700, fontStyle: "italic", fontSize: fs, lineHeight: 1, letterSpacing: "-0.02em" }}>
        <span>{main}</span>
        {cents && <span style={{ fontSize: fs * 0.48, marginTop: fs * 0.06 }}>{cents}</span>}
      </div>
      <div style={{ fontSize: size * 0.1, fontWeight: 400, marginTop: size * 0.02 }}>{label}</div>
    </div>
  );
};

/** White pill with a navy pin and the location name in navy Bold, as on the Hofplein post. */
export const PlacePill: React.FC<{ name: string; start: number; height?: number; icon?: boolean }> = ({ name, start, height = 110, icon = true }) => {
  const frame = useCurrentFrame();
  const p = enter(frame, start, 20);
  return (
    <div style={{ display: "inline-flex", alignItems: "center", gap: height * 0.22, height, padding: `0 ${height * 0.42}px 0 ${height * (icon ? 0.32 : 0.42)}px`, borderRadius: height / 2, background: BRAND.wit, fontFamily: FONT, fontWeight: 500, fontSize: height * 0.42, color: BRAND.blauw, whiteSpace: "nowrap", opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * 30}px) scale(${0.92 + 0.08 * p})`, boxShadow: "0 14px 34px rgba(6,14,50,0.22)" }}>
      {icon && (
        <svg width={height * 0.36} height={height * 0.48} viewBox="0 0 30 40"><path d="M15 0C6.7 0 0 6.6 0 14.8C0 25.9 15 40 15 40C15 40 30 25.9 30 14.8C30 6.6 23.3 0 15 0ZM15 20.5C11.8 20.5 9.3 18 9.3 14.8C9.3 11.6 11.8 9.1 15 9.1C18.2 9.1 20.7 11.6 20.7 14.8C20.7 18 18.2 20.5 15 20.5Z" fill={BRAND.blauw} /></svg>
      )}
      {name}
    </div>
  );
};

/**
 * Small logo at the top. Brand rules (Rick, November 2026):
 * - light blue (the cyan GLOW gradient): all white with a white dot (derived -whitedot file; the library's white logo has a hole there);
 * - navy and photo: white with the aqua dot (open reverse logo), never the navy ring fill;
 * - the pale "light" backdrop: the colour logo, because white disappears on it.
 */
export const TopLogo: React.FC<{ start?: number; width?: number }> = ({ start = -10, width = 300 }) => {
  const frame = useCurrentFrame();
  const kind = useBackdrop();
  const p = enter(frame, start, 18);
  const id = kind === "glow" ? "py-atom-logo-horizontal-reverse-whitedot" : kind === "light" ? "py-atom-logo-horizontal-color" : "py-atom-logo-horizontal-reverse-open";
  return (
    <div style={{ opacity: p, transform: `translateY(${(1 - p) * -14}px)` }}>
      <AssetImg id={id} width={width} />
    </div>
  );
};
