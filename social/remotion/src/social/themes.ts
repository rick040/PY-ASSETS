import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";
import { BRAND, FONT, VERLOOP } from "../theme";
import t27 from "../../../../brand-2027/tokens/tokens.json";

/**
 * A theme is everything a layout may take from the brand: palette, fonts, grounds, logo per ground and element rules.
 * Archetypes only read from here, so one post spec renders in the current feed style or in the 2027 identity.
 * Every colour comes from tokens.json (feed) or brand-2027/tokens/tokens.json (2027). Nothing else is allowed on a
 * post: no lighting effects, grain, vignettes, shadows or extra gradients (Rick, 25 November 2026, decision S13).
 */
export type ThemeId = "feed" | "2027";
export type Ground = "navy" | "verloop" | "white" | "photo";

type Ink = { text: string; muted: string; key: string; logo: string; figure: "white" | "navy"; accent: string };

export type Theme = {
  id: ThemeId;
  font: string;
  weights: { regular: number; key: number; label: number; display: number };
  /** Every colour a template may use. check_brand.py compares the rendered pixels with this list (and the gradient). */
  palette: Record<string, string>;
  /** CSS fill of a ground. Photo grounds draw the photo themselves and use a navy field for text. */
  fill: (g: Ground) => string;
  ink: (g: Ground) => Ink;
  /** URL of a logo or kit asset by ID. */
  asset: (id: string) => string;
  url: string;
  rules: { maxElements: number | null; priceBadge: boolean; figuresPerPost: number; italicPrices: boolean; priceSpace: boolean };
};

const assetUrl = (id: string) => {
  if (id.endsWith("-open") || id.endsWith("-whitedot")) return staticFile(`py/derived/${id}.svg`);
  return staticFile(`py/svg/${id.split("-")[1]}/${id}.svg`);
};

export const feedTheme: Theme = {
  id: "feed",
  font: FONT,
  weights: { regular: 400, key: 700, label: 500, display: 700 },
  palette: { blauw: BRAND.blauw, aqua: BRAND.aqua, oranje: BRAND.oranje, grijs: BRAND.grijs, zwart: BRAND.zwart, wit: BRAND.wit },
  fill: (g) => (g === "verloop" ? VERLOOP : g === "white" ? BRAND.wit : BRAND.blauw),
  ink: (g) =>
    g === "white"
      ? { text: BRAND.blauw, muted: BRAND.blauw, key: BRAND.blauw, logo: "py-atom-logo-horizontal-color", figure: "navy", accent: BRAND.aqua }
      : { text: BRAND.wit, muted: BRAND.wit, key: BRAND.wit, logo: "py-atom-logo-horizontal-reverse-open", figure: "white", accent: BRAND.aqua },
  asset: assetUrl,
  url: "parkingyou.nl",
  rules: { maxElements: null, priceBadge: true, figuresPerPost: 6, italicPrices: true, priceSpace: false },
};

// ---- 2027 ----
const hex = (group: string, step: string): string => (t27 as any).color[group][step].$value.hex.toUpperCase();
const C27 = { blauw: hex("blue", "700"), diep: hex("blue", "900"), paper: hex("blue", "50"), aqua: hex("aqua", "500"), wit: hex("neutral", "0") };
const FONT27 = "Ubuntu Sans";
loadFont({ family: FONT27, url: staticFile("py/2027/fonts/UbuntuSans[wdth,wght].ttf"), weight: "100 800", style: "normal" });

export const theme2027: Theme = {
  id: "2027",
  font: FONT27,
  weights: { regular: 400, key: 800, label: 600, display: 800 },
  palette: { blauw: C27.blauw, diep: C27.diep, paper: C27.paper, aqua: C27.aqua, wit: C27.wit },
  fill: (g) => (g === "white" ? C27.wit : C27.blauw),
  ink: (g) =>
    g === "white"
      ? { text: C27.blauw, muted: C27.blauw, key: C27.blauw, logo: "2027/logo-horizontal-color", figure: "navy", accent: C27.aqua }
      : { text: C27.wit, muted: C27.wit, key: C27.wit, logo: "2027/logo-horizontal-reverse", figure: "white", accent: C27.aqua },
  asset: (id) => (id.startsWith("2027/") ? staticFile(`py/2027/assets/${id.slice(5)}.svg`) : assetUrl(id)),
  url: "parkingyou.nl",
  rules: { maxElements: 2, priceBadge: false, figuresPerPost: 1, italicPrices: false, priceSpace: true },
};

export const themes: Record<ThemeId, Theme> = { feed: feedTheme, "2027": theme2027 };
export const getTheme = (id: ThemeId): Theme => {
  const t = themes[id];
  if (!t) throw new Error(`Unknown theme "${id}"`);
  return t;
};

/** "€ 12,50" (2027) or "€12,50" (feed); whole amounts without cents. */
export const euro = (theme: Theme, amount: number) => {
  const s = Number.isInteger(amount) ? String(amount) : amount.toFixed(2).replace(".", ",");
  return theme.rules.priceSpace ? `€ ${s}` : `€${s}`;
};
