import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { DrieStappenProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { TopLogo } from "../../v2/Badges";
import { Confetti } from "../../v2/Fx";
import { EASE_IN_OUT, enter } from "../../v2/ease";
import { Slagboom } from "../../components/Slagboom";
import { AssetImg } from "../../components/AssetImg";
import { BRAND } from "../../theme";

export const T_OPEN = 14;
export const T_DRIVE = 26;
export const T_FIGURE = 50;

/** Barrier scene. Hook: navy, barrier opens, car drives through. Outcome: GLOW gradient, car drives out, confetti, figure cheers. */
export const GateScene: React.FC<{ p: DrieStappenProps; headline: string; withFigure: boolean; dur: number }> = ({ p, headline, withFigure, dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const open = spring({ frame: frame - T_OPEN, fps, config: { damping: 15, stiffness: 70, mass: 1 } });
  const drive = interpolate(frame, [T_DRIVE, T_DRIVE + 40], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: EASE_IN_OUT });
  const exit = withFigure ? interpolate(frame, [T_DRIVE + 14, T_FIGURE], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: EASE_IN_OUT }) : 0;
  const fig = spring({ frame: frame - T_FIGURE, fps, config: { damping: 11, stiffness: 120 } });
  const carW = interpolate(drive, [0, 1], [240, 520]) + exit * 300;
  const carX = STAGE_W / 2 - carW / 2 + interpolate(drive, [0, 1], [60, 0]);
  const carY = interpolate(drive, [0, 1], [820, 1040]) + exit * 460;
  const road = enter(frame, -10, 24);
  return (
    <Backdrop kind={withFigure ? "glow" : "navy"} seed={withFigure ? "r4out" : "r4hook"}>
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center" }}>
          <TopLogo width={320} start={withFigure ? -20 : -10} />
        </div>
        <div style={{ position: "absolute", left: 60, top: 140 }}>
          <Title text={headline} color={BRAND.wit} maxSize={150} width={960} delay={withFigure ? -2 : -14} end={dur} />
        </div>
        <svg width={STAGE_W} height={1340} style={{ position: "absolute", left: 0, top: 0, opacity: road }}>
          <path d={`M${STAGE_W / 2 - 70} 720 L${STAGE_W / 2 - 430} 1340 M${STAGE_W / 2 + 70} 720 L${STAGE_W / 2 + 430} 1340`} stroke={BRAND.wit} strokeWidth={8} strokeLinecap="round" opacity={0.4} />
        </svg>
        <div style={{ position: "absolute", left: carX, top: carY, opacity: 1 - exit, filter: `blur(${exit * 6}px) drop-shadow(0 20px 30px rgba(4,10,40,0.35))` }}>
          <AssetImg id="py-atom-picto-car" width={carW} tint="white" />
        </div>
        <div style={{ position: "absolute", left: 80, top: 600 }}>
          <Slagboom open={open} width={500} accent={BRAND.aqua} post={BRAND.wit} />
        </div>
        {withFigure && (
          <div style={{ position: "absolute", left: STAGE_W / 2 - 240, top: 780, width: 480, display: "flex", justifyContent: "center", transform: `translateY(${(1 - fig) * 320}px) scale(${0.6 + 0.4 * fig})`, opacity: Math.min(1, fig * 1.5) }}>
            <AssetImg id={p.outcome.figure} width={480} tint="white" style={{ transform: `translateY(${-Math.abs(Math.sin((frame - T_FIGURE) / 5)) * 22}px)` }} />
          </div>
        )}
      </Stage>
      {withFigure && <Confetti start={T_FIGURE + 2} x={0.5} y={0.62} />}
    </Backdrop>
  );
};
