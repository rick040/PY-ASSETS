import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Q } from "../qa";
import { contentBox, FormatId, PostProps } from "../spec";
import { euro, getTheme, Ground, Theme } from "../themes";
import {
  ArtDisc, Asset, Bubble, FormatProvider, Copy, CtaButton, Eyebrow, Figure, Headline, Icon, Logo, Opened, Page, Pill, PriceBadge, PriceText, Regions, scaleOf, Url, Watermark, plain, fit,
} from "../kit";

/**
 * All archetypes (plugins/parkingyou-social/schema/archetypes.json). Each builds the regions of <Page> for both themes.
 * Theme feed: pills, badges and buttons in token colours. Theme 2027: de stem, prices as text, one parkeerder,
 * at most two elements besides the logo (brand-visual.md §4).
 */

type Ctx = { t: Theme; g: Ground; f: FormatId; k: number; w: number; hw: number; s: Record<string, any>; story: boolean; wide: boolean; inv: boolean };

const ctx = (p: PostProps, slots?: Record<string, any>, ground?: Ground): Ctx => {
  const t = getTheme(p.spec.theme);
  const b = contentBox(p.format);
  const m27 = p.format === "landscape" ? 64 : 108;
  const m = t.id === "2027" ? Math.max(b.x, m27) + Math.max(b.safe.right, m27) : b.x + b.safe.right;
  const g = ground ?? p.spec.ground;
  const inner = b.width - m;
  const wide = p.format === "landscape";
  return { t, g, f: p.format, k: scaleOf(p.format), w: inner * (wide ? 0.6 : 1), hw: inner * (wide ? 0.36 : 1), s: slots ?? p.spec.slots, story: p.format === "story", wide, inv: g === "white" };
};

// ---------- shared pieces ----------

/** The headline, opened by de stem in 2027. */
const Head: React.FC<{ c: Ctx; text: string; max: number }> = ({ c, text, max }) => {
  // De stem is as tall as the headline block and takes its width (10/45.44 of its height) plus a gap of 0.3 x
  // its height x 0.45 from the text; the headline size and the stem size depend on each other, so iterate.
  const lines = text.split("\n").length;
  const lh = 50 / 48;
  let width = c.w;
  let size = fit(c.t, text, width, max * c.k);
  if (c.t.id === "2027") {
    for (let i = 0; i < 4; i++) {
      const stemTotal = size * lines * lh * (10 / 45.44 + 0.135) + 4;
      width = c.w - stemTotal;
      size = fit(c.t, text, width, max * c.k);
    }
  }
  const blockH = size * lines * lh;
  return (
    <Opened theme={c.t} height={blockH}>
      <Headline theme={c.t} ground={c.g} text={text} width={width} max={max * c.k} />
    </Opened>
  );
};

const Footer: React.FC<{ c: Ctx; cta?: string }> = ({ c, cta }) => {
  if (cta === "none") return null;
  const label = cta === "reserve" ? "Reserveer online" : cta === "subscribe" ? "Abonnement aanvragen" : cta === "contact" ? "Neem contact op" : cta === "info" ? "Meer info" : null;
  if (c.t.id === "2027") {
    const prefix = cta === "reserve" ? "Reserveer je plek op" : cta === "subscribe" ? "Vraag je abonnement aan op" : cta === "info" ? "Meer info op" : undefined;
    return <Url theme={c.t} ground={c.g} size={31 * c.k} prefix={prefix} />;
  }
  return (
    <div style={{ display: "flex", alignItems: "center", flexWrap: "wrap", gap: 28 * c.k, maxWidth: c.w }}>
      {label && cta !== "url" && <CtaButton theme={c.t} text={label} height={104 * c.k} />}
      <Url theme={c.t} ground={c.g} size={42 * c.k} />
    </div>
  );
};

const Stack: React.FC<{ gap: number; children: React.ReactNode; align?: "flex-start" | "center" }> = ({ gap, children, align = "flex-start" }) => (
  <div style={{ display: "flex", flexDirection: "column", gap, alignItems: align }}>{children}</div>
);

