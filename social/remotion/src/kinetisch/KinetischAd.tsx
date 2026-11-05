import React from "react";
import { TransitionSeries, springTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import "../theme";
import { KinetischProps, kinetischFrames } from "./schema";
import { HookScene } from "./scenes/HookScene";
import { LinesScene } from "./scenes/LinesScene";
import { EndScene } from "./scenes/EndScene";
import { EndCard } from "../components/EndCard";
import { SafeZones } from "../components/SafeZones";

export const KinetischAd: React.FC<KinetischProps> = (props) => {
  const f = kinetischFrames(props.timing);
  const timing = springTiming({ config: { damping: 200 }, durationInFrames: f.transition });
  return (
    <>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={f.hook}>
          <HookScene {...props} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={slide({ direction: "from-right" })} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.lines}>
          <LinesScene {...props} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.end}>
          <EndScene {...props} />
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
