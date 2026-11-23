import { z } from "zod";
import { zColor } from "@remotion/zod-types";
import { BRAND } from "../theme";

/**
 * Template R2 "Prijsrol": the same spot at 2 to 4 prices. Prices count up, the dearer ones are struck through,
 * the cheapest (or `highlight`) gets the aqua card, the saving is calculated from the numbers, never typed.
 */
export const prijsrolSchema = z.object({
  itemId: z.string(),
  hook: z.object({ headline: z.string().describe("\\n = new line, *word* = key phrase") }),
  location: z.object({ name: z.string(), city: z.string() }),
  rows: z.object({
    title: z.string(),
    items: z
      .array(z.object({ label: z.string(), icon: z.string().describe("PY-ASSETS ID or glyph"), amount: z.number().min(0), suffix: z.string().describe("Shown after the price, for example /mnd") }))
      .min(2)
      .max(4),
    highlight: z.number().int().min(-1).max(3).describe("-1 = cheapest"),
    saving: z.string().describe("{x} = difference between the highest and the highlighted price; empty = no badge"),
  }),
  bubble: z.object({ headline: z.string(), label: z.string(), note: z.string() }),
  cta: z.object({ headline: z.string(), button: z.string(), url: z.string(), tagline: z.string() }),
  colors: z.object({ bg: zColor(), text: zColor(), accent: zColor(), muted: zColor(), ctaBgFrom: zColor(), ctaBgTo: zColor() }),
  timing: z.object({
    hook: z.number().min(1.5).max(5),
    rows: z.number().min(3).max(8),
    bubble: z.number().min(2).max(5),
    cta: z.number().min(2).max(6),
    transition: z.number().min(0.2).max(1),
  }),
  showSafeZones: z.boolean(),
});

export type PrijsrolProps = z.infer<typeof prijsrolSchema>;

export const prijsrolDefaults: PrijsrolProps = {
  itemId: "IG-017",
  hook: { headline: "Zelfde plek.\n*Drie prijzen.*" },
  location: { name: "Hofplein", city: "Rotterdam" },
  rows: {
    title: "Een dag\n*parkeren*",
    items: [
      { label: "Ter plaatse", icon: "py-atom-picto-car", amount: 30, suffix: "" },
      { label: "Online reserveren", icon: "py-atom-illustration-phone-qr", amount: 25, suffix: "" },
      { label: "Vroegboeken", icon: "py-atom-icon-calendar", amount: 20, suffix: "" },
    ],
    highlight: -1,
    saving: "Je bespaart *{x}* per dag",
  },
  bubble: { headline: "Zelfde garage.\nAlleen *eerder*\n*geboekt.*", label: "per dag", note: "Doordeweeks, vroegboeken online" },
  cta: { headline: "Boek *vroeg*,\nbetaal minder", button: "Reserveer online", url: "voordeligparkeren.nl", tagline: "The other way of parking" },
  colors: { bg: BRAND.blauw, text: BRAND.wit, accent: BRAND.aqua, muted: BRAND.grijs, ctaBgFrom: BRAND.blauw, ctaBgTo: BRAND.aqua },
  timing: { hook: 2.8, rows: 4.6, bubble: 3, cta: 3.4, transition: 0.5 },
  showSafeZones: false,
};

export const FPS = 30;
export const prijsrolFrames = (t: PrijsrolProps["timing"]) => ({
  hook: Math.round(t.hook * FPS),
  rows: Math.round(t.rows * FPS),
  bubble: Math.round(t.bubble * FPS),
  cta: Math.round(t.cta * FPS),
  transition: Math.round(t.transition * FPS),
});
export const prijsrolTotal = (t: PrijsrolProps["timing"]) => {
  const f = prijsrolFrames(t);
  return f.hook + f.rows + f.bubble + f.cta - 3 * f.transition;
};

/** Index of the highlighted row: the cheapest unless set. */
export const highlightIndex = (p: PrijsrolProps) => {
  if (p.rows.highlight >= 0 && p.rows.highlight < p.rows.items.length) return p.rows.highlight;
  let best = 0;
  p.rows.items.forEach((r, i) => { if (r.amount < p.rows.items[best].amount) best = i; });
  return best;
};
