/** Dutch price notation: €30, €12,50. */
export const euro = (n: number) => (Number.isInteger(n) ? `€${n}` : `€${n.toFixed(2).replace(".", ",")}`);
