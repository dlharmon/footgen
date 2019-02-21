#!/usr/bin/python3
import footgen

def fpc_tail(npins, name):
    f = footgen.Footgen(name)
    g = f.generator
    g.mask_clearance = 0.0 # mm
    g.clearance = 0.0 # mm
    pitch = 0.3 # mm
    # 0,0 is front, center
    centerpin = (npins+1) // 2
    for i in range(1, npins+1)[::2]: # odd pin numbers
        f.add_pad(name = str(i),
                  x = pitch * (i-centerpin),
                  y = -0.65,
                  xsize = 0.3,
                  ysize = 0.7,
                  paste = False,
                  shape='oval'
        )
    for i in range(2, npins)[::2]: # even pin numbers
        f.add_pad(name = str(i),
                  x = pitch * (i-centerpin),
                  y = -1.5,
                  xsize = 0.3, # mm
                  ysize = 0.9, # mm
                  paste = False,
                  shape='oval'
        )

    width = (1 + npins) * 0.3
    x = 0.5*width - 0.2
    g.silk_line(-x, 0, x, 0, layer='Edge.Cuts', width=0.1)
    g.silk_arc(-x, -0.2, -x, 0, 90, layer='Edge.Cuts', width=0.1)
    g.silk_arc(x, -0.2, x, 0, -90, layer='Edge.Cuts', width=0.1)
    x += 0.2
    g.silk_line(-x, -0.2, -x, -2.5, layer='Edge.Cuts', width=0.1)
    g.silk_line(x, -0.2, x, -2.5, layer='Edge.Cuts', width=0.1)
    g.add_polygon(points=[[-x,0],[-x,-2.5],[x,-2.5],[x,0]], layer='F.Mask')
    f.finish()

def fpc_socket(npins, name):
    f = footgen.Footgen(name)
    g = f.generator
    g.mask_clearance = 0.0 # mm
    g.clearance = 0.0 # mm
    pitch = 0.3 # mm
    # 0,0 is front, center
    centerpin = (npins+1) // 2
    for i in range(1, npins+1)[::2]: # odd pin numbers
        f.add_pad(name = str(i),
                  x = pitch * (i-centerpin),
                  y = 1.4,
                  xsize = 0.3,
                  ysize = 0.8
        )
    for i in range(2, npins)[::2]: # even pin numbers
        f.add_pad(name = str(i),
                  x = pitch * (i-centerpin),
                  y = -1.8 + 0.65/2,
                  xsize = 0.3,
                  ysize = 0.65
        )
    x = pitch * (1-centerpin) - 0.7
    for (x, n) in [(x, npins+1), (-x,npins+2)]:
        f.add_pad(name = str(n),
                  x = x,
                  y = 1.8 - (0.95/2 + 0.2),
                  xsize = 0.4,
                  ysize = 0.95
        )
    x += 0.2
    for x in [-x,x]:
        g.silk_line(x, 0.5, x, -1.1, width=0.1)
    f.finish()

for n in [13, 15, 21, 25, 31, 33, 39, 45]:
    fpc_tail(n, "fpc_0.3_{}_tail".format(n))
    fpc_socket(n, "fpc_0.3_{}_socket".format(n))
