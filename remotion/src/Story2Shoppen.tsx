import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Atom, Fonts, Pill, Rise, headline, useOutro, useSpring} from './components';
import {DURATION, SAFE, colors, verloop} from './theme';

/** Story 2: "Jouw dagje shoppen start hier!" (copy from py-app-poster-partner-a4). */
export const Story2Shoppen: React.FC = () => {
  const frame = useCurrentFrame();
  const out = useOutro(DURATION);
  const bubble = useSpring(14, {damping: 11, stiffness: 100});
  const walkIn = useSpring(20, {damping: 20, stiffness: 70});
  const jump = useSpring(70, {damping: 7, stiffness: 160, mass: 0.8});
  const cheering = frame >= 70;
  const hop = cheering ? -Math.sin(Math.min(1, jump) * Math.PI) * 60 : Math.abs(Math.sin(frame / 5)) * -10;
  const x = cheering ? 0 : (1 - walkIn) * -700;
  const pulse = 1 + Math.sin(frame / 9) * 0.02;
  const gradShift = interpolate(frame, [0, DURATION], [0, 100]);

  return (
    <AbsoluteFill style={{background: colors.wit, opacity: out}}>
      <Fonts />
      {/* faint watermark beeldmerk, as on the print files */}
      <div style={{position: 'absolute', right: -240, bottom: -120, opacity: 0.9}}>
        <Atom id="logo-beeldmerk-watermark" width={900} />
      </div>

      <Rise delay={0} distance={-40} style={{position: 'absolute', top: SAFE.top + 10, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <Atom id="logo-horizontal-color" width={430} />
      </Rise>

      <div style={{position: 'absolute', top: 440, width: '100%', textAlign: 'center', ...headline, fontSize: 108, color: colors.blauw}}>
        <Rise delay={8}>Jouw dagje</Rise>
        <Rise delay={14}>shoppen</Rise>
        <Rise delay={22}>
          <span
            style={{
              background: verloop,
              backgroundSize: '200% 200%',
              backgroundPosition: `${gradShift}% 50%`,
              WebkitBackgroundClip: 'text',
              backgroundClip: 'text',
              color: 'transparent',
              WebkitTextFillColor: 'transparent',
            }}
          >
            start hier!
          </span>
        </Rise>
      </div>

      {/* orange bubble with the shopper */}
      <div
        style={{
          position: 'absolute',
          top: 790,
          left: '50%',
          marginLeft: -280,
          transform: `scale(${bubble})`,
          transformOrigin: '50% 100%',
        }}
      >
        <Atom id="shape-bubble-solid" width={560} />
        <div style={{position: 'absolute', left: 0, right: 0, top: 105, display: 'flex', justifyContent: 'center'}}>
          <div style={{transform: `translate(${x}px, ${hop}px)`}}>
            <Atom id={cheering ? 'figure-bags-cheer' : 'figure-bags-walk'} width={cheering ? 420 : 360} />
          </div>
        </div>
      </div>

      <Rise delay={56} style={{position: 'absolute', bottom: SAFE.bottom + 20, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <div style={{transform: `scale(${pulse})`}}>
          <Pill background={colors.blauw} size={44}>
            Slim parkeren. Snel in de stad.
          </Pill>
        </div>
      </Rise>
    </AbsoluteFill>
  );
};
