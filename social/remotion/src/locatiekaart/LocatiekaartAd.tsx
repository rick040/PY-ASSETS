import React from "react";
import { TransitionSeries, springTiming } from "@remotion/transitions";
import "../theme";
import { LocatiekaartProps, locatiekaartFrames } from "./schema";
import { HookScene } from "./scenes/HookScene";
import { MainScene } from "./scenes/MainScene";
import { PriceScene } from "./scenes/PriceScene";
import { CtaScene } from "./scenes/CtaScene";
import { SafeZones } from "../components/SafeZones";
import { slideBlur, bubbleReveal, zoomThrough } from "../v2/transitions";

export const LocatiekaartAd: React.FC<LocatiekaartProps> = (props) => {
  const f = locatiekaartFrames(props.timing);
  const timing = springTiming({ config: { damping: 200 }, durationInFrames: f.transition });
  return (
    <>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={f.hook}>
          <HookScene {...props} dur={f.hook} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={slideBlur()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.main}>
          <MainScene {...props} dur={f.main} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={bubbleReveal()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.price}>
          <PriceScene {...props} dur={f.price} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={zoomThrough()} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.cta}>
          <CtaScene {...props} />
        </TransitionSeries.Sequence>
      </TransitionSeries>
      {props.showSafeZones && <SafeZones />}
    </>
  );
};
