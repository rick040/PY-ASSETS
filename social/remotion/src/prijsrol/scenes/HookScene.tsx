import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { PrijsrolProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { pop, springs } from "../../lib/anim";
import { Headline } from "../../components/Headline";
import { LocationPill } from "../../components/LocationPill";
import { PriceBubble } from "../../components/PriceBubble";
import { euro } from "../../lib/euro";

export const T_PILL = 12;

/** Three small price bubbles that swing like price tags: the question before the answer. */
export const HookScene: React.FC<PrijsrolProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pill = pop(frame, fps, T_PILL, springs.bouncy);
  const items = p.rows.items;
  const w = Math.min(330, (STAGE_W - 60) / items.length);
  return (
    <AbsoluteFill style={{ backgroundColor: p.colors.bg }}>
      <Stage>
        <Headline text={p.hook.headline} color={p.colors.text} keyColor={p.colors.accent} size={118} delay={-24} stagger={3} top={0} />
        {items.map((it, i) => {
          const s = pop(frame, fps, -14 + i * 4, springs.bouncy);
          const swing = Math.sin((frame + i * 9) / 9) * 5;
          return (
            <div key={i} style={{ position: "absolute", left: STAGE_W / 2 - (items.length * w) / 2 + i * w, top: 470 + (i % 2) * 100, width: w, display: "flex", justifyContent: "center", transform: `scale(${s}) rotate(${swing}deg)`, transformOrigin: "50% 0%" }}>
              <PriceBubble width={w - 20} price={euro(it.amount)} label="" fill={i === items.length - 1 ? p.colors.accent : "rgba(255,255,255,0.16)"} text={p.colors.text} />
            </div>
          );
        })}
        <div style={{ position: "absolute", left: 0, right: 0, top: 1140, display: "flex", justifyContent: "center", opacity: Math.min(1, pill * 1.5), transform: `scale(${0.7 + 0.3 * pill})` }}>
          <LocationPill name={p.location.name} city={p.location.city} bg={p.colors.accent} fg={p.colors.text} accent={p.colors.bg} height={124} />
        </div>
      </Stage>
    </AbsoluteFill>
  );
};
