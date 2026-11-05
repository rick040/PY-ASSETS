import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { PrijsrolProps, highlightIndex } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { fadeIn, pop, springs } from "../../lib/anim";
import { Headline } from "../../components/Headline";
import { PriceBubble } from "../../components/PriceBubble";
import { Rich } from "../../lib/rich";
import { FONT } from "../../theme";
import { euro } from "../../lib/euro";

export const T_BUBBLE = 8;
export const T_NOTE = 26;

export const BubbleScene: React.FC<PrijsrolProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const b = pop(frame, fps, T_BUBBLE, springs.pop);
  const r = p.rows.items[highlightIndex(p)];
  const W = 720;
  return (
    <AbsoluteFill style={{ backgroundColor: p.colors.bg }}>
      <Stage>
        <Headline text={p.bubble.headline} color={p.colors.text} keyColor={p.colors.accent} size={86} delay={-16} stagger={3} top={0} />
        <div style={{ position: "absolute", left: (STAGE_W - W) / 2, top: 300, transform: `scale(${Math.min(b, 1.03)}) rotate(${(1 - b) * -12}deg)`, transformOrigin: "50% 95%" }}>
          <PriceBubble width={W} price={euro(r.amount)} label={p.bubble.label} fill={p.colors.accent} text={p.colors.text} />
        </div>
        <div style={{ position: "absolute", left: 60, right: 60, top: 1180, textAlign: "center", fontFamily: FONT, fontSize: 54, color: p.colors.text, opacity: fadeIn(frame, T_NOTE, 12) }}>
          <Rich text={p.bubble.note} keyColor={p.colors.accent} />
        </div>
      </Stage>
    </AbsoluteFill>
  );
};
