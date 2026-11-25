import React, { useEffect, useState } from "react";
import { continueRender, delayRender } from "remotion";

/**
 * QA plumbing. Every element that QA should know about is wrapped in <Q>: text, logos and graphics.
 * <Measure> waits for fonts and images, then logs one line "PY_QA_LAYOUT {json}" with the box, colours and variant
 * of every <Q>. scripts/render-spec.mjs catches that line and writes layout-<format>.json for check_brand.py.
 */
export type QKind = "text" | "logo" | "graphic";

export const Q: React.FC<{
  name: string;
  kind: QKind;
  /** Text colour (text) or main fill (graphic). */
  fg?: string;
  /** Element ID for logos and assets. */
  variant?: string;
  /** Font size in px for text, so QA can apply the large-text contrast rule. */
  size?: number;
  bold?: boolean;
  /** The visible text as written (the DOM loses spaces that are drawn as margins). */
  label?: string;
  style?: React.CSSProperties;
  children: React.ReactNode;
}> = ({ name, kind, fg, variant, size, bold, label, style, children }) => (
  <div data-qa={name} data-qa-kind={kind} data-qa-fg={fg} data-qa-variant={variant} data-qa-size={size} data-qa-bold={bold ? "1" : undefined} data-qa-label={label} style={style}>
    {children}
  </div>
);

const collect = () =>
  Array.from(document.querySelectorAll<HTMLElement>("[data-qa]")).map((el) => {
    const r = el.getBoundingClientRect();
    const d = el.dataset;
    return {
      name: d.qa,
      kind: d.qaKind,
      fg: d.qaFg ?? null,
      variant: d.qaVariant ?? null,
      size: d.qaSize ? Number(d.qaSize) : null,
      bold: d.qaBold === "1",
      text: d.qaKind === "text" ? (d.qaLabel ?? el.innerText).replace(/\s+/g, " ").trim() : null,
      box: { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) },
    };
  });

export const Measure: React.FC<{ hideText?: boolean; children: React.ReactNode }> = ({ hideText, children }) => {
  const [handle] = useState(() => delayRender("PY QA measure"));
  useEffect(() => {
    let done = false;
    const finish = () => {
      if (done) return;
      done = true;
      // The page is rendered at composition size; the scale of the output image does not change these numbers.
      console.debug("PY_QA_LAYOUT " + JSON.stringify(collect()));
      continueRender(handle);
    };
    const imgs = Array.from(document.images).filter((i) => !i.complete);
    Promise.all([document.fonts.ready, ...imgs.map((i) => new Promise((ok) => { i.onload = ok; i.onerror = ok; }))]).then(() => requestAnimationFrame(() => requestAnimationFrame(finish)));
    const t = setTimeout(finish, 8000);
    return () => clearTimeout(t);
  }, [handle]);
  return (
    <>
      {hideText && <style>{`[data-qa-kind="text"], [data-qa-kind="text"] * { color: transparent !important; text-shadow: none !important; }`}</style>}
      {children}
    </>
  );
};
