import React from 'react';
import {Img, staticFile} from 'remotion';
import {colors} from './theme';
import {ease, tween, wrap} from './LocatieSpot';

// Fact cards shared by DroogSpot and LaadSpot: a title block (kicker, "Parking <naam>", city) and three white cards with a
// pictogram and a text whose [bracketed] parts are bold.

export type FeitIcoon = 'plekken' | 'loop' | 'lift' | 'klok' | 'camera' | 'laden';
export type Feit = [FeitIcoon, string];

export type FeitenGeo = {titelX: number; titelY: number; titelW: number; titel: number; align: 'center' | 'left'; x: number; y: number; w: number; h: number; gap: number; tekst: number; icoon: number};

const ICOON: Record<Exclude<FeitIcoon, 'klok'>, string> = {
  plekken: 'svg/atom/py-atom-symbol-p-garage-outline.svg',
  loop: 'svg/atom/py-atom-figure-walk.svg',
  lift: 'svg/atom/py-atom-picto-lift.svg',
  camera: 'svg/atom/py-atom-sign-camera.svg',
  laden: 'svg/atom/py-atom-picto-ev.svg',
};

const Icoon: React.FC<{soort: FeitIcoon; size: number}> = ({soort, size}) =>
  soort === 'klok' ? (
    <svg width={size} height={size} viewBox="0 0 100 100">
      <circle cx={50} cy={50} r={42} fill="none" stroke={colors.blauw} strokeWidth={9} />
      <line x1={50} y1={50} x2={50} y2={22} stroke={colors.blauw} strokeWidth={9} strokeLinecap="round" />
      <line x1={50} y1={50} x2={70} y2={60} stroke={colors.blauw} strokeWidth={9} strokeLinecap="round" />
    </svg>
  ) : (
    <Img src={staticFile(ICOON[soort])} style={{width: size, height: size, objectFit: 'contain', display: 'block'}} />
  );

export const delen = (s: string) => s.split(/(\[[^\]]*\])/).filter(Boolean).map((x) => (x.startsWith('[') ? {t: x.slice(1, -1), vet: true} : {t: x, vet: false}));

export const Feiten: React.FC<{frame: number; start: number; F: FeitenGeo; kicker: string; naam: string; stad: string; feiten: Feit[]}> = ({frame, start, F, kicker, naam, stad, feiten}) => {
  if (frame < start - 20) return null;
  return (
    <>
      <div style={{position: 'absolute', left: F.titelX, top: F.titelY, width: F.titelW, textAlign: F.align, color: colors.wit, opacity: tween(frame, start - 10, start + 16)}}>
        <div style={{fontSize: F.titel * 0.5, fontWeight: 400, marginBottom: 10}}>{kicker}</div>
        <div style={{fontSize: F.titel, fontWeight: 300, lineHeight: 1.05}}>Parking</div>
        <div style={{fontSize: F.titel, fontWeight: 700, lineHeight: 1.05}}>{naam}</div>
        <div style={{fontSize: F.titel * 0.5, fontWeight: 400, marginTop: 14, color: colors.aqua}}>{stad}</div>
      </div>
      {feiten.map(([soort, tekst], i) => {
        const v = tween(frame, start + 20 + i * 22, start + 46 + i * 22, ease(0.2, 0.9, 0.3, 1.1));
        const tekstW = F.w - F.icoon - 3 * 36;
        const regels = wrap(tekst.replace(/[[\]]/g, ''), F.tekst, '700', tekstW);
        return (
          <div key={i} style={{position: 'absolute', left: F.x, top: F.y + i * (F.h + F.gap), width: F.w, height: F.h, borderRadius: 32, background: colors.wit, opacity: Math.min(1, v * 1.5), transform: `translateX(${(1 - v) * 60}px)`}}>
            <div style={{position: 'absolute', left: 36, top: (F.h - F.icoon) / 2, width: F.icoon, height: F.icoon, borderRadius: 26, background: '#E3F5F8', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
              <Icoon soort={soort} size={F.icoon * 0.62} />
            </div>
            <div style={{position: 'absolute', left: F.icoon + 72, top: 0, height: F.h, width: tekstW, display: 'flex', alignItems: 'center', color: colors.blauw, fontSize: regels.length > 1 ? F.tekst * 0.88 : F.tekst, lineHeight: 1.15}}>
              <div>
                {delen(tekst).map((x, j) => (
                  <span key={j} style={{fontWeight: x.vet ? 700 : 400}}>
                    {x.t}
                  </span>
                ))}
              </div>
            </div>
          </div>
        );
      })}
    </>
  );
};
