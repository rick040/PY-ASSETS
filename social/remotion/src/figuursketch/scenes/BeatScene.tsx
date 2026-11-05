import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { FiguursketchProps } from "../schema";
import { Stage } from "../../lib/layout";
import { fadeIn, pop, springs } from "../../lib/anim";
import { Glyph } from "../../components/Glyph";
import { Rich } from "../../lib/rich";
import { FONT } from "../../theme";
import { Figure } from "./Figure";

export const T_TITLE = 6;
export const T_PROP = 14;
export const T_LINE = 18;

export const BeatScene: React.FC<{ p: FiguursketchProps; index: number }> = ({ p, index }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const b = p.beats[index];
  const title = pop(frame, fps, T_TITLE, springs.pop);
  const prop = pop(frame, fps, T_PROP, springs.bouncy);
  return (
    <AbsoluteFill style={{ backgroundColor: p.colors.bg }}>
      <Stage>
        {/* counter */}
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, textAlign: "center", fontFamily: FONT, fontSize: 52, fontWeight: 500, color: p.colors.accent, letterSpacing: "0.08em" }}>
          {index + 1} / {p.beats.length}
        </div>
        {/* title card */}
        <div style={{ position: "absolute", left: 60, right: 60, top: 90, padding: "34px 40px", borderRadius: 48, background: p.colors.card, textAlign: "center", boxShadow: "0 16px 40px rgba(26,53,128,0.12)", opacity: Math.min(1, title * 1.4), transform: `translateY(${(1 - title) * -40}px)` }}>
          <div style={{ fontFamily: FONT, fontSize: 84, lineHeight: 1.1, color: p.colors.text, whiteSpace: "nowrap" }}>
            <Rich text={b.title} keyColor={p.colors.accent} />
          </div>
          <div style={{ fontFamily: FONT, fontSize: 56, marginTop: 12, color: p.colors.text, opacity: fadeIn(frame, T_LINE, 10) }}>{b.line}</div>
        </div>
        {/* floor */}
        <div style={{ position: "absolute", left: 120, right: 120, top: 1290, height: 10, borderRadius: 5, background: p.colors.accent, opacity: 0.5 }} />
        <div style={{ position: "absolute", left: 140, top: 1290 - 820, width: 520, display: "flex", justifyContent: "center" }}>
          <Figure id={b.figure} height={820} frame={frame} motion={b.motion} />
        </div>
        {b.prop && (
          <div style={{ position: "absolute", left: 660, top: 560, width: 300, height: 300, borderRadius: 150, background: p.colors.card, display: "flex", alignItems: "center", justifyContent: "center", boxShadow: "0 16px 40px rgba(26,53,128,0.15)", transform: `scale(${prop}) rotate(${(1 - prop) * 20}deg)` }}>
            <Glyph name={b.prop} size={190} color={p.colors.accent} tint="none" />
          </div>
        )}
      </Stage>
    </AbsoluteFill>
  );
};
