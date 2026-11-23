import React from "react";
import { AbsoluteFill } from "remotion";
import { useLayout } from "../lib/layout";

/** Studio helper only: shades the areas Instagram covers with UI. */
export const SafeZones: React.FC = () => {
  const { safeTop, safeBottom } = useLayout();
  const s: React.CSSProperties = { position: "absolute", left: 0, right: 0, background: "rgba(255,0,80,0.25)", borderColor: "rgba(255,0,80,0.8)", borderStyle: "dashed", borderWidth: 0 };
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ ...s, top: 0, height: safeTop, borderBottomWidth: 3 }} />
      <div style={{ ...s, bottom: 0, height: safeBottom, borderTopWidth: 3 }} />
    </AbsoluteFill>
  );
};