/** Facts: pills with an icon (feed) or plain lines (2027, at most two). */
const Facts: React.FC<{ c: Ctx; facts?: { icon: string; text: string }[]; location?: { label?: string; code?: string } }> = ({ c, facts = [], location }) => {
  if (c.t.id === "2027") {
    const lines = facts.slice(0, 2).map((f) => plain(f.text));
    return lines.length ? <Copy theme={c.t} ground={c.g} name="facts" text={lines.join("\n")} size={31 * c.k} /> : null;
  }
  const h = (c.story ? 104 : 92) * c.k;
  return (
    <Stack gap={18 * c.k}>
      {location?.label && <Pill theme={c.t} name="location" text={location.label} height={h} pin />}
      {facts.map((f, i) => <Pill key={i} theme={c.t} name={`fact-${i + 1}`} text={f.text} height={h} icon={f.icon} />)}
    </Stack>
  );
};

const pose = (s: Record<string, any>, fallback: string) => (s.figure ? String(s.figure).replace(/^py-atom-figure-/, "") : fallback);

/** One parkeerder (2027 only) for the bottom-right corner. */
const Parkeerder: React.FC<{ c: Ctx; fallback: string; u?: number }> = ({ c, fallback, u = 7 }) =>
  c.t.id === "2027" && !c.wide ? <Figure theme={c.t} ground={c.g} pose={pose(c.s, fallback)} height={54 * u * c.k} flip /> : null;

// ---------- archetypes ----------

const typografisch = (c: Ctx): Regions => ({
  under: c.t.id === "feed" && c.g !== "white" ? <Watermark theme={c.t} size={(c.wide ? 900 : 1150) * c.k} /> : undefined,
  headline: (
    <div style={{ marginTop: c.wide ? 0 : (c.story ? 260 : 180) * c.k }}>
      <Head c={c} text={c.s.headline} max={c.wide ? 100 : 150} />
    </div>
  ),
  details: c.s.subline ? <Copy theme={c.t} ground={c.g} name="subline" text={c.s.subline} size={(c.t.id === "2027" ? 34 : 42) * c.k} width={c.w} /> : undefined,
  footer: <Footer c={c} cta={c.s.cta ?? "url"} />,
});

const prijs = (c: Ctx): Regions => {
  const p = c.s.price;
  if (c.t.id === "2027") {
    return {
      eyebrow: c.s.location?.label ? <Eyebrow theme={c.t} ground={c.g} text={c.s.location.label} size={30 * c.k} /> : undefined,
      headline: <Head c={c} text={c.s.headline} max={117} />,
      hero: <PriceText theme={c.t} ground={c.g} amount={p.amount} unit={p.unit} size={96 * c.k} from={p.from} note={c.s.body} />,
      details: <Facts c={c} facts={c.s.facts} />,
      footer: <Footer c={c} cta={c.s.cta ?? "reserve"} />,
      figure: <Parkeerder c={c} fallback="cap-wave" />,
    };
  }
  return {
    headline: <Head c={c} text={c.s.headline} max={112} />,
    hero: <PriceBadge theme={c.t} amount={p.amount} unit={p.unit} from={p.from} size={(c.story ? 460 : c.wide ? 300 : 380) * (c.wide ? 1 : c.k)} tone={c.g === "white" ? "aqua" : "white"} />,
    details: (
      <Stack gap={16 * c.k}>
        <Facts c={c} facts={c.s.facts} location={c.s.location} />
        {c.s.body && <Copy theme={c.t} ground={c.g} name="body" text={c.s.body} size={34 * c.k} width={c.w} />}
      </Stack>
    ),
    footer: <Footer c={c} cta={c.s.cta ?? "url"} />,
  };
};

