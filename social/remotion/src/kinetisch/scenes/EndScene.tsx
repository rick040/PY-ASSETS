import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { KinetischProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { pop, springs } from "../../lib/anim";
import { Headline } from "../../components/Headline";
import { AssetImg } from "../../components/AssetImg";
import { Glyph } from "../../components/Glyph";
import { Bg } from "./Bg";

export const T_ARRIVE = 4; // car starts driving in
export const T_PARKED = 34; // car stands under the roof
export const T_CHECK = 40; // check mark

export const EndScene: React.FC<KinetischProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const drive = interpolate(frame, [T_ARRIVE, T_PARKED], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: (t) => 1 - Math.pow(1 - t, 3) });
  const check = pop(frame, fps, T_CHECK, springs.bouncy);
  const cx = STAGE_W / 2;
  const carW = interpolate(drive, [0, 1], [90, 380]);
  const carY = interpolate(drive, [0, 1], [560, 900]);
  return (
    <Bg top={p.colors.bgTop} bottom={p.colors.bgBottom}>
      <Stage>
        <Headline text={p.end.headline} color={p.colors.text} keyColor={p.colors.accent} size={104} delay={-12} stagger={3} top={0} />
        {p.end.visual === "arrive" && (
          <>
            {/* road: two lines converging to the horizon */}
            <svg width={STAGE_W} height={1340} style={{ position: "absolute", left: 0, top: 0 }}>
              <path d={`M${cx - 40} 560 L${cx - 330} 1300 M${cx + 40} 560 L${cx + 330} 1300`} stroke={p.colors.accent} strokeWidth={8} strokeLinecap="round" opacity={0.6} />
            </svg>
            <div style={{ position: "absolute", left: cx - 150, top: 420, width: 300, display: "flex", justifyContent: "center", opacity: 0.95 }}>
              <AssetImg id="py-atom-symbol-p-roof" height={150} />
            </div>
            <div style={{ position: "absolute", left: cx - carW / 2, top: carY }}>
              <AssetImg id="py-atom-picto-car" width={carW} tint="white" />
            </div>
            <div style={{ position: "absolute", left: cx + 170, top: 830, width: 150, height: 150, borderRadius: 75, background: p.colors.accent, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${check})` }}>
              <Glyph name="check" size={96} color={p.colors.text} />
            </div>
          </>
        )}
      </Stage>
    </Bg>
  );
};
