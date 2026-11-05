import React from "react";
import { Composition, Folder } from "remotion";
import { LocatiekaartAd } from "./locatiekaart/LocatiekaartAd";
import { locatiekaartSchema, locatiekaartDefaults, locatiekaartTotal, LocatiekaartProps } from "./locatiekaart/schema";
import { KinetischAd } from "./kinetisch/KinetischAd";
import { kinetischSchema, kinetischDefaults, kinetischTotal, KinetischProps } from "./kinetisch/schema";
import { FiguursketchAd } from "./figuursketch/FiguursketchAd";
import { figuursketchSchema, figuursketchDefaults, figuursketchTotal, FiguursketchProps } from "./figuursketch/schema";
import ig002 from "./items/IG-002.json";
import ig021 from "./items/IG-021.json";
import ig064 from "./items/IG-064.json";

const FPS = 30;
const SIZES = [
  { suffix: "Reel", width: 1080, height: 1920 },
  { suffix: "Feed", width: 1080, height: 1350 },
];

// One entry per library item; "Template" shows the defaults of each template.
const r1: Array<[string, LocatiekaartProps]> = [["Template", locatiekaartDefaults], ["IG-002", ig002 as LocatiekaartProps]];
const r5: Array<[string, FiguursketchProps]> = [["Template", figuursketchDefaults], ["IG-064", ig064 as FiguursketchProps]];
const r7: Array<[string, KinetischProps]> = [["Template", kinetischDefaults], ["IG-021", ig021 as KinetischProps]];

export const RemotionRoot: React.FC = () => (
  <>
    <Folder name="R1-Locatiekaart">
      {r1.flatMap(([id, props]) =>
        SIZES.map((s) => (
          <Composition key={id + s.suffix} id={`PY-R1-${id}-${s.suffix}`} component={LocatiekaartAd} schema={locatiekaartSchema} defaultProps={props} calculateMetadata={({ props: p }) => ({ durationInFrames: locatiekaartTotal(p.timing) })} durationInFrames={locatiekaartTotal(props.timing)} fps={FPS} width={s.width} height={s.height} />
        )),
      )}
    </Folder>
    <Folder name="R5-Figuursketch">
      {r5.flatMap(([id, props]) =>
        SIZES.map((s) => (
          <Composition key={id + s.suffix} id={`PY-R5-${id}-${s.suffix}`} component={FiguursketchAd} schema={figuursketchSchema} defaultProps={props} calculateMetadata={({ props: p }) => ({ durationInFrames: figuursketchTotal(p) })} durationInFrames={figuursketchTotal(props)} fps={FPS} width={s.width} height={s.height} />
        )),
      )}
    </Folder>
    <Folder name="R7-Kinetische-tekst">
      {r7.flatMap(([id, props]) =>
        SIZES.map((s) => (
          <Composition key={id + s.suffix} id={`PY-R7-${id}-${s.suffix}`} component={KinetischAd} schema={kinetischSchema} defaultProps={props} calculateMetadata={({ props: p }) => ({ durationInFrames: kinetischTotal(p.timing) })} durationInFrames={kinetischTotal(props.timing)} fps={FPS} width={s.width} height={s.height} />
        )),
      )}
    </Folder>
  </>
);
