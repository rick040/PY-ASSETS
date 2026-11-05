import React from "react";
import { FONT } from "../theme";
import { Rich } from "../lib/rich";
import { AssetImg } from "./AssetImg";

export type Fact = { icon: string; tint: "none" | "white"; text: string };

export const FactRow: React.FC<{ fact: Fact; p: number; color: string; keyColor: string; ring: string }> = ({ fact, p, color, keyColor, ring }) => (
  <div style={{ display: "flex", alignItems: "center", gap: 36, opacity: Math.min(1, p * 1.5), transform: `translateX(${(1 - p) * -80}px)` }}>
    <div style={{ width: 150, height: 150, borderRadius: 75, border: `5px solid ${ring}`, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, transform: `scale(${0.6 + 0.4 * p})` }}>
      <AssetImg id={fact.icon} width={86} height={86} tint={fact.tint} />
    </div>
    <div style={{ fontFamily: FONT, fontSize: 66, lineHeight: 1.15, color }}>
      <Rich text={fact.text} keyColor={keyColor} />
    </div>
  </div>
);
