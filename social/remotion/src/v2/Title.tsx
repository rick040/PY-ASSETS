import React from "react";
import { useCurrentFrame } from "remotion";
import { parseRich } from "../lib/rich";
import { FONT } from "../theme";
import { enter, leave, EASE_OUT } from "./ease";

// Average advance widths of Ubuntu (em), used to fit each headline to the stage width without measuring in the DOM.
const AVG_REG = 0.53;
const AVG_BOLD = 0.57;

export const fitSize = (text: string, maxWidth: number, max: number, min = 56) => {
  const lines = parseRich(text);
  let widest = 0;
  for (const line of lines) {
    let w = 0;
    line.forEach((word, i) => {
      word.forEach((seg) => (w += seg.text.length * (seg.key ? AVG_BOLD : AVG_REG)));
      if (i < line.length - 1) w += 0.28;
    });
    widest = Math.max(widest, w);
  }
  return Math.max(min, Math.min(max, Math.floor(maxWidth / Math.max(widest, 1))));
};

/**
 * Feed-style headline: big, white, key words Bold (weight contrast, same colour by default).
 * Each line rises out of a mask with an expo-out curve, staggered; lines leave upwards before the scene ends.
 */
export const Title: React.FC<{
  text: string;
  color: string;
  keyColor?: string;
  align?: "left" | "center";
  maxSize?: number;
  width?: number;
  delay?: number;
  stagger?: number;
  end?: number; // scene-local frame where the title has left; omit to stay
  lineHeight?: number;
}> = ({ text, color, keyColor, align = "left", maxSize = 132, width = 960, delay = 0, stagger = 5, end, lineHeight = 1.06 }) => {
  const frame = useCurrentFrame();
  const size = fitSize(text, width, maxSize);
  const lines = parseRich(text);
  return (
    <div style={{ width, fontFamily: FONT, fontSize: size, lineHeight, color, textAlign: align, letterSpacing: "-0.015em" }}>
      {lines.map((line, li) => {
        const p = enter(frame, delay + li * stagger, 22, EASE_OUT);
        const out = end === undefined ? 0 : leave(frame, end - (lines.length - 1 - li) * 2, 12);
        return (
          <div key={li} style={{ overflow: "hidden", paddingBottom: size * 0.12, marginBottom: -size * 0.12 }}>
            <div style={{ whiteSpace: "nowrap", transform: `translateY(${(1 - p) * 105 - out * 105}%)`, opacity: Math.min(1, p * 1.2) * (1 - out * 0.6) }}>
              {line.map((word, wi) => (
                <span key={wi} style={{ marginRight: "0.26em" }}>
                  {word.map((seg, si) => (
                    <span key={si} style={{ fontWeight: seg.key ? 700 : 400, color: seg.key ? keyColor ?? color : color }}>{seg.text}</span>
                  ))}
                </span>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
};
