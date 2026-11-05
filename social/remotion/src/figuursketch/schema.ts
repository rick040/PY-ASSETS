import { z } from "zod";
import { zColor } from "@remotion/zod-types";
import { BRAND } from "../theme";

const beat = z.object({
  figure: z.string().describe("PY-ASSETS figure, for example py-atom-figure-walk"),
  title: z.string().describe("*word* = key phrase"),
  line: z.string(),
  prop: z.string().describe("PY-ASSETS ID or glyph (check, cross, clock, fuel, mood, pin); empty for none"),
  motion: z.enum(["bob", "walk", "jump", "dance"]),
});

/** Template R5 "Figuursketch": hook with a line-up of figures, one beat per figure, an outro question, the shared end card. */
export const figuursketchSchema = z.object({
  itemId: z.string(),
  hook: z.object({ headline: z.string() }),
  beats: z.array(beat).min(2).max(5),
  outro: z.object({ headline: z.string(), highlight: z.number().int().min(0).max(4) }),
  cta: z.object({ headline: z.string(), url: z.string(), tagline: z.string() }),
  colors: z.object({ bg: zColor(), text: zColor(), accent: zColor(), card: zColor(), ctaBgFrom: zColor(), ctaBgTo: zColor() }),
  timing: z.object({
    hook: z.number().min(1.5).max(5),
    beat: z.number().min(1.4).max(4),
    outro: z.number().min(1.5).max(5),
    cta: z.number().min(2).max(6),
    transition: z.number().min(0.2).max(1),
  }),
  showSafeZones: z.boolean(),
});

export type FiguursketchProps = z.infer<typeof figuursketchSchema>;

export const figuursketchDefaults: FiguursketchProps = {
  itemId: "IG-064",
  hook: { headline: "Welk *parkeertype*\nben jij?" },
  beats: [
    { figure: "py-atom-figure-walk", title: "De *rondjesrijder*", line: "Derde rondje. Bijna.", prop: "py-atom-picto-car", motion: "walk" },
    { figure: "py-atom-figure-jump", title: "De *last-minute* boeker", line: "Boekt op de oprit.", prop: "py-atom-illustration-phone-qr", motion: "jump" },
    { figure: "py-atom-figure-dance", title: "De *vroegboeker*", line: "Betaalt het minst.", prop: "check", motion: "dance" },
    { figure: "py-atom-figure-point", title: "De *zoeker*", line: "Waar stond hij ook alweer?", prop: "pin", motion: "bob" },
  ],
  outro: { headline: "Tag een\n*rondjesrijder.*", highlight: 0 },
  cta: { headline: "Word een\n*vroegboeker*", url: "parkingyou.nl", tagline: "The other way of parking" },
  // light background = aqua at 10 percent on white (tints are transparency, observed print rule 8)
  colors: { bg: "#EAF8FA", text: BRAND.blauw, accent: BRAND.aqua, card: BRAND.wit, ctaBgFrom: BRAND.blauw, ctaBgTo: BRAND.aqua },
  timing: { hook: 2.4, beat: 2.1, outro: 2.4, cta: 3, transition: 0.35 },
  showSafeZones: false,
};

export const FPS = 30;
export const figuursketchFrames = (t: FiguursketchProps["timing"]) => ({
  hook: Math.round(t.hook * FPS),
  beat: Math.round(t.beat * FPS),
  outro: Math.round(t.outro * FPS),
  cta: Math.round(t.cta * FPS),
  transition: Math.round(t.transition * FPS),
});
export const figuursketchTotal = (p: Pick<FiguursketchProps, "timing" | "beats">) => {
  const f = figuursketchFrames(p.timing);
  const scenes = 3 + p.beats.length;
  return f.hook + f.beat * p.beats.length + f.outro + f.cta - (scenes - 1) * f.transition;
};
