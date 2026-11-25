import React from 'react';
import {Composition} from 'remotion';
import {Story1App} from './Story1App';
import {Story2Shoppen} from './Story2Shoppen';
import {Story3Tagline} from './Story3Tagline';
import {LocatieSpot, SPOT} from './LocatieSpot';
import {locaties} from './locaties';
import {DURATION, FPS, HEIGHT, WIDTH} from './theme';

const common = {durationInFrames: DURATION, fps: FPS, width: WIDTH, height: HEIGHT};

export const Root: React.FC = () => (
  <>
    <Composition id="Story1-App" component={Story1App} {...common} />
    <Composition id="Story2-Shoppen" component={Story2Shoppen} {...common} />
    <Composition id="Story3-Tagline" component={Story3Tagline} {...common} />
    {locaties.map((l) => (
      <Composition
        key={l.slug}
        id={`Spot-${l.slug}`}
        component={LocatieSpot}
        durationInFrames={SPOT.duration}
        fps={SPOT.fps}
        width={SPOT.width}
        height={SPOT.height}
        defaultProps={{locatie: l}}
      />
    ))}
  </>
);
