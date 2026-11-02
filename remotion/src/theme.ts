import tokens from '../../tokens.json';

const c = tokens.colors;
const stops = tokens.gradients['py-tok-gradient-verloop'].stops;

// Brand values come straight from tokens.json (handbook 1.3), never retyped.
export const colors = {
  blauw: c['py-tok-color-blauw'].hex, // #1A3580
  aqua: c['py-tok-color-aqua'].hex, // #32B9CD
  oranje: c['py-tok-color-oranje'].hex, // #F08300
  grijs: c['py-tok-color-grijs'].hex,
  zwart: c['py-tok-color-zwart'].hex,
  wit: '#FFFFFF',
};

// Verloop (blauw to aqua), 45 degrees as in the print files.
export const verloop = `linear-gradient(135deg, ${stops
  .map((s) => `${s.hex} ${Math.round(s.offset * 100)}%`)
  .join(', ')})`;

export const FPS = 30;
export const WIDTH = 1080;
export const HEIGHT = 1920;
export const DURATION = 240; // 8 s per story

// Instagram / TikTok keep the top ~250 px and bottom ~340 px free of UI.
export const SAFE = {top: 250, bottom: 340};

export const font = "'Ubuntu', sans-serif";
