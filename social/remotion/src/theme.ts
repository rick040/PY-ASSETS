import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";
import tokens from "../../../tokens.json";

// Brand values come straight from PY-ASSETS tokens.json (handbook 1.3).
export const BRAND = {
  blauw: tokens.colors["py-tok-color-blauw"].hex,
  aqua: tokens.colors["py-tok-color-aqua"].hex,
  oranje: tokens.colors["py-tok-color-oranje"].hex,
  grijs: tokens.colors["py-tok-color-grijs"].hex,
  zwart: tokens.colors["py-tok-color-zwart"].hex,
  wit: "#FFFFFF",
} as const;

const v = tokens.gradients["py-tok-gradient-verloop"].stops;
export const VERLOOP = `linear-gradient(135deg, ${v.map((s) => `${s.hex} ${Math.round(s.offset * 100)}%`).join(", ")})`;
export const VERLOOP_STOPS = v;

export const FONT = "Ubuntu";

const weights: Array<[string, string]> = [
  ["Ubuntu-Light.ttf", "300"],
  ["Ubuntu-Regular.ttf", "400"],
  ["Ubuntu-Medium.ttf", "500"],
  ["Ubuntu-Bold.ttf", "700"],
];
for (const [file, weight] of weights) {
  loadFont({ family: FONT, url: staticFile(`py/fonts/${file}`), weight, style: "normal" });
}
loadFont({ family: FONT, url: staticFile("py/fonts/Ubuntu-BoldItalic.ttf"), weight: "700", style: "italic" });
