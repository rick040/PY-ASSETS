"""Shared colour lockup: horizontal logo in colour with the tagline in aqua (letterhead, envelope, P+R sign, tariff panel)."""
from pyassets.compose import Doc
from pyassets.registry import element
import p01_tagline as t1


@element("py-comp-lockup-logo-tagline-color", "Taglinelockup (kleur)", "comp", "lockup", 1, src="briefpapier", status="rebuilt",
         variables=("tagline text", "scale"),
         notes="Library logo py-atom-logo-horizontal-color plus the tagline atom recoloured to PY-Aqua, same geometry as the white A6 lockup "
               "(tagline size 0.158 x beeldmerk height, left aligned with the wordmark; measured equal on Briefpapier_nieuw, "
               "ParkingYou_Envelop_220x156 and PR_RoadSignage). Navy logo on a light ground. Observed in print, not an official rule.")
def _(src):
    d = Doc("py-comp-lockup-logo-tagline-color", "Taglinelockup (kleur)", tight=True)
    x0, y0, x1, y1 = t1._tagline_box()
    d.place("py-atom-logo-horizontal-color", *t1.LOGO_XY, h=28.949)
    d.place("py-atom-text-tagline", x0, y0, scale=1.0, recolor={"#FFFFFF": "#32B9CD"})
    return d
