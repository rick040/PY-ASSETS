import React from "react";
import { AssetImg } from "./AssetImg";

/**
 * Icon for a text line: a PY-ASSETS element ID ("py-...") or a simple built-in glyph drawn in the same
 * rounded stroke style, for ideas the library has no pictogram for yet (clock, fuel, mood, pin, check, cross).
 */
export const Glyph: React.FC<{ name: string; size: number; color: string; tint?: "none" | "white" }> = ({ name, size, color, tint = "white" }) => {
  if (name.startsWith("py-")) return <AssetImg id={name} width={size} height={size} tint={tint} />;
  const sw = 7;
  const common = { fill: "none", stroke: color, strokeWidth: sw, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
  return (
    <svg width={size} height={size} viewBox="0 0 100 100">
      {name === "clock" && (<><circle cx={50} cy={50} r={40} {...common} /><path d="M50 26V50L66 60" {...common} /></>)}
      {name === "fuel" && (<><path d="M24 88V22C24 17 28 13 33 13H57C62 13 66 17 66 22V88" {...common} /><path d="M17 88H73" {...common} /><path d="M33 30H57V46H33Z" {...common} /><path d="M66 40H74C78 40 80 43 80 47V72C80 76 86 76 86 72V36L76 26" {...common} /></>)}
      {name === "mood" && (<><circle cx={50} cy={50} r={40} {...common} /><circle cx={36} cy={42} r={3} fill={color} /><circle cx={64} cy={42} r={3} fill={color} /><path d="M33 70C41 62 59 62 67 70" {...common} /></>)}
      {name === "pin" && (<><path d="M50 90C50 90 20 58 20 38C20 21 33 9 50 9C67 9 80 21 80 38C80 58 50 90 50 90Z" {...common} /><circle cx={50} cy={38} r={11} {...common} /></>)}
      {name === "check" && <path d="M20 52L42 74L82 28" {...common} strokeWidth={10} />}
      {name === "cross" && <path d="M26 26L74 74M74 26L26 74" {...common} strokeWidth={10} />}
    </svg>
  );
};
