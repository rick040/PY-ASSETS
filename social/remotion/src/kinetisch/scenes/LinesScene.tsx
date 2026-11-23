import React from "react";
import { useCurrentFrame } from "remotion";
import { KinetischProps } from "../schema";
import { Stage } from "../../lib/layout";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { TopLogo } from "../../v2/Badges";
import { Card } from "../../v2/Card";
import { enter, leave } from "../../v2/ease";
import { BRAND } from "../../theme";

export const T_LINE0 = 16;
export const T_LINE_STEP = 12;

export const LinesScene: React.FC<KinetischProps & { dur: number }> = (p) => {
  const frame = useCurrentFrame();
  const out = leave(frame, p.dur - 4, 12);
  return (
    <Backdrop kind="navy" seed="r7lines">
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center" }}>
          <TopLogo width={320} start={-20} />
        </div>
        <div style={{ position: "absolute", left: 60, top: 150 }}>
          <Title text={p.lines.title} color={BRAND.wit} maxSize={150} width={960} delay={-4} end={p.dur} />
        </div>
        <div style={{ position: "absolute", left: 50, right: 50, top: 640, display: "flex", flexDirection: "column", gap: 60 }}>
          {p.lines.items.map((it, i) => {
            const e = enter(frame, T_LINE0 + i * T_LINE_STEP, 22);
            return <Card key={i} icon={it.icon} text={it.text} height={220} style={{ opacity: Math.min(1, e * 1.3) * (1 - out), transform: `translateX(${(1 - e) * -110 + out * 60}%) rotate(${(1 - e) * -3}deg)` }} />;
          })}
        </div>
      </Stage>
    </Backdrop>
  );
};
