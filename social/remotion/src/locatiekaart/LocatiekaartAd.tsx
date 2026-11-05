import React from "react";
import { TransitionSeries, springTiming } from "@remotion/transitions";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import "../theme";
import { LocatiekaartProps, locatiekaartFrames } from "./schema";
import { MainScene } from "./scenes/MainScene";
import { PriceScene } from "./scenes/PriceScene";
import { CtaScene } from "./scenes/CtaScene";
import { SafeZones } from "../components/SafeZones";

export const LocatiekaartAd: React.FC<LocatiekaartProps> = (props) => {
  const f = locatiekaartFrames(props.timing);
  const timing = springTiming({ config: { damping: 200 }, durationInFrames: f.transition });
  return (
    <>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={f.main}>
          <MainScene {...props} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={slide({ direction: "from-bottom" })} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.price}>
          <PriceScene {...props} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={wipe({ direction: "from-top-left" })} timing={timing} />
        <TransitionSeries.Sequence durationInFrames={f.cta}>
          <CtaScene {...props} />
        </TransitionSeries.Sequence>
      </TransitionSeries>
      {props.showSafeZones && <SafeZones />}
    </>
  );
};
