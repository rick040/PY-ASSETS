import React from "react";
import { useCurrentFrame } from "remotion";
import { evolvePath } from "@remotion/paths";
import { LooprouteProps } from "../schema";
import { Stage } from "../../lib/layout";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { TopLogo } from "../../v2/Badges";
import { enter, leave, EASE_OUT } from "../../v2/ease";
import { AssetImg } from "../../components/AssetImg";
import { BRAND, FONT } from "../../theme";

export const T_ROW0 = 14;
export const T_ROW_STEP = 8;

/**
 * Walking minutes per location: white cards on a dotted route line, minutes count up, and a bar shows the
 * distance relative to the farthest location.
 */
export const RouteScene: React.FC<LooprouteProps & { dur: number }> = (p) => {
  const frame = useCurrentFrame();
  const ds = p.route.destinations;
  const max = Math.max(...ds.map((d) => d.minutes), 1);
  const out = leave(frame, p.dur - 4, 12);
  const H = ds.length > 5 ? 124 : 144;
  const gap = ds.length > 5 ? 24 : 32;
  const top = 500;
  const lineLen = (ds.length - 1) * (H + gap);
  const line = `M 0 0 L 0 ${lineLen}`;
  const { strokeDasharray, strokeDashoffset } = evolvePath(enter(frame, T_ROW0, ds.length * T_ROW_STEP + 10), line);
  return (
    <Backdrop kind="navy" seed="r3route">
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center" }}>
          <TopLogo width={320} start={-20} />
        </div>
        <div style={{ position: "absolute", left: 60, top: 150 }}>
          <Title text={p.route.title} color={BRAND.wit} maxSize={130} width={960} delay={-4} end={p.dur} />
        </div>
        <svg width={40} height={lineLen + 20} style={{ position: "absolute", left: 50 + H / 2 - 20, top: top + H / 2, overflow: "visible", opacity: 1 - out }}>
          <path d={line} transform="translate(20 0)" stroke={BRAND.aqua} strokeWidth={8} strokeLinecap="round" fill="none" strokeDasharray={strokeDasharray} strokeDashoffset={strokeDashoffset} />
        </svg>
        {ds.map((d, i) => {
          const e = enter(frame, T_ROW0 + i * T_ROW_STEP, 22);
          const bar = enter(frame, T_ROW0 + i * T_ROW_STEP + 8, 26, EASE_OUT);
          const shown = bar >= 1 ? d.minutes : Math.round(d.minutes * bar);
          return (
            <div key={i} style={{ position: "absolute", left: 50, right: 50, top: top + i * (H + gap), height: H, display: "flex", alignItems: "center", gap: 26, opacity: Math.min(1, e * 1.4) * (1 - out), transform: `translateX(${(1 - e) * -80 + out * 40}px)` }}>
              <div style={{ width: H, height: H, borderRadius: H / 2, background: BRAND.aqua, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, boxShadow: "0 10px 24px rgba(4,10,40,0.3)" }}>
                <AssetImg id="py-atom-picto-pedestrian" height={H * 0.55} tint="white" />
              </div>
              <div style={{ flex: 1, height: H, borderRadius: H / 2, background: BRAND.wit, display: "flex", alignItems: "center", padding: `0 ${H * 0.32}px`, gap: 20, boxShadow: "0 14px 30px rgba(4,10,40,0.25)", position: "relative", overflow: "hidden" }}>
                <div style={{ position: "absolute", left: 0, bottom: 0, height: 8, width: `${(d.minutes / max) * 100 * bar}%`, background: BRAND.aqua, opacity: 0.8 }} />
                <span style={{ flex: 1, fontFamily: FONT, fontWeight: 700, fontSize: H * 0.38, color: BRAND.blauw, whiteSpace: "nowrap" }}>{d.name}</span>
                <span style={{ fontFamily: FONT, fontSize: H * 0.36, color: BRAND.blauw, whiteSpace: "nowrap", fontVariantNumeric: "tabular-nums" }}>
                  <b style={{ fontStyle: "italic", fontSize: H * 0.46 }}>{shown}</b> min
                </span>
              </div>
            </div>
          );
        })}
      </Stage>
    </Backdrop>
  );
};
