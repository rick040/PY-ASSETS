import React from "react";

/**
 * A barrier (slagboom) in brand colours: white post, white arm with aqua stripes, pivoting at the top of the post.
 * `open` 0 = closed (horizontal), 1 = open (arm up). Drawn left-anchored; width is the arm length.
 */
export const Slagboom: React.FC<{ open: number; width: number; accent: string; post: string }> = ({ open, width, accent, post }) => {
  const armH = width * 0.065;
  const postW = width * 0.11;
  const postH = width * 0.42;
  const stripes = 7;
  return (
    <div style={{ position: "relative", width: width + postW, height: postH + width }}>
      {/* arm */}
      <div style={{ position: "absolute", left: postW * 0.5, top: width - armH / 2 + postH * 0.12, width, height: armH, borderRadius: armH / 2, overflow: "hidden", background: post, transform: `rotate(${-82 * open}deg)`, transformOrigin: `${armH / 2}px 50%`, boxShadow: "0 8px 20px rgba(0,0,0,0.2)" }}>
        {new Array(stripes).fill(0).map((_, i) => (
          <div key={i} style={{ position: "absolute", top: 0, bottom: 0, left: `${12 + i * 12}%`, width: "6%", background: accent, transform: "skewX(-30deg)" }} />
        ))}
      </div>
      {/* post */}
      <div style={{ position: "absolute", left: 0, top: width, width: postW, height: postH, borderRadius: postW * 0.25, background: post, boxShadow: "0 10px 26px rgba(0,0,0,0.22)" }}>
        <div style={{ position: "absolute", left: "25%", right: "25%", top: "12%", height: postW * 0.5, borderRadius: postW * 0.25, background: accent }} />
      </div>
    </div>
  );
};
