import React from "react";
import { useCurrentFrame } from "remotion";
import { KinetischProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { TopLogo } from "../../v2/Badges";
import { enter } from "../../v2/ease";
import { AssetImg } from "../../components/AssetImg";
import { BRAND, FONT } from "../../theme";

export const LAP = 40;

/** Hook: a white car keeps circling the P (with depth), lap counter in a white pill. */
export const HookScene: React.FC<KinetischProps & { dur: number }> = (p) => {
  const frame = useCurrentFrame();
  const inP = enter(frame, -10, 24);
  const cx = STAGE_W / 2;
  const cy = 900;
  const a = (frame / LAP) * Math.PI * 2 + Math.PI / 2;
  const depth = (Math.sin(a) + 1) / 2;
  const carW = 170 + depth * 130;
  const x = cx + Math.cos(a) * 380;
  const y = cy + 30 + Math.sin(a) * 210;
  const lap = Math.floor(frame / LAP + 0.25) + 1;
  const car = (
    <div style={{ position: "absolute", left: x - carW / 2, top: y - carW * 0.36, opacity: inP, filter: `blur(${(1 - depth) * 2}px) drop-shadow(0 ${10 + depth * 20}px 20px rgba(4,10,40,0.35))` }}>
      <AssetImg id="py-atom-picto-car" width={carW} tint="white" />
    </div>
  );
  return (
    <Backdrop kind="navy" seed="r7hook">
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center" }}>
          <TopLogo width={320} />
        </div>
        <div style={{ position: "absolute", left: 60, top: 140 }}>
          <Title text={p.hook.headline} color={BRAND.wit} maxSize={150} width={960} delay={-16} end={p.dur} />
        </div>
        {p.hook.visual === "orbit" && (
          <>
            {/* orbit track */}
            <svg width={STAGE_W} height={1340} style={{ position: "absolute", left: 0, top: 0, opacity: 0.35 * inP }}>
              <ellipse cx={cx} cy={cy + 30} rx={380} ry={210} fill="none" stroke={BRAND.aqua} strokeWidth={6} strokeDasharray="2 22" strokeLinecap="round" />
            </svg>
            {depth < 0.5 && car}
            <div style={{ position: "absolute", left: cx - 175, top: cy - 230, width: 350, height: 350, borderRadius: 175, background: BRAND.aqua, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${inP})`, boxShadow: "0 0 80px rgba(50,185,205,0.45), 0 24px 60px rgba(4,10,40,0.35)" }}>
              <AssetImg id="py-atom-symbol-p-roof" height={240} />
            </div>
            {depth >= 0.5 && car}
            <div style={{ position: "absolute", left: 0, right: 0, top: 1220, display: "flex", justifyContent: "center", opacity: inP }}>
              <div style={{ height: 110, padding: "0 46px", borderRadius: 55, background: BRAND.wit, display: "flex", alignItems: "center", gap: 18, fontFamily: FONT, fontSize: 52, color: BRAND.blauw }}>
                {p.hook.counterLabel} <b style={{ fontVariantNumeric: "tabular-nums" }}>{lap}</b>
              </div>
            </div>
          </>
        )}
      </Stage>
    </Backdrop>
  );
};
