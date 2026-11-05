import React from "react";
import { CHEVRON } from "../lib/paths";
import { FONT } from "../theme";

/** py-comp-url-chevron: URL in Ubuntu Bold with the aqua chevron; `nudge` moves the chevron to invite a tap. */
export const UrlCta: React.FC<{ url: string; color: string; chevron: string; size?: number; nudge?: number }> = ({ url, color, chevron, size = 84, nudge = 0 }) => (
  <div style={{ display: "inline-flex", alignItems: "center", gap: size * 0.35, fontFamily: FONT, fontWeight: 700, fontSize: size, color }}>
    <span>{url}</span>
    <svg width={size * 0.62} height={(size * 0.62 * CHEVRON.h) / CHEVRON.w} viewBox={`0 0 ${CHEVRON.w} ${CHEVRON.h}`} style={{ transform: `translateX(${nudge}px)` }}>
      <path d={CHEVRON.d} fill={chevron} />
    </svg>
  </div>
);
