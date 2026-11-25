import React, { createContext, useContext, useLayoutEffect, useRef, useState } from "react";
import { AbsoluteFill, Img, continueRender, delayRender, staticFile } from "remotion";
import { parseRich } from "../lib/rich";
import { Q } from "./qa";
import { contentBox, FormatId } from "./spec";
import { euro, Ground, Theme } from "./themes";
import elements from "../../../../elements.json";

/** Library artwork drawn in white only (elements.json colours): it needs a navy ground, never a white disc. */
const WHITE_ART = new Set(
  (elements as any).elements
    .filter((e: any) => e.colors?.length && e.colors.every((c: any) => String(c?.hex ?? c).toUpperCase() === "#FFFFFF"))
    .map((e: any) => e.id as string),
);
export const isWhiteArt = (id: string) => WHITE_ART.has(id);

/**
 * A pictogram or illustration on a round disc that keeps it visible on any ground: coloured artwork on a white disc,
 * white artwork straight on navy, or on a navy disc on white grounds.
 */
export const ArtDisc: React.FC<{ theme: Theme; ground: Ground; id: string; size: number; name: string; art?: number }> = ({ theme, ground, id, size, name, art = 0.62 }) => {
  const white = isWhiteArt(id);
  const onWhite = ground === "white";
  const disc = white ? (onWhite ? theme.palette.blauw : "transparent") : theme.palette.wit;
  const border = !white && onWhite ? `${Math.max(2, size * 0.02)}px solid ${theme.palette.blauw}` : undefined;
  return (
    <Q name={name} kind="graphic" variant={id}>
      <div style={{ width: size, height: size, borderRadius: size, background: disc, border, boxSizing: "border-box", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <Asset theme={theme} id={id} width={size * (white && !onWhite ? 0.9 : art)} height={size * (white && !onWhite ? 0.9 : art)} />
      </div>
    </Q>
  );
};

/**
 * Static, theme-aware building blocks. Every colour comes from theme.palette or theme.fill; no shadows, lights,
 * grain, vignettes or extra gradients (decision S13). Every visible part is wrapped in <Q> for QA.
 */

/** Visible text of a rich string: no key markers, line breaks as spaces. */
export const plain = (t: string) => t.replace(/\*/g, "").replace(/\s*\n\s*/g, " ");

/**
 * Smallest text size on the canvas: 12 px when the post is seen at about 0.4x on a phone. A 1200 px wide canvas
 * is shown at the same width as a 1080 one, so it needs proportionally bigger text. Page provides the format.
 */
const FormatCtx = createContext<FormatId>("feed");
const minText = (f: FormatId) => (12 / 0.4) * (f === "square" || f === "landscape" ? 1200 / 1080 : 1);
export const useMinText = () => minText(useContext(FormatCtx));
const clampSize = (size: number, min: number) => Math.max(size, min);

/** Size scale per format: the layouts are drawn for a 1080 x 1350 feed post. */
export const scaleOf = (f: FormatId) => (f === "landscape" ? 0.74 : f === "square" ? 0.95 : f === "story" ? 1.04 : 1);

// ---------- text ----------

const AVG = { feed: { reg: 0.53, key: 0.58 }, "2027": { reg: 0.54, key: 0.62 } };

/** Largest size at which the widest line fits the width (character-width estimate, no DOM measuring). */
export const fit = (theme: Theme, text: string, width: number, max: number, min = 40) => {
  const a = AVG[theme.id];
  let widest = 0;
  for (const line of parseRich(text)) {
    let w = 0;
    line.forEach((word, i) => {
      word.forEach((seg) => (w += seg.text.length * (seg.key ? a.key : a.reg)));
      if (i < line.length - 1) w += 0.27;
    });
    widest = Math.max(widest, w);
  }
  return Math.max(min, Math.min(max, Math.floor(width / Math.max(widest, 1))));
};

const RichLine: React.FC<{ theme: Theme; text: string; color: string; keyColor?: string }> = ({ theme, text, color, keyColor }) => (
  <>
    {text.split(/(\*[^*]+\*)/g).filter(Boolean).map((part, i) =>
      part.startsWith("*") && part.endsWith("*") ? (
        <span key={i} style={{ fontWeight: theme.weights.key, color: keyColor ?? color }}>{part.slice(1, -1)}</span>
      ) : (
        <span key={i}>{part}</span>
      ),
    )}
  </>
);

export const Headline: React.FC<{ theme: Theme; ground: Ground; text: string; width: number; max: number; name?: string; color?: string }> = ({ theme, ground, text, width, max, name = "headline", color }) => {
  const ink = theme.ink(ground);
  const c = color ?? ink.text;
  const size = fit(theme, text, width, max);
  const lh = theme.id === "2027" ? 50 / 48 : 1.06;
  return (
    <Q name={name} kind="text" fg={c} size={size} bold label={plain(text)}>
      <div style={{ width, fontFamily: theme.font, fontSize: size, lineHeight: lh, color: c, fontWeight: theme.weights.regular, letterSpacing: theme.id === "feed" ? "-0.015em" : "-0.01em" }}>
        {text.split("\n").map((l, i) => (
          <div key={i} style={{ whiteSpace: "nowrap" }}><RichLine theme={theme} text={l} color={c} keyColor={ink.key} /></div>
        ))}
      </div>
    </Q>
  );
};

export const Copy: React.FC<{ theme: Theme; ground: Ground; name: string; text: string; size: number; width?: number; weight?: number; color?: string; align?: "left" | "center" }> = ({ theme, ground, name, text, size: wanted, width, weight, color, align = "left" }) => {
  const size = clampSize(wanted, useMinText());
  const c = color ?? theme.ink(ground).text;
  return (
    <Q name={name} kind="text" fg={c} size={size} bold={!!weight && weight >= 600} label={plain(text)}>
      <div style={{ width, maxWidth: "100%", fontFamily: theme.font, fontSize: size, lineHeight: 1.3, color: c, fontWeight: weight ?? theme.weights.regular, textAlign: align }}>
        {text.split("\n").map((l, i) => <div key={i}><RichLine theme={theme} text={l} color={c} /></div>)}
      </div>
    </Q>
  );
};

export const Eyebrow: React.FC<{ theme: Theme; ground: Ground; text: string; size: number }> = ({ theme, ground, text, size: wanted }) => {
  const size = clampSize(wanted, useMinText());
  const ink = theme.ink(ground);
  if (theme.id === "2027") {
    return (
      <Q name="eyebrow" kind="text" fg={ink.text} size={size} bold label={text}>
        <div style={{ fontFamily: theme.font, fontSize: size, fontWeight: theme.weights.label, letterSpacing: "0.08em", textTransform: "uppercase", color: ink.text }}>{text}</div>
      </Q>
    );
  }
  // feed: a white pill outline with the text, as the GLOW and campaign tags
  return (
    <Q name="eyebrow" kind="text" fg={ink.text} size={size} bold label={text}>
      <div style={{ display: "inline-block", padding: `${size * 0.35}px ${size * 0.8}px`, borderRadius: size * 2, border: `${Math.max(2, size * 0.08)}px solid ${ink.text}`, fontFamily: theme.font, fontSize: size, fontWeight: theme.weights.label, color: ink.text, whiteSpace: "nowrap" }}>{text}</div>
    </Q>
  );
};

// ---------- marks ----------

export const Asset: React.FC<{ theme: Theme; id: string; width?: number; height?: number; white?: boolean; style?: React.CSSProperties }> = ({ theme, id, width, height, white, style }) => (
  <Img src={theme.asset(id)} style={{ width, height, objectFit: "contain", display: "block", filter: white ? "brightness(0) invert(1)" : undefined, ...style }} />
);

export const Logo: React.FC<{ theme: Theme; ground: Ground; width: number }> = ({ theme, ground, width }) => {
  const id = theme.ink(ground).logo;
  return (
    <Q name="logo" kind="logo" variant={id}>
      <Asset theme={theme} id={id} width={width} />
    </Q>
  );
};

/** "parkingyou.nl" as plain text. The chevron belongs to the voordeligparkeren sub-brand logo only (decision S14). */
export const Url: React.FC<{ theme: Theme; ground: Ground; size: number; prefix?: string }> = ({ theme, ground, size: wanted, prefix }) => {
  const size = clampSize(wanted, useMinText());
  const c = theme.ink(ground).text;
  const text = prefix ? `${prefix} ${theme.url}` : theme.url;
  return (
    <Q name="url" kind="text" fg={c} size={size} bold label={text}>
      <div style={{ fontFamily: theme.font, fontSize: size, color: c, fontWeight: theme.weights.label, whiteSpace: prefix ? "normal" : "nowrap", lineHeight: 1.3 }}>{text}</div>
    </Q>
  );
};

/** De stem (2027): the half arc that opens a message; height = the block it opens. Aqua on navy and white. */
export const Stem: React.FC<{ theme: Theme; height: number }> = ({ theme, height }) => (
  <Q name="stem" kind="graphic" fg={theme.palette.aqua} variant="2027/arc">
    <Asset theme={theme} id="2027/arc" height={height} width={(height * 10) / 45.44} />
  </Q>
);

/** A block opened by de stem (2027) or shown as is (feed). */
export const Opened: React.FC<{ theme: Theme; height: number; children: React.ReactNode }> = ({ theme, height, children }) =>
  theme.id === "2027" ? (
    <div style={{ display: "flex", alignItems: "center", gap: height * 0.3 * 0.45 }}>
      <Stem theme={theme} height={height} />
      <div>{children}</div>
    </div>
  ) : (
    <>{children}</>
  );

/** One parkeerder standing on a short line (2027), or a library figure (feed). */
export const Figure: React.FC<{ theme: Theme; ground: Ground; pose: string; height: number; flip?: boolean; line?: number }> = ({ theme, ground, pose, height, flip, line }) => {
  const colour = theme.ink(ground).figure;
  const fg = colour === "white" ? theme.palette.wit : theme.palette.blauw;
  const p = pose.replace(/^py-atom-figure-/, "");
  if (theme.id === "2027") {
    const id = `2027/figure-${p}-${colour}${flip ? "-flip" : ""}`;
    return (
      <Q name="figure" kind="graphic" fg={fg} variant={id}>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
          <Asset theme={theme} id={id} height={height} />
          <div style={{ width: line ?? height * 0.62, height: Math.max(3, height * 0.02), background: fg }} />
        </div>
      </Q>
    );
  }
  const id = `py-atom-figure-${p}`;
  return (
    <Q name="figure" kind="graphic" fg={fg} variant={id}>
      <Asset theme={theme} id={id} height={height} white={colour === "white"} style={{ transform: flip ? "scaleX(-1)" : undefined }} />
    </Q>
  );
};

/** A pictogram or icon from the library in the ink colour of the ground (or a given colour: white or navy only). */
export const Icon: React.FC<{ theme: Theme; id: string; size: number; white: boolean }> = ({ theme, id, size, white }) => (
  <Asset theme={theme} id={id} width={size} height={size} white={white} />
);

// ---------- feed elements (theme feed only) ----------

/** Round price badge: white with navy, or aqua with navy (white on aqua fails contrast). Italic numerals, small cents. */
export const PriceBadge: React.FC<{ theme: Theme; amount: number; unit: string; size: number; tone?: "white" | "aqua"; from?: boolean; rays?: boolean }> = ({ theme, amount, unit, size, tone = "white", from, rays = true }) => {
  const P = theme.palette;
  const bg = tone === "white" ? P.wit : P.aqua;
  const fg = P.blauw;
  const s = euro(theme, amount);
  const [main, cents] = s.includes(",") ? [s.split(",")[0], "," + s.split(",")[1]] : [s, ""];
  const fs = size * (main.length > 3 ? 0.31 : 0.38);
  return (
    <div style={{ position: "relative", width: size, height: size, margin: rays ? size * 0.26 : 0 }}>
      {rays && (
        <svg width={size * 1.5} height={size * 1.5} viewBox="-75 -75 150 150" style={{ position: "absolute", left: -size * 0.25, top: -size * 0.25 }}>
          {Array.from({ length: 24 }, (_, i) => {
            const a = (i / 24) * Math.PI * 2;
            const r1 = 56, r2 = i % 2 ? 66 : 72;
            return <line key={i} x1={Math.cos(a) * r1} y1={Math.sin(a) * r1} x2={Math.cos(a) * r2} y2={Math.sin(a) * r2} stroke={P.wit} strokeWidth={1.6} strokeLinecap="round" />;
          })}
        </svg>
      )}
      <Q name="price" kind="text" fg={fg} size={fs} bold label={`${s} ${unit}`} style={{ position: "absolute", inset: 0 }}>
        <div style={{ width: size, height: size, borderRadius: size / 2, background: bg, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", transform: "rotate(-7deg)", fontFamily: theme.font, color: fg }}>
          {from && <div style={{ fontSize: size * 0.09, marginBottom: size * 0.01 }}>vanaf</div>}
          <div style={{ display: "flex", alignItems: "flex-start", fontWeight: 700, fontStyle: theme.rules.italicPrices ? "italic" : "normal", fontSize: fs, lineHeight: 1, letterSpacing: "-0.02em" }}>
            <span>{main}</span>
            {cents && <span style={{ fontSize: fs * 0.48, marginTop: fs * 0.06 }}>{cents}</span>}
          </div>
          <div style={{ fontSize: size * 0.095, marginTop: size * 0.02 }}>{unit}</div>
        </div>
      </Q>
    </div>
  );
};

/** White pill with a navy icon disc (or pin) and navy text: facts, places, rows. */
export const Pill: React.FC<{ theme: Theme; name: string; text: string; height: number; icon?: string; pin?: boolean; right?: string; width?: number; struck?: boolean; tone?: "white" | "aqua" }> = ({ theme, name, text, height: wanted, icon, pin, right, width, struck, tone = "white" }) => {
  const height = clampSize(wanted, useMinText() / 0.4);
  const P = theme.palette;
  const fs = height * 0.4;
  const bg = tone === "aqua" ? P.aqua : P.wit;
  const fg = P.blauw;
  return (
    <Q name={name} kind="text" fg={fg} size={fs} label={plain(text) + (right ? " " + right : "")}>
      <div style={{ display: "inline-flex", alignItems: "center", gap: height * 0.2, height, width, padding: `0 ${height * 0.4}px 0 ${icon || pin ? height * 0.12 : height * 0.4}px`, borderRadius: height / 2, background: bg, fontFamily: theme.font, fontSize: fs, color: fg, whiteSpace: "nowrap", boxSizing: "border-box" }}>
        {icon && (
          <div style={{ width: height * 0.76, height: height * 0.76, borderRadius: height, background: P.blauw, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
            <Icon theme={theme} id={icon} size={height * 0.44} white />
          </div>
        )}
        {pin && !icon && (
          <svg width={height * 0.34} height={height * 0.46} viewBox="0 0 30 40" style={{ marginLeft: height * 0.2 }}><path d="M15 0C6.7 0 0 6.6 0 14.8C0 25.9 15 40 15 40C15 40 30 25.9 30 14.8C30 6.6 23.3 0 15 0ZM15 20.5C11.8 20.5 9.3 18 9.3 14.8C9.3 11.6 11.8 9.1 15 9.1C18.2 9.1 20.7 11.6 20.7 14.8C20.7 18 18.2 20.5 15 20.5Z" fill={P.blauw} /></svg>
        )}
        <span style={{ flex: 1, textDecoration: struck ? "line-through" : undefined }}><RichLine theme={theme} text={text} color={fg} /></span>
        {right && <span style={{ fontWeight: 700, textDecoration: struck ? "line-through" : undefined }}>{right}</span>}
      </div>
    </Q>
  );
};

/** CTA button (feed): aqua pill, navy label (white on aqua fails contrast), library arrow circle on the left. */
export const CtaButton: React.FC<{ theme: Theme; text: string; height: number }> = ({ theme, text, height: wanted }) => {
  const height = clampSize(wanted, useMinText() / 0.38);
  const P = theme.palette;
  return (
    <Q name="cta" kind="text" fg={P.blauw} size={height * 0.38} bold label={text}>
      <div style={{ display: "inline-flex", alignItems: "center", gap: height * 0.22, height, padding: `0 ${height * 0.42}px 0 ${height * 0.12}px`, borderRadius: height / 2, background: P.aqua, fontFamily: theme.font, fontWeight: 500, fontSize: height * 0.38, color: P.blauw, whiteSpace: "nowrap" }}>
        <Asset theme={theme} id="py-atom-arrow-right-circle" width={height * 0.76} height={height * 0.76} />
        {text}
      </div>
    </Q>
  );
};

/** De bubbel (2027) or a round badge (feed) with one short item: a number, a level, a word of at most 6 characters. */
export const Bubble: React.FC<{ theme: Theme; ground: Ground; text: string; size: number }> = ({ theme, ground, text, size }) => {
  const P = theme.palette;
  const onNavy = ground !== "white";
  const fill = onNavy ? P.aqua : P.blauw;
  const fg = onNavy ? P.blauw : P.wit;
  const fs = size * (text.length > 2 ? 0.32 : 0.44);
  return (
    <Q name="bubble" kind="text" fg={fg} size={fs} bold label={text}>
      <div style={{ position: "relative", width: size, height: size * (43.423 / 36) }}>
        <svg width={size} height={size * (43.423 / 36)} viewBox="0 0 36 43.423" style={{ position: "absolute", inset: 0 }}>
          <path d="M0 18C0 8.059 8.059 0 18 0C27.941 0 36 8.059 36 18C36 27.941 27.941 36 18 36L18 42.338C18 43.009 17.264 43.426 16.691 43.077C16.691 43.077 0 34.703 0 18" fill={fill} />
        </svg>
        <div style={{ position: "absolute", left: 0, top: 0, width: size, height: size, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: theme.font, fontWeight: theme.weights.display, fontSize: fs, color: fg, fontVariantNumeric: "tabular-nums" }}>{text}</div>
      </div>
    </Q>
  );
};

/** Price as text (2027, and feed rows): amount in display weight, unit regular beside it. */
export const PriceText: React.FC<{ theme: Theme; ground: Ground; amount: number; unit: string; size: number; from?: boolean; note?: string }> = ({ theme, ground, amount, unit, size, from, note }) => {
  const c = theme.ink(ground).text;
  const s = euro(theme, amount);
  return (
    <Q name="price" kind="text" fg={c} size={size} bold label={`${from ? "vanaf " : ""}${s} ${unit}`}>
      <div style={{ fontFamily: theme.font, color: c }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: size * 0.25 }}>
          {from && <span style={{ fontSize: size * 0.4 }}>vanaf</span>}
          <span style={{ fontSize: size, fontWeight: theme.weights.display, fontVariantNumeric: "tabular-nums", lineHeight: 1 }}>{s}</span>
          <span style={{ fontSize: size * 0.4 }}>{unit}</span>
        </div>
        {note && <div style={{ fontSize: size * 0.4, marginTop: size * 0.15, opacity: 1 }}>{note}</div>}
      </div>
    </Q>
  );
};

// ---------- page ----------

/**
 * Scales its content down (never up) so it fits the box it gets from the layout. The hero of a post (badge, steps,
 * rows) has a natural size; on a format with less room it shrinks instead of running into the headline.
 */
export const FitBox: React.FC<{ align?: "center" | "flex-start"; children: React.ReactNode }> = ({ align = "center", children }) => {
  const outer = useRef<HTMLDivElement>(null);
  const inner = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(1);
  const [handle] = useState(() => delayRender("PY FitBox"));
  useLayoutEffect(() => {
    const o = outer.current, i = inner.current;
    if (o && i) {
      const s = Math.min(1, o.clientHeight / Math.max(1, i.scrollHeight), o.clientWidth / Math.max(1, i.scrollWidth));
      setScale(Number.isFinite(s) && s > 0 ? s : 1);
    }
    continueRender(handle);
  }, [handle]);
  return (
    <div ref={outer} style={{ width: "100%", height: "100%", display: "flex", alignItems: "center", justifyContent: align, overflow: "visible" }}>
      <div ref={inner} style={{ transform: `scale(${scale})`, transformOrigin: align === "center" ? "center" : "left center" }}>{children}</div>
    </div>
  );
};

export type Regions = {
  eyebrow?: React.ReactNode;
  headline?: React.ReactNode;
  hero?: React.ReactNode;
  details?: React.ReactNode;
  footer?: React.ReactNode;
  /** 2027: the one parkeerder, bottom right on the bottom margin. */
  figure?: React.ReactNode;
  /** Full-bleed layer under everything (photo, watermark). */
  under?: React.ReactNode;
};

/**
 * The page frame shared by all archetypes. Portrait formats stack logo, eyebrow, headline, hero (flexible), details
 * and footer inside the safe content box; landscape puts the text left and the hero right. Theme feed centres the
 * logo on top; theme 2027 puts it top left on a 2u margin (u = 54 px on 1080 wide).
 */
export const Page: React.FC<{ theme: Theme; ground: Ground; format: FormatId; regions: Regions; gap?: number }> = ({ theme, ground, format, regions, gap }) => {
  const b = contentBox(format);
  const k = scaleOf(format);
  const m27 = format === "landscape" ? 64 : 108;
  const box = theme.id === "2027" ? { x: Math.max(b.x, m27), y: Math.max(b.y, format === "landscape" ? 64 : 108), r: Math.max(b.safe.right, m27), bt: Math.max(b.safe.bottom, format === "landscape" ? 64 : 108) } : { x: b.x, y: b.y, r: b.safe.right, bt: b.safe.bottom };
  const w = b.width - box.x - box.r;
  const h = b.height - box.y - box.bt;
  const logoW = (format === "landscape" ? 250 : 280) * (theme.id === "2027" ? 0.86 : 1);
  const G = gap ?? 44 * k;
  const bgFill = ground === "photo" ? theme.palette.blauw : theme.fill(ground);
  const logo = <Logo theme={theme} ground={ground === "photo" ? "navy" : ground} width={logoW} />;

  if (format === "landscape") {
    return (
      <FormatCtx.Provider value={format}>
      <AbsoluteFill style={{ background: bgFill }}>
        {regions.under}
        <div style={{ position: "absolute", left: box.x, top: box.y, width: w * 0.6, height: h, display: "flex", flexDirection: "column", gap: G * 0.5 }}>
          <div style={{ marginBottom: 34 }}>{logo}</div>
          {regions.eyebrow}
          {regions.headline}
          {regions.details}
          <div style={{ marginTop: "auto" }}>{regions.footer}</div>
        </div>
        <div style={{ position: "absolute", left: box.x + w * 0.62, top: box.y, width: w * 0.38, height: h, display: "flex", alignItems: "center", justifyContent: "center" }}>
          {regions.hero && <FitBox>{regions.hero}</FitBox>}
          {!regions.hero && regions.figure}
        </div>
      </AbsoluteFill>
      </FormatCtx.Provider>
    );
  }

  return (
    <FormatCtx.Provider value={format}>
    <AbsoluteFill style={{ background: bgFill }}>
      {regions.under}
      <div style={{ position: "absolute", left: box.x, top: box.y, width: w, height: h, display: "flex", flexDirection: "column", gap: G }}>
        <div style={{ display: "flex", justifyContent: theme.id === "feed" ? "center" : "flex-start" }}>{logo}</div>
        {regions.eyebrow && <div style={{ marginTop: G * 0.4 }}>{regions.eyebrow}</div>}
        {regions.headline}
        <div style={{ flex: 1, minHeight: 0, display: "flex", alignItems: "center", justifyContent: theme.id === "feed" ? "center" : "flex-start" }}>
          {regions.hero && <FitBox align={theme.id === "feed" ? "center" : "flex-start"}>{regions.hero}</FitBox>}
        </div>
        {regions.details && <div style={{ maxWidth: regions.figure ? w * 0.56 : undefined }}>{regions.details}</div>}
        {regions.footer && <div style={{ maxWidth: regions.figure ? w * 0.56 : undefined }}>{regions.footer}</div>}
      </div>
      {regions.figure && <div style={{ position: "absolute", right: box.r, bottom: box.bt }}>{regions.figure}</div>}
    </AbsoluteFill>
    </FormatCtx.Provider>
  );
};

/** For archetypes with their own frame (foto-kop). */
export const FormatProvider: React.FC<{ format: FormatId; children: React.ReactNode }> = ({ format, children }) => <FormatCtx.Provider value={format}>{children}</FormatCtx.Provider>;

/** The beeldmerk watermark from the library (aqua at 5 %, observed rule 7), centred and large. */
export const Watermark: React.FC<{ theme: Theme; size: number }> = ({ theme, size }) => (
  <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
    <Q name="watermark" kind="graphic" variant="py-atom-logo-beeldmerk-watermark" fg={theme.palette.aqua}>
      <Asset theme={theme} id="py-atom-logo-beeldmerk-watermark" width={size} />
    </Q>
  </AbsoluteFill>
);

/** A photo (public/media/...) or an illustration element; photos never carry text (2027 CS 9). */
export const Media: React.FC<{ theme: Theme; media?: { type: string; src: string; alt?: string }; width: number; height: number; mask?: boolean; white?: boolean }> = ({ theme, media, width, height, mask, white }) => {
  if (!media) return null;
  if (media.type === "illustration") {
    return (
      <Q name="media" kind="graphic" variant={media.src}>
        <Asset theme={theme} id={media.src} width={width} height={height} white={white} />
      </Q>
    );
  }
  return (
    <Q name="media" kind="graphic" variant="photo">
      <Img src={staticFile(media.src)} style={{ width, height, objectFit: "cover", display: "block" }} />
    </Q>
  );
};
