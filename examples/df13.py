#!/usr/bin/python
import footgen
mm = 1

for n in range(2,10):
    f = footgen.Footgen('DF13_SM_{}'.format(n))
    x0 = 1.25*mm * 0.5 * (n-1)
    for i in range(n):
        f.add_pad(name = i+1,
                  x = x0 + i*-1.25*mm,
                  y = 2.4-0.9,
                  xsize = 0.7*mm,
                  ysize = 1.8*mm,
                  shape = 'rect')

    for i in [-1,1]:
        f.add_pad(name = 'GND',
                  x = 0.5*(3.45 + n*1.25)*i,
                  y = -2.4 + 1.1,
                  xsize = 1.6*mm,
                  ysize = 2.2*mm,
                  shape = 'rect')
    x = 0.5*(3.15*mm + 1.25*mm*n)
    y = -3
    f.silk_line(-x, y, x, y, width = 0.15*mm)
    f.finish()

for n in [10]:
    f = footgen.Footgen('DF13_DR_SM_{}'.format(n))
    f.generator.mirror = 'x'
    f.soh(pitch = 1.25, width = 4.3, padwidth = 1.7, padheight = 0.7, pins = 10)
    for i in [-1,1]:
        f.add_pad(name = 'GND',
                  y = i*(5.35 + (n-10)*0.25*1.25),
                  x = 0,
                  xsize = 2.0,
                  ysize = 2.2,
                  shape = 'rect')
    for i in [-1, 1]:
        for j in [-1, 1]:
            x = 2.75
            y = 0.5*(12.1 + (n-10)*0.5*1.25)
            f.silk_line(x*i, y*j, (x - 0.75)*i, y*j, width = 0.15*mm)
            f.silk_line(x*i, y*j, x*i, (y-1.75)*j, width = 0.15*mm)

    f.finish()
