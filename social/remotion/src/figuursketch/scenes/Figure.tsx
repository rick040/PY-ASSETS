import React from "react";
import { AssetImg } from "../../components/AssetImg";

/** A PY-ASSETS figure with a small loop so it feels alive. Origin at the feet. */
export const Figure: React.FC<{ id: string; height: number; frame: number; motion: "bob" | "walk" | "jump" | "dance"; tint?: "none" | "white"; opacity?: number }> = ({ id, height, frame, motion, tint = "none", opacity = 1 }) => {
  let y = 0;
  let r = 0;
  let sx = 1;
  let sy = 1;
  if (motion === "bob") y = Math.sin(frame / 7) * 8;
  if (motion === "walk") { y = -Math.abs(Math.sin(frame / 4)) * 14; r = Math.sin(frame / 4) * 2; }
  if (motion === "jump") {
    const t = (frame % 24) / 24;
    y = -Math.sin(t * Math.PI) * 70;
    sy = t < 0.08 || t > 0.92 ? 0.93 : 1;
    sx = 2 - sy;
  }
  if (motion === "dance") { r = Math.sin(frame / 5) * 7; y = -Math.abs(Math.sin(frame / 5)) * 18; }
  return (
    <div style={{ height, display: "flex", alignItems: "flex-end", transform: `translateY(${y}px) rotate(${r}deg) scale(${sx}, ${sy})`, transformOrigin: "50% 100%", opacity }}>
      <AssetImg id={id} height={height} tint={tint} />
    </div>
  );
};
