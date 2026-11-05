import React from "react";
import { FONT } from "../theme";
import { Rich } from "../lib/rich";

export const LabelPill: React.FC<{ text: string; bg: string; fg: string; keyColor: string; height?: number }> = ({ text, bg, fg, keyColor, height = 110 }) => (
  <div style={{ display: "inline-flex", alignItems: "center", height, padding: `0 ${height * 0.45}px`, borderRadius: height / 2, background: bg, fontFamily: FONT, fontSize: height * 0.44, fontWeight: 500, color: fg, whiteSpace: "nowrap" }}>
    <span style={{ whiteSpace: "pre" }}><Rich text={text} keyColor={keyColor} /></span>
  </div>
);
