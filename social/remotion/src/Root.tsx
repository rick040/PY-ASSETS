import React from "react";
import { Composition, Folder } from "remotion";
import { LocatiekaartAd } from "./locatiekaart/LocatiekaartAd";
import { locatiekaartSchema, locatiekaartDefaults, locatiekaartTotal, FPS, LocatiekaartProps } from "./locatiekaart/schema";
import ig002 from "./items/IG-002.json";

const meta = ({ props }: { props: LocatiekaartProps }) => ({ durationInFrames: locatiekaartTotal(props.timing) });

const items: Array<{ id: string; props: LocatiekaartProps }> = [
  { id: "Template", props: locatiekaartDefaults },
  { id: "IG-002", props: ig002 as LocatiekaartProps },
];

export const RemotionRoot: React.FC = () => (
  <Folder name="R1-Locatiekaart">
    {items.map(({ id, props }) => (
      <React.Fragment key={id}>
        <Composition id={`PY-R1-${id}-Reel`} component={LocatiekaartAd} schema={locatiekaartSchema} defaultProps={props} calculateMetadata={meta} durationInFrames={locatiekaartTotal(props.timing)} fps={FPS} width={1080} height={1920} />
        <Composition id={`PY-R1-${id}-Feed`} component={LocatiekaartAd} schema={locatiekaartSchema} defaultProps={props} calculateMetadata={meta} durationInFrames={locatiekaartTotal(props.timing)} fps={FPS} width={1080} height={1350} />
      </React.Fragment>
    ))}
  </Folder>
);
