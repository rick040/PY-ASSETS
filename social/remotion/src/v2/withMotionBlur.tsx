import React from "react";
import { CameraMotionBlur } from "@remotion/motion-blur";

/**
 * Real camera motion blur (@remotion/motion-blur): each output frame is the average of several sub-frames,
 * so every moving element gets natural blur along its path. Costs `samples` x render time.
 */
export const withMotionBlur = <P extends object>(Comp: React.FC<P>, samples = 6): React.FC<P & { motionBlur?: boolean }> => {
  const Wrapped: React.FC<P & { motionBlur?: boolean }> = ({ motionBlur = true, ...props }) =>
    motionBlur ? (
      <CameraMotionBlur shutterAngle={180} samples={samples}>
        <Comp {...(props as P)} />
      </CameraMotionBlur>
    ) : (
      <Comp {...(props as P)} />
    );
  return Wrapped;
};
