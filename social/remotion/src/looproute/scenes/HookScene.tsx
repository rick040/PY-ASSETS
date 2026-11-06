import React from "react";
import { useCurrentFrame } from "remotion";
import { evolvePath } from "@remotion/paths";
import { LooprouteProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { TopLogo } from "../../v2/Badges";
import { enter, EASE_IN_OUT } from "../../v2/ease";
import { AssetImg } from "../../components/AssetImg";
import { BRAND, FONT } from "../../theme";

// The walking route: a curve from the parking (P) to the event (pin), drawn while a figure walks along it.
const ROUTE = "M 170 1210 C 330 1210 300 980 520 960 C 740 940 700 760 900 720";
export const T_ROUTE = 8;
export const T_ROUTE_DUR = 64;

/** Point on the route at progress t (cubic Bezier segments, two pieces). */
const pointAt = (t: number) => {
  const segs = [
    [170, 1210, 330, 1210, 300, 980, 520, 960],
    [520, 960, 740, 940, 700, 760, 900, 720],
  ];
  const s = Math.min(1, Math.floor(t * 2));
  const u = Math.min(1, t * 2 - s);
  const [x0, y0, x1, y1, x2, y2, x3, y3] = segs[Math.min(s, 1)];
  const k = 1 - u;
  return {
    x: k * k * k * x0 + 3 * k * k * u * x1 + 3 * k * u * u * x2 + u * u * u * x3,
    y: k * k * k * y0 + 3 * k * k * u * y1 + 3 * k * u * u * y2 + u * u * u * y3,
  };
};

export const HookScene: React.FC<LooprouteProps & { dur: number }> = (p) => {
  const frame = useCurrentFrame();
  const t = enter(frame, T_ROUTE, T_ROUTE_DUR, EASE_IN_OUT);
  const { strokeDasharray, strokeDashoffset } = evolvePath(t, ROUTE);
  const pos = pointAt(t);
  const label = enter(frame, 10, 18);
  const pin = enter(frame, T_ROUTE + T_ROUTE_DUR - 10, 18);
  const parkIn = enter(frame, -6, 18);
  const step = Math.sin(frame / 3.2);
  return (
    <Backdrop kind="glow" seed="r3hook">
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center", alignItems: "center", gap: 26 }}>
          <TopLogo width={300} />
          {p.hook.partner && (
            <>
              <span style={{ fontFamily: FONT, fontSize: 44, color: BRAND.wit, opacity: label }}>×</span>
              <span style={{ fontFamily: FONT, fontWeight: 700, fontSize: 52, letterSpacing: "-0.01em", color: BRAND.wit, opacity: label, lineHeight: 0.9 }}>{p.hook.partner.toUpperCase().replace(" ", " ")}</span>
            </>
          )}
        </div>
        <div style={{ position: "absolute", left: 60, top: 150 }}>
          <Title text={p.hook.headline} color={BRAND.wit} maxSize={150} width={960} delay={-14} end={p.dur} />
        </div>
        {p.hook.partnerLabel && (
          <div style={{ position: "absolute", left: 66, top: 500, fontFamily: FONT, fontSize: 46, color: BRAND.wit, opacity: label * 0.9 }}>{p.hook.partnerLabel}</div>
        )}
        <svg width={STAGE_W} height={1340} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
          <path d={ROUTE} fill="none" stroke="rgba(255,255,255,0.25)" strokeWidth={14} strokeLinecap="round" strokeDasharray="2 28" />
          <path d={ROUTE} fill="none" stroke={BRAND.wit} strokeWidth={14} strokeLinecap="round" strokeDasharray={strokeDasharray} strokeDashoffset={strokeDashoffset} />
        </svg>
        {/* parking: white disc with the P */}
        <div style={{ position: "absolute", left: 170 - 95, top: 1210 - 95, width: 190, height: 190, borderRadius: 95, background: BRAND.blauw, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${parkIn})`, boxShadow: "0 18px 40px rgba(6,14,50,0.3)" }}>
          <AssetImg id="py-atom-symbol-p-roof" height={120} />
        </div>
        {/* event: pin pops when the walker arrives */}
        <div style={{ position: "absolute", left: 900 - 70, top: 720 - 170, width: 140, transform: `scale(${0.4 + 0.6 * pin}) translateY(${(1 - pin) * 30}px)`, transformOrigin: "50% 100%", opacity: pin }}>
          <svg width={140} height={186} viewBox="0 0 30 40"><path d="M15 0C6.7 0 0 6.6 0 14.8C0 25.9 15 40 15 40C15 40 30 25.9 30 14.8C30 6.6 23.3 0 15 0Z" fill={BRAND.wit} /><circle cx={15} cy={14.8} r={5.6} fill={BRAND.aqua} /></svg>
        </div>
        {/* walker */}
        <div style={{ position: "absolute", left: pos.x - 80, top: pos.y - 270, width: 160, transform: `translateY(${-Math.abs(step) * 8}px) rotate(${step * 2}deg)`, opacity: Math.min(1, t * 8) }}>
          <AssetImg id="py-atom-figure-walk" height={260} tint="white" />
        </div>
      </Stage>
    </Backdrop>
  );
};
