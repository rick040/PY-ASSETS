import React from "react";
import { CalculateMetadataFunction } from "remotion";
import "../theme";
import { FORMATS, PostProps } from "./spec";
import { Measure } from "./qa";
import { ARCHETYPES } from "./archetypes";

export const PostComposition: React.FC<PostProps> = (props) => {
  const C = ARCHETYPES[props.spec.archetype];
  if (!C) throw new Error(`Archetype "${props.spec.archetype}" is not built yet`);
  return (
    <Measure hideText={props.hideText}>
      <C {...props} />
    </Measure>
  );
};

/** Canvas size follows the format in the props, so one composition serves every format. */
export const postMetadata: CalculateMetadataFunction<PostProps> = ({ props }) => {
  const f = FORMATS[props.format];
  if (!f) throw new Error(`Unknown format "${props.format}"`);
  return { width: f.width, height: f.height, durationInFrames: 1, fps: 30 };
};
