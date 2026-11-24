import React from "react";
import { contentBox, PostProps } from "../spec";
import { getTheme } from "../themes";
import { At, Copy, GroundFill, Headline, Logo, Url, Watermark } from "../kit";

/**
 * typografisch (S4): text only. Logo on top, a big headline, an optional subline, the URL at the bottom,
 * the beeldmerk as a faint watermark. Layout per format; nothing is stretched.
 */
export const Typografisch: React.FC<PostProps> = ({ spec, format }) => {
  const theme = getTheme(spec.theme);
  const { headline, subline, cta } = spec.slots as { headline: string; subline?: string; cta?: string };
  const b = contentBox(format);
  const g = spec.ground;
  const wide = format === "landscape";

  if (wide) {
    // 1.91:1: logo and URL left, text block right of a narrow left column.
    const col = 300;
    return (
      <GroundFill theme={theme} ground={g} seed={spec.id}>
        <Watermark theme={theme} ground={g} size={b.height * 1.4} />
        <At x={b.x} y={b.y}><Logo theme={theme} ground={g} width={220} /></At>
        <At x={b.x + col} y={b.y + 10} w={b.w - col}>
          <Headline theme={theme} ground={g} text={headline} width={b.w - col} maxSize={96} />
          {subline && <div style={{ marginTop: 24 }}><Copy theme={theme} ground={g} name="subline" text={subline} size={30} width={b.w - col} /></div>}
        </At>
        {cta !== "none" && <At x={b.x} y={b.safe.bottom} anchor="bottom"><Url theme={theme} ground={g} size={34} /></At>}
      </GroundFill>
    );
  }

  const tall = format === "story";
  const logoW = format === "square" ? 280 : 280;
  const headTop = tall ? b.y + 330 : b.y + b.h * 0.3;
  const headSize = tall ? 150 : format === "square" ? 140 : 150;
  return (
    <GroundFill theme={theme} ground={g} seed={spec.id}>
      <Watermark theme={theme} ground={g} size={b.width * 1.02} />
      <At x={0} y={b.y} w={b.width}>
        <div style={{ display: "flex", justifyContent: "center" }}><Logo theme={theme} ground={g} width={logoW} /></div>
      </At>
      <At x={b.x} y={headTop} w={b.w}>
        <Headline theme={theme} ground={g} text={headline} width={b.w} maxSize={headSize} />
        {subline && (
          <div style={{ marginTop: tall ? 64 : 48 }}>
            <Copy theme={theme} ground={g} name="subline" text={subline} size={tall ? 48 : 44} width={b.w} />
          </div>
        )}
      </At>
      {cta !== "none" && <At x={b.x + 6} y={b.safe.bottom + 10} anchor="bottom"><Url theme={theme} ground={g} size={48} /></At>}
    </GroundFill>
  );
};
