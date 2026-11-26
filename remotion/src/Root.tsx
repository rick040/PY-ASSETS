import React from 'react';
import {Composition} from 'remotion';
import {Story1App} from './Story1App';
import {Story2Shoppen} from './Story2Shoppen';
import {Story3Tagline} from './Story3Tagline';
import {LocatieSpot, REEL, SPOT} from './LocatieSpot';
import {locaties} from './locaties';
import {ZOEK_SIZE, ZoekSpot, timeline} from './ZoekSpot';
import {zoekopdrachten} from './zoekopdrachten';
import {CHAT_SIZE, ChatSpot, chatTimeline} from './ChatSpot';
import {chatgesprekken} from './chatgesprekken';
import {LIJST_SIZE, LijstSpot, lijstTimeline} from './LijstSpot';
import {BORD_SIZE, BordSpot, bordTimeline} from './BordSpot';
import {bordjes} from './borden';
import {KAART_SIZE, KaartSpot, kaartTimeline} from './KaartSpot';
import {kaartjes} from './kaartjes';
import {lijstjes} from './lijstjes';
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
        defaultProps={{locatie: l, formaat: 'liggend' as const}}
      />
    ))}
    {locaties.map((l) => (
      <Composition
        key={`reel-${l.slug}`}
        id={`Reel-${l.slug}`}
        component={LocatieSpot}
        durationInFrames={REEL.duration}
        fps={REEL.fps}
        width={REEL.width}
        height={REEL.height}
        defaultProps={{locatie: l, formaat: 'staand' as const}}
      />
    ))}
    {zoekopdrachten.flatMap((z) =>
      (['staand', 'liggend'] as const).map((formaat) => (
        <Composition
          key={`${formaat}-${z.slug}`}
          id={`${formaat === 'staand' ? 'Zoek' : 'ZoekYT'}-${z.slug}`}
          component={ZoekSpot}
          durationInFrames={timeline(z).duration}
          fps={60}
          {...ZOEK_SIZE[formaat]}
          defaultProps={{zoekopdracht: z, formaat}}
        />
      )),
    )}
    {chatgesprekken.flatMap((c) =>
      (['staand', 'liggend'] as const).map((formaat) => (
        <Composition
          key={`chat-${formaat}-${c.slug}`}
          id={`${formaat === 'staand' ? 'Chat' : 'ChatYT'}-${c.slug}`}
          component={ChatSpot}
          durationInFrames={chatTimeline().duration}
          fps={60}
          {...CHAT_SIZE[formaat]}
          defaultProps={{gesprek: c, formaat}}
        />
      )),
    )}
    {lijstjes.flatMap((s) =>
      (['staand', 'liggend'] as const).map((formaat) => (
        <Composition
          key={`lijst-${formaat}-${s.slug}`}
          id={`${formaat === 'staand' ? 'Lijst' : 'LijstYT'}-${s.slug}`}
          component={LijstSpot}
          durationInFrames={lijstTimeline().duration}
          fps={60}
          {...LIJST_SIZE[formaat]}
          defaultProps={{lijstje: s, formaat}}
        />
      )),
    )}
    {bordjes.flatMap((s) =>
      (['staand', 'liggend'] as const).map((formaat) => (
        <Composition
          key={`bord-${formaat}-${s.slug}`}
          id={`${formaat === 'staand' ? 'Bord' : 'BordYT'}-${s.slug}`}
          component={BordSpot}
          durationInFrames={bordTimeline(s.borden.length).duration}
          fps={60}
          {...BORD_SIZE[formaat]}
          defaultProps={{bordje: s, formaat}}
        />
      )),
    )}
    {kaartjes.flatMap((s) =>
      (['staand', 'liggend'] as const).map((formaat) => (
        <Composition
          key={`kaart-${formaat}-${s.slug}`}
          id={`${formaat === 'staand' ? 'Kaart' : 'KaartYT'}-${s.slug}`}
          component={KaartSpot}
          durationInFrames={kaartTimeline(s.parkings.length).duration}
          fps={60}
          {...KAART_SIZE[formaat]}
          defaultProps={{kaartje: s, formaat}}
        />
      )),
    )}
  </>
);
