import React from "react";
import { TransitionSeries, springTiming } from "@remotion/transitions";
import { flip } from "@remotion/transitions/flip";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import "../theme";
import { PrijsrolProps, prijsrolFrames } from "./schema";
import { HookScene } from "./scenes/HookScene";
import { RowsScene } from "./scenes/RowsScene";
import { BubbleScene } from "./scenes/BubbleScene";
import { EndCard } from "../components/EndCard";
import { SafeZones } from "../components/SafeZones";

export const PrijsrolAd: React.FC<PrijsrolProps> = (props) => {
  const f = prijsrolFrames(props.timing);
  const timing = springTiming({ config: { damping: 200 }, durationInFrames: f.transition });
  return (
    <>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={f.hook}>
          <HookScene {...props} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={slide({ direction: "from-bottom" })} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.rows}>
          <RowsScene {...props} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={flip({ direction: "from-right" })} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.bubble}>
          <BubbleScene {...props} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={wipe({ direction: "from-top-right" })} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.cta}>
          <EndCard cta={props.cta} text={props.colors.text} from={props.colors.ctaBgFrom} to={props.colors.ctaBgTo} />
        </TransitionSeries.Sequence>
      </TransitionSeries>
      {props.showSafeZones && <SafeZones />}
    </>
  );
};
