#!/usr/bin/python
import footgen

f = footgen.Footgen("LQFP48")
f.pitch = 0.5
f.pins = 48
f.width = 7
f.padheight = 0.27
f.padwidth = 1.2
f.qfn()
f.silk_crop(7, pin1="circle")
f.finish()
    
f = footgen.Footgen("LP2")
f.pitch = 0.65
f.pins = 6
f.width = 1.31
f.padheight = 0.25
f.padwidth = 0.6
f.so()
f.thermal_pad(0.8, 1.4)
f.silkbox(2.1, circle=0.15, nosides=True)
f.via_array(columns=1, rows=2, pitch=0.9)
f.finish()

f = footgen.Footgen("LP3")
f.pitch = 0.5
f.pins = 16
f.width = 2.2
f.padheight = 0.254
f.padwidth = 0.66
f.qfn()
f.thermal_pad(1.8)
f.silk_crop(3.0)
f.via_array(columns=2, pitch=1.0)
f.finish()

f = footgen.Footgen("LC4B")
f.pitch = 0.5
f.pins = 24
f.width = 3.2
f.padheight = 0.254
f.padwidth = 0.66
f.qfn()
f.thermal_pad(2.6924)
f.silk_crop(4.0)
f.via_array(columns=3, pitch=0.86)
f.finish()

f = footgen.Footgen("LP5")
f.pitch = 0.5
f.pins = 32
f.width = 4.191
f.padheight = 0.254
f.padwidth = 0.61
f.qfn()
f.thermal_pad(3.5)
f.via_array(columns=4, pitch=0.86)
f.silk_crop(5.0, pin1="circle")
f.finish()

#def via_array(self, columns=None, rows=None, pitch = None, size = 0.3302, pad = 0.7, pin = None):
f = footgen.Footgen("LP6G")
f.pitch = 0.5
f.pins = 40
f.width = 5.41
f.padheight = 0.254
f.padwidth = 0.61
f.qfn()
f.thermal_pad(4.4)
f.via_array(columns=3, pitch=1.75)
f.silk_crop(6.0, pin1="circle")
f.finish()

f = footgen.Footgen("testDIP")
f.pitch = 2.54
f.drill = 30.0*footgen.mil
f.diameter = 55.0*footgen.mil
f.pins = 8
f.width = 0.3*footgen.inch
f.dip()
f.finish()

f = footgen.Footgen("HEADER_2x6_100mil")
f.pitch = 2.54
f.drill = 1.0
f.diameter = 1.6
f.pins = 12
f.width = 2.54
f.dih()
f.finish()

f = footgen.Footgen("testtab")
f.padheight = 5.08
f.tabheight = 11.43
f.tabwidth = 12.95
# distance from pads to tab pad
f.height = 2.16
# DDPAK3 specific
f.pitch = 2.54
f.pins = 3
f.padwidth = 1.35
f.tabbed()
f.finish()

f = footgen.Footgen("TO-252")
f.padheight = 1.3
f.padwidth = 1.7
f.tabheight = 5.7
f.tabwidth = 5.5
# distance from pads to tab pad
f.height = 2.74
f.pitch = 4.57
f.pins = 2
f.tabbed()
f.finish()
