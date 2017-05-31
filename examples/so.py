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

f = Footgen("1008")
f.so(pitch = 0.5, width = 1.1, pins = 2, padheight = 1.5, padwidth = 0.6)
f.finish()

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

f = Footgen("MSOP-8G")
f.so(pitch = 0.65, pins = 8, width = 3.2, padheight = 0.38, padwidth = 1.1)
f.silkbox(h=3.1, w = 2.5, arc=0.5)
f.thermal_pad(w=1.6, h=2.4, pin=9, copper_expansion=0.4, dots=[1,1], coverage=0.9)
f.via_array(columns=3, rows=7, pitch=1.05, pitchy = 0.5, size=0.2, pad=0.5, pin=9,
            mask_clearance = -0.1,
            outer_only=True)
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

# Murata DC - DC
f = Footgen("LXDC2HL")
f.so(pitch = 1.45, pins = 4, width = .5, padheight = 0.85, padwidth = 0.6)
f.silkbox(h=2.7, w = 2.2, arc=0.15)
f.finish()

# Skyworks MIS
f = Footgen("Skyworks_MIS")
f.so(pitch = 0.73, pins = 4, width = .5, padheight = 0.3, padwidth = 0.5)
f.finish()

# Anaren 0805
f = Footgen("anaren_0805_6")
f.so(pitch = 0.65, pins = 6, width = 0.76, padheight = 0.3, padwidth = 0.3)
f.silkbox(h=2.04, w = 1.29, arc=0.2)
f.finish()

# resonator 2.5x2 Murata
f = Footgen("resonator_2.5.2")
f.so(pitch = 1.0, pins = 6, width = 1.0, padheight = 0.5, padwidth = 0.6)
f.silkbox(h=2.5, w = 2.0, arc=0.4)
f.finish()

# Transformer
f = Footgen("MCL_DB1627")
f.so(pitch = 1.27, pins = 6, width = 2.02, padheight = 0.71, padwidth = 1.02)
f.silkbox(h=3.81, w = 1.5, arc=0.4)
f.finish()

# ARM JTAG header
f = Footgen("header_10x1.27")
f.soh(pitch = 1.27, width = 6.3-4.8, padwidth = 2.4, padheight = 0.76, pins = 10)
f.finish()

# Ublox NEO-M8T - requires moving some pins manually post generation
f = Footgen("NEO-M8")
f.so(pitch = 1.1, width = 12.2 - 1.8, padwidth = 2.0, padheight = 0.8, pins = 24)
f.silkbox(h=16.0, w = 12.2, arc=1.0)
f.finish()

# 5x7 mm 6 pin oscillator
f = Footgen("OSC_5x7_6")
f.so(pitch = 2.54, pins = 6, width = 2.54, padheight = 1.5, padwidth = 1.6)
f.silkbox(h=7, w = 1.8, arc=0.5)
f.finish()
