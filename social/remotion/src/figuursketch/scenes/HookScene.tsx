import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { FiguursketchProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { pop, springs } from "../../lib/anim";
import { Headline } from "../../components/Headline";
import { Figure } from "./Figure";

/** Line-up of all beat figures under the question. Used again by the outro with one figure highlighted. */
export const LineUp: React.FC<{ p: FiguursketchProps; frame: number; fps: number; highlight?: number; top: number }> = ({ p, frame, fps, highlight, top }) => {
  const n = p.beats.length;
  const slot = Math.min(260, (STAGE_W - 40) / n);
  return (
    <>
      <div style={{ position: "absolute", left: 60, right: 60, top: top + 560, height: 10, borderRadius: 5, background: p.colors.accent, opacity: 0.5 }} />
      {p.beats.map((b, i) => {
        const s = pop(frame, fps, -8 + i * 3, springs.bouncy);
        const on = highlight === undefined || highlight === i;
        const h = highlight === i ? 460 : 360;
        return (
          <div key={i} style={{ position: "absolute", left: STAGE_W / 2 - (n * slot) / 2 + i * slot, width: slot, top: top + 560 - h, display: "flex", justifyContent: "center", transform: `translateY(${(1 - s) * 200}px)` }}>
            <Figure id={b.figure} height={h} frame={frame + i * 7} motion={on ? b.motion : "bob"} opacity={on ? 1 : 0.25} />
          </div>
        );
      })}
    </>
  );
};

export const HookScene: React.FC<FiguursketchProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: p.colors.bg }}>
      <Stage>
        <Headline text={p.hook.headline} color={p.colors.text} keyColor={p.colors.accent} size={112} delay={-16} stagger={3} top={0} />
        <LineUp p={p} frame={frame} fps={fps} top={520} />
      </Stage>
    </AbsoluteFill>
  );
};

export const OutroScene: React.FC<FiguursketchProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: p.colors.bg }}>
      <Stage>
        <Headline text={p.outro.headline} color={p.colors.text} keyColor={p.colors.accent} size={112} delay={-6} stagger={3} top={0} />
        <LineUp p={p} frame={frame} fps={fps} top={520} highlight={p.outro.highlight} />
      </Stage>
    </AbsoluteFill>
  );
};
