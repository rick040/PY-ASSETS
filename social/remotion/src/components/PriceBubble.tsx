import React from "react";
import { SPEECH } from "../lib/paths";
import { FONT } from "../theme";

/** py-comp-price-bubble-speech with live text: price numerals bold, label regular, both rotated -6.7 degrees as in print. */
export const PriceBubble: React.FC<{ width: number; price: string; label: string; fill: string; text: string }> = ({ width, price, label, fill, text }) => {
  const cx = 150; // optical centre of the round part
  const size = price.length > 3 ? 132 : 150;
  return (
    <svg width={width} height={(width * SPEECH.h) / SPEECH.w} viewBox={`0 0 ${SPEECH.w} ${SPEECH.h}`} style={{ overflow: "visible" }}>
      <path d={SPEECH.d} fill={fill} />
      <g transform={`rotate(-6.708 ${cx} 170)`} fontFamily={FONT} fill={text} textAnchor="middle">
        <text x={cx} y={192} fontSize={size} fontWeight={700}>{price}</text>
        <text x={cx} y={246} fontSize={36} fontWeight={400}>{label}</text>
      </g>
    </svg>
  );
};
