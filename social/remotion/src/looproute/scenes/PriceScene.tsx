import React from "react";
import { useCurrentFrame } from "remotion";
import { LooprouteProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { PriceBadge, TopLogo } from "../../v2/Badges";
import { Sunburst } from "../../v2/Fx";
import { enter } from "../../v2/ease";
import { BRAND, FONT } from "../../theme";
import { Rich } from "../../lib/rich";

export const T_BADGE = 12;
export const T_NOTE = 32;

export const PriceScene: React.FC<LooprouteProps & { dur: number }> = (p) => {
  const frame = useCurrentFrame();
  const note = enter(frame, T_NOTE, 18);
  const S = 520;
  return (
    <Backdrop kind="navy" seed="r3price">
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center" }}>
          <TopLogo width={320} start={-20} />
        </div>
        <div style={{ position: "absolute", left: 60, top: 150 }}>
          <Title text={p.price.headline} color={BRAND.wit} maxSize={140} width={960} delay={-2} end={p.dur} />
        </div>
        <div style={{ position: "absolute", left: STAGE_W / 2 - 410, top: 900 - 410, width: 820, height: 820, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <Sunburst start={T_BADGE + 4} size={820} />
        </div>
        <div style={{ position: "absolute", left: STAGE_W / 2 - S / 2, top: 900 - S / 2 }}>
          <PriceBadge amount={p.price.amount} label={p.price.label} start={T_BADGE} size={S} />
        </div>
        <div style={{ position: "absolute", left: 60, right: 60, top: 1300, textAlign: "center", fontFamily: FONT, fontSize: 48, color: BRAND.wit, opacity: note, transform: `translateY(${(1 - note) * 16}px)` }}>
          <Rich text={p.price.note} keyColor={BRAND.wit} />
        </div>
      </Stage>
    </Backdrop>
  );
};
