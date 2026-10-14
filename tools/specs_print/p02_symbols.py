"""Shared print symbols used by more than one application."""
from pyassets import printsrc
from pyassets.registry import crop, element


@element("py-atom-symbol-p-plain", "P (plat, live tekst)", "atom", "symbol", 1, src="maashaven",
         variables=("colour", "size"),
         notes="Plain bold P as live Ubuntu Bold text (white on navy), 91.7 mm as on the Maashaven header; GLOW uses it at 173.4 mm. "
               "Not the P with roof (py-atom-symbol-p-roof). White on transparent: view on a dark background.")
def _(src):
    return crop(src, 1, printsrc.box_mm(160, 0, 240, 120), texts=True)
