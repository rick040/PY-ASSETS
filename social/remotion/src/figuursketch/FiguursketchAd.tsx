import React from "react";
import { TransitionSeries, springTiming } from "@remotion/transitions";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import "../theme";
import { FiguursketchProps, figuursketchFrames } from "./schema";
import { HookScene, OutroScene } from "./scenes/HookScene";
import { BeatScene } from "./scenes/BeatScene";
import { EndCard } from "../components/EndCard";
import { SafeZones } from "../components/SafeZones";

export const FiguursketchAd: React.FC<FiguursketchProps> = (props) => {
  const f = figuursketchFrames(props.timing);
  const timing = springTiming({ config: { damping: 200 }, durationInFrames: f.transition });
  const t = () => <TransitionSeries.Transition presentation={slide({ direction: "from-right" })} timing={timing} />;
  return (
    <>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={f.hook}>
          <HookScene {...props} />
        </TransitionSeries.Sequence>
        {props.beats.flatMap((_, i) => [
          <React.Fragment key={`t${i}`}>{t()}</React.Fragment>,
          <TransitionSeries.Sequence key={`b${i}`} durationInFrames={f.beat}>
            <BeatScene p={props} index={i} />
          </TransitionSeries.Sequence>,
        ])}
        <TransitionSeries.Transition presentation={slide({ direction: "from-right" })} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.outro}>
          <OutroScene {...props} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={wipe({ direction: "from-bottom-left" })} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.cta}>
          <EndCard cta={props.cta} text="#FFFFFF" from={props.colors.ctaBgFrom} to={props.colors.ctaBgTo} />
        </TransitionSeries.Sequence>
      </TransitionSeries>
      {props.showSafeZones && <SafeZones />}
    </>
  );
};
