import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { PrijsrolProps, highlightIndex } from "../schema";
import { Stage } from "../../lib/layout";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { TopLogo } from "../../v2/Badges";
import { Card } from "../../v2/Card";
import { enter, leave, EASE_OUT } from "../../v2/ease";
import { BRAND, FONT } from "../../theme";
import { Rich } from "../../lib/rich";
import { euro } from "../../lib/euro";

export const T_ROW0 = 14;
export const T_ROW_STEP = 9;
export const T_COUNT = 22;
export const T_STRIKE = 70;
export const T_HIGHLIGHT = 86;
export const T_SAVING = 98;

/** Price rows as white cards: prices count up, dearer ones get an aqua strike and dim, the cheapest turns aqua. */
export const RowsScene: React.FC<PrijsrolProps & { dur: number }> = (p) => {
  const frame = useCurrentFrame();
  const items = p.rows.items;
  const hi = highlightIndex(p);
  const max = Math.max(...items.map((r) => r.amount));
  const diff = Math.round((max - items[hi].amount) * 100) / 100;
  const out = leave(frame, p.dur - 4, 12);
  const hiP = enter(frame, T_HIGHLIGHT, 16);
  const save = enter(frame, T_SAVING, 20);
  const H = 190;
  return (
    <Backdrop kind="navy" seed="r2rows">
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center" }}>
          <TopLogo width={320} start={-20} />
        </div>
        <div style={{ position: "absolute", left: 60, top: 150 }}>
          <Title text={p.rows.title} color={BRAND.wit} maxSize={140} width={960} delay={-4} end={p.dur} />
        </div>
        <div style={{ position: "absolute", left: 50, right: 50, top: 560, display: "flex", flexDirection: "column", gap: 40 }}>
          {items.map((r, i) => {
            const start = T_ROW0 + i * T_ROW_STEP;
            const e = enter(frame, start, 22);
            const c = enter(frame, start + 4, T_COUNT, EASE_OUT);
            const shown = c >= 1 ? r.amount : Math.round(r.amount * c);
            const isHi = i === hi;
            const strike = isHi ? 0 : enter(frame, T_STRIKE + i * 4, 12);
            const bg = isHi ? `rgb(${Math.round(255 - (255 - 50) * hiP)},${Math.round(255 - (255 - 185) * hiP)},${Math.round(255 - (255 - 205) * hiP)})` : BRAND.wit;
            const fg = isHi && hiP > 0.5 ? BRAND.wit : BRAND.blauw;
            return (
              <Card
                key={i}
                icon={r.icon}
                text={r.label}
                height={H}
                bg={bg}
                fg={fg}
                disc={isHi && hiP > 0.5 ? BRAND.blauw : BRAND.blauw}
                textWidth={520}
                maxFont={60}
                style={{ opacity: Math.min(1, e * 1.3) * (1 - 0.45 * strike) * (1 - out), transform: `translateX(${(1 - e) * -110 + out * 60}%) scale(${isHi ? 1 + 0.045 * hiP : 1})`, boxShadow: isHi && hiP > 0 ? `0 0 ${60 * hiP}px rgba(50,185,205,${0.55 * hiP}), 0 18px 40px rgba(4,10,40,0.26)` : undefined }}
                right={
                  <div style={{ position: "relative", fontFamily: FONT, fontWeight: 700, fontStyle: "italic", fontSize: 104, color: fg, fontVariantNumeric: "tabular-nums" }}>
                    {euro(shown)}
                    {r.suffix && <span style={{ fontSize: 44, fontWeight: 400, fontStyle: "normal" }}>{r.suffix}</span>}
                    <div style={{ position: "absolute", left: -10, top: "52%", height: 12, borderRadius: 6, width: `${strike * 112}%`, background: BRAND.aqua, transform: "rotate(-9deg)", transformOrigin: "0 50%" }} />
                  </div>
                }
              />
            );
          })}
        </div>
        {p.rows.saving && diff > 0 && (
          <div style={{ position: "absolute", left: 0, right: 0, top: 1230, display: "flex", justifyContent: "center", opacity: save * (1 - out), transform: `translateY(${(1 - save) * 30}px) scale(${0.9 + 0.1 * save})` }}>
            <div style={{ height: 116, padding: "0 50px", borderRadius: 58, background: BRAND.wit, display: "flex", alignItems: "center", fontFamily: FONT, fontSize: 52, color: BRAND.blauw, boxShadow: "0 14px 34px rgba(4,10,40,0.25)" }}>
              <span style={{ whiteSpace: "pre" }}><Rich text={p.rows.saving.replace("{x}", euro(diff))} keyColor={BRAND.blauw} /></span>
            </div>
          </div>
        )}
      </Stage>
    </Backdrop>
  );
};
export const _i = interpolate;
