#!/usr/bin/python

from footgen import *

pins = [14, 16, 20, 24]
height = [5.0, 5.0, 6.6, 7.80]

for i in range(len(pins)):
    f = Footgen("TSSOP-{}".format(pins[i]))
    f.so(pitch = 0.65, pins = pins[i],
         width = 5.0, padheight = 0.35, padwidth = 1.0)
    f.silkbox(h=height[i], w = 4.0, arc=0.5)
    f.finish()

f = Footgen("TSSOP-16EP")
f.so(pitch = 0.65, pins = 16, width = 5.0, padheight = 0.35, padwidth = 1.0)
f.silkbox(h=5.0, w = 4.0, arc=0.5)
f.thermal_pad(w=2.0, pin=17, copper_expansion=1.0, dots=[1,1], coverage=0.9)
f.via_array(columns=5, pitch=0.75, size=0.3, pad=0.7, pin=17, mask_clearance = -0.1, outer_only=True)
f.finish()
