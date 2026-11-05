import React from "react";

/**
 * "*word*" marks a key phrase (bold, accent colour). parseRich returns lines of words; a word can mix plain and key
 * segments, so punctuation right after a key phrase ("*vroeg*,") stays attached to it.
 */
export type Segment = { text: string; key: boolean };
export type Word = Segment[];

export const parseRich = (text: string): Word[][] =>
  text.split("\n").map((line) => {
    const words: Word[] = [];
    let glue = false; // true when the previous segment ended without whitespace
    line.split(/(\*[^*]+\*)/g).filter(Boolean).forEach((part) => {
      const key = part.startsWith("*") && part.endsWith("*");
      const clean = key ? part.slice(1, -1) : part;
      const tokens = clean.split(/(\s+)/);
      tokens.forEach((tok, ti) => {
        if (!tok) return;
        if (/^\s+$/.test(tok)) { glue = false; return; }
        if (glue && ti === 0 && words.length) words[words.length - 1].push({ text: tok, key });
        else words.push([{ text: tok, key }]);
        glue = true;
      });
      if (/\s$/.test(clean)) glue = false;
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
