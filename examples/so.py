#!/usr/bin/python

from footgen import *

#f = Footgen("LP2")
#f.pitch = 0.65
#f.pins = 6
#f.width = 1.31
#f.padheight = 0.25
#f.padwidth = 0.6
#f.so()
#f.thermal_pad(0.8, 1.4, dotpitch=0.5)
#f.silkbox(2.1, circle=0.15, nosides=True)
#f.via_array(columns=1, rows=2, pitch=0.9)
#f.finish()

f = Footgen("0804_8")
f.so(pitch = 0.5, width = 0.5, pins = 8, padheight = 0.3, padwidth = 0.4)
f.finish()

f = Footgen("LLA21")
f.so(pitch = 0.5, width = 0.6, pins = 8, padheight = 0.25, padwidth = 0.5)
f.finish()

f = Footgen("SO-8")
f.so(pitch = 1.27, width = 3.66, pins = 8, padheight = 0.5, padwidth = 1.4)
f.silkbox(h=5.0, w = 3.66-0.75, arc=0.5)
f.finish()

f = Footgen("SO-16")
f.so(pitch = 1.27, pins = 16, width = 3.9, padheight = 0.5, padwidth = 1.2)
f.silkbox(h=10.0, w = 3.9-0.75, arc=0.5)
f.finish()

f = Footgen("SO-8W")
f.so(pitch = 1.27, pins = 8, width = 5.4, padheight = 0.5, padwidth = 1.4)
f.silkbox(h=5.0, w = 5.4-0.75, arc=0.5)
f.finish()

f = Footgen("SOT23-6")
f.so(pitch = 0.95, pins = 6, width = 1.7, padheight = 0.55, padwidth = 1.0)
f.silkbox(h=3.0, w = 4.2, arc=0.5)
f.finish()

f = Footgen("SOT23-8")
f.so(pitch = 0.65, pins = 8, width = 1.7, padheight = 0.38, padwidth = 0.7)
f.silkbox(h=3.0, w = 1.2, arc=0.3)
f.finish()

f = Footgen("SC70-6")
f.so(pitch = 0.65, pins = 6, width = 1.4, padheight = 0.4, padwidth = 0.5)
f.silkbox(h=2.2, w = 2.9, arc=0.4)
f.finish()

# HMC213AMS8E
f = Footgen("MSOP-8")
f.so(pitch = 0.65, pins = 8, width = 3.2, padheight = 0.38, padwidth = 1.1)
f.silkbox(h=3.1, w = 2.5, arc=0.5)
f.finish()

f = Footgen("FPC40")
f.so(pitch = 0.5, pins = 80, width = 3.2, padheight = 0.3, padwidth = 1.2)
f.finish()

f = Footgen("FPC6")
f.so(pitch = 1.0, pins = 12, width = 3.2, padheight = 0.6, padwidth = 1.9)
f.finish()

f = Footgen("VSSOP-8")
f.so(pitch = 0.5, pins = 8, width = 2.6, padheight = 0.25, padwidth = 0.4)
f.silkbox(h=2.1, w = 2.1, arc=0.4)
f.finish()

f = Footgen("VSSOP-10")
f.so(pitch = 0.5, pins = 10, width = 3.6, padheight = 0.25, padwidth = 0.8)
f.silkbox(h=3.0, w = 3.0, arc=0.5)
f.finish()

# Bourns ethernet transformer
f = Footgen("PT61017")
f.so(pitch = 1.27, pins = 16, width = 7.1, padheight = 0.75, padwidth = 1.7)
f.silkbox(h=12.7, w = 6.9, arc=0.5)
f.finish()

# Murata DC - DC
f = Footgen("LXDC2HL")
f.so(pitch = 1.45, pins = 4, width = .5, padheight = 0.85, padwidth = 0.6)
f.silkbox(h=2.7, w = 2.2, arc=0.15)
f.finish()

# resonator 2.5x2 Murata
f = Footgen("resonator_2.5.2")
f.so(pitch = 1.0, pins = 6, width = 1.0, padheight = 0.5, padwidth = 0.6)
f.silkbox(h=2.5, w = 2.0, arc=0.4)
f.finish()

# HMC439
f = Footgen("QSOP16G")
f.so(pitch = 0.65, pins = 16, width = 4.5, padheight = 0.35, padwidth = 1.0)
f.silkbox(h=5, w=3.9, arc=0.4)
f.thermal_pad(w=1.7, h=2.3, pin=17, copper_expansion=0.8)
f.via_array(columns=5, rows=6, pitch=0.6, pitchy=0.6, size=0.2, pad=0.46, pin=17, mask_clearance=-0.1, outer_only=True)

f.finish()
