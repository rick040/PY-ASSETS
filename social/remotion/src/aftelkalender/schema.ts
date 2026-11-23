import { z } from "zod";

/** Template R6 "Aftelkalender": a tear-off calendar flips from the posting date to the event date, event info, price, end card. */
export const aftelkalenderSchema = z.object({
  itemId: z.string(),
  hook: z.object({
    headline: z.string().describe("\\n = new line, *word* = key phrase"),
    from: z.string().describe("Posting date, YYYY-MM-DD; the countdown starts here"),
    to: z.string().describe("Event date, YYYY-MM-DD"),
    countdown: z.string().describe("{n} = days from 'from' to 'to'; empty for no countdown pill"),
    sparkles: z.boolean(),
  }),
  event: z.object({
    name: z.string(),
    lines: z.array(z.object({ icon: z.string(), text: z.string() })).min(1).max(3),
    locations: z.array(z.string()).max(4),
  }),
  price: z.object({ headline: z.string(), amount: z.number().min(0), label: z.string(), note: z.string() }),
  cta: z.object({ headline: z.string(), button: z.string(), url: z.string(), tagline: z.string() }),
  timing: z.object({
    hook: z.number().min(2).max(6),
    event: z.number().min(2).max(7),
    price: z.number().min(2).max(6),
    cta: z.number().min(2).max(6),
    transition: z.number().min(0.2).max(1),
  }),
  showSafeZones: z.boolean(),
});

export type AftelkalenderProps = z.infer<typeof aftelkalenderSchema>;

export const aftelkalenderDefaults: AftelkalenderProps = {
  itemId: "IG-041",
  hook: { headline: "Amsterdam\ngaat *weer aan.*", from: "2026-11-06", to: "2026-11-26", countdown: "Nog *{n} dagen*", sparkles: true },
  event: {
    name: "*Amsterdam*\n*Light Festival*",
    lines: [
      { icon: "py-atom-icon-calendar", text: "*26 nov* t/m *17 jan*" },
      { icon: "clock", text: "Elke avond vanaf *±17:00*" },
    ],
    locations: ["Plantage", "Cruquius", "Zeeburgerkade"],
  },
  price: { headline: "Parkeer vooraf\nvanaf *€17,50*", amount: 17.5, label: "per dag", note: "Vroegboeken bij Cruquius en Zeeburgerkade" },
  cta: { headline: "Reserveer\n*je plek*", button: "Reserveer online", url: "voordeligparkeren.nl", tagline: "The other way of parking" },
  timing: { hook: 3.4, event: 3.8, price: 3.2, cta: 3.4, transition: 0.5 },
  showSafeZones: false,
};

export const FPS = 30;
export const aftelkalenderFrames = (t: AftelkalenderProps["timing"]) => ({
  hook: Math.round(t.hook * FPS),
  event: Math.round(t.event * FPS),
  price: Math.round(t.price * FPS),
  cta: Math.round(t.cta * FPS),
  transition: Math.round(t.transition * FPS),
});
export const aftelkalenderTotal = (t: AftelkalenderProps["timing"]) => {
  const f = aftelkalenderFrames(t);
  return f.hook + f.event + f.price + f.cta - 3 * f.transition;
};

const MONTHS = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"];

/** Every date from `from` to `to` inclusive, as { day, month } (UTC, so no timezone drift). */
export const datesBetween = (from: string, to: string) => {
  const a = new Date(`${from}T00:00:00Z`).getTime();
  const b = new Date(`${to}T00:00:00Z`).getTime();
  const out: Array<{ day: number; month: string }> = [];
  for (let t = a; t <= b && out.length < 400; t += 86400000) {
    const d = new Date(t);
    out.push({ day: d.getUTCDate(), month: MONTHS[d.getUTCMonth()] });
  }
  return out.length ? out : [{ day: new Date(`${to}T00:00:00Z`).getUTCDate(), month: MONTHS[new Date(`${to}T00:00:00Z`).getUTCMonth()] }];
};
