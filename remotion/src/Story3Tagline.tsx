import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, Easing} from 'remotion';
import {Atom, Fonts, FloatingCircles, Pill, Rise, headline, useOutro, useSpring} from './components';
import {DURATION, HEIGHT, SAFE, WIDTH, colors, font, verloop} from './theme';

const WORDS = ['Voordelig', 'parkeren', 'zonder', 'gedoe?'];
const REVEAL_AT = 96; // frame where the gradient circle wipes in

/** Story 3: question, then brand reveal with the tagline (copy from the brand print files). */
export const Story3Tagline: React.FC = () => {
  const frame = useCurrentFrame();
  const out = useOutro(DURATION);

  // Circle wipe from the centre; radius covers the full diagonal.
  const maxR = Math.hypot(WIDTH, HEIGHT) / 2 + 40;
  const wipe = interpolate(frame, [REVEAL_AT, REVEAL_AT + 26], [0, maxR], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(0.7, 0, 0.3, 1),
  });
  const qOut = interpolate(frame, [REVEAL_AT - 6, REVEAL_AT + 8], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const logo = useSpring(REVEAL_AT + 22, {damping: 12, stiffness: 110});
  const tagline = interpolate(frame, [REVEAL_AT + 44, REVEAL_AT + 66], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const pulse = 1 + Math.sin(frame / 8) * 0.025;

  return (
    <AbsoluteFill style={{background: colors.blauw, opacity: out}}>
      <Fonts />
      <FloatingCircles color={colors.aqua} opacity={0.12} />

      {/* the question */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          bottom: 0,
          left: 90,
          right: 90,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          opacity: qOut,
          ...headline,
          fontSize: 140,
          color: colors.wit,
        }}
      >
        {WORDS.map((w, i) => (
          <Rise key={w} delay={8 + i * 14} distance={80} style={{color: i === 3 ? colors.aqua : colors.wit}}>
            {w}
          </Rise>
        ))}
      </div>

      {/* brand reveal */}
      <AbsoluteFill style={{background: verloop, clipPath: `circle(${wipe}px at 50% 50%)`}}>
        <FloatingCircles color={colors.wit} opacity={0.07} />
        <div
          style={{
            position: 'absolute',
            top: 640,
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 40,
            transform: `scale(${0.6 + 0.4 * logo})`,
            opacity: Math.min(1, logo * 1.5),
          }}
        >
          <Atom id="logo-stacked-white" width={720} />
          <div
            style={{
              fontFamily: font,
              fontWeight: 400,
              fontSize: 50,
              letterSpacing: 4,
              color: colors.wit,
              opacity: tagline,
              transform: `translateY(${(1 - tagline) * 20}px)`,
            }}
          >
            The other way of parking
          </div>
        </div>

        <Rise delay={REVEAL_AT + 70} style={{position: 'absolute', bottom: SAFE.bottom + 20, width: '100%', display: 'flex', justifyContent: 'center'}}>
          <div style={{transform: `scale(${pulse})`}}>
            <Pill background={colors.wit} color={colors.blauw} size={50}>
              voordeligparkeren.nl
            </Pill>
          </div>
        </Rise>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
