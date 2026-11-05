import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { KinetischProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { pop, springs } from "../../lib/anim";
import { Headline } from "../../components/Headline";
import { AssetImg } from "../../components/AssetImg";
import { LabelPill } from "../../components/LabelPill";
import { Bg } from "./Bg";

export const LAP = 42; // frames per lap of the car around the P

/** Car circles the P on an ellipse; behind the P it is smaller and drawn underneath (simple depth). */
const Orbit: React.FC<{ frame: number; accent: string; text: string; label: string; enter: number }> = ({ frame, accent, text, label, enter }) => {
  const cx = STAGE_W / 2;
  const cy = 720;
  const a = (frame / LAP) * Math.PI * 2 + Math.PI / 2; // start in front
  const x = cx + Math.cos(a) * 370;
  const y = cy + 40 + Math.sin(a) * 200;
  const depth = (Math.sin(a) + 1) / 2; // 0 back, 1 front
  const carW = 170 + depth * 110;
  const lap = Math.floor(frame / LAP + 0.25) + 1;
  const car = (
    <div style={{ position: "absolute", left: x - carW / 2, top: y - carW * 0.36, opacity: enter }}>
      <AssetImg id="py-atom-picto-car" width={carW} tint="white" />
    </div>
  );
  return (
    <>
      {depth < 0.5 && car}
      <div style={{ position: "absolute", left: cx - 190, top: cy - 300, width: 380, height: 380, borderRadius: 190, background: accent, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${enter})`, boxShadow: "0 20px 50px rgba(0,0,0,0.25)" }}>
        <AssetImg id="py-atom-symbol-p-roof" height={260} />
      </div>
      {depth >= 0.5 && car}
      <div style={{ position: "absolute", left: 0, right: 0, top: 1190, display: "flex", justifyContent: "center", opacity: enter }}>
        <LabelPill text={`${label} *${lap}*`} bg="rgba(255,255,255,0.14)" fg={text} keyColor={accent} height={130} />
      </div>
    </>
  );
};

export const HookScene: React.FC<KinetischProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = pop(frame, fps, -12, springs.smooth);
  return (
    <Bg top={p.colors.bgTop} bottom={p.colors.bgBottom}>
      <Stage>
        <Headline text={p.hook.headline} color={p.colors.text} keyColor={p.colors.accent} size={112} delay={-24} stagger={3} top={0} />
        {p.hook.visual === "orbit" && <Orbit frame={frame} accent={p.colors.accent} text={p.colors.text} label={p.hook.counterLabel} enter={enter} />}
      </Stage>
    </Bg>
  );
};
