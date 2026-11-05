import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { FiguursketchProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { pop, springs } from "../../lib/anim";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { TopLogo } from "../../v2/Badges";
import { Confetti } from "../../v2/Fx";
import { BRAND } from "../../theme";
import { Figure } from "./Figure";

/** Line-up of all beat figures under the question. Used again by the outro with one figure highlighted. */
export const LineUp: React.FC<{ p: FiguursketchProps; frame: number; fps: number; highlight?: number; top: number }> = ({ p, frame, fps, highlight, top }) => {
  const n = p.beats.length;
  const slot = Math.min(260, (STAGE_W - 40) / n);
  return (
    <>
      <div style={{ position: "absolute", left: 60, right: 60, top: top + 560, height: 10, borderRadius: 5, background: BRAND.blauw, opacity: 0.15 }} />
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

const Head: React.FC<{ text: string; dur: number; delay: number }> = ({ text, dur, delay }) => (
  <>
    <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center" }}>
      <TopLogo width={320} start={-20} dark />
    </div>
    <div style={{ position: "absolute", left: 60, top: 140 }}>
      <Title text={text} color={BRAND.blauw} maxSize={150} width={960} delay={delay} end={dur} />
    </div>
  </>
);

export const HookScene: React.FC<FiguursketchProps & { dur: number }> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Backdrop kind="light" seed="r5hook">
      <Stage>
        <Head text={p.hook.headline} dur={p.dur} delay={-16} />
        <LineUp p={p} frame={frame} fps={fps} top={640} />
      </Stage>
    </Backdrop>
  );
};

export const OutroScene: React.FC<FiguursketchProps & { dur: number }> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Backdrop kind="light" seed="r5out">
      <Stage>
        <Head text={p.outro.headline} dur={p.dur} delay={-2} />
        <LineUp p={p} frame={frame} fps={fps} top={640} highlight={p.outro.highlight} />
      </Stage>
      <Confetti start={10} x={0.3} y={0.62} count={50} colors={[BRAND.oranje, BRAND.aqua, BRAND.blauw]} />
    </Backdrop>
  );
};
