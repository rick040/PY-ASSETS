import React from "react";
import { BRAND, FONT } from "../theme";
import { Rich } from "../lib/rich";
import { Glyph } from "../components/Glyph";

/** White pill card with a navy icon disc, as used for facts, price rows and lines. Text auto-fits. */
export const Card: React.FC<{
  icon?: string;
  tint?: "none" | "white";
  text: string;
  right?: React.ReactNode;
  height?: number;
  bg?: string;
  fg?: string;
  disc?: string;
  maxFont?: number;
  textWidth?: number;
  style?: React.CSSProperties;
}> = ({ icon, tint = "white", text, right, height = 196, bg = BRAND.wit, fg = BRAND.blauw, disc = BRAND.blauw, maxFont = 68, textWidth = 760, style }) => {
  const plain = text.replace(/\*/g, "");
  const fs = Math.min(maxFont, Math.floor(textWidth / (Math.max(plain.length, 6) * 0.56)));
  return (
    <div style={{ display: "flex", alignItems: "center", gap: height * 0.17, height, padding: `0 ${height * 0.24}px 0 ${height * 0.15}px`, borderRadius: height / 2, background: bg, boxShadow: "0 18px 40px rgba(4,10,40,0.26)", ...style }}>
      {icon && (
        <div style={{ width: height * 0.7, height: height * 0.7, borderRadius: height * 0.35, background: disc, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
          <Glyph name={icon} size={height * 0.4} color={BRAND.wit} tint={tint} />
        </div>
      )}
      <div style={{ flex: 1, fontFamily: FONT, fontSize: fs, color: fg, whiteSpace: "nowrap" }}>
        <Rich text={text} keyColor={fg} />
      </div>
      {right}
    </div>
  );
};
