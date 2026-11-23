// Shapes copied from PY-ASSETS SVGs (absolute commands only, so they can be scaled by multiplying every number).

/** py-atom-shape-bubble-solid / -image-mask, viewBox 36 x 43.423 */
export const BUBBLE = {
  w: 36,
  h: 43.423,
  d: "M18 0C8.059 0 0 8.058 0 17.998C0 34.701 16.691 43.073 16.691 43.073C17.264 43.423 18 43.006 18 42.335L18 35.997C27.941 35.997 36 27.939 36 17.998C36 8.058 27.941 0 18 0Z",
};

/** py-comp-price-bubble-speech, bubble only, already moved to the origin (translate -408.096 8.654). */
export const SPEECH = {
  w: 301.024,
  h: 350.949,
  d: "M133.887 9.171C55.917 18.341 0 89.166 9.17 167.136C24.588 298.227 163.424 348.665 163.424 348.665C168.102 350.949 173.602 346.838 172.981 341.557L167.135 291.855C245.106 282.684 301.023 211.86 291.853 133.888C282.682 55.917 211.858 0 133.887 9.171Z",
};

/** chevron from py-comp-url-chevron, moved to the origin. */
export const CHEVRON = {
  w: 29.682,
  h: 44.581,
  d: "M6.987 0.127L0.104 7.001C-0.066 7.171 -0.066 7.447 0.104 7.618L14.487 21.982C14.657 22.151 14.657 22.428 14.487 22.599L0.104 36.962C-0.066 37.132 -0.066 37.409 0.104 37.579L6.987 44.452C7.158 44.623 7.434 44.623 7.605 44.452L29.488 22.599C29.657 22.428 29.657 22.151 29.488 21.982L7.605 0.127C7.434 -0.044 7.158 -0.044 6.987 0.127Z",
};

export const scalePath = (d: string, s: number) => d.replace(/-?\d*\.?\d+/g, (n) => String(+(parseFloat(n) * s).toFixed(3)));
