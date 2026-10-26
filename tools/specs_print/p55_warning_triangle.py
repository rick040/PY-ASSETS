"""Warning triangle shared by the barrier banner and the A3 storing poster."""
from pyassets import printsrc
from pyassets.registry import crop, element


@element("py-atom-icon-warning-triangle", "Waarschuwingsdriehoek", "atom", "icon", 1, src="dranghek",
         variables=("colour",),
         notes="Light aqua warning triangle with exclamation mark (outline triangle, bar and dot as three paths) from the barrier banner "
               "(dranghekspandoek-dubbelzijdig_01.pdf, 346.8 x 302.7 mm there). Light aqua CMYK 51/1/11/0 (viewer #71CBDF) has no token and is kept as sampled. "
               "The A3 storing poster draws the same icon as a light aqua fill and a small navy outline version.")
def _(src):
    return crop(src, 1, printsrc.box_mm(70, 1055, 425, 1365), texts=False)
