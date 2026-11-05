import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { DrieStappenProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { pop, springs } from "../../lib/anim";
import { Headline } from "../../components/Headline";
import { Slagboom } from "../../components/Slagboom";
import { AssetImg } from "../../components/AssetImg";

export const T_OPEN = 14; // barrier starts to open
export const T_DRIVE = 26; // car drives through
export const T_FIGURE = 50; // outcome scene: figure cheers after the car has driven out

/** Barrier opening with a car driving through. Used as the hook (outcome first) and as the outcome scene. */
export const GateScene: React.FC<{ p: DrieStappenProps; headline: string; withFigure: boolean }> = ({ p, headline, withFigure }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const open = pop(frame, fps, T_OPEN, { damping: 12, stiffness: 90, mass: 0.9 });
  const drive = interpolate(frame, [T_DRIVE, T_DRIVE + 40], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: (t) => t * t * (3 - 2 * t) });
  const fig = pop(frame, fps, T_FIGURE, springs.bouncy);
  // hook: the car stops just past the barrier; outcome: it drives on, out of the frame
  const exit = withFigure ? interpolate(frame, [T_DRIVE + 14, T_FIGURE], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
  const carW = interpolate(drive, [0, 1], [240, 520]) + exit * 260;
  const carX = STAGE_W / 2 - carW / 2 + interpolate(drive, [0, 1], [60, 0]);
  const carY = interpolate(drive, [0, 1], [760, 980]) + exit * 420;
  return (
    <AbsoluteFill style={{ backgroundColor: p.colors.bg }}>
      <Stage>
        <Headline text={headline} color={p.colors.text} keyColor={p.colors.accent} size={104} delay={-18} stagger={3} top={0} />
        {/* road */}
        <svg width={STAGE_W} height={1340} style={{ position: "absolute", left: 0, top: 0 }}>
          <path d={`M${STAGE_W / 2 - 80} 640 L${STAGE_W / 2 - 430} 1340 M${STAGE_W / 2 + 80} 640 L${STAGE_W / 2 + 430} 1340`} stroke={p.colors.accent} strokeWidth={8} strokeLinecap="round" opacity={0.5} />
        </svg>
        <div style={{ position: "absolute", left: carX, top: carY, opacity: 1 - exit }}>
          <AssetImg id="py-atom-picto-car" width={carW} tint="white" />
        </div>
        <div style={{ position: "absolute", left: 90, top: 300 }}>
          <Slagboom open={open} width={620} accent={p.colors.accent} post={p.colors.text} />
        </div>
        {withFigure && (
          <div style={{ position: "absolute", left: STAGE_W / 2 - 230, top: 760, width: 460, display: "flex", justifyContent: "center", transform: `translateY(${(1 - fig) * 300}px) scale(${0.6 + 0.4 * fig})`, opacity: Math.min(1, fig * 1.5) }}>
            <AssetImg id={p.outcome.figure} width={460} tint="white" style={{ transform: `translateY(${-Math.abs(Math.sin(frame / 5)) * 20}px)` }} />
          </div>
        )}
      </Stage>
    </AbsoluteFill>
  );
};
