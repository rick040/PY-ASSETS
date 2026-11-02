import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Atom, Fonts, FloatingCircles, Pill, Rise, headline, useOutro, useSpring} from './components';
import {DURATION, SAFE, colors, verloop} from './theme';

/** Story 1: "Makkelijk parkeren vanuit je broekzak" (copy from py-app-poster-app-a2). */
export const Story1App: React.FC = () => {
  const frame = useCurrentFrame();
  const out = useOutro(DURATION);
  const phone = useSpring(34, {damping: 12, stiffness: 90});
  const float = Math.sin(frame / 22) * 14;
  const pulse = 1 + Math.sin(frame / 8) * 0.025;
  // QR "scan" line sweeping over the phone once it has landed
  const scan = interpolate((frame - 90) % 70, [0, 35, 70], [0, 1, 0], {extrapolateLeft: 'clamp'});

  return (
    <AbsoluteFill style={{background: verloop, opacity: out}}>
      <Fonts />
      <FloatingCircles color={colors.wit} opacity={0.08} />

      <Rise delay={0} distance={-40} style={{position: 'absolute', top: SAFE.top + 10, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <Atom id="logo-horizontal-white" width={430} />
      </Rise>

      <div style={{position: 'absolute', top: 460, width: '100%', textAlign: 'center', ...headline, fontSize: 104, color: colors.wit}}>
        <Rise delay={10}>Makkelijk</Rise>
        <Rise delay={16}>parkeren</Rise>
        <Rise delay={24} style={{color: colors.aqua}}>
          vanuit je broekzak
        </Rise>
      </div>

      <div
        style={{
          position: 'absolute',
          top: 860 + float,
          width: '100%',
          display: 'flex',
          justifyContent: 'center',
          opacity: Math.min(1, phone * 1.5),
          transform: `translateY(${(1 - phone) * 500}px) rotate(${(1 - phone) * -8}deg)`,
        }}
      >
        <div style={{position: 'relative'}}>
          <Atom id="illustration-phone-qr" width={300} style={{filter: 'drop-shadow(0 30px 40px rgba(10,30,90,0.45))'}} />
          <div
            style={{
              position: 'absolute',
              left: 22,
              right: 22,
              top: 125 + scan * 150,
              height: 8,
              borderRadius: 4,
              background: colors.aqua,
              boxShadow: `0 0 24px ${colors.aqua}`,
              opacity: frame > 90 ? 0.9 : 0,
            }}
          />
        </div>
      </div>

      <Rise delay={60} style={{position: 'absolute', bottom: SAFE.bottom + 20, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <div style={{transform: `scale(${pulse})`}}>
          <Pill background={colors.wit} color={colors.blauw} size={50}>
            Download nu onze app
          </Pill>
        </div>
      </Rise>
    </AbsoluteFill>
  );
};
