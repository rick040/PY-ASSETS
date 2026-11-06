import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { DrieStappenProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { TopLogo } from "../../v2/Badges";
import { Sunburst } from "../../v2/Fx";
import { enter, leave } from "../../v2/ease";
import { Glyph } from "../../components/Glyph";
import { BRAND, FONT } from "../../theme";

export const T_CARD = 6;
export const T_TEXT = 10;

/** One step on the pale feed background (as the Easter post): number badge, illustration in a white disc over rays, navy text. */
export const StepScene: React.FC<{ p: DrieStappenProps; index: number; dur: number }> = ({ p, index, dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const st = p.steps[index];
  const card = spring({ frame: frame - T_CARD, fps, config: { damping: 14, stiffness: 110, mass: 0.9 } });
  const num = enter(frame, 0, 16);
  const out = leave(frame, dur - 2, 10);
  const D = 600;
  const cy = 820;
  return (
    <Backdrop kind="light" seed={`r4s${index}`}>
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center" }}>
          <TopLogo width={320} start={-20} />
        </div>
        {/* progress */}
        <div style={{ position: "absolute", right: 60, top: 170, display: "flex", gap: 14 }}>
          {p.steps.map((_, i) => (
            <div key={i} style={{ width: i === index ? 80 : 24, height: 24, borderRadius: 12, background: i <= index ? BRAND.blauw : "rgba(26,53,128,0.2)" }} />
          ))}
        </div>
        <div style={{ position: "absolute", left: 60, top: 130, fontFamily: FONT, fontWeight: 700, fontSize: 210, lineHeight: 1, color: BRAND.aqua, opacity: num, transform: `translateY(${(1 - num) * 60}px)` }}>
          {index + 1}
        </div>
        <div style={{ position: "absolute", left: STAGE_W / 2 - 420, top: cy - 420, width: 840, height: 840 }}>
          <Sunburst start={T_CARD + 4} size={840} color={BRAND.aqua} opacity={0.6} />
        </div>
        <div style={{ position: "absolute", left: STAGE_W / 2 - D / 2, top: cy - D / 2, width: D, height: D, borderRadius: "50%", background: BRAND.wit, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${card * (1 - out * 0.15)}) rotate(${(1 - card) * -12}deg)`, opacity: 1 - out, boxShadow: "0 30px 70px rgba(26,53,128,0.22)" }}>
          <div style={{ transform: `rotate(${Math.sin(frame / 12) * 3}deg)` }}>
            <Glyph name={st.illustration} size={D * 0.6} color={BRAND.blauw} tint="none" />
          </div>
        </div>
        <div style={{ position: "absolute", left: 60, top: 1170 }}>
          <Title text={st.text} color={BRAND.blauw} maxSize={92} width={960} delay={T_TEXT} end={dur} />
        </div>
      </Stage>
    </Backdrop>
  );
};
