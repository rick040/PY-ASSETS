import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { Stage } from "../lib/layout";
import { fadeIn, pop, springs } from "../lib/anim";
import { FONT } from "../theme";
import { AssetImg } from "./AssetImg";
import { Headline } from "./Headline";
import { UrlCta } from "./UrlCta";

export type EndCardProps = { headline: string; url: string; tagline: string };

export const T_URL = 14;
export const T_LOGO = 26;

/** Shared end card: verloop, beeldmerk watermark, headline, parkingyou.nl with chevron, open reverse logo (white + aqua only) and tagline. */
export const EndCard: React.FC<{ cta: EndCardProps; text: string; from: string; to: string }> = ({ cta, text, from, to }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const url = pop(frame, fps, T_URL, springs.pop);
  const nudge = interpolate(Math.sin((frame - T_URL) / 5), [-1, 1], [0, 14]) * (frame > T_URL + 20 ? 1 : 0);
  const logo = pop(frame, fps, T_LOGO, springs.smooth);
  return (
    <AbsoluteFill style={{ background: `linear-gradient(160deg, ${from} 0%, ${from} 30%, #097BAE 72%, ${to} 100%)` }}>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: 0.06 }}>
        <AssetImg id="py-atom-logo-beeldmerk-white" width={1100} />
      </AbsoluteFill>
      <Stage>
        <Headline text={cta.headline} color={text} keyColor={text} size={124} delay={-10} stagger={3} top={170} />
        <div style={{ position: "absolute", left: 0, right: 0, top: 560, display: "flex", justifyContent: "center", opacity: Math.min(1, url * 1.4), transform: `translateY(${(1 - url) * 40}px)` }}>
          <div style={{ background: "rgba(255,255,255,0.12)", borderRadius: 80, padding: "26px 56px", border: "3px solid rgba(255,255,255,0.35)" }}>
            <UrlCta url={cta.url} color={text} chevron={text} size={80} nudge={nudge} />
          </div>
        </div>
        <div style={{ position: "absolute", left: 0, right: 0, top: 1000, display: "flex", flexDirection: "column", alignItems: "center", gap: 26, opacity: logo, transform: `translateY(${(1 - logo) * 30}px)` }}>
          <AssetImg id="py-atom-logo-horizontal-reverse-open" width={660} />
          <div style={{ fontFamily: FONT, fontSize: 44, letterSpacing: "0.06em", color: text, opacity: fadeIn(frame, T_LOGO + 10, 12) }}>{cta.tagline}</div>
        </div>
      </Stage>
    </AbsoluteFill>
  );
};
