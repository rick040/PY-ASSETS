import React from "react";
import { Composition, Folder } from "remotion";
import { withMotionBlur } from "./v2/withMotionBlur";
import { LocatiekaartAd } from "./locatiekaart/LocatiekaartAd";
import { locatiekaartSchema, locatiekaartDefaults, locatiekaartTotal, LocatiekaartProps } from "./locatiekaart/schema";
import { KinetischAd } from "./kinetisch/KinetischAd";
import { kinetischSchema, kinetischDefaults, kinetischTotal, KinetischProps } from "./kinetisch/schema";
import { FiguursketchAd } from "./figuursketch/FiguursketchAd";
import { figuursketchSchema, figuursketchDefaults, figuursketchTotal, FiguursketchProps } from "./figuursketch/schema";
import { PrijsrolAd } from "./prijsrol/PrijsrolAd";
import { prijsrolSchema, prijsrolDefaults, prijsrolTotal, PrijsrolProps } from "./prijsrol/schema";
import { DrieStappenAd } from "./driestappen/DrieStappenAd";
import { drieStappenSchema, drieStappenDefaults, drieStappenTotal, DrieStappenProps } from "./driestappen/schema";
import { LooprouteAd } from "./looproute/LooprouteAd";
import { looprouteSchema, looprouteDefaults, looprouteTotal, LooprouteProps } from "./looproute/schema";
import { AftelkalenderAd } from "./aftelkalender/AftelkalenderAd";
import { aftelkalenderSchema, aftelkalenderDefaults, aftelkalenderTotal, AftelkalenderProps } from "./aftelkalender/schema";
import { Post, POSTS, STILL_FRAME } from "./posts/Posts";
import ig002 from "./items/IG-002.json";
import ig039 from "./items/IG-039.json";
import ig041 from "./items/IG-041.json";
import ig028 from "./items/IG-028.json";
import ig017 from "./items/IG-017.json";
import ig018 from "./items/IG-018.json";
import ig021 from "./items/IG-021.json";
import ig064 from "./items/IG-064.json";

const FPS = 30;
const SIZES = [
  { suffix: "Reel", width: 1080, height: 1920 },
  { suffix: "Feed", width: 1080, height: 1350 },
];

// One entry per library item; "Template" shows the defaults of each template.
const r1: Array<[string, LocatiekaartProps]> = [["Template", locatiekaartDefaults], ["IG-002", ig002 as LocatiekaartProps]];
const r2: Array<[string, PrijsrolProps]> = [["Template", prijsrolDefaults], ["IG-017", ig017 as PrijsrolProps], ["IG-018", ig018 as PrijsrolProps]];
const r4: Array<[string, DrieStappenProps]> = [["Template", drieStappenDefaults], ["IG-028", ig028 as DrieStappenProps]];
const r5: Array<[string, FiguursketchProps]> = [["Template", figuursketchDefaults], ["IG-064", ig064 as FiguursketchProps]];
const r7: Array<[string, KinetischProps]> = [["Template", kinetischDefaults], ["IG-021", ig021 as KinetischProps]];

const LocatiekaartMB = withMotionBlur(LocatiekaartAd);
const PrijsrolMB = withMotionBlur(PrijsrolAd);
const DrieStappenMB = withMotionBlur(DrieStappenAd);
const FiguursketchMB = withMotionBlur(FiguursketchAd);
const KinetischMB = withMotionBlur(KinetischAd);
const LooprouteMB = withMotionBlur(LooprouteAd);
const AftelkalenderMB = withMotionBlur(AftelkalenderAd);
const r3: Array<[string, LooprouteProps]> = [["Template", looprouteDefaults], ["IG-039", ig039 as LooprouteProps]];
const r6: Array<[string, AftelkalenderProps]> = [["Template", aftelkalenderDefaults], ["IG-041", ig041 as AftelkalenderProps]];

