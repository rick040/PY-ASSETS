import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { LocatiekaartProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { pop, springs, mix } from "../../lib/anim";
import { Headline } from "../../components/Headline";
import { BubbleMedia } from "../../components/BubbleMedia";
import { LocationPill } from "../../components/LocationPill";
import { FactRow } from "../../components/FactRow";
import { Rain } from "../../components/Rain";
import { BUBBLE } from "../../lib/paths";

// Scene-local beats (frames at 30 fps). Measured by the voice-over table, so change them here only.
export const T_PILL = 18; // location pill lands
export const T_SHRINK = 92; // bubble makes room for the facts
export const T_FACTS = [112, 130, 148]; // fact rows

const BIG_W = 700;
const SMALL_W = 330;
const HOOK_TOP = 270; // under a two-line headline (2 x 84 x 1.12)

export const MainScene: React.FC<LocatiekaartProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const shrink = pop(frame, fps, T_SHRINK, springs.smooth);
  const pill = pop(frame, fps, T_PILL, springs.bouncy);

  const bw = mix(BIG_W, SMALL_W, shrink);
  const bh = (bw * BUBBLE.h) / BUBBLE.w;
  const bTop = mix(HOOK_TOP, 250, shrink);
  const bLeft = mix((STAGE_W - BIG_W) / 2, 70, shrink);
  // pill sits under the big bubble, then moves next to the small one
  const pillTop = mix(HOOK_TOP + (BIG_W * BUBBLE.h) / BUBBLE.w + 30, 250 + 110, shrink);
  const pillLeft = mix(STAGE_W / 2, 70 + SMALL_W + 40, shrink);
  const pillX = mix(-50, 0, shrink); // percent: centred, then left aligned
  const pillScale = mix(1, 0.86, shrink);
  const rainFade = interpolate(frame, [T_SHRINK, T_SHRINK + 20], [1, 0.35], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: p.colors.bg }}>
      {p.hook.weather === "rain" && (
        <AbsoluteFill style={{ opacity: rainFade }}>
          <Rain width={width} height={height} color={p.colors.accent} />
        </AbsoluteFill>
      )}
      <Stage>
        <Headline text={p.hook.headline} color={p.colors.text} keyColor={p.colors.accent} size={84} delay={-30} stagger={3} top={0} />
        <div style={{ position: "absolute", left: bLeft, top: bTop, filter: "drop-shadow(0 18px 40px rgba(0,0,0,0.25))" }}>
          <BubbleMedia width={bw} media={p.media.src} mediaType={p.media.type} />
        </div>
        <div style={{ position: "absolute", left: pillLeft, top: pillTop, transform: `translateX(${pillX}%) scale(${pillScale * (0.7 + 0.3 * pill)})`, transformOrigin: "0% 50%", opacity: Math.min(1, pill * 1.5) }}>
          <LocationPill name={p.location.name} city={p.location.city} bg={p.colors.accent} fg={p.colors.text} accent={p.colors.bg} />
        </div>
        <div style={{ position: "absolute", left: 70, right: 40, top: 250 + (SMALL_W * BUBBLE.h) / BUBBLE.w + 90, display: "flex", flexDirection: "column", gap: 64 }}>
          {p.facts.map((f, i) => (
            <FactRow key={i} fact={f} p={pop(frame, fps, T_FACTS[i] ?? T_FACTS[0] + i * 18)} color={p.colors.text} keyColor={p.colors.accent} ring={p.colors.accent} />
          ))}
        </div>
      </Stage>
    </AbsoluteFill>
  );
};
