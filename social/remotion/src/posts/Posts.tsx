import React from "react";
import { AbsoluteFill, useVideoConfig } from "remotion";
import "../theme";
import { BRAND, FONT } from "../theme";
import { Backdrop, BackdropKind } from "../v2/Backdrop";
import { Title } from "../v2/Title";
import { CtaPill, UrlLine } from "../v2/CtaPill";
import { PlacePill, PriceBadge, TopLogo } from "../v2/Badges";
import { Card } from "../v2/Card";
import { Confetti, Skyline, Sparkles, Sunburst } from "../v2/Fx";
import { AssetImg } from "../components/AssetImg";
import { Rain } from "../components/Rain";
import { Rich } from "../lib/rich";

/**
 * Static feed posts (1080 x 1350), built from the same kit as the reels and rendered as stills at STILL_FRAME,
 * when every entrance has finished. One function per post; texts and prices are in the JSX on purpose,
 * so a post reads top to bottom like the image.
 */
export const STILL_FRAME = 110;
const W = 1080;
const M = 70;

const Frame: React.FC<{ kind: BackdropKind; title: string; titleSize?: number; titleTop?: number; cta?: string; ctaVariant?: "aqua" | "navy"; url?: string; dark?: boolean; children?: React.ReactNode; partner?: string; seed: string }> = ({ kind, title, titleSize = 118, titleTop = 150, cta, ctaVariant = "aqua", url = "voordeligparkeren.nl", children, partner, seed }) => {
  const ink = kind === "light" ? BRAND.blauw : BRAND.wit;
  return (
    <Backdrop kind={kind} seed={seed}>
      <AbsoluteFill>
        <div style={{ position: "absolute", left: 0, right: 0, top: 56, display: "flex", justifyContent: "center", alignItems: "center", gap: 22 }}>
          <TopLogo width={280} start={0} />
          {partner && <span style={{ fontFamily: FONT, fontWeight: 700, fontSize: 44, color: ink }}>× {partner}</span>}
        </div>
        <div style={{ position: "absolute", left: M, top: titleTop }}>
          <Title text={title} color={ink} maxSize={titleSize} width={W - 2 * M} />
        </div>
        {children}
        {cta && (
          <div style={{ position: "absolute", left: M, top: 1110 }}>
            <CtaPill text={cta} start={0} height={118} variant={ctaVariant} />
          </div>
        )}
        {url && (
          <div style={{ position: "absolute", left: M + 6, top: cta ? 1252 : 1230 }}>
            <UrlLine url={url} start={0} size={48} color={ink} />
          </div>
        )}
      </AbsoluteFill>
    </Backdrop>
  );
};

const Abs: React.FC<{ x?: number; y: number; w?: number; center?: boolean; children: React.ReactNode; style?: React.CSSProperties }> = ({ x = M, y, w, center, children, style }) => (
  <div style={{ position: "absolute", left: center ? 0 : x, right: center ? 0 : undefined, top: y, width: w, display: center ? "flex" : undefined, justifyContent: center ? "center" : undefined, ...style }}>{children}</div>
);

const Small: React.FC<{ y: number; text: string; color?: string; size?: number }> = ({ y, text, color = BRAND.wit, size = 38 }) => (
  <div style={{ position: "absolute", left: M, right: M, top: y, fontFamily: FONT, fontSize: size, color, opacity: 0.85 }}>
    <Rich text={text} keyColor={color} />
  </div>
);

const Burst: React.FC<{ cx: number; cy: number; size: number; color?: string }> = ({ cx, cy, size, color }) => (
  <div style={{ position: "absolute", left: cx - size / 2, top: cy - size / 2, width: size, height: size }}>
    <Sunburst start={-40} size={size} color={color} />
  </div>
);

