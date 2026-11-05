import React from "react";
import { Img, staticFile } from "remotion";

/** Reverse logos: always use the "-open" variant (white and aqua only, no navy ring fill), for example py-atom-logo-horizontal-reverse-open. */
/** Loads an element from PY-ASSETS by its ID (py-atom-*, py-comp-*, py-prod-*). `tint: "white"` recolours a one-colour mark. */
export const assetUrl = (id: string) => {
  if (id.endsWith("-open")) return staticFile(`py/derived/${id}.svg`);
  const level = id.split("-")[1];
  return staticFile(`py/svg/${level}/${id}.svg`);
};

export const AssetImg: React.FC<{ id: string; width?: number; height?: number; tint?: "none" | "white"; style?: React.CSSProperties }> = ({ id, width, height, tint = "none", style }) => (
  <Img src={assetUrl(id)} style={{ width, height, objectFit: "contain", filter: tint === "white" ? "brightness(0) invert(1)" : undefined, ...style }} />
);