export const RemotionRoot: React.FC = () => (
  <>
    <Folder name="R1-Locatiekaart">
      {r1.flatMap(([id, props]) =>
        SIZES.map((s) => (
          <Composition key={id + s.suffix} id={`PY-R1-${id}-${s.suffix}`} component={LocatiekaartMB} schema={locatiekaartSchema} defaultProps={props} calculateMetadata={({ props: p }) => ({ durationInFrames: locatiekaartTotal(p.timing) })} durationInFrames={locatiekaartTotal(props.timing)} fps={FPS} width={s.width} height={s.height} />
        )),
      )}
    </Folder>
    <Folder name="R2-Prijsrol">
      {r2.flatMap(([id, props]) =>
        SIZES.map((s) => (
          <Composition key={id + s.suffix} id={`PY-R2-${id}-${s.suffix}`} component={PrijsrolMB} schema={prijsrolSchema} defaultProps={props} calculateMetadata={({ props: p }) => ({ durationInFrames: prijsrolTotal(p.timing) })} durationInFrames={prijsrolTotal(props.timing)} fps={FPS} width={s.width} height={s.height} />
        )),
      )}
    </Folder>
    <Folder name="R3-Looproute">
      {r3.flatMap(([id, props]) =>
        SIZES.map((s) => (
          <Composition key={id + s.suffix} id={`PY-R3-${id}-${s.suffix}`} component={LooprouteMB} schema={looprouteSchema} defaultProps={props} calculateMetadata={({ props: p }) => ({ durationInFrames: looprouteTotal(p.timing) })} durationInFrames={looprouteTotal(props.timing)} fps={FPS} width={s.width} height={s.height} />
        )),
      )}
    </Folder>
    <Folder name="R4-Drie-stappen">
      {r4.flatMap(([id, props]) =>
        SIZES.map((s) => (
          <Composition key={id + s.suffix} id={`PY-R4-${id}-${s.suffix}`} component={DrieStappenMB} schema={drieStappenSchema} defaultProps={props} calculateMetadata={({ props: p }) => ({ durationInFrames: drieStappenTotal(p) })} durationInFrames={drieStappenTotal(props)} fps={FPS} width={s.width} height={s.height} />
        )),
      )}
    </Folder>
    <Folder name="R5-Figuursketch">
      {r5.flatMap(([id, props]) =>
        SIZES.map((s) => (
          <Composition key={id + s.suffix} id={`PY-R5-${id}-${s.suffix}`} component={FiguursketchMB} schema={figuursketchSchema} defaultProps={props} calculateMetadata={({ props: p }) => ({ durationInFrames: figuursketchTotal(p) })} durationInFrames={figuursketchTotal(props)} fps={FPS} width={s.width} height={s.height} />
        )),
      )}
    </Folder>
    <Folder name="R6-Aftelkalender">
      {r6.flatMap(([id, props]) =>
        SIZES.map((s) => (
          <Composition key={id + s.suffix} id={`PY-R6-${id}-${s.suffix}`} component={AftelkalenderMB} schema={aftelkalenderSchema} defaultProps={props} calculateMetadata={({ props: p }) => ({ durationInFrames: aftelkalenderTotal(p.timing) })} durationInFrames={aftelkalenderTotal(props.timing)} fps={FPS} width={s.width} height={s.height} />
        )),
      )}
    </Folder>
    <Folder name="Posts">
      {Object.keys(POSTS).map((id) => (
        <Composition key={id} id={`PY-POST-${id}`} component={Post} defaultProps={{ id }} durationInFrames={STILL_FRAME + 1} fps={FPS} width={1080} height={1350} />
      ))}
    </Folder>
    <Folder name="R7-Kinetische-tekst">
      {r7.flatMap(([id, props]) =>
        SIZES.map((s) => (
          <Composition key={id + s.suffix} id={`PY-R7-${id}-${s.suffix}`} component={KinetischMB} schema={kinetischSchema} defaultProps={props} calculateMetadata={({ props: p }) => ({ durationInFrames: kinetischTotal(p.timing) })} durationInFrames={kinetischTotal(props.timing)} fps={FPS} width={s.width} height={s.height} />
        )),
      )}
    </Folder>
  </>
);
