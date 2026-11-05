import { z } from "zod";
import { zColor } from "@remotion/zod-types";
import { BRAND } from "../theme";

/** Template R1 "Locatiekaart" (see social/instagram/content-library.json). Every text, price, colour and timing is a prop. */
export const locatiekaartSchema = z.object({
  itemId: z.string(),
  hook: z.object({
    headline: z.string().describe("Use \\n for a line break and *word* for the key phrase"),
    weather: z.enum(["none", "rain"]),
  }),
  media: z.object({
    type: z.enum(["none", "image", "video"]).describe("none = branded stand-in illustration"),
    src: z.string().describe("Path inside public/, for example media/hofplein.mp4"),
  }),
  location: z.object({ name: z.string(), city: z.string() }),
  facts: z
    .array(z.object({ icon: z.string().describe("PY-ASSETS element ID"), tint: z.enum(["none", "white"]), text: z.string() }))
    .min(1)
    .max(3),
  price: z.object({ headline: z.string(), amount: z.string(), label: z.string(), note: z.string() }),
  cta: z.object({ headline: z.string(), url: z.string(), tagline: z.string() }),
  colors: z.object({ bg: zColor(), text: zColor(), accent: zColor(), ctaBgFrom: zColor(), ctaBgTo: zColor() }),
  timing: z.object({
    main: z.number().min(5).max(12),
    price: z.number().min(2).max(6),
    cta: z.number().min(2).max(6),
    transition: z.number().min(0.2).max(1),
  }),
  showSafeZones: z.boolean(),
});

export type LocatiekaartProps = z.infer<typeof locatiekaartSchema>;

export const locatiekaartDefaults: LocatiekaartProps = {
  itemId: "IG-002",
  hook: { headline: "Midden in *Rotterdam.*\n*Droog* geparkeerd.", weather: "rain" },
  media: { type: "none", src: "" },
  location: { name: "Hofplein", city: "Rotterdam" },
  facts: [
    { icon: "py-atom-symbol-p-roof", tint: "none", text: "*300* overdekte plekken" },
    { icon: "py-atom-sign-camera", tint: "none", text: "*Camerabewaking*" },
    { icon: "py-atom-icon-calendar", tint: "none", text: "Vroegboeken *€20* per dag" },
  ],
  price: { headline: "En in het *weekend?*", amount: "€15", label: "per dag", note: "Zaterdag en zondag, ter plaatse" },
  cta: { headline: "Reserveer\n*je plek*", url: "parkingyou.nl", tagline: "The other way of parking" },
  colors: { bg: BRAND.blauw, text: BRAND.wit, accent: BRAND.aqua, ctaBgFrom: BRAND.blauw, ctaBgTo: BRAND.aqua },
  timing: { main: 7, price: 3, cta: 3, transition: 0.4 },
  showSafeZones: false,
};

export const FPS = 30;
export const locatiekaartFrames = (t: LocatiekaartProps["timing"]) => ({
  main: Math.round(t.main * FPS),
  price: Math.round(t.price * FPS),
  cta: Math.round(t.cta * FPS),
  transition: Math.round(t.transition * FPS),
});
export const locatiekaartTotal = (t: LocatiekaartProps["timing"]) => {
  const f = locatiekaartFrames(t);
  return f.main + f.price + f.cta - 2 * f.transition;
};
