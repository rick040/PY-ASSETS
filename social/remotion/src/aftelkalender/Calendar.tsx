import React from "react";
import { BRAND, FONT } from "../theme";

/** One calendar page in the style of py-comp-calendar-date: navy header with two rings, white body, big day, month. */
export const Page: React.FC<{ w: number; day: number; month: string; highlight?: number }> = ({ w, day, month, highlight = 0 }) => {
  const h = w * 1.08;
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, borderRadius: w * 0.09, background: BRAND.wit, overflow: "hidden", boxShadow: `0 0 0 ${highlight * 10}px rgba(50,185,205,${0.9 * highlight})` }}>
      <div style={{ height: h * 0.22, background: BRAND.blauw }} />
      <div style={{ position: "absolute", top: h * 0.22, left: 0, right: 0, bottom: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", fontFamily: FONT, color: BRAND.blauw }}>
        <div style={{ fontWeight: 700, fontSize: w * 0.46, lineHeight: 1, letterSpacing: "-0.03em", fontVariantNumeric: "tabular-nums" }}>{day}</div>
        <div style={{ fontWeight: 400, fontSize: w * 0.13, marginTop: w * 0.01 }}>{month}</div>
      </div>
    </div>
  );
};

/** Tear-off calendar: page `index` (fractional) is flipping away over the top edge, the next page shows underneath. */
export const FlipCalendar: React.FC<{ w: number; dates: Array<{ day: number; month: string }>; progress: number; highlight: number }> = ({ w, dates, progress, highlight }) => {
  const n = dates.length;
  const idx = progress * (n - 1);
  const cur = Math.min(n - 1, Math.floor(idx));
  const frac = idx - cur;
  const next = Math.min(n - 1, cur + 1);
  const h = w * 1.08;
  return (
    <div style={{ position: "relative", width: w, height: h, perspective: w * 3 }}>
      {/* rings */}
      {[0.27, 0.73].map((x) => (
        <div key={x} style={{ position: "absolute", left: w * x - w * 0.035, top: -w * 0.07, width: w * 0.07, height: w * 0.17, borderRadius: w * 0.035, background: BRAND.wit, border: `${w * 0.012}px solid ${BRAND.blauw}`, zIndex: 3 }} />
      ))}
      {cur === n - 1 ? (
        <Page w={w} {...dates[cur]} highlight={highlight} />
      ) : (
        <>
          <Page w={w} {...dates[next]} />
          <div style={{ position: "absolute", inset: 0, transformOrigin: "50% 0%", transform: `rotateX(${frac * 115}deg)`, backfaceVisibility: "hidden", filter: `brightness(${1 - frac * 0.35})` }}>
            <Page w={w} {...dates[cur]} />
          </div>
        </>
      )}
    </div>
  );
};
