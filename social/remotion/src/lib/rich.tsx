import React from "react";

/** "*word*" marks a key phrase (bold, accent colour). Returns tokens per line, per word. */
export type Word = { text: string; key: boolean };
export const parseRich = (text: string): Word[][] =>
  text.split("\n").map((line) => {
    const words: Word[] = [];
    line.split(/(\*[^*]+\*)/g).filter(Boolean).forEach((part) => {
      const key = part.startsWith("*") && part.endsWith("*");
      const clean = key ? part.slice(1, -1) : part;
      clean.split(/(\s+)/).filter((w) => w.trim()).forEach((w) => words.push({ text: w, key }));
    });
    return words;
  });

export const Rich: React.FC<{ text: string; keyColor: string; keyWeight?: number }> = ({ text, keyColor, keyWeight = 700 }) => (
  <>
    {text.split(/(\*[^*]+\*)/g).filter(Boolean).map((part, i) =>
      part.startsWith("*") && part.endsWith("*") ? (
        <span key={i} style={{ color: keyColor, fontWeight: keyWeight }}>{part.slice(1, -1)}</span>
      ) : (
        <span key={i}>{part}</span>
      ),
    )}
  </>
);
