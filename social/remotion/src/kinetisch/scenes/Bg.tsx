import React from "react";
import { AbsoluteFill } from "remotion";
import { AssetImg } from "../../components/AssetImg";

/** Vertical verloop (py-tok-gradient-verloop-vertical) with the beeldmerk watermark at 5 percent. */
export const Bg: React.FC<{ top: string; bottom: string; children: React.ReactNode }> = ({ top, bottom, children }) => (
  <AbsoluteFill style={{ background: `linear-gradient(180deg, ${top} 0%, ${top} 18%, ${bottom} 100%)` }}>
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-end", opacity: 0.05 }}>
      <AssetImg id="py-atom-logo-beeldmerk-white" width={1300} style={{ marginBottom: -300 }} />
    </AbsoluteFill>
    {children}
  </AbsoluteFill>
);
