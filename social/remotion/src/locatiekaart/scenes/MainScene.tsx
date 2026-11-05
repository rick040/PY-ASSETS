import React from "react";
import { useCurrentFrame } from "remotion";
import { LocatiekaartProps } from "../schema";
import { Stage } from "../../lib/layout";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { TopLogo } from "../../v2/Badges";
import { enter, leave } from "../../v2/ease";
import { AssetImg } from "../../components/AssetImg";
import { Rich } from "../../lib/rich";
import { BRAND, FONT } from "../../theme";

export const T_FACTS = [16, 24, 32];

/** Facts: location name big, then white cards with a navy icon disc, staggered in, leaving together. */
export const MainScene: React.FC<LocatiekaartProps & { dur: number }> = (p) => {
  const frame = useCurrentFrame();
  const out = leave(frame, p.dur - 4, 12);
  return (
    <Backdrop kind="navy" seed="facts">
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center" }}>
          <TopLogo width={320} start={-20} />
        </div>
        <div style={{ position: "absolute", left: 60, top: 150 }}>
          <Title text={`*${p.location.name}*\n${p.location.city}`} color={BRAND.wit} maxSize={170} width={960} delay={-4} end={p.dur} />
        </div>
        <div style={{ position: "absolute", left: 60, right: 60, top: 600, display: "flex", flexDirection: "column", gap: 44 }}>
          {p.facts.map((f, i) => {
            const plain = f.text.replace(/\*/g, "");
            const fs = Math.min(68, Math.floor(760 / (plain.length * 0.56)));
            const e = enter(frame, T_FACTS[i] ?? 16 + i * 8, 22);
            return (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 34, height: 196, padding: "0 44px 0 30px", borderRadius: 98, background: BRAND.wit, boxShadow: "0 18px 40px rgba(4,10,40,0.28)", opacity: Math.min(1, e * 1.3) * (1 - out), transform: `translateX(${(1 - e) * -110 + out * 60}%)` }}>
                <div style={{ width: 136, height: 136, borderRadius: 68, background: BRAND.blauw, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                  <AssetImg id={f.icon} width={78} height={78} tint={f.tint} />
                </div>
                <div style={{ fontFamily: FONT, fontSize: fs, color: BRAND.blauw, whiteSpace: "nowrap" }}>
                  <Rich text={f.text} keyColor={BRAND.blauw} />
                </div>
              </div>
            );
          })}
        </div>
      </Stage>
    </Backdrop>
  );
};