const locatie = (c: Ctx): Regions => {
  const m = c.s.media;
  const heroSize = (c.story ? 560 : c.wide ? 320 : 420) * (c.wide ? 1 : c.k);
  const media = m ? (
    m.type === "illustration" ? (
      <ArtDisc theme={c.t} ground={c.g} id={m.src} size={heroSize} name="media" />
    ) : (
      <BubblePhoto src={m.src} size={heroSize} />
    )
  ) : c.s.price && c.t.id === "feed" ? (
    <PriceBadge theme={c.t} amount={c.s.price.amount} unit={c.s.price.unit} from={c.s.price.from} size={heroSize * 0.85} />
  ) : null;
  if (c.t.id === "2027") {
    return {
      headline: <Head c={c} text={c.s.headline} max={96} />,
      hero: media,
      details: (
        <Stack gap={20 * c.k}>
          {c.s.location?.label && <Copy theme={c.t} ground={c.g} name="location" text={`*${c.s.location.label}*`} size={44 * c.k} />}
          <Facts c={c} facts={c.s.facts} />
          {c.s.price && <PriceText theme={c.t} ground={c.g} amount={c.s.price.amount} unit={c.s.price.unit} size={60 * c.k} from={c.s.price.from} />}
        </Stack>
      ),
      footer: <Footer c={c} cta={c.s.cta ?? "reserve"} />,
      figure: <Parkeerder c={c} fallback="walk" u={4} />,
    };
  }
  return { headline: <Head c={c} text={c.s.headline} max={112} />, hero: media, details: <Facts c={c} facts={c.s.facts} location={c.s.location} />, footer: <Footer c={c} cta={c.s.cta ?? "url"} /> };
};

/** A photo inside the beeldmerk bubble (py-atom-shape-bubble-image-mask, observed rule 23). */
const BubblePhoto: React.FC<{ src: string; size: number }> = ({ src, size }) => (
  <Q name="media" kind="graphic" variant="photo">
    <svg width={size} height={size * (43.423 / 36)} viewBox="0 0 36 43.423">
      <defs><clipPath id="bubbleclip"><path d="M0 18C0 8.059 8.059 0 18 0C27.941 0 36 8.059 36 18C36 27.941 27.941 36 18 36L18 42.338C18 43.009 17.264 43.426 16.691 43.077C16.691 43.077 0 34.703 0 18" /></clipPath></defs>
      <image href={staticFile(src)} x={0} y={0} width={36} height={36} preserveAspectRatio="xMidYMid slice" clipPath="url(#bubbleclip)" />
    </svg>
  </Q>
);

const prijsvergelijk = (c: Ctx): Regions => {
  const rows: { label: string; amount: number; unit?: string; struck?: boolean }[] = c.s.prices;
  if (c.t.id === "2027") {
    const size = Math.max(40 * c.k, 34);
    return {
      eyebrow: c.s.location?.label ? <Eyebrow theme={c.t} ground={c.g} text={c.s.location.label} size={30 * c.k} /> : undefined,
      headline: <Head c={c} text={c.s.headline} max={110} />,
      hero: (
        <Q name="prices" kind="text" fg={c.t.ink(c.g).text} size={size} label={rows.map((r) => `${r.label} ${euro(c.t, r.amount)}`).join(" ")}>
          <div style={{ width: c.wide ? c.hw : c.w * 0.86, fontFamily: c.t.font, color: c.t.ink(c.g).text, fontSize: size }}>
            {rows.map((r, i) => (
              <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: `${size * 0.35}px 0`, borderTop: i ? `${Math.max(2, size * 0.04)}px solid ${c.t.ink(c.g).text}` : undefined, textDecoration: r.struck ? "line-through" : undefined, fontWeight: r.struck ? 400 : c.t.weights.key }}>
                <span>{r.label}</span><span style={{ fontVariantNumeric: "tabular-nums" }}>{euro(c.t, r.amount)}</span>
              </div>
            ))}
          </div>
        </Q>
      ),
      details: c.s.body ? <Copy theme={c.t} ground={c.g} name="body" text={c.s.body} size={31 * c.k} width={c.w} /> : undefined,
      footer: <Footer c={c} cta={c.s.cta ?? "reserve"} />,
      // no parkeerder here: the price table needs the full width (stem + table = the two elements)
    };
  }
  const h = (c.story ? 120 : 104) * c.k;
  return {
    headline: <Head c={c} text={c.s.headline} max={110} />,
    hero: (
      <Stack gap={22 * c.k}>
        {c.s.location?.label && <Pill theme={c.t} name="location" text={c.s.location.label} height={h * 0.85} pin />}
        {rows.map((r, i) => (
          <Pill key={i} theme={c.t} name={`price-${i + 1}`} text={r.label} right={euro(c.t, r.amount)} height={h} width={c.wide ? c.hw : c.w * 0.86} icon={r.struck ? "py-atom-picto-car" : "py-atom-icon-calendar"} struck={r.struck} tone={r.struck ? "white" : "aqua"} />
        ))}
      </Stack>
    ),
    details: c.s.body ? <Copy theme={c.t} ground={c.g} name="body" text={c.s.body} size={36 * c.k} width={c.w} /> : undefined,
    footer: <Footer c={c} cta={c.s.cta ?? "reserve"} />,
  };
};

