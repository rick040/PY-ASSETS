import { BRAND, FONT } from "../theme";

/**
 * A theme is everything a layout may take from the brand: palette, fonts, logo choice per ground and element rules.
 * Archetypes only read from here, so the same post spec renders in the current feed style or in the 2027 identity.
 * Values come from tokens.json (feed) and brand-2027/tokens/tokens.json (2027); none are typed in twice.
 */
export type ThemeId = "feed" | "2027";
export type Ground = "navy" | "glow" | "light" | "photo" | "white";

export type Theme = {
  id: ThemeId;
  font: string;
  /** Every colour a template may use for text, fills and lines. check_brand.py compares the measured colours to this list. */
  palette: Record<string, string>;
  /** Text colour, key-phrase colour and logo element ID for a ground. */
  ink: (g: Ground) => { text: string; key: string; logo: string };
  url: string;
  /** Element rules from references/brand-visual.md. */
  rules: { maxElements: number | null; priceBadge: boolean; gradients: boolean; figuresPerPost: number; italicPrices: boolean };
};

export const feedTheme: Theme = {
  id: "feed",
  font: FONT,
  palette: { blauw: BRAND.blauw, aqua: BRAND.aqua, oranje: BRAND.oranje, grijs: BRAND.grijs, zwart: BRAND.zwart, wit: BRAND.wit },
  ink: (g) => {
    if (g === "light" || g === "white") return { text: BRAND.blauw, key: BRAND.blauw, logo: "py-atom-logo-horizontal-color" };
    if (g === "glow") return { text: BRAND.wit, key: BRAND.wit, logo: "py-atom-logo-horizontal-reverse-whitedot" };
    return { text: BRAND.wit, key: BRAND.wit, logo: "py-atom-logo-horizontal-reverse-open" };
  },
  url: "parkingyou.nl",
  rules: { maxElements: null, priceBadge: true, gradients: true, figuresPerPost: 6, italicPrices: true },
};

export const themes: Record<ThemeId, Theme | null> = {
  feed: feedTheme,
  // Built in phase 3 from brand-2027/tokens/tokens.json (branch claude/parkingyou-brand-refresh-hz67bb).
  "2027": null,
};

export const getTheme = (id: ThemeId): Theme => {
  const t = themes[id];
  if (!t) throw new Error(`Theme "${id}" is not built yet`);
  return t;
};