const TextBadge: React.FC<{ text: string; label: string; size: number; tone?: "white" | "aqua" }> = ({ text, label, size, tone = "aqua" }) => (
  <div style={{ width: size, height: size, borderRadius: size / 2, background: tone === "aqua" ? BRAND.aqua : BRAND.wit, color: tone === "aqua" ? BRAND.wit : BRAND.blauw, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", transform: "rotate(-8deg)", boxShadow: "0 24px 60px rgba(6,14,50,0.3)", fontFamily: FONT }}>
    <div style={{ fontWeight: 700, fontStyle: "italic", fontSize: size * 0.34, lineHeight: 1 }}>{text}</div>
    <div style={{ fontSize: size * 0.1, marginTop: size * 0.03 }}>{label}</div>
  </div>
);

const Egg: React.FC<{ w: number; rotate: number }> = ({ w, rotate }) => (
  <div style={{ position: "relative", width: w, height: w * 1.3, transform: `rotate(${rotate}deg)`, filter: "drop-shadow(0 26px 30px rgba(26,53,128,0.35))" }}>
    <svg width={w} height={w * 1.3} viewBox="0 0 100 130" style={{ position: "absolute", inset: 0 }}>
      <defs>
        <radialGradient id={`egg${w}`} cx="35%" cy="30%" r="80%">
          <stop offset="0%" stopColor="#3D5DC4" />
          <stop offset="60%" stopColor={BRAND.blauw} />
          <stop offset="100%" stopColor="#0E1E52" />
        </radialGradient>
      </defs>
      <path d="M50 2C22 2 2 50 2 82C2 110 24 128 50 128C76 128 98 110 98 82C98 50 78 2 50 2Z" fill={`url(#egg${w})`} />
      <ellipse cx="34" cy="34" rx="9" ry="16" fill="#FFFFFF" opacity="0.18" transform="rotate(-20 34 34)" />
    </svg>
    <div style={{ position: "absolute", left: w * 0.3, top: w * 0.5, width: w * 0.4 }}>
      <AssetImg id="py-atom-logo-beeldmerk-white" width={w * 0.4} />
    </div>
  </div>
);

export const POSTS: Record<string, { slug: string; render: () => React.ReactNode }> = {
  "IG-004": {
    slug: "cruquius-busje-past",
    render: () => (
      <Frame kind="navy" seed="p004" title={"2,70 meter.\n*Ook je busje past.*"} cta="Reserveer online">
        {/* height indicator: two levels and a double arrow */}
        <svg width={W} height={360} style={{ position: "absolute", left: 0, top: 430 }}>
          <line x1={M} y1={20} x2={W - M} y2={20} stroke={BRAND.wit} strokeWidth={6} strokeDasharray="18 14" opacity={0.6} />
          <line x1={M} y1={330} x2={W - M} y2={330} stroke={BRAND.wit} strokeWidth={6} opacity={0.6} />
          <path d={`M${M + 50} 34 L${M + 50} 316 M${M + 30} 60 L${M + 50} 34 L${M + 70} 60 M${M + 30} 290 L${M + 50} 316 L${M + 70} 290`} stroke={BRAND.aqua} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" fill="none" />
        </svg>
        <Abs x={M + 120} y={500}><div style={{ fontFamily: FONT, fontWeight: 700, fontStyle: "italic", fontSize: 220, color: BRAND.aqua, lineHeight: 1 }}>2,70 m</div></Abs>
        <Abs y={820} w={W - 2 * M}><div style={{ display: "flex", flexDirection: "column", gap: 26 }}>
          <Card icon="py-atom-sign-camera" tint="none" text="Ondergronds, met *camerabewaking*" height={120} maxFont={46} textWidth={700} />
          <Card icon="py-atom-icon-calendar" text="Vroegboeken *€17,50* per dag" height={120} maxFont={46} textWidth={700} />
        </div></Abs>
        <Abs x={640} y={1118}><PlacePill name="Cruquius" start={0} height={104} /></Abs>
      </Frame>
    ),
  },
  "IG-011": {
    slug: "blijdorp-parkeer-ernaast",
    render: () => (
      <Frame kind="glow" seed="p011" title={"Naar Blijdorp?\n*Parkeer ernaast.*"}>
        <Burst cx={760} cy={740} size={620} />
        <Abs x={760 - 220} y={740 - 220}><PriceBadge amount={12.5} label="per dag" start={-40} size={440} float={false} /></Abs>
        <Abs y={590} w={450}><div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
          <Card icon="py-atom-symbol-p-roof" text="*1.200* plekken" height={116} maxFont={46} textWidth={330} />
          <Card icon="py-atom-picto-ev" text="*Laadpalen*" height={116} maxFont={46} textWidth={330} />
          <Card icon="py-atom-picto-family" text="Naast de *ingang*" height={116} maxFont={46} textWidth={330} />
        </div></Abs>
        <Abs y={1080}><PlacePill name="Diergaarde Blijdorp" start={0} height={110} /></Abs>
      </Frame>
    ),
  },
  "IG-013": {
    slug: "almere-wtc-6-euro",
    render: () => (
      <Frame kind="navy" seed="p013" title={"Een hele dag\nparkeren in Almere\nvoor *€6.*"}>
        <Burst cx={W / 2} cy={790} size={640} />
        <Abs x={W / 2 - 220} y={790 - 220}><PriceBadge amount={6} label="per dag" start={-40} size={440} tone="aqua" float={false} /></Abs>
        <Abs y={1040}><PlacePill name="P2 Mandela WTC" start={0} height={104} /></Abs>
        <Small y={1165} text="*250* overdekte plekken onder het WTC Almere" size={40} />
      </Frame>
    ),
  },
  "IG-015": {
    slug: "heerhugowaard-1-euro-per-uur",
    render: () => (
      <Frame kind="glow" seed="p015" title={"Parkeren in\nHeerhugowaard:\n*€1 per uur.*"}>
        <Burst cx={790} cy={790} size={560} />
        <Abs x={790 - 200} y={790 - 200}><PriceBadge amount={0.2} label="per 12 min" start={-40} size={400} float={false} /></Abs>
        <Abs y={640} w={460}><div style={{ display: "flex", flexDirection: "column", gap: 26 }}>
          <Card icon="clock" text="Per *12 minuten*" height={116} maxFont={44} textWidth={290} />
          <Card icon="py-atom-icon-calendar" text="Hele dag *€9*" height={116} maxFont={44} textWidth={290} />
          <Card icon="py-atom-picto-ev" text="*Laadpalen*" height={116} maxFont={44} textWidth={290} />
        </div></Abs>
        <Abs y={1100}><PlacePill name="P1 Zuidtangent · P2 Middenwaard" start={0} height={104} /></Abs>
      </Frame>
    ),
  },
  "IG-019": {
    slug: "vroegboeken-derde-goedkoper",
    render: () => (
      <Frame kind="navy" seed="p019" title={"Vroeg boeken =\ntot *1/3 goedkoper*"} cta="Reserveer online">
        <Burst cx={780} cy={700} size={560} />
        <Abs x={780 - 190} y={700 - 190}><TextBadge text="-33%" label="vroegboeken" size={380} /></Abs>
        <Abs y={520} w={470}><div style={{ fontFamily: FONT, fontSize: 44, color: BRAND.wit, opacity: 0.85, marginBottom: 18 }}>Plantage, Amsterdam</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
            <Card icon="py-atom-picto-car" text="Ter plaatse *€45*" height={116} maxFont={46} textWidth={360} style={{ opacity: 0.6 }} />
            <Card icon="py-atom-icon-calendar" text="Vroegboeken *€30*" height={116} maxFont={46} textWidth={360} bg={BRAND.aqua} fg={BRAND.wit} />
          </div>
        </Abs>
        <Small y={930} text="Zelfde plek, zelfde dag. Alleen eerder geboekt." size={40} />
      </Frame>
    ),
  },
  "IG-022": {
    slug: "pr-schiedam-364",
    render: () => (
      <Frame kind="navy" seed="p022" title={"Met de trein naar\nRotterdam? Parkeer\nvoor *€3,64.*"}>
        <Burst cx={790} cy={680} size={460} />
        <Abs x={790 - 160} y={680 - 160}><PriceBadge amount={3.64} label="per dag" start={-40} size={320} float={false} /></Abs>
        <Abs y={860} w={W - 2 * M}><div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          <Card icon="clock" text="Ma t/m vr, *05:15 - 19:00*" height={100} maxFont={42} textWidth={760} />
          <Card icon="check" text="Met de trein: *check in en uit*" height={100} maxFont={42} textWidth={760} />
        </div></Abs>
        <Abs y={1110}><div style={{ display: "flex", alignItems: "center", gap: 20 }}>
          <div style={{ width: 104, height: 104, borderRadius: 24, background: BRAND.wit, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: FONT, fontWeight: 700, fontSize: 44, color: BRAND.blauw }}>P+R</div>
          <PlacePill name="Schiedam Centrum" start={0} height={104} />
        </div></Abs>
      </Frame>
    ),
  },
  "IG-027": {
    slug: "artis-leden-15",
    render: () => (
      <Frame kind="glow" seed="p027" title={"Artis-lid?\nParkeer voor *€15*\nper dag."}>
        <Burst cx={W / 2} cy={800} size={620} />
        <Abs x={W / 2 - 220} y={800 - 220}><PriceBadge amount={15} label="per dag" start={-40} size={440} float={false} /></Abs>
        <Abs y={1040}><PlacePill name="Plantage, naast Artis" start={0} height={104} /></Abs>
        <Small y={1165} text="Met een los Artis-ticket betaal je *€17,50* per dag." size={40} />
      </Frame>
    ),
  },
  "IG-036": {
    slug: "storing-bel-ons",
    render: () => (
      <Frame kind="navy" seed="p036" title={"Gaat de slagboom\nniet open?\n*Bel ons.*"} url="">
        <Abs y={640} w={W - 2 * M}><div style={{ height: 230, borderRadius: 115, background: BRAND.wit, display: "flex", alignItems: "center", gap: 34, padding: "0 50px 0 30px", boxShadow: "0 24px 60px rgba(6,14,50,0.3)" }}>
          <div style={{ width: 170, height: 170, borderRadius: 85, background: BRAND.blauw, display: "flex", alignItems: "center", justifyContent: "center" }}><AssetImg id="py-atom-icon-headset-agent" width={100} tint="white" /></div>
          <div style={{ fontFamily: FONT, fontWeight: 700, fontSize: 92, color: BRAND.blauw, letterSpacing: "-0.01em", whiteSpace: "nowrap" }}>085 401 16 47</div>
        </div></Abs>
        <Abs y={930} w={W - 2 * M}><Card icon="py-atom-icon-info-bubble" tint="white" text="Noem het *automaatnummer* op de sticker" height={130} maxFont={46} textWidth={760} /></Abs>
        <Small y={1120} text="Dan weten we meteen waar je staat en helpen we je verder." size={42} />
      </Frame>
    ),
  },
  "IG-040": {
    slug: "carnaval-auto-veilig",
    render: () => (
      <Frame kind="navy" seed="p040" title={"Te gezellig?\nJe auto wacht\nhier *veilig.*"} cta="Reserveer online">
        <Confetti start={STILL_FRAME - 22} x={0.5} y={0.42} count={90} />
        <Abs x={M} y={720}><Skyline start={-40} width={W - 2 * M} /></Abs>
        <Abs x={660} y={1118}><div style={{ fontFamily: FONT, fontWeight: 700, fontSize: 64, color: BRAND.oranje, transform: "rotate(-6deg)" }}>Salaai!</div></Abs>
        <Abs x={M} y={590}><PlacePill name="DLL Garage, Eindhoven" start={0} height={100} /></Abs>
      </Frame>
    ),
  },
  "IG-043": {
    slug: "oud-en-nieuw-hofplein",
    render: () => (
      <Frame kind="navy" seed="p043" title={"Vuurwerk kijken.\n*Auto blijft staan.*"}>
        <Sparkles seed="p043s" count={60} colors={["#FFFFFF", "#FFD38A", BRAND.oranje, BRAND.aqua]} />
        <Burst cx={W / 2} cy={760} size={620} color="#FFD38A" />
        <Abs x={W / 2 - 220} y={760 - 220}><PriceBadge amount={15} label="nachttarief" start={-40} size={440} float={false} /></Abs>
        <Abs y={1040}><PlacePill name="Hofplein, Rotterdam" start={0} height={104} /></Abs>
        <Small y={1165} text="Nachttarief van *00:00 tot 09:00*" size={40} />
      </Frame>
    ),
  },
  "IG-049": {
    slug: "regen-droog-uitstappen",
    render: () => {
      const { width, height } = useVideoConfig();
      return (
        <Frame kind="navy" seed="p049" title={"Het regent.\n*Jij stapt droog uit.*"} cta="Reserveer online">
          <AbsoluteFill style={{ opacity: 0.55 }}><Rain width={width} height={height} color="#8FDDEA" count={110} /></AbsoluteFill>
          <Abs x={W - M - 300} y={430}><div style={{ width: 300, height: 300, borderRadius: 150, background: BRAND.aqua, display: "flex", alignItems: "center", justifyContent: "center", boxShadow: "0 0 80px rgba(50,185,205,0.45)" }}><AssetImg id="py-atom-symbol-p-roof" height={200} /></div></Abs>
          <Small y={760} text="Overdekt parkeren bij" size={44} />
          <Abs y={830} w={W - 2 * M}><div style={{ display: "flex", flexWrap: "wrap", gap: 16 }}>
            {["Hofplein", "Europoint", "Cruquius", "Zeeburgerkade", "DLL garage", "At the Park"].map((n) => <PlacePill key={n} name={n} start={0} height={80} />)}
          </div></Abs>
        </Frame>
      );
    },
  },
  "IG-055": {
    slug: "avond-weekend-abonnement",
    render: () => (
      <Frame kind="navy" seed="p055" title={"Overdag weg?\n's Avonds en in het\nweekend *je vaste plek.*"} cta="Abonnement aanvragen">
        <Abs y={600} w={W - 2 * M}><div style={{ display: "flex", flexDirection: "column", gap: 28 }}>
          <Card icon="py-atom-illustration-card-pas" text="Heerhugowaard  *€39,42* p/m" height={150} maxFont={52} textWidth={760} />
          <Card icon="py-atom-illustration-card-pas" text="Bos en Lommer, Cruquius  *€205* p/m" height={150} maxFont={52} textWidth={760} />
        </div></Abs>
        <Small y={960} text="Avond- en weekendabonnement. Exclusief €5 servicekosten per maand." size={36} />
      </Frame>
    ),
  },
  "IG-058": {
    slug: "zakelijk-team-groeit",
    render: () => (
      <Frame kind="glow" seed="p058" title={"Je team groeit.\n*De parkeerplaats ook.*"} cta="Neem contact op" ctaVariant="navy" url="info@parkingyou.nl">
        <Abs x={M} y={470}><Skyline start={-40} width={W - 2 * M} figures={["py-atom-picto-car", "py-atom-figure-cap-wave", "py-atom-picto-car", "py-atom-figure-point", "py-atom-picto-car", "py-atom-figure-walk"]} /></Abs>
        <Abs y={820} w={W - 2 * M}><Card icon="py-atom-illustration-card-pas" text="Bedrijfsabonnement vanaf *€79,14* p/m" height={150} maxFont={52} textWidth={760} /></Abs>
        <Small y={1000} text="Heerhugowaard, exclusief €5 servicekosten per maand. Ook op andere locaties." size={36} />
      </Frame>
    ),
  },
  "IG-063": {
    slug: "pasen-eieren-zoeken",
    render: () => (
      <Frame kind="light" seed="p063" title={"We hebben\n*3 ParkingYou-eieren*\nverstopt."} url="">
        <Abs x={150} y={640}><Egg w={240} rotate={-12} /></Abs>
        <Abs x={420} y={590}><Egg w={270} rotate={4} /></Abs>
        <Abs x={710} y={660}><Egg w={230} rotate={14} /></Abs>
        <Abs y={1050} w={W - 2 * M}><div style={{ fontFamily: FONT, fontSize: 50, lineHeight: 1.25, color: BRAND.blauw }}><Rich text={"Vind je er één? Dan parkeer je *gratis*\nbij je volgende reservering."} keyColor={BRAND.blauw} /></div></Abs>
        <Small y={1240} text="Actievoorwaarden op voordeligparkeren.nl" color={BRAND.blauw} size={32} />
      </Frame>
    ),
  },
  "IG-065": {
    slug: "the-other-way-of-parking",
    render: () => (
      <Frame kind="glow" seed="p065" title={"The other way\nof *parking.*"} titleTop={520} titleSize={150} url="voordeligparkeren.nl">
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: 0.1 }}><AssetImg id="py-atom-logo-beeldmerk-white" width={1100} /></AbsoluteFill>
        <Small y={900} text="Parkeren in Amsterdam, Rotterdam, Eindhoven, Den Haag, Almere, Zoetermeer en meer. *Vooraf geregeld*, zonder gedoe." size={44} />
      </Frame>
    ),
  },
};

export const Post: React.FC<{ id: string }> = ({ id }) => <>{POSTS[id]?.render()}</>;
