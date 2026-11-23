import { z } from "zod";
import { zColor } from "@remotion/zod-types";
import { BRAND } from "../theme";

/** Template R7 "Kinetische tekst": a hook, 1 to 4 lines with an icon, an end line, the shared end card. */
export const kinetischSchema = z.object({
  itemId: z.string(),
  hook: z.object({ headline: z.string().describe("\\n = new line, *word* = key phrase"), visual: z.enum(["none", "orbit"]), counterLabel: z.string() }),
  lines: z.object({
    title: z.string(),
    items: z.array(z.object({ icon: z.string().describe("PY-ASSETS ID or clock | fuel | mood | pin | check | cross"), text: z.string() })).min(1).max(4),
  }),
  end: z.object({ headline: z.string(), visual: z.enum(["none", "arrive"]) }),
  cta: z.object({ headline: z.string(), button: z.string(), url: z.string(), tagline: z.string() }),
  colors: z.object({ bgTop: zColor(), bgBottom: zColor(), text: zColor(), accent: zColor(), ctaBgFrom: zColor(), ctaBgTo: zColor() }),
  timing: z.object({
    hook: z.number().min(2).max(6),
    lines: z.number().min(2).max(8),
    end: z.number().min(2).max(6),
    cta: z.number().min(2).max(6),
    transition: z.number().min(0.2).max(1),
  }),
  showSafeZones: z.boolean(),
});

export type KinetischProps = z.infer<typeof kinetischSchema>;

export const kinetischDefaults: KinetischProps = {
  itemId: "IG-021",
  hook: { headline: "Rondjes\nrijden is ook\n*betalen.*", visual: "orbit", counterLabel: "Rondje" },
  lines: {
    title: "Je betaalt\n*met:*",
    items: [
      { icon: "fuel", text: "*Benzine*" },
      { icon: "clock", text: "*Tijd*" },
      { icon: "mood", text: "Je *goede humeur*" },
    ],
  },
  end: { headline: "Reserveer vooraf.\nRijd *direct*\nnaar je plek.", visual: "arrive" },
  cta: { headline: "Reserveer\n*je plek*", button: "Reserveer online", url: "voordeligparkeren.nl", tagline: "The other way of parking" },
  colors: { bgTop: BRAND.blauw, bgBottom: "#097BAE", text: BRAND.wit, accent: BRAND.aqua, ctaBgFrom: BRAND.blauw, ctaBgTo: BRAND.aqua },
  timing: { hook: 3.2, lines: 3.4, end: 3, cta: 3.4, transition: 0.5 },
  showSafeZones: false,
};

export const FPS = 30;
export const kinetischFrames = (t: KinetischProps["timing"]) => ({
  hook: Math.round(t.hook * FPS),
  lines: Math.round(t.lines * FPS),
  end: Math.round(t.end * FPS),
  cta: Math.round(t.cta * FPS),
  transition: Math.round(t.transition * FPS),
});
export const kinetischTotal = (t: KinetischProps["timing"]) => {
  const f = kinetischFrames(t);
  return f.hook + f.lines + f.end + f.cta - 3 * f.transition;
};
