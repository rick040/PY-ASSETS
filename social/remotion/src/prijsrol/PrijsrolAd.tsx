import React from "react";
import { TransitionSeries, springTiming } from "@remotion/transitions";
import "../theme";
import { PrijsrolProps, prijsrolFrames } from "./schema";
import { HookScene } from "./scenes/HookScene";
import { RowsScene } from "./scenes/RowsScene";
import { BubbleScene } from "./scenes/BubbleScene";
import { EndCardV2 } from "../v2/EndCardV2";
import { SafeZones } from "../components/SafeZones";
import { slideBlur, bubbleReveal, zoomThrough } from "../v2/transitions";

export const PrijsrolAd: React.FC<PrijsrolProps> = (props) => {
  const f = prijsrolFrames(props.timing);
  const timing = springTiming({ config: { damping: 200 }, durationInFrames: f.transition });
  return (
    <>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={f.hook}>
          <HookScene {...props} dur={f.hook} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={slideBlur()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.rows}>
          <RowsScene {...props} dur={f.rows} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={bubbleReveal()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.bubble}>
          <BubbleScene {...props} dur={f.bubble} />
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
