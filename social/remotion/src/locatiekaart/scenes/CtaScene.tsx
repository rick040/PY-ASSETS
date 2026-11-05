import React from "react";
import { LocatiekaartProps } from "../schema";
import { EndCard } from "../../components/EndCard";

export { T_URL, T_LOGO } from "../../components/EndCard";

export const CtaScene: React.FC<LocatiekaartProps> = (p) => <EndCard cta={p.cta} text={p.colors.text} from={p.colors.ctaBgFrom} to={p.colors.ctaBgTo} />;