const stappen = (c: Ctx): Regions => {
  const steps: { illustration: string; title: string; text?: string }[] = c.s.steps;
  const d = (c.story ? 170 : 140) * c.k;
  const ink = c.t.ink(c.g);
  return {
    headline: <Head c={c} text={c.s.headline} max={104} />,
    hero: (
      <Stack gap={34 * c.k}>
        {steps.map((st, i) => (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: 30 * c.k }}>
            <Q name={`step-${i + 1}-number`} kind="text" fg={c.t.id === "feed" ? c.t.palette.blauw : ink.text} size={d * 0.42} bold label={String(i + 1)}>
              {c.t.id === "feed" ? (
                <div style={{ width: d * 0.62, height: d * 0.62, borderRadius: d, background: c.t.palette.aqua, color: c.t.palette.blauw, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: c.t.font, fontWeight: 700, fontSize: d * 0.36 }}>{i + 1}</div>
              ) : (
                <div style={{ width: d * 0.5, fontFamily: c.t.font, fontWeight: c.t.weights.display, fontSize: d * 0.5, color: ink.text, textAlign: "center" }}>{i + 1}</div>
              )}
            </Q>
            <ArtDisc theme={c.t} ground={c.g} id={st.illustration} size={d} name={`step-${i + 1}-image`} art={0.7} />
            <Copy theme={c.t} ground={c.g} name={`step-${i + 1}`} text={st.text ? `${st.title}\n${st.text}` : st.title} size={(c.story ? 44 : 40) * c.k} width={c.w - (c.t.id === "feed" ? d * 0.62 : d * 0.5) - d - 60 * c.k - 24} />
          </div>
        ))}
      </Stack>
    ),
    footer: <Footer c={c} cta={c.s.cta ?? "reserve"} />,
  };
};

const abonnement = (c: Ctx): Regions => {
  const rows: { label: string; value: string }[] = c.s.rows;
  if (c.t.id === "2027") {
    const size = Math.max(38 * c.k, 34);
    return {
      headline: <Head c={c} text={c.s.headline} max={104} />,
      hero: (
        <Q name="rows" kind="text" fg={c.t.ink(c.g).text} size={size} label={rows.map((r) => `${plain(r.label)} ${r.value}`).join(" ")}>
          <div style={{ width: c.wide ? c.hw : c.w * 0.7, fontFamily: c.t.font, fontSize: size, color: c.t.ink(c.g).text }}>
            {rows.map((r, i) => (
              <div key={i} style={{ display: "flex", justifyContent: "space-between", gap: 20, padding: `${size * 0.35}px 0`, borderTop: i ? `${Math.max(2, size * 0.04)}px solid ${c.t.ink(c.g).text}` : undefined }}>
                <span>{plain(r.label)}</span><span style={{ fontWeight: c.t.weights.key, fontVariantNumeric: "tabular-nums" }}>{r.value}</span>
              </div>
            ))}
          </div>
        </Q>
      ),
      details: c.s.body ? <Copy theme={c.t} ground={c.g} name="body" text={c.s.body} size={32 * c.k} width={c.w * 0.6} /> : undefined,
      footer: <Footer c={c} cta={c.s.cta ?? "subscribe"} />,
      figure: <Parkeerder c={c} fallback="cap-wave" />,
    };
  }
  const h = (c.story ? 118 : 104) * c.k;
  return {
    headline: <Head c={c} text={c.s.headline} max={104} />,
    hero: (
      <Stack gap={22 * c.k}>
        {rows.map((r, i) => <Pill key={i} theme={c.t} name={`row-${i + 1}`} text={r.label} right={r.value} height={h} width={c.wide ? c.hw : c.w * 0.96} icon="py-atom-icon-calendar" />)}
      </Stack>
    ),
    details: c.s.body ? <Copy theme={c.t} ground={c.g} name="body" text={c.s.body} size={32 * c.k} width={c.w} /> : undefined,
    footer: <Footer c={c} cta={c.s.cta ?? "subscribe"} />,
  };
};

