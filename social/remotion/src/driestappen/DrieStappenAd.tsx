import React from "react";
import { TransitionSeries, springTiming } from "@remotion/transitions";
import { slideBlur, bubbleReveal, zoomThrough } from "../v2/transitions";
import { EndCardV2 } from "../v2/EndCardV2";
import "../theme";
import { DrieStappenProps, drieStappenFrames } from "./schema";
import { GateScene } from "./scenes/GateScene";
import { StepScene } from "./scenes/StepScene";
import { SafeZones } from "../components/SafeZones";

export const DrieStappenAd: React.FC<DrieStappenProps> = (props) => {
  const f = drieStappenFrames(props.timing);
  const timing = springTiming({ config: { damping: 200 }, durationInFrames: f.transition });
  return (
    <>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={f.hook}>
          <GateScene p={props} headline={props.hook.headline} withFigure={false} dur={f.hook} />
        </TransitionSeries.Sequence>
        {props.steps.flatMap((_, i) => [
          <TransitionSeries.Transition key={`t${i}`} presentation={i === 0 ? bubbleReveal() : slideBlur()} timing={timing} />,
          <TransitionSeries.Sequence key={`s${i}`} durationInFrames={f.step}>
            <StepScene p={props} index={i} dur={f.step} />
          </TransitionSeries.Sequence>,
        ])}
        <TransitionSeries.Transition presentation={zoomThrough()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.outcome}>
          <GateScene p={props} headline={props.outcome.headline} withFigure dur={f.outcome} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={slideBlur()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.cta}>
          <EndCardV2 cta={props.cta} />
        </TransitionSeries.Sequence>
      </TransitionSeries>
      {props.showSafeZones && <SafeZones />}
    </>
  );
};
