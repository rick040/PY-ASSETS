import React from "react";
import { TransitionSeries, springTiming } from "@remotion/transitions";
import { slideBlur, bubbleReveal, zoomThrough } from "../v2/transitions";
import { EndCardV2 } from "../v2/EndCardV2";
import "../theme";
import { FiguursketchProps, figuursketchFrames } from "./schema";
import { HookScene, OutroScene } from "./scenes/HookScene";
import { BeatScene } from "./scenes/BeatScene";
import { SafeZones } from "../components/SafeZones";

export const FiguursketchAd: React.FC<FiguursketchProps> = (props) => {
  const f = figuursketchFrames(props.timing);
  const timing = springTiming({ config: { damping: 200 }, durationInFrames: f.transition });
  const t = (i: number) => <TransitionSeries.Transition presentation={i === 0 ? bubbleReveal() : slideBlur()} timing={timing} />;
  return (
    <>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={f.hook}>
          <HookScene {...props} dur={f.hook} />
        </TransitionSeries.Sequence>
        {props.beats.flatMap((_, i) => [
          <React.Fragment key={`t${i}`}>{t(i)}</React.Fragment>,
          <TransitionSeries.Sequence key={`b${i}`} durationInFrames={f.beat}>
            <BeatScene p={props} index={i} dur={f.beat} />
          </TransitionSeries.Sequence>,
        ])}
        <TransitionSeries.Transition presentation={slideBlur()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.outro}>
          <OutroScene {...props} dur={f.outro} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={zoomThrough()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.cta}>
          <EndCardV2 cta={props.cta} />
        </TransitionSeries.Sequence>
      </TransitionSeries>
      {props.showSafeZones && <SafeZones />}
    </>
  );
};