const DateTile: React.FC<{ c: Ctx; date: { day: number; month: string } }> = ({ c, date }) => {
  const s = (c.story ? 210 : 180) * c.k;
  return (
    <Q name="date" kind="text" fg={c.t.palette.blauw} size={s * 0.42} bold label={`${date.day} ${date.month}`}>
      <div style={{ width: s, height: s, borderRadius: s * 0.12, background: c.t.palette.wit, color: c.t.palette.blauw, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", fontFamily: c.t.font, border: c.inv ? `${4 * c.k}px solid ${c.t.palette.blauw}` : undefined }}>
        <div style={{ fontWeight: 700, fontSize: s * 0.46, lineHeight: 1 }}>{date.day}</div>
        <div style={{ fontSize: s * 0.16 }}>{date.month}</div>
      </div>
    </Q>
  );
};

const evenement = (c: Ctx): Regions => {
  const locs: { label?: string; code: string }[] = c.s.locations ?? [];
  if (c.t.id === "2027") {
    const line = [c.s.date?.label, locs.length ? locs.map((l) => l.label ?? l.code).join(", ") : null].filter(Boolean).join("\n");
    return {
      eyebrow: c.s.eyebrow ? <Eyebrow theme={c.t} ground={c.g} text={c.s.eyebrow} size={30 * c.k} /> : undefined,
      headline: <Head c={c} text={c.s.headline} max={90} />,
      hero: c.s.price ? <PriceText theme={c.t} ground={c.g} amount={c.s.price.amount} unit={c.s.price.unit} from={c.s.price.from} size={72 * c.k} /> : undefined,
      details: line ? <Copy theme={c.t} ground={c.g} name="event-line" text={line} size={31 * c.k} width={c.w * 0.62} /> : undefined,
      footer: <Footer c={c} cta={c.s.cta ?? "reserve"} />,
      figure: <Parkeerder c={c} fallback="dance" u={6} />,
    };
  }
  const h = (c.story ? 92 : 80) * c.k;
  return {
    eyebrow: c.s.eyebrow ? <Eyebrow theme={c.t} ground={c.g} text={c.s.eyebrow} size={30 * c.k} /> : undefined,
    headline: <Head c={c} text={c.s.headline} max={110} />,
    hero: (
      <div style={{ display: "flex", alignItems: "flex-end", gap: 50 * c.k }}>
        {c.s.date && <DateTile c={c} date={c.s.date} />}
        {c.s.price && <PriceBadge theme={c.t} amount={c.s.price.amount} unit={c.s.price.unit} from={c.s.price.from} size={(c.story ? 300 : 250) * c.k} rays={false} tone="aqua" />}
        {!c.wide && <Figure theme={c.t} ground={c.g} pose={pose(c.s, "dance")} height={(c.story ? 330 : 270) * c.k} />}
      </div>
    ),
    details: locs.length ? (
      <div style={{ display: "flex", flexWrap: "wrap", gap: 14 * c.k, width: c.w }}>
        {locs.map((l, i) => <Pill key={i} theme={c.t} name={`location-${i + 1}`} text={l.label ?? l.code} height={h} pin />)}
      </div>
    ) : undefined,
    footer: <Footer c={c} cta={c.s.cta ?? "reserve"} />,
  };
};

const aftellen = (c: Ctx): Regions => {
  if (c.t.id === "2027") {
    return {
      eyebrow: c.s.eyebrow ? <Eyebrow theme={c.t} ground={c.g} text={c.s.eyebrow} size={30 * c.k} /> : undefined,
      hero: <Bubble theme={c.t} ground={c.g} text={String(c.s.number)} size={(c.story ? 440 : 380) * c.k} />,
      headline: undefined,
      details: (
        <Stack gap={24 * c.k}>
          <Head c={c} text={c.s.headline} max={96} />
          {c.s.body && <Copy theme={c.t} ground={c.g} name="body" text={c.s.body} size={31 * c.k} />}
        </Stack>
      ),
      footer: <Footer c={c} cta={c.s.cta ?? "reserve"} />,
    };
  }
  const n = (c.story ? 620 : 520) * c.k;
  return {
    eyebrow: c.s.eyebrow ? <Eyebrow theme={c.t} ground={c.g} text={c.s.eyebrow} size={30 * c.k} /> : undefined,
    hero: (
      <Q name="number" kind="text" fg={c.t.palette.aqua} size={n} bold label={String(c.s.number)}>
        <div style={{ fontFamily: c.t.font, fontWeight: 700, fontSize: n, lineHeight: 0.9, color: c.inv ? c.t.palette.blauw : c.t.palette.aqua }}>{c.s.number}</div>
      </Q>
    ),
    details: (
      <Stack gap={22 * c.k}>
        <Head c={c} text={c.s.headline} max={96} />
        {c.s.body && <Pill theme={c.t} name="body" text={c.s.body} height={84 * c.k} />}
      </Stack>
    ),
    footer: <Footer c={c} cta={c.s.cta ?? "reserve"} />,
  };
};

const service = (c: Ctx): Regions => {
  const phone: string = c.s.contact.phone;
  if (c.t.id === "2027") {
    return {
      headline: <Head c={c} text={c.s.headline} max={110} />,
      hero: (
        <Q name="contact" kind="text" fg={c.t.ink(c.g).text} size={96 * c.k} bold label={phone}>
          <div style={{ fontFamily: c.t.font, fontWeight: c.t.weights.display, fontSize: 96 * c.k, color: c.t.ink(c.g).text, fontVariantNumeric: "tabular-nums", whiteSpace: "nowrap" }}>{phone}</div>
        </Q>
      ),
      details: c.s.body ? <Copy theme={c.t} ground={c.g} name="body" text={c.s.body} size={31 * c.k} width={c.w * 0.62} /> : undefined,
      footer: <Footer c={c} cta="none" />,
      figure: <Parkeerder c={c} fallback="cap-point" />,
    };
  }
  const h = (c.story ? 190 : 160) * c.k;
  return {
    headline: <Head c={c} text={c.s.headline} max={110} />,
    hero: (
      <Q name="contact" kind="text" fg={c.t.palette.blauw} size={h * 0.4} bold label={phone}>
        <div style={{ display: "flex", alignItems: "center", gap: h * 0.2, height: h, padding: `0 ${h * 0.4}px 0 ${h * 0.12}px`, borderRadius: h / 2, background: c.t.palette.wit, fontFamily: c.t.font, fontWeight: 700, fontSize: h * 0.4, color: c.t.palette.blauw, whiteSpace: "nowrap" }}>
          <div style={{ width: h * 0.76, height: h * 0.76, borderRadius: h, background: c.t.palette.blauw, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Icon theme={c.t} id="py-atom-icon-headset-agent" size={h * 0.46} white />
          </div>
          {phone}
        </div>
      </Q>
    ),
    details: c.s.body ? <Copy theme={c.t} ground={c.g} name="body" text={c.s.body} size={36 * c.k} width={c.w} /> : undefined,
    footer: <Footer c={c} cta="none" />,
  };
};

// ---------- archetypes with their own frame ----------

/** foto-kop: own photo on top, a navy field with logo, headline and body below. Text never on the photo. */
const FotoKop: React.FC<PostProps> = (p) => {
  const c = ctx(p, undefined, "navy");
  const b = contentBox(p.format);
  const photoH = p.format === "landscape" ? b.height : Math.round(b.height * (p.format === "story" ? 0.5 : 0.52));
  const m = c.s.media;
  const left = p.format === "landscape" ? b.width * 0.5 : 0;
  return (
    <FormatProvider format={p.format}>
    <AbsoluteFill style={{ background: c.t.palette.blauw }}>
      <Q name="media" kind="graphic" variant="photo" style={{ position: "absolute", left: 0, top: p.format === "story" ? 0 : 0, width: p.format === "landscape" ? b.width * 0.5 : b.width, height: photoH }}>
        <Img src={staticFile(m.src)} style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }} />
      </Q>
      <div style={{ position: "absolute", left: left + b.x, right: b.safe.right, top: p.format === "landscape" ? b.y : photoH + 50 * c.k, bottom: b.safe.bottom, display: "flex", flexDirection: "column", gap: 30 * c.k }}>
        <Logo theme={c.t} ground="navy" width={240 * c.k} />
        <Head c={{ ...c, w: p.format === "landscape" ? b.width * 0.5 - b.x - b.safe.right : c.w }} text={c.s.headline} max={96} />
        {c.s.body && <Copy theme={c.t} ground="navy" name="body" text={c.s.body} size={32 * c.k} width={c.w} />}
        <div style={{ marginTop: "auto" }}><Footer c={c} cta={c.s.cta ?? "url"} /></div>
      </div>
    </AbsoluteFill>
    </FormatProvider>
  );
};

/** carrousel: one slide per render; grounds alternate navy and white (feed and 2027). */
const Carrousel: React.FC<PostProps> = (p) => {
  const i = p.slide ?? 0;
  const slides: { archetype: string; slots: Record<string, any> }[] = p.spec.slots.slides;
  const slide = slides[i];
  const n = slides.length;
  const g: Ground = i % 2 === 0 ? "navy" : "white";
  const c = ctx(p, slide.slots, g);
  const counter = (
    <Q name="counter" kind="text" fg={c.t.ink(g).text} size={32 * c.k} label={`${i + 1}/${n}`}>
      <div style={{ fontFamily: c.t.font, fontSize: 32 * c.k, color: c.t.ink(g).text }}>{i + 1}/{n}</div>
    </Q>
  );
  let r: Regions;
  if (slide.archetype === "carrousel-cover") {
    r = {
      headline: <div style={{ marginTop: 120 * c.k }}><Head c={c} text={slide.slots.headline} max={130} /></div>,
      details: slide.slots.subline ? <Copy theme={c.t} ground={g} name="subline" text={slide.slots.subline} size={40 * c.k} width={c.w} /> : undefined,
      footer: <Copy theme={c.t} ground={g} name="swipe" text="Swipe" size={32 * c.k} weight={c.t.weights.label} />,
      figure: <Parkeerder c={c} fallback="point" u={6} />,
    };
  } else if (slide.archetype === "carrousel-punt") {
    const d = 200 * c.k;
    r = {
      hero: slide.slots.icon ? <ArtDisc theme={c.t} ground={g} id={slide.slots.icon} size={d} name="icon" art={0.56} /> : undefined,
      headline: <Head c={c} text={slide.slots.headline} max={100} />,
      details: <Stack gap={30 * c.k}>{slide.slots.body && <Copy theme={c.t} ground={g} name="body" text={slide.slots.body} size={40 * c.k} width={c.w} />}{counter}</Stack>,
    };
  } else {
    r = {
      headline: <div style={{ marginTop: 80 * c.k }}><Head c={c} text={slide.slots.headline} max={110} /></div>,
      details: slide.slots.body ? <Copy theme={c.t} ground={g} name="body" text={slide.slots.body} size={38 * c.k} width={c.w} /> : undefined,
      footer: <Footer c={c} cta={slide.slots.cta ?? "reserve"} />,
      figure: <Parkeerder c={c} fallback="bags-cheer" u={6} />,
    };
  }
  return <Page theme={c.t} ground={g} format={p.format} regions={r} />;
};

// ---------- registry ----------

const paged = (build: (c: Ctx) => Regions): React.FC<PostProps> => (p) => {
  const c = ctx(p);
  return <Page theme={c.t} ground={c.g} format={p.format} regions={build(c)} />;
};

export const ARCHETYPES: Record<string, React.FC<PostProps>> = {
  typografisch: paged(typografisch),
  prijs: paged(prijs),
  locatie: paged(locatie),
  prijsvergelijk: paged(prijsvergelijk),
  stappen: paged(stappen),
  abonnement: paged(abonnement),
  evenement: paged(evenement),
  aftellen: paged(aftellen),
  service: paged(service),
  "foto-kop": FotoKop,
  carrousel: Carrousel,
};
