import React from "react";
import { TransitionSeries, springTiming } from "@remotion/transitions";
import "../theme";
import { AftelkalenderProps, aftelkalenderFrames } from "./schema";
import { HookScene } from "./scenes/HookScene";
import { EventScene } from "./scenes/EventScene";
import { PriceScene } from "./scenes/PriceScene";
import { EndCardV2 } from "../v2/EndCardV2";
import { SafeZones } from "../components/SafeZones";
import { slideBlur, bubbleReveal, zoomThrough } from "../v2/transitions";

export const AftelkalenderAd: React.FC<AftelkalenderProps> = (props) => {
  const f = aftelkalenderFrames(props.timing);
  const timing = springTiming({ config: { damping: 200 }, durationInFrames: f.transition });
  return (
    <>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={f.hook}>
          <HookScene {...props} dur={f.hook} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={slideBlur()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.event}>
          <EventScene {...props} dur={f.event} />
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
