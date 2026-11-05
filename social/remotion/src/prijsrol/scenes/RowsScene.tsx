import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { PrijsrolProps, highlightIndex } from "../schema";
import { Stage } from "../../lib/layout";
import { pop, springs } from "../../lib/anim";
import { Headline } from "../../components/Headline";
import { Glyph } from "../../components/Glyph";
import { LabelPill } from "../../components/LabelPill";
import { FONT } from "../../theme";
import { euro } from "../../lib/euro";

// Beats in scene frames. Rows land one by one and count up, then the dearer ones are struck through.
export const T_ROW0 = 10;
export const T_ROW_STEP = 14;
export const T_COUNT = 18; // frames a price takes to count up
export const T_STRIKE = 72;
export const T_HIGHLIGHT = 92;
export const T_SAVING = 104;

const ease = (t: number) => 1 - Math.pow(1 - t, 3);

export const RowsScene: React.FC<PrijsrolProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const items = p.rows.items;
  const hi = highlightIndex(p);
  const max = Math.max(...items.map((r) => r.amount));
  const diff = Math.round((max - items[hi].amount) * 100) / 100;
  const rowH = 236;
  const gap = 40;
  const top = 220 + ((4 - items.length) * (rowH + gap)) / 2 - 60;
  const hiP = pop(frame, fps, T_HIGHLIGHT, springs.bouncy);
  const saving = pop(frame, fps, T_SAVING, springs.bouncy);

  return (
    <AbsoluteFill style={{ backgroundColor: p.colors.bg }}>
      <Stage>
        <Headline text={p.rows.title} color={p.colors.text} keyColor={p.colors.accent} size={96} delay={-12} top={0} />
        {items.map((r, i) => {
          const start = T_ROW0 + i * T_ROW_STEP;
          const s = pop(frame, fps, start, springs.pop);
          const count = ease(interpolate(frame, [start, start + T_COUNT], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
          const shown = count >= 1 ? r.amount : Math.round(r.amount * count); // whole euros while counting
          const isHi = i === hi;
          const strike = isHi ? 0 : interpolate(frame, [T_STRIKE + i * 4, T_STRIKE + i * 4 + 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const dim = 1 - 0.5 * strike;
          return (
            <div
              key={i}
              style={{
                position: "absolute", left: 50, right: 50, top: top + i * (rowH + gap), height: rowH, borderRadius: 48,
                background: isHi ? `rgba(50,185,205,${0.16 + 0.84 * hiP})` : "rgba(255,255,255,0.10)",
                display: "flex", alignItems: "center", padding: "0 48px", gap: 36,
                opacity: Math.min(1, s * 1.5) * dim, transform: `translateX(${(1 - s) * -120}px) scale(${isHi ? 1 + 0.04 * hiP : 1})`,
                boxShadow: isHi && hiP > 0.1 ? "0 18px 44px rgba(0,0,0,0.25)" : undefined,
              }}
            >
              <div style={{ width: 120, height: 120, borderRadius: 60, border: `5px solid ${isHi && hiP > 0.5 ? p.colors.text : p.colors.accent}`, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                <Glyph name={r.icon} size={68} color={p.colors.text} tint="white" />
              </div>
              <div style={{ flex: 1, fontFamily: FONT, fontSize: 62, color: p.colors.text, fontWeight: isHi ? 500 : 400, whiteSpace: "nowrap" }}>{r.label}</div>
              <div style={{ position: "relative", fontFamily: FONT, fontWeight: 700, fontSize: 116, color: p.colors.text, fontVariantNumeric: "tabular-nums", whiteSpace: "nowrap" }}>
                {euro(shown)}
                {r.suffix && <span style={{ fontSize: 48, fontWeight: 400 }}>{r.suffix}</span>}
                <div style={{ position: "absolute", left: -8, top: "54%", height: 10, borderRadius: 5, width: `${strike * 104}%`, background: p.colors.accent, transform: "rotate(-8deg)" }} />
              </div>
            </div>
          );
        })}
        {p.rows.saving && diff > 0 && (
          <div style={{ position: "absolute", left: 0, right: 0, top: 1150, display: "flex", justifyContent: "center", opacity: Math.min(1, saving * 1.5), transform: `scale(${0.6 + 0.4 * saving})` }}>
            <LabelPill text={p.rows.saving.replace("{x}", euro(diff))} bg={p.colors.text} fg={p.colors.bg} keyColor={p.colors.accent} height={132} />
          </div>
        )}
      </Stage>
    </AbsoluteFill>
  );
};
