import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { DrieStappenProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { fadeIn, pop, springs } from "../../lib/anim";
import { Glyph } from "../../components/Glyph";
import { Rich } from "../../lib/rich";
import { FONT } from "../../theme";

export const T_CARD = 4;
export const T_TEXT = 12;

export const StepScene: React.FC<{ p: DrieStappenProps; index: number }> = ({ p, index }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const st = p.steps[index];
  const card = pop(frame, fps, T_CARD, springs.bouncy);
  const num = pop(frame, fps, 0, springs.pop);
  const D = 660;
  const ring = (frame % 36) / 36; // pulse ring loop
  const cardBg = st.card === "accent" ? p.colors.accent : p.colors.card;
  return (
    <AbsoluteFill style={{ backgroundColor: p.colors.bg }}>
      <Stage>
        {/* progress */}
        <div style={{ position: "absolute", left: 0, right: 0, top: 10, display: "flex", justifyContent: "center", gap: 18 }}>
          {p.steps.map((_, i) => (
            <div key={i} style={{ width: i === index ? 90 : 26, height: 26, borderRadius: 13, background: i <= index ? p.colors.accent : "rgba(255,255,255,0.25)" }} />
          ))}
        </div>
        {/* step number */}
        <div style={{ position: "absolute", left: 0, right: 0, top: 90, display: "flex", justifyContent: "center" }}>
          <div style={{ width: 170, height: 170, borderRadius: 85, background: p.colors.accent, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: FONT, fontWeight: 700, fontSize: 120, color: p.colors.text, transform: `scale(${num})` }}>{index + 1}</div>
        </div>
        {/* illustration card with a pulse ring */}
        <div style={{ position: "absolute", left: STAGE_W / 2 - D / 2, top: 330, width: D, height: D }}>
          <div style={{ position: "absolute", inset: -40 * ring, borderRadius: "50%", border: `6px solid ${p.colors.accent}`, opacity: (1 - ring) * 0.7 * card }} />
          <div style={{ position: "absolute", inset: 0, borderRadius: "50%", background: cardBg, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${card}) rotate(${(1 - card) * -15}deg)`, boxShadow: "0 24px 60px rgba(0,0,0,0.28)" }}>
            <div style={{ transform: `rotate(${interpolate(Math.sin(frame / 10), [-1, 1], [-4, 4])}deg)` }}>
              <Glyph name={st.illustration} size={D * 0.62} color={p.colors.bg} tint="none" />
            </div>
          </div>
        </div>
        <div style={{ position: "absolute", left: 40, right: 40, top: 1090, textAlign: "center", fontFamily: FONT, fontSize: 92, lineHeight: 1.12, color: p.colors.text, opacity: fadeIn(frame, T_TEXT, 10), transform: `translateY(${(1 - fadeIn(frame, T_TEXT, 10)) * 30}px)` }}>
          <Rich text={st.text} keyColor={p.colors.accent} />
        </div>
      </Stage>
    </AbsoluteFill>
  );
};
