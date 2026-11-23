import React from "react";
import { Img, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { BUBBLE, scalePath } from "../lib/paths";
import { pop, springs } from "../lib/anim";
import { VERLOOP_STOPS } from "../theme";
import { AssetImg } from "./AssetImg";

/**
 * The speech bubble from py-atom-shape-bubble-image-mask with a photo or video inside.
 * Without media it shows a branded stand-in: the verloop, the P-with-roof symbol and a car parking under it.
 */
export const BubbleMedia: React.FC<{ width: number; media?: string; mediaType: "image" | "video" | "none"; carDelay?: number }> = ({ width, media, mediaType, carDelay = -6 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = width / BUBBLE.w;
  const height = BUBBLE.h * s;
  const clip = `path('${scalePath(BUBBLE.d, s)}')`;
  const car = pop(frame, fps, carDelay, springs.smooth);
  const zoom = interpolate(frame, [0, 300], [1.0, 1.08]);

  return (
    <div style={{ position: "relative", width, height }}>
      <div style={{ position: "absolute", inset: 0, clipPath: clip, overflow: "hidden" }}>
        {mediaType === "image" && media ? (
          <Img src={staticFile(media)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${zoom})` }} />
        ) : mediaType === "video" && media ? (
          <OffthreadVideo src={staticFile(media)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        ) : (
          <svg width={width} height={height} viewBox={`0 0 ${BUBBLE.w} ${BUBBLE.h}`}>
            <defs>
              <linearGradient id="bm-grad" x1="0" y1="0" x2="1" y2="1">
                {VERLOOP_STOPS.map((st) => (
                  <stop key={st.offset} offset={st.offset} stopColor={st.hex} />
                ))}
              </linearGradient>
            </defs>
            <rect width={BUBBLE.w} height={BUBBLE.h} fill="url(#bm-grad)" />
            {/* garage floor */}
            <rect x={0} y={31.9} width={BUBBLE.w} height={0.35} fill="#FFFFFF" opacity={0.35} />
          </svg>
        )}
        {mediaType === "none" && (
          <>
            <AssetImg id="py-atom-symbol-p-roof" width={width * 0.36} style={{ position: "absolute", left: width * 0.32, top: height * 0.1 }} />
            <AssetImg
              id="py-atom-picto-car"
              width={width * 0.42}
              tint="white"
              style={{ position: "absolute", left: interpolate(car, [0, 1], [-width * 0.5, width * 0.29]), top: height * 0.47, transform: `rotate(${(1 - car) * -2}deg)` }}
            />
          </>
        )}
      </div>
    </div>
  );
};
