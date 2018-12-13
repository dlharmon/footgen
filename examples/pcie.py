#!/usr/bin/python
import footgen

def pciecard(npins, name):
    f = footgen.Footgen(name)
    g = f.generator
    g.mask_clearance = 0.0 # mm
    g.clearance = 0.0 # mm
    x = 45.65 # mm
    y = -3.5 # mm
    for i in range(1,1+npins/2):
        f.add_pad(name = "B"+str(i),
                  x = x,
                  y = y,
                  xsize = 0.7, # mm
                  ysize = 4.2, # mm
                  paste = False)
        f.add_pad(name = "A"+str(i),
                  x = x,
                  y = y,
                  xsize = 0.7, # mm
                  ysize = 4.2, # mm
                  paste = False,
                  bottom = True)
        if i == 11:
            x += 3.0 # mm, key
        else:
            x += 1.0 # mm
    g.silk_line(0.0, -4.5, 15.0, -4.5, layer='Edge.Cuts', width=0.1)
    g.silk_line(15.0, -4.5, 15.0, -12.75, layer='Edge.Cuts', width=0.1)
    g.silk_line(15.0, -12.75, 33.35, -12.75, layer='Edge.Cuts', width=0.1)
    g.silk_line(33.35, -12.75, 33.35, -4.5, layer='Edge.Cuts', width=0.1)
    g.silk_line(33.35, -4.5, 41.35, -4.5, layer='Edge.Cuts', width=0.1) # pci block lower edge
    g.silk_line(41.35, -4.5, 41.35, -10.925, layer='Edge.Cuts', width=0.1)
    g.silk_arc(43.175, -10.925, 41.35, -10.925, 180, layer='Edge.Cuts', width=0.1)
    g.silk_line(45.0, -10.925, 45.0, -0.7, layer='Edge.Cuts', width=0.1)
    g.silk_line(45.7, 0, 45.0, -0.7, layer='Edge.Cuts', width=0.1) # diagonal at 1
    g.silk_line(45.7, 0, 56.2 - 0.7, 0, layer='Edge.Cuts', width=0.1) # lower edge contacts 1 - 11
    g.silk_line(56.2 - 0.7, 0, 56.2, -0.7, layer='Edge.Cuts', width=0.1) # diagonal at 11
    g.silk_line(56.2, -0.7, 56.2, -8.0, layer='Edge.Cuts', width=0.1)
    g.silk_arc(57.15, -8.0, 56.2, -8.0, 180, layer='Edge.Cuts', width=0.1)
    g.silk_line(58.1, -8.0, 58.1, -0.7, layer='Edge.Cuts', width=0.1)
    g.silk_line(58.1 + 0.7, 0, 58.1, -0.7, layer='Edge.Cuts', width=0.1) # diagonal at 12
    cardedge_endx = 65.3 + 0.5*(npins-36)
    g.silk_line(58.1 + 0.7, 0.0, cardedge_endx - 0.7, 0.0, layer='Edge.Cuts', width=0.1) # lower edge 2nd contacts
    g.silk_line(cardedge_endx -0.7, 0.0, cardedge_endx, -0.7, layer='Edge.Cuts', width=0.1)
    g.silk_line(cardedge_endx, -0.7, cardedge_endx, -13.0, layer='Edge.Cuts', width=0.1)
    f.finish()

pciecard(36, "pciex1fingers")
pciecard(64, "pciex4fingers")
pciecard(98, "pciex8fingers")
pciecard(164, "pciex16fingers")
