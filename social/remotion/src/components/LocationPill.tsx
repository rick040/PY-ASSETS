import React from "react";
import { FONT } from "../theme";
import { AssetImg } from "./AssetImg";

/** py-comp-pill-location: pin + location name, with the city in the light weight. */
export const LocationPill: React.FC<{ name: string; city: string; bg: string; fg: string; accent: string; height?: number }> = ({ name, city, bg, fg, accent, height = 120 }) => (
  <div style={{ display: "inline-flex", alignItems: "center", gap: height * 0.2, height, padding: `0 ${height * 0.45}px 0 ${height * 0.32}px`, borderRadius: height / 2, background: bg, fontFamily: FONT, fontSize: height * 0.42, color: fg, whiteSpace: "nowrap", boxShadow: "0 10px 30px rgba(0,0,0,0.18)" }}>
    <AssetImg id="py-atom-icon-location-pin-symmetric" height={height * 0.5} tint="white" />
    <span style={{ fontWeight: 500 }}>{name}</span>
    <span style={{ fontWeight: 300, color: accent }}>{city}</span>
  </div>
);
