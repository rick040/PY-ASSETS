import React from "react";
import { AbsoluteFill, useVideoConfig } from "remotion";

/** Design box inside the safe zones. Every scene draws in these fixed coordinates. */
export const STAGE_W = 1080;
export const STAGE_H = 1340;

export const useLayout = () => {
  const { width, height } = useVideoConfig();
  const tall = height / width > 1.5; // 9:16 reel versus 4:5 feed
  const safeTop = tall ? 250 : 80;
  const safeBottom = tall ? 330 : 80;
  const k = Math.min((height - safeTop - safeBottom) / STAGE_H, width / STAGE_W);
  const left = (width - STAGE_W * k) / 2;
  return { tall, safeTop, safeBottom, k, left, width, height };
};

export const Stage: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { safeTop, k, left } = useLayout();
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left, top: safeTop, width: STAGE_W, height: STAGE_H, transform: `scale(${k})`, transformOrigin: "0 0" }}>
        {children}
      </div>
    </AbsoluteFill>
  );
};
