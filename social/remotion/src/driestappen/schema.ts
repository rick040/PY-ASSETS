import { z } from "zod";
import { zColor } from "@remotion/zod-types";
import { BRAND } from "../theme";

/** Template R4 "Drie stappen": outcome first (barrier opens), then one scene per step, outcome again, end card. */
export const drieStappenSchema = z.object({
  itemId: z.string(),
  hook: z.object({ headline: z.string().describe("\\n = new line, *word* = key phrase") }),
  steps: z
    .array(z.object({ illustration: z.string().describe("PY-ASSETS ID or glyph"), text: z.string(), card: z.enum(["light", "accent"]) }))
    .min(2)
    .max(4),
  outcome: z.object({ headline: z.string(), figure: z.string() }),
  cta: z.object({ headline: z.string(), button: z.string(), url: z.string(), tagline: z.string() }),
  colors: z.object({ bg: zColor(), text: zColor(), accent: zColor(), card: zColor(), ctaBgFrom: zColor(), ctaBgTo: zColor() }),
  timing: z.object({
    hook: z.number().min(1.5).max(5),
    step: z.number().min(1.5).max(4),
    outcome: z.number().min(1.5).max(5),
    cta: z.number().min(2).max(6),
    transition: z.number().min(0.2).max(1),
  }),
  showSafeZones: z.boolean(),
});

export type DrieStappenProps = z.infer<typeof drieStappenSchema>;

export const drieStappenDefaults: DrieStappenProps = {
  itemId: "IG-028",
  hook: { headline: "Je plek\ngeregeld in\n*3 stappen.*" },
  steps: [
    { illustration: "py-atom-illustration-phone-qr", text: "Kies je *locatie en tijd*", card: "light" },
    { illustration: "py-atom-illustration-contactless-hand", text: "Betaal *online*", card: "light" },
    { illustration: "py-atom-illustration-reader-qr", text: "Rijd in met je *code*", card: "light" },
  ],
  outcome: { headline: "Slagboom open.\n*Je plek*\n*staat klaar.*", figure: "py-atom-figure-bags-cheer" },
  cta: { headline: "Reserveer\n*je plek*", button: "Reserveer online", url: "voordeligparkeren.nl", tagline: "The other way of parking" },
  colors: { bg: BRAND.blauw, text: BRAND.wit, accent: BRAND.aqua, card: BRAND.wit, ctaBgFrom: BRAND.blauw, ctaBgTo: BRAND.aqua },
  timing: { hook: 2.8, step: 2.3, outcome: 3.2, cta: 3.4, transition: 0.5 },
  showSafeZones: false,
};

export const FPS = 30;
export const drieStappenFrames = (t: DrieStappenProps["timing"]) => ({
  hook: Math.round(t.hook * FPS),
  step: Math.round(t.step * FPS),
  outcome: Math.round(t.outcome * FPS),
  cta: Math.round(t.cta * FPS),
  transition: Math.round(t.transition * FPS),
});
export const drieStappenTotal = (p: Pick<DrieStappenProps, "timing" | "steps">) => {
  const f = drieStappenFrames(p.timing);
  const scenes = 3 + p.steps.length;
  return f.hook + f.step * p.steps.length + f.outcome + f.cta - (scenes - 1) * f.transition;
};
