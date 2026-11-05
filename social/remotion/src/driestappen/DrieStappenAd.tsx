import React from "react";
import { TransitionSeries, springTiming } from "@remotion/transitions";
import { slide } from "@remotion/transitions/slide";
import { fade } from "@remotion/transitions/fade";
import { wipe } from "@remotion/transitions/wipe";
import "../theme";
import { DrieStappenProps, drieStappenFrames } from "./schema";
import { GateScene } from "./scenes/GateScene";
import { StepScene } from "./scenes/StepScene";
import { EndCard } from "../components/EndCard";
import { SafeZones } from "../components/SafeZones";

export const DrieStappenAd: React.FC<DrieStappenProps> = (props) => {
  const f = drieStappenFrames(props.timing);
  const timing = springTiming({ config: { damping: 200 }, durationInFrames: f.transition });
  return (
    <>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={f.hook}>
          <GateScene p={props} headline={props.hook.headline} withFigure={false} />
        </TransitionSeries.Sequence>
        {props.steps.flatMap((_, i) => [
          <TransitionSeries.Transition key={`t${i}`} presentation={i === 0 ? fade() : slide({ direction: "from-right" })} timing={timing} />,
          <TransitionSeries.Sequence key={`s${i}`} durationInFrames={f.step}>
            <StepScene p={props} index={i} />
          </TransitionSeries.Sequence>,
        ])}
        <TransitionSeries.Transition presentation={fade()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.outcome}>
          <GateScene p={props} headline={props.outcome.headline} withFigure />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={wipe({ direction: "from-bottom" })} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.cta}>
          <EndCard cta={props.cta} text={props.colors.text} from={props.colors.ctaBgFrom} to={props.colors.ctaBgTo} />
        </TransitionSeries.Sequence>
      </TransitionSeries>
      {props.showSafeZones && <SafeZones />}
    </>
  );
};
