#!/usr/bin/python

from footgen import *

f = Footgen("MCL_HV1195")
f.so(pitch = 1.27, pins = 8, width = 3.01, padheight = 0.76, padwidth = 1.52)
f.silkbox(h=5.08, w=4.57, arc=0.5)
f.finish()
