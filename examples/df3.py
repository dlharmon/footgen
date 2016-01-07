#!/usr/bin/python
import footgen

for n in range(2,11):
    f = footgen.Footgen('DF3_{}'.format(n))
    f.sip(pitch=2.0, drill = 0.85, diameter = 1.5, pins = n, draw_silk = False)
    silky = 1.0 + n
    f.box_corners(1.0,silky,-4.0,-silky)
    f.finish()
