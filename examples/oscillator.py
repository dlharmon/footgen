#!/usr/bin/python

from footgen import *

f = Footgen("Oscillator_5x3.2")
f.so(pitch = 2.49+1.35, pins = 4, width = 1.27, padheight = 1.35, padwidth = 1.27)
f.finish()

f = Footgen("osc_2.5x2")
f.so(pitch = 1.9, pins = 4, width = 0.5, padheight = 1.1, padwidth = 1.0)
f.finish()

f = Footgen("Crystek_CVHD")
f.so(pitch = 5.08, pins = 4, width = 4.83, padheight = 1.27, padwidth = 2.28)
f.finish()

# 1x1" 5 pin OCXO package
# need to delete pin 5, nename pin 6 to 5 after generation
f = Footgen("OCXO_1")
f.dip(pitch = 9.52, pins = 6, drill = 1.1, diameter = 2.0, width = 19.05, silkboxwidth = 25.4, silkboxheight = 25.4)
f.finish()
