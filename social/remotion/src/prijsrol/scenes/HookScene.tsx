import React from "react";
import { PrijsrolProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { PlacePill, PriceBadge, TopLogo } from "../../v2/Badges";
import { BRAND } from "../../theme";

export const T_PILL = 30;

/** Hook: GLOW gradient, big question, the prices as round badges tumbling in, the location pill. */
export const HookScene: React.FC<PrijsrolProps & { dur: number }> = (p) => {
  const items = p.rows.items;
  const n = items.length;
  const S = n > 3 ? 280 : 340;
  const slots = [
    { x: 0.06, y: 560, r: -10 },
    { x: 0.52, y: 640, r: 7 },
    { x: 0.3, y: 840, r: -4 },
    { x: 0.62, y: 900, r: 9 },
  ];
  return (
    <Backdrop kind="glow" seed="r2hook">
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center" }}>
          <TopLogo width={320} />
        </div>
        <div style={{ position: "absolute", left: 60, top: 140 }}>
          <Title text={p.hook.headline} color={BRAND.wit} maxSize={160} width={960} delay={-14} end={p.dur} />
        </div>
        {items.map((it, i) => {
          const s = slots[i];
          const last = i === n - 1;
          return (
            <div key={i} style={{ position: "absolute", left: s.x * STAGE_W, top: s.y - (n > 3 ? 40 : 0) }}>
              <PriceBadge amount={it.amount} label="" start={-6 + i * 5} size={last ? S * 1.12 : S} tone={last ? "white" : "aqua"} rotate={s.r} />
            </div>
          );
        })}
        <div style={{ position: "absolute", left: 60, top: 1250 }}>
          <PlacePill name={p.location.name} start={T_PILL} height={112} />
        </div>
      </Stage>
    </Backdrop>
  );
};
