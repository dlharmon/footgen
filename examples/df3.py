#!/usr/bin/python
import footgen

for n in range(2,11):
    f = footgen.Footgen('DF3_{}'.format(n))
    f.sip(pitch=2.0, drill = 0.85, diameter = 1.5, pins = n, draw_silk = False)
    silky = 1.0 + n
    f.box_corners(1.0,silky,-4.0,-silky)
    f.finish()

for n in range(2,15):
    f = footgen.Footgen('DF3_SM_{}'.format(n))
    x0 = 2.0 * 0.5 * (n-1)
    for i in range(n):
        f.add_pad(name = i+1,
                  x = x0 + i*-2.0,
                  y = 4.45,
                  xsize = 1.2,
                  ysize = 2.6,
                  shape = 'rect')

    for i in [-1,1]:
        f.add_pad(name = str(n+1) if i==1 else str(n+2),
                  x = 0.5*(7.04 + n*2.0)*i,
                  y = 0,
                  xsize = 2.3,
                  ysize = 3.3,
                  shape = 'rect')
    x = 0.5*(4.74 + 2.0*n)
    y = -2.8
    f.silk_line(-x, y, x, y, width = 0.15)
    f.finish()
