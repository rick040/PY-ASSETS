import React from "react";
import { TransitionSeries, springTiming } from "@remotion/transitions";
import "../theme";
import { LooprouteProps, looprouteFrames } from "./schema";
import { HookScene } from "./scenes/HookScene";
import { RouteScene } from "./scenes/RouteScene";
import { PriceScene } from "./scenes/PriceScene";
import { EndCardV2 } from "../v2/EndCardV2";
import { SafeZones } from "../components/SafeZones";
import { slideBlur, bubbleReveal, zoomThrough } from "../v2/transitions";

export const LooprouteAd: React.FC<LooprouteProps> = (props) => {
  const f = looprouteFrames(props.timing);
  const timing = springTiming({ config: { damping: 200 }, durationInFrames: f.transition });
  return (
    <>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={f.hook}>
          <HookScene {...props} dur={f.hook} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={slideBlur()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.route}>
          <RouteScene {...props} dur={f.route} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={bubbleReveal()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.price}>
          <PriceScene {...props} dur={f.price} />
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
