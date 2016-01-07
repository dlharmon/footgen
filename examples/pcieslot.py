#!/usr/bin/python
import footgen

def pciecard(npins, name):
    f = footgen.Footgen(name)
    g = f.generator
    g.mask_clearance = 0.0 # mm
    g.clearance = 0.0 # mm
    x = -11.65 # mm
    for i in range(1,1+npins/2):
        odd = (i & 1) != 0
        y = 1.25 if odd else 3.25
        f.add_pad(name = "B"+str(i),
                  x = x,
                  y = y,
                  diameter = 1.1,
                  shape = "circle",
                  drill = 0.7)
        f.add_pad(name = "A"+str(i),
                  x = x,
                  y = -y,
                  diameter = 1.1,
                  shape = "circle",
                  drill = 0.7)
        if i == 11:
            x += 3.0 # mm, key
        else:
            x += 1.0 # mm
    for x in [0, 9.15 + (npins-36)*0.5]:
        f.add_pad(name = "x",
                  x = x,
                  y = 0,
                  diameter = 2.35,
                  shape = "circle",
                  plated = False,
                  masked = True,
                  drill = 2.35)

    for x in [-14.5, -14.5 + 7 + 0.5*npins]:
        g.silk_line(x, -3.7, x, 5.1)
    output_file = open(name + ".kicad_mod", "w")
    output_file.write(g.finish())
    output_file.close()

pciecard(36, "pciex1slot")
pciecard(64, "pciex4slot")
pciecard(98, "pciex8slot")
pciecard(164, "pciex16slot")
