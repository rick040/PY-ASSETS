import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { FiguursketchProps } from "../schema";
import { Stage } from "../../lib/layout";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { TopLogo } from "../../v2/Badges";
import { enter, leave } from "../../v2/ease";
import { Glyph } from "../../components/Glyph";
import { BRAND, FONT } from "../../theme";
import { Figure } from "./Figure";

export const T_TITLE = 2;
export const T_PROP = 14;
export const T_LINE = 16;

/** One type: counter, big title, one-liner, the figure stepping in from the side, a prop in a white disc. */
export const BeatScene: React.FC<{ p: FiguursketchProps; index: number; dur: number }> = ({ p, index, dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const b = p.beats[index];
  const fig = enter(frame, 0, 22);
  const prop = spring({ frame: frame - T_PROP, fps, config: { damping: 12, stiffness: 120 } });
  const line = enter(frame, T_LINE, 16);
  const out = leave(frame, dur - 2, 10);
  return (
    <Backdrop kind="light" seed={`r5b${index}`}>
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center" }}>
          <TopLogo width={320} start={-20} />
        </div>
        <div style={{ position: "absolute", left: 60, top: 130, fontFamily: FONT, fontSize: 46, fontWeight: 500, letterSpacing: "0.08em", color: BRAND.aqua }}>
          {index + 1} / {p.beats.length}
        </div>
        <div style={{ position: "absolute", left: 60, top: 200 }}>
          <Title text={b.title.replace(/^De /, "De\n")} color={BRAND.blauw} maxSize={140} width={960} delay={T_TITLE} end={dur} />
        </div>
        <div style={{ position: "absolute", left: 60, right: 60, top: 520, fontFamily: FONT, fontSize: 54, color: BRAND.blauw, opacity: line * (1 - out), transform: `translateY(${(1 - line) * 20}px)` }}>{b.line}</div>
        <div style={{ position: "absolute", left: 100, right: 100, top: 1300, height: 10, borderRadius: 5, background: BRAND.blauw, opacity: 0.12 }} />
        <div style={{ position: "absolute", left: 120, top: 1300 - 640, width: 480, display: "flex", justifyContent: "center", opacity: fig * (1 - out), transform: `translateX(${(1 - fig) * -300 + out * 200}px)` }}>
          <Figure id={b.figure} height={640} frame={frame} motion={b.motion} />
        </div>
        {b.prop && (
          <div style={{ position: "absolute", left: 650, top: 760, width: 300, height: 300, borderRadius: 150, background: BRAND.wit, display: "flex", alignItems: "center", justifyContent: "center", boxShadow: "0 24px 50px rgba(26,53,128,0.18)", transform: `scale(${prop * (1 - out)}) rotate(${(1 - prop) * 25}deg)` }}>
            <Glyph name={b.prop} size={180} color={BRAND.aqua} tint="none" />
          </div>
        )}
      </Stage>
    </Backdrop>
  );
};
