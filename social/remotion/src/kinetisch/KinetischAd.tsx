import React from "react";
import { TransitionSeries, springTiming } from "@remotion/transitions";
import "../theme";
import { KinetischProps, kinetischFrames } from "./schema";
import { HookScene } from "./scenes/HookScene";
import { LinesScene } from "./scenes/LinesScene";
import { EndScene } from "./scenes/EndScene";
import { EndCardV2 } from "../v2/EndCardV2";
import { SafeZones } from "../components/SafeZones";
import { slideBlur, bubbleReveal, zoomThrough } from "../v2/transitions";

export const KinetischAd: React.FC<KinetischProps> = (props) => {
  const f = kinetischFrames(props.timing);
  const timing = springTiming({ config: { damping: 200 }, durationInFrames: f.transition });
  return (
    <>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={f.hook}>
          <HookScene {...props} dur={f.hook} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={slideBlur()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.lines}>
          <LinesScene {...props} dur={f.lines} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={bubbleReveal()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.end}>
          <EndScene {...props} dur={f.end} />
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
