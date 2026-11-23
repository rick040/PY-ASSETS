import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig, spring } from "remotion";
import { KinetischProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { TopLogo } from "../../v2/Badges";
import { EASE_OUT } from "../../v2/ease";
import { AssetImg } from "../../components/AssetImg";
import { Glyph } from "../../components/Glyph";
import { BRAND } from "../../theme";

export const T_ARRIVE = 4;
export const T_PARKED = 38;
export const T_CHECK = 42;

/** The answer on the GLOW gradient: the car drives straight in under the roof, check mark. */
export const EndScene: React.FC<KinetischProps & { dur: number }> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const drive = interpolate(frame, [T_ARRIVE, T_PARKED], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: EASE_OUT });
  const check = spring({ frame: frame - T_CHECK, fps, config: { damping: 12, stiffness: 140 } });
  const cx = STAGE_W / 2;
  const carW = interpolate(drive, [0, 1], [80, 400]);
  const carY = interpolate(drive, [0, 1], [700, 1000]);
  return (
    <Backdrop kind="glow" seed="r7end">
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center" }}>
          <TopLogo width={320} start={-20} />
        </div>
        <div style={{ position: "absolute", left: 60, top: 140 }}>
          <Title text={p.end.headline} color={BRAND.wit} maxSize={140} width={960} delay={-4} end={p.dur} />
        </div>
        {p.end.visual === "arrive" && (
          <>
            <svg width={STAGE_W} height={1340} style={{ position: "absolute", left: 0, top: 0 }}>
              <path d={`M${cx - 30} 690 L${cx - 360} 1340 M${cx + 30} 690 L${cx + 360} 1340`} stroke={BRAND.wit} strokeWidth={8} strokeLinecap="round" opacity={0.45} />
              <path d={`M${cx} 720 L${cx} 1340`} stroke={BRAND.wit} strokeWidth={8} strokeDasharray="40 50" strokeDashoffset={-frame * 12 * (1 - drive)} opacity={0.35} />
            </svg>
            <div style={{ position: "absolute", left: cx - 90, top: 560, opacity: 0.95 }}>
              <AssetImg id="py-atom-symbol-p-roof" height={150} />
            </div>
            <div style={{ position: "absolute", left: cx - carW / 2, top: carY, filter: `blur(${(1 - drive) * 3}px) drop-shadow(0 20px 30px rgba(4,10,40,0.35))` }}>
              <AssetImg id="py-atom-picto-car" width={carW} tint="white" />
            </div>
            <div style={{ position: "absolute", left: cx + 190, top: 900, width: 150, height: 150, borderRadius: 75, background: BRAND.wit, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${check})`, boxShadow: "0 14px 34px rgba(4,10,40,0.3)" }}>
              <Glyph name="check" size={96} color={BRAND.aqua} />
            </div>
          </>
        )}
      </Stage>
    </Backdrop>
  );
};
