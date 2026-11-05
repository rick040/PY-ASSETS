import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { KinetischProps } from "../schema";
import { Stage } from "../../lib/layout";
import { pop, springs } from "../../lib/anim";
import { Headline } from "../../components/Headline";
import { Glyph } from "../../components/Glyph";
import { Rich } from "../../lib/rich";
import { FONT } from "../../theme";
import { Bg } from "./Bg";

export const T_LINE0 = 14;
export const T_LINE_STEP = 18;

export const LinesScene: React.FC<KinetischProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const n = p.lines.items.length;
  const rowH = 230;
  const top = 300 + ((4 - n) * rowH) / 2;
  return (
    <Bg top={p.colors.bgTop} bottom={p.colors.bgBottom}>
      <Stage>
        <Headline text={p.lines.title} color={p.colors.text} keyColor={p.colors.accent} size={104} delay={-12} top={20} />
        {p.lines.items.map((it, i) => {
          const s = pop(frame, fps, T_LINE0 + i * T_LINE_STEP, springs.bouncy);
          return (
            <div key={i} style={{ position: "absolute", left: 80, right: 30, top: top + i * rowH, height: 190, display: "flex", alignItems: "center", gap: 48, opacity: Math.min(1, s * 1.5), transform: `translateX(${(1 - s) * 140}px)` }}>
              <div style={{ width: 180, height: 180, borderRadius: 90, border: `6px solid ${p.colors.accent}`, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${0.5 + 0.5 * s}) rotate(${(1 - s) * -30}deg)`, flexShrink: 0 }}>
                <Glyph name={it.icon} size={104} color={p.colors.text} />
              </div>
              <div style={{ fontFamily: FONT, fontSize: 84, color: p.colors.text, whiteSpace: "nowrap" }}>
                <Rich text={it.text} keyColor={p.colors.accent} />
              </div>
            </div>
          );
        })}
      </Stage>
    </Bg>
  );
};
