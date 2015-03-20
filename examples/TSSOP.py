#!/usr/bin/python

from footgen import *

pins = [14,16,20]
height = [5,5,6.6]

for i in range(len(pins)):
    f = Footgen("TSSOP-{}".format(pins[i]))
    f.so(pitch = 0.65, pins = pins[i],
         width = 5.0, padheight = 0.35, padwidth = 1.0)
    f.silkbox(h=height[i], w = 4.0, arc=0.5)
    f.finish()
