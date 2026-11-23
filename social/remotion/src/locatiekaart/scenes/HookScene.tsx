import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { LocatiekaartProps } from "../schema";
import { Stage, STAGE_W } from "../../lib/layout";
import { Backdrop } from "../../v2/Backdrop";
import { Title } from "../../v2/Title";
import { PlacePill, TopLogo } from "../../v2/Badges";
import { enter, lerp } from "../../v2/ease";
import { BubbleMedia } from "../../components/BubbleMedia";
import { Rain } from "../../components/Rain";
import { BRAND } from "../../theme";

export const T_PILL = 26;

/** Hook: photo (Ken Burns) or the branded stand-in in the speech bubble, big feed-style headline, white place pill. */
export const HookScene: React.FC<LocatiekaartProps & { dur: number }> = (p) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const photo = p.media.type !== "none" && p.media.src;
  const hero = enter(frame, -12, 30);
  const W = 520;
  return (
    <Backdrop kind={photo ? "photo" : "navy"} media={p.media.src} mediaType={p.media.type === "video" ? "video" : "image"} seed="hook">
      {p.hook.weather === "rain" && !photo && (
        <AbsoluteFill style={{ opacity: 0.5 }}>
          <Rain width={width} height={height} color="#8FDDEA" count={90} opacity={0.5} />
        </AbsoluteFill>
      )}
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, display: "flex", justifyContent: "center" }}>
          <TopLogo width={320} />
        </div>
        <div style={{ position: "absolute", left: 60, top: 120 }}>
          <Title text={p.hook.headline} color={BRAND.wit} maxSize={150} width={960} delay={-14} end={p.dur} />
        </div>
        {!photo && (
          <div style={{ position: "absolute", left: STAGE_W - W - 30, top: lerp(900, 800, hero), opacity: hero, transform: `scale(${lerp(0.86, 1, hero)}) rotate(${lerp(6, 0, hero)}deg)`, transformOrigin: "50% 100%", filter: "drop-shadow(0 30px 60px rgba(4,10,40,0.45))" }}>
            <BubbleMedia width={W} media="" mediaType="none" carDelay={4} />
          </div>
        )}
        <div style={{ position: "absolute", left: 60, top: 1190 }}>
          <PlacePill name={p.location.name} start={T_PILL} height={118} />
        </div>
      </Stage>
    </Backdrop>
  );
};
