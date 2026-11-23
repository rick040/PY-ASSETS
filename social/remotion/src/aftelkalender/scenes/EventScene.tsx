import React from "react";
import { useCurrentFrame } from "remotion";
import { AftelkalenderProps } from "../schema";
import { Stage } from "../../lib/layout";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { PlacePill, TopLogo } from "../../v2/Badges";
import { Card } from "../../v2/Card";
import { Sparkles } from "../../v2/Fx";
import { enter, leave } from "../../v2/ease";
import { BRAND, FONT } from "../../theme";

export const T_LINE0 = 14;
export const T_LOC0 = 40;

export const EventScene: React.FC<AftelkalenderProps & { dur: number }> = (p) => {
  const frame = useCurrentFrame();
  const out = leave(frame, p.dur - 4, 12);
  const locLabel = enter(frame, T_LOC0 - 6, 16);
  return (
    <Backdrop kind="navy" seed="r6event">
      {p.hook.sparkles && <Sparkles seed="r6b" count={30} />}
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center" }}>
          <TopLogo width={320} start={-20} />
        </div>
        <div style={{ position: "absolute", left: 60, top: 150 }}>
          <Title text={p.event.name} color={BRAND.wit} maxSize={150} width={960} delay={-4} end={p.dur} />
        </div>
        <div style={{ position: "absolute", left: 50, right: 50, top: 520, display: "flex", flexDirection: "column", gap: 32 }}>
          {p.event.lines.map((l, i) => {
            const e = enter(frame, T_LINE0 + i * 8, 22);
            return <Card key={i} icon={l.icon} text={l.text} height={170} maxFont={62} style={{ opacity: Math.min(1, e * 1.3) * (1 - out), transform: `translateX(${(1 - e) * -110 + out * 60}%)` }} />;
          })}
        </div>
        {p.event.locations.length > 0 && (
          <>
            <div style={{ position: "absolute", left: 66, top: 930, fontFamily: FONT, fontSize: 48, color: BRAND.wit, opacity: locLabel * (1 - out) }}>Parkeer bij</div>
            <div style={{ position: "absolute", left: 60, right: 40, top: 1010, display: "flex", flexWrap: "wrap", gap: 22, opacity: 1 - out }}>
              {p.event.locations.map((loc, i) => (
                <PlacePill key={i} name={loc} start={T_LOC0 + i * 5} height={104} />
              ))}
            </div>
          </>
        )}
      </Stage>
    </Backdrop>
  );
};
