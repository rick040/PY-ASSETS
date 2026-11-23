import React from "react";
import { useCurrentFrame } from "remotion";
import { AftelkalenderProps, datesBetween } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { TopLogo } from "../../v2/Badges";
import { Sparkles, Sunburst } from "../../v2/Fx";
import { enter, EASE_IN_OUT } from "../../v2/ease";
import { BRAND, FONT } from "../../theme";
import { Rich } from "../../lib/rich";
import { FlipCalendar } from "../Calendar";

export const T_FLIP = 10;
export const T_FLIP_DUR = 46;
export const T_LAND = T_FLIP + T_FLIP_DUR;

export const HookScene: React.FC<AftelkalenderProps & { dur: number }> = (p) => {
  const frame = useCurrentFrame();
  const dates = datesBetween(p.hook.from, p.hook.to);
  const n = dates.length - 1;
  const flip = enter(frame, T_FLIP, T_FLIP_DUR, EASE_IN_OUT);
  const land = enter(frame, T_LAND, 16);
  const cal = enter(frame, -8, 22);
  const W = 470;
  return (
    <Backdrop kind="navy" seed="r6hook">
      {p.hook.sparkles && <Sparkles seed="r6" />}
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center" }}>
          <TopLogo width={320} />
        </div>
        <div style={{ position: "absolute", left: 60, top: 150 }}>
          <Title text={p.hook.headline} color={BRAND.wit} maxSize={150} width={960} delay={-14} end={p.dur} />
        </div>
        <div style={{ position: "absolute", left: STAGE_W / 2 - 400, top: 900 - 400, width: 800, height: 800, opacity: land }}>
          <Sunburst start={T_LAND} size={800} color={BRAND.aqua} opacity={0.8} />
        </div>
        <div style={{ position: "absolute", left: STAGE_W / 2 - W / 2, top: 900 - (W * 1.08) / 2, transform: `translateY(${(1 - cal) * 200}px) rotate(${(1 - cal) * 8 - land * 3}deg) scale(${1 + land * 0.04})`, opacity: cal }}>
          <FlipCalendar w={W} dates={dates} progress={flip} highlight={land} />
        </div>
        {p.hook.countdown && n > 0 && (
          <div style={{ position: "absolute", left: 0, right: 0, top: 1240, display: "flex", justifyContent: "center", opacity: land, transform: `translateY(${(1 - land) * 30}px)` }}>
            <div style={{ height: 112, padding: "0 50px", borderRadius: 56, background: BRAND.wit, display: "flex", alignItems: "center", fontFamily: FONT, fontSize: 54, color: BRAND.blauw }}>
              <span style={{ whiteSpace: "pre" }}><Rich text={p.hook.countdown.replace("{n}", String(n))} keyColor={BRAND.blauw} /></span>
            </div>
          </div>
        )}
      </Stage>
    </Backdrop>
  );
};
