import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { pop } from "../lib/anim";
import { parseRich } from "../lib/rich";
import { FONT } from "../theme";

/** Words pop in one by one. Key phrases ("*...*") are bold in the accent colour, the rest regular (observed print rule 2). */
export const Headline: React.FC<{
  text: string;
  color: string;
  keyColor: string;
  size?: number;
  delay?: number;
  stagger?: number;
  top?: number;
  align?: "left" | "center";
}> = ({ text, color, keyColor, size = 100, delay = 0, stagger = 4, top = 0, align = "center" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  let i = 0;
  return (
    <div style={{ position: "absolute", top, left: 60, right: 60, textAlign: align, fontFamily: FONT, fontSize: size, lineHeight: 1.12, color, letterSpacing: "-0.01em" }}>
      {parseRich(text).map((line, li) => (
        <div key={li} style={{ whiteSpace: "nowrap" }}>
          {line.map((w, wi) => {
            const p = pop(frame, fps, delay + i++ * stagger);
            return (
              <span key={wi} style={{ display: "inline-block", marginRight: "0.26em", opacity: Math.min(1, p * 1.6), transform: `translateY(${(1 - p) * 40}px) scale(${0.85 + 0.15 * p})` }}>
                {w.map((seg, si) => (
                  <span key={si} style={{ fontWeight: seg.key ? 700 : 400, color: seg.key ? keyColor : color }}>{seg.text}</span>
                ))}
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};
