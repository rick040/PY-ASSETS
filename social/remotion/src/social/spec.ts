import archetypes from "../../../../plugins/parkingyou-social/schema/archetypes.json";
import type { Ground, ThemeId } from "./themes";

/** The post spec as the compositions see it (plugins/parkingyou-social/schema/post-spec.schema.json). */
export type FormatId = "feed" | "story" | "square" | "landscape";

export type PostSpec = {
  id: string;
  slug?: string;
  archetype: string;
  theme: ThemeId;
  formats: FormatId[];
  ground: Ground;
  slots: Record<string, any>;
  caption?: string;
  alt?: string;
};

export type PostProps = {
  spec: PostSpec;
  format: FormatId;
  slide?: number;
  /** QA pass: hides all text so check_brand.py can read the real pixels behind it. */
  hideText?: boolean;
};

type Box = { top: number; right: number; bottom: number; left: number };
export type Format = { width: number; height: number; safe: Box };

export const FORMATS = archetypes.formats as Record<FormatId, Format>;

/** The content box of a format: canvas minus safe zones. */
export const contentBox = (f: FormatId) => {
  const { width, height, safe } = FORMATS[f];
  return { x: safe.left, y: safe.top, w: width - safe.left - safe.right, h: height - safe.top - safe.bottom, width, height, safe };
};

export const defaultSpec: PostSpec = {
  id: "IG-065",
  slug: "the-other-way-of-parking",
  archetype: "typografisch",
  theme: "feed",
  formats: ["feed"],
  ground: "glow",
  slots: {
    headline: "The other way\nof *parking.*",
    subline: "Parkeren in Amsterdam, Rotterdam, Eindhoven en meer. *Vooraf geregeld*, zonder gedoe.",
    cta: "url",
  },
};
