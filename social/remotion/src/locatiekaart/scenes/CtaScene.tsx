import React from "react";
import { LocatiekaartProps } from "../schema";
import { EndCardV2 } from "../../v2/EndCardV2";

export const CtaScene: React.FC<LocatiekaartProps> = (p) => <EndCardV2 cta={p.cta} />;
