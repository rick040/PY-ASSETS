import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { LocatiekaartProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { pop, springs, fadeIn } from "../../lib/anim";
import { Headline } from "../../components/Headline";
import { PriceBubble } from "../../components/PriceBubble";
import { FONT } from "../../theme";
import { Rich } from "../../lib/rich";

export const T_BUBBLE = 10; // price bubble lands
export const T_NOTE = 30; // small print under the bubble

export const PriceScene: React.FC<LocatiekaartProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const b = pop(frame, fps, T_BUBBLE, springs.pop);
  const W = 760;
  return (
    <AbsoluteFill style={{ backgroundColor: p.colors.bg }}>
      <Stage>
        <Headline text={p.price.headline} color={p.colors.text} keyColor={p.colors.accent} size={88} delay={-20} top={0} />
        <div style={{ position: "absolute", left: (STAGE_W - W) / 2, top: 190, transform: `scale(${Math.min(b, 1.03)}) rotate(${(1 - b) * -12}deg)`, transformOrigin: "50% 95%" }}>
          <PriceBubble width={W} price={p.price.amount} label={p.price.label} fill={p.colors.accent} text={p.colors.text} />
        </div>
        <div style={{ position: "absolute", left: 60, right: 60, top: 1130, textAlign: "center", fontFamily: FONT, fontSize: 56, color: p.colors.text, opacity: fadeIn(frame, T_NOTE, 12) }}>
          <Rich text={p.price.note} keyColor={p.colors.accent} />
        </div>
      </Stage>
    </AbsoluteFill>
  );
};
