import React from "react";
import { AbsoluteFill } from "remotion";
import { Backdrop, BackdropKind } from "../v2/Backdrop";
import { Title, fitSize } from "../v2/Title";
import { AssetImg } from "../components/AssetImg";
import { Rich } from "../lib/rich";
import { Q } from "./qa";
import type { Ground, Theme } from "./themes";

/**
 * Theme-aware building blocks for archetypes. They are static (every entrance has finished at frame 0),
 * wrapped in <Q> for QA, and take colours from the theme only. The v2 kit stays untouched for the reels.
 */

const SETTLED = -120;

/** Visible text of a rich string: no key markers, line breaks as spaces. */
export const plain = (t: string) => t.replace(/\*/g, "").replace(/\s*\n\s*/g, " "); // start frame far before 0, so animated kit parts are at rest

export const GroundFill: React.FC<{ theme: Theme; ground: Ground; seed: string; media?: string; children: React.ReactNode }> = ({ theme, ground, seed, media, children }) => {
  if (theme.id === "feed") {
    const kind: BackdropKind = ground === "white" ? "light" : (ground as BackdropKind);
    return (
      <Backdrop kind={kind} seed={seed} media={media}>
        <AbsoluteFill>{children}</AbsoluteFill>
      </Backdrop>
    );
  }
  throw new Error(`GroundFill: theme ${theme.id} not built yet`);
};

export const Logo: React.FC<{ theme: Theme; ground: Ground; width: number }> = ({ theme, ground, width }) => {
  const id = theme.ink(ground).logo;
  return (
    <Q name="logo" kind="logo" variant={id}>
      <AssetImg id={id} width={width} />
    </Q>
  );
};

export const Headline: React.FC<{ theme: Theme; ground: Ground; text: string; width: number; maxSize: number; align?: "left" | "center" }> = ({ theme, ground, text, width, maxSize, align = "left" }) => {
  const ink = theme.ink(ground);
  const size = fitSize(text, width, maxSize);
  return (
    <Q name="headline" kind="text" fg={ink.text} size={size} bold label={plain(text)}>
      <Title text={text} color={ink.text} keyColor={ink.key} width={width} maxSize={maxSize} delay={SETTLED} align={align} />
    </Q>
  );
};

export const Copy: React.FC<{ theme: Theme; ground: Ground; name: string; text: string; size: number; width: number; opacity?: number; align?: "left" | "center" }> = ({ theme, ground, name, text, size, width, opacity = 0.92, align = "left" }) => {
  const ink = theme.ink(ground);
  return (
    <Q name={name} kind="text" fg={ink.text} size={size} label={plain(text)}>
      <div style={{ width, fontFamily: theme.font, fontSize: size, lineHeight: 1.3, color: ink.text, opacity, textAlign: align }}>
        <Rich text={text} keyColor={ink.text} />
      </div>
    </Q>
  );
};

/** "parkingyou.nl" with the aqua chevron (decision S1). Token aqua, not the observed light aqua of the v2 UrlLine. */
export const Url: React.FC<{ theme: Theme; ground: Ground; size: number }> = ({ theme, ground, size }) => {
  const ink = theme.ink(ground);
  const [a, b] = theme.url.split(/(?=\.)/);
  return (
    <Q name="url" kind="text" fg={ink.text} size={size} bold>
      <div style={{ display: "inline-flex", alignItems: "center", gap: size * 0.3, fontFamily: theme.font, fontSize: size, color: ink.text }}>
        <span><span style={{ fontWeight: 700 }}>{a}</span><span style={{ fontWeight: 400 }}>{b}</span></span>
        <svg width={size * 0.42} height={size * 0.62} viewBox="0 0 30 45"><path d="M7 0L0 7L15 22L0 37L7 45L30 22Z" fill={theme.palette.aqua} /></svg>
      </div>
    </Q>
  );
};

/** The beeldmerk as a large, faint background mark (observed rule 7: watermark). */
export const Watermark: React.FC<{ theme: Theme; ground: Ground; size: number; opacity?: number }> = ({ theme, ground, size, opacity = 0.1 }) => (
  <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity }}>
    <Q name="watermark" kind="graphic" variant="py-atom-logo-beeldmerk-white" fg={theme.palette.wit}>
      <AssetImg id="py-atom-logo-beeldmerk-white" width={size} />
    </Q>
  </AbsoluteFill>
);

/** Absolute placement helper. */
export const At: React.FC<{ x: number; y: number; w?: number; children: React.ReactNode; anchor?: "top" | "bottom" }> = ({ x, y, w, children, anchor = "top" }) => (
  <div style={{ position: "absolute", left: x, width: w, ...(anchor === "top" ? { top: y } : { bottom: y }) }}>{children}</div>
);
