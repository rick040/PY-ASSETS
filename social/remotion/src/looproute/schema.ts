import { z } from "zod";

/** Template R3 "Looproute": where to park for an event, as walking minutes per location, then the price, then the end card. */
export const looprouteSchema = z.object({
  itemId: z.string(),
  hook: z.object({
    headline: z.string().describe("\\n = new line, *word* = key phrase"),
    partner: z.string().describe("Shown next to the logo as 'parkingyou x <partner>'; empty for none"),
    partnerLabel: z.string().describe("Small line under the headline, for example 'Official parking partner'; empty for none"),
  }),
  route: z.object({
    title: z.string(),
    destinations: z.array(z.object({ name: z.string(), minutes: z.number().min(0) })).min(2).max(6),
  }),
  price: z.object({ headline: z.string(), amount: z.number().min(0), label: z.string(), note: z.string() }),
  cta: z.object({ headline: z.string(), button: z.string(), url: z.string(), tagline: z.string() }),
  timing: z.object({
    hook: z.number().min(2).max(6),
    route: z.number().min(3).max(8),
    price: z.number().min(2).max(6),
    cta: z.number().min(2).max(6),
    transition: z.number().min(0.2).max(1),
  }),
  showSafeZones: z.boolean(),
});

export type LooprouteProps = z.infer<typeof looprouteSchema>;

export const looprouteDefaults: LooprouteProps = {
  itemId: "IG-039",
  hook: { headline: "Waar parkeer je\ntijdens *GLOW?*", partner: "GLOW Eindhoven", partnerLabel: "Official parking partner" },
  route: {
    title: "Op *1 tot 15 min*\nlopen van de route",
    destinations: [
      { name: "Philips Stadion", minutes: 1 },
      { name: "DLL", minutes: 3 },
      { name: "TD-Gebouw", minutes: 4 },
      { name: "Bedrijfsschool", minutes: 8 },
      { name: "Evoluon", minutes: 15 },
    ],
  },
  price: { headline: "Reserveer vooraf\nvoor *€15*", amount: 15, label: "per avond", note: "Rijd je gewoon aan? Dan betaal je €20." },
  cta: { headline: "Reserveer\n*je plek*", button: "Reserveer online", url: "voordeligparkeren.nl", tagline: "The other way of parking" },
  timing: { hook: 3, route: 5, price: 3.2, cta: 3.4, transition: 0.5 },
  showSafeZones: false,
};

export const FPS = 30;
export const looprouteFrames = (t: LooprouteProps["timing"]) => ({
  hook: Math.round(t.hook * FPS),
  route: Math.round(t.route * FPS),
  price: Math.round(t.price * FPS),
  cta: Math.round(t.cta * FPS),
  transition: Math.round(t.transition * FPS),
});
export const looprouteTotal = (t: LooprouteProps["timing"]) => {
  const f = looprouteFrames(t);
  return f.hook + f.route + f.price + f.cta - 3 * f.transition;
};
