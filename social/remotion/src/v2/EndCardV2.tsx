import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage } from "../lib/layout";
import { BRAND } from "../theme";
import { Backdrop } from "./Backdrop";
import { Title } from "./Title";
import { CtaPill, UrlLine } from "./CtaPill";
import { TopLogo } from "./Badges";
import { enter } from "./ease";

export type EndCardV2Props = { headline: string; button: string; url: string; tagline: string };

export const T_BUTTON = 16;
export const T_URL = 34;

/** End card in the feed style: GLOW gradient, small logo on top, big headline, "Reserveer online" button, url line, tagline. */
export const EndCardV2: React.FC<{ cta: EndCardV2Props }> = ({ cta }) => {
  const frame = useCurrentFrame();
  const tag = enter(frame, T_URL + 10, 18);
  return (
    <Backdrop kind="glow" seed="end">
      <Stage>
        <div style={{ position: "absolute", left: 0, right: 0, top: 10, display: "flex", justifyContent: "center" }}>
          <TopLogo start={-4} width={380} />
        </div>
        <div style={{ position: "absolute", left: 60, top: 300 }}>
          <Title text={cta.headline} color={BRAND.wit} maxSize={175} width={960} align="left" delay={-2} />
        </div>
        <div style={{ position: "absolute", left: 60, top: 740 }}>
          <CtaPill text={cta.button} start={T_BUTTON} height={160} />
        </div>
        <div style={{ position: "absolute", left: 66, top: 960 }}>
          <UrlLine url={cta.url} start={T_URL} size={62} />
        </div>
        <div style={{ position: "absolute", left: 66, top: 1200, fontFamily: "Ubuntu", fontSize: 46, letterSpacing: "0.06em", color: BRAND.wit, opacity: tag * 0.85 }}>{cta.tagline}</div>
      </Stage>
    </Backdrop>
  );
};

export const EndCardScene = EndCardV2;
export const _keep = AbsoluteFill;
