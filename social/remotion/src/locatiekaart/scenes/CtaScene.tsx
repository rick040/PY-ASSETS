import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { LocatiekaartProps } from "../schema";
import { Stage } from "../../lib/layout";
import { pop, springs, fadeIn } from "../../lib/anim";
import { Headline } from "../../components/Headline";
import { UrlCta } from "../../components/UrlCta";
import { AssetImg } from "../../components/AssetImg";
import { FONT } from "../../theme";

export const T_URL = 14;
export const T_LOGO = 26;

export const CtaScene: React.FC<LocatiekaartProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const url = pop(frame, fps, T_URL, springs.pop);
  const nudge = interpolate(Math.sin((frame - T_URL) / 5), [-1, 1], [0, 14]) * (frame > T_URL + 20 ? 1 : 0);
  const logo = pop(frame, fps, T_LOGO, springs.smooth);
  return (
    <AbsoluteFill style={{ background: `linear-gradient(160deg, ${p.colors.ctaBgFrom} 0%, ${p.colors.ctaBgFrom} 30%, #097BAE 72%, ${p.colors.ctaBgTo} 100%)` }}>
      {/* beeldmerk watermark, aqua at 5 percent (observed print rule 7) */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: 0.06 }}>
        <AssetImg id="py-atom-logo-beeldmerk-white" width={1100} />
      </AbsoluteFill>
      <Stage>
        <Headline text={p.cta.headline} color={p.colors.text} keyColor={p.colors.text} size={124} delay={-10} stagger={3} top={170} />
        <div style={{ position: "absolute", left: 0, right: 0, top: 560, display: "flex", justifyContent: "center", opacity: Math.min(1, url * 1.4), transform: `translateY(${(1 - url) * 40}px)` }}>
          <div style={{ background: "rgba(255,255,255,0.12)", borderRadius: 80, padding: "26px 56px", border: "3px solid rgba(255,255,255,0.35)" }}>
            <UrlCta url={p.cta.url} color={p.colors.text} chevron={p.colors.text} size={80} nudge={nudge} />
          </div>
        </div>
        <div style={{ position: "absolute", left: 0, right: 0, top: 1000, display: "flex", flexDirection: "column", alignItems: "center", gap: 26, opacity: logo, transform: `translateY(${(1 - logo) * 30}px)` }}>
          <AssetImg id="py-atom-logo-horizontal-reverse" width={660} />
          <div style={{ fontFamily: FONT, fontSize: 44, letterSpacing: "0.06em", color: p.colors.text, opacity: fadeIn(frame, T_LOGO + 10, 12) }}>{p.cta.tagline}</div>
        </div>
      </Stage>
    </AbsoluteFill>
  );
};
