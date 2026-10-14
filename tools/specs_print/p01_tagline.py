"""Tagline lockup and the A6 brand background (Naamloos-7.pdf) plus the reverse lockup used on the card back."""
from pyassets import printsrc
from pyassets.compose import Doc
from pyassets.registry import crop, element
from pyassets.apps import application

T_BOX = printsrc.box_mm(50, 58, 113, 68)  # tagline ink area on the A6 background (page mm)


@element("py-atom-text-tagline", "Tagline The other way of parking", "atom", "text", 1, src="tagline",
         variables=("colour", "text"),
         notes="Live Ubuntu Regular, tracking about +60/1000 em (measured on both print files), white on navy. Size 4.58 mm is the size on the A6 background; "
               "observed ratio 0.158 x the beeldmerk height. Observed in print, not an official rule.")
def _(src):
    return crop(src, 1, T_BOX, texts=True)


def _tagline_box():
    """Ink box (mm) of the tagline on the A6 background."""
    from pyassets.core import PT_MM

    src = printsrc.source("tagline")
    t = [it for it in crop(src, 1, T_BOX, texts=True) if hasattr(it, "text")][0]
    return tuple(v * PT_MM for v in t.box)


# logo as printed on the A6 background: 104.9 x 28.9 mm at (21.7, 38.1), i.e. the library logo at scale 1
LOGO_XY = (21.7, 38.1)


def _lockup(doc, logo_id):
    x0, y0, x1, y1 = _tagline_box()
    doc.place(logo_id, *LOGO_XY, h=28.949)
    doc.place("py-atom-text-tagline", x0, y0, scale=1.0)


@element("py-comp-tagline-lockup", "Taglinelockup (wit)", "comp", "lockup", 1, src="tagline", status="rebuilt",
         variables=("background colour", "tagline text"),
         notes="Library logo py-atom-logo-horizontal-white (white dot) at scale 1 plus the tagline atom, positions measured on Naamloos-7. "
               "White on navy; place on PY-Blauw. Centred on the format in print (observed).")
def _(src):
    d = Doc("py-comp-tagline-lockup", "Taglinelockup (wit)", tight=True)
    _lockup(d, "py-atom-logo-horizontal-white")
    return d


@element("py-comp-tagline-lockup-reverse", "Taglinelockup (omgekeerd, aqua stip)", "comp", "lockup", 2, src="evoluon", status="rebuilt",
         variables=("background colour", "tagline text"),
         notes="Same lockup with py-atom-logo-horizontal-reverse (white bubble, navy ring, aqua dot) as used on the card back (EvoluonPasjes p2). "
               "Geometry follows the A6 lockup; the card back uses it at 0.511x. Two reverse logos are in use in print (white dot versus aqua dot).")
def _(src):
    d = Doc("py-comp-tagline-lockup-reverse", "Taglinelockup (omgekeerd)", tight=True)
    _lockup(d, "py-atom-logo-horizontal-reverse")
    return d


@application("py-app-brand-background-tagline", "Merkachtergrond met tagline", "brand-background", trim_mm=(148, 105),
             source=[("tagline", [1])], bleed_mm=3.0, status="rebuilt",
             notes="Template is built in the official PY-Blauw (CMYK 100/83/0/17, #1A3580). The source is RGB only (#1A3680).")
def _(ctx):
    d = ctx.Doc("py-app-brand-background-tagline", "Merkachtergrond met tagline", trim=(148, 105), bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-type-ubuntu-regular", "py-comp-tagline-lockup")
    d.rect(-3, -3, 151, 108, fill="#1A3580", gid="background", variable="background-colour", example="#1A3580")
    _lockup_in_doc(d)
    d.guides(148, 105)
    return dict(reference={"": ctx.reference("tagline", 1)}, template={"": d})


def _lockup_in_doc(d):
    x0, y0, x1, y1 = _tagline_box()
    with d.group("py-comp-tagline-lockup"):
        d.place("py-atom-logo-horizontal-white", *LOGO_XY, h=28.949)
        d.text(x0 - 0.0, y1 - 0.0, "The other way of parking", size=4.58, fill="#FFFFFF", spacing=0.27, variable="tagline-text")
