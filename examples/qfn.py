#!/usr/bin/python

from footgen import *

f = Footgen("QFN16_3x3")
f.qfn(pitch=0.5, pins=16, width=2.2, padheight=0.25, padwidth=0.66, silk_xsize=3.0)
f.add_pad(name='17', x=0, y=0, diameter=1.2, shape="circle", mask_clearance = 0.2)
f.add_pad(name='17', x=0, y=0, xsize=1.9, ysize=1.9, masked = True, paste = False)
f.via_array(columns=2, pitch=2*0.72, size=0.2, pad=0.46, pin = 17, mask_clearance = -0.1, outer_only = True)
f.finish()

f = Footgen("MCL_DQ1225")
f.qfn(pitch = 0.5, pins = 12, width = 2.2, padheight = 0.25, padwidth = 0.55, silk_xsize = 3.0)
f.thermal_pad(1.3, pin=13)
f.via_array(columns=2, pitch=0.8, size=0.2, pad=0.5, pin=13)
f.finish()

f = Footgen("QFN48_7x7")
f.qfn(pitch = 0.5, pins = 48, width = 6.2, padheight = 0.254, padwidth = 0.60, silk_xsize = 7.0)
f.thermal_pad(5.1, pin=49)
f.via_array(columns=4, pitch=1.4, pin=49, pad=0.5, size=0.2)
f.finish()

f = Footgen("QFN48_KSZ9031")
f.qfn(pitch = 0.5, pins = 48, width = 6.3, padheight = 0.25, padwidth = 0.6, silk_xsize = 7.0)
f.thermal_pad(3.5, pin=49, copper_expansion = 0.5)
f.via_array(columns=4, pitch=1.35, pin=49, pad=0.46, size=0.2, mask_clearance = -0.1, outer_only = True)
f.finish()

f = Footgen("QFN40_6x6")
f.qfn(pitch = 0.5, pins = 40, width = 5.2, padheight = 0.254, padwidth = 0.60, silk_xsize = 6.0)
f.thermal_pad(3.8, pin=41)
f.via_array(columns=4, pitch=1.25, pin=41, pad=0.5, size=0.2, outer_only=True)
f.finish()

f = Footgen("QFN64_9x9")
f.qfn(pitch = 0.5, pins = 64, width = 8.2, padheight = 0.254, padwidth = 0.60, silk_xsize = 9.0)
f.thermal_pad(6.0, pin=65, copper_expansion = 0.4)
f.via_array(columns=6, pitch=1.3, pin=65, pad=0.46, size=0.2, mask_clearance=-0.1, outer_only=True)
f.finish()

f = Footgen("QFN32_5x5")
f.qfn(pitch = 0.5, pins = 32, width = 4.15, padheight = 0.254, padwidth = 0.7, silk_xsize = 5.0)
f.thermal_pad(3.15, pin=33, copper_expansion = 0.3)
f.via_array(columns=6, pitch=0.65, size=0.2, pad=0.46, pin = 33, mask_clearance=-0.1, outer_only=True)
f.finish()

f = Footgen("QFN32_5x5_4V")
f.qfn(pitch = 0.5, pins = 32, width = 4.15, padheight = 0.254, padwidth = 0.7, silk_xsize = 5.0)
f.thermal_pad(3.15, pin=33, copper_expansion = 0.3)
f.via_array(columns=2, pitch=5*0.65, size=0.25, pad=0.5, pin = 33, mask_clearance=-0.1, outer_only=True)
f.finish()

f = Footgen("QFN32_5x5_12V")
f.qfn(pitch = 0.5, pins = 32, width = 4.15, padheight = 0.25, padwidth = 0.7, silk_xsize = 5.0)
f.thermal_pad(2.8, pin=33, copper_expansion = 0.5)
f.via_array(columns=4, pitch=1.1, size=0.2, pad=0.46, pin = 33, mask_clearance=-0.1, outer_only=True)
f.finish()

f = Footgen("QFN36_6x6")
f.qfn(pitch = 0.5, pins = 36, width = 4.65, padheight = 0.254, padwidth = 0.7, silk_xsize = 6.0)
f.thermal_pad(3.15, pin=37, copper_expansion = 0.3)
f.via_array(columns=6, pitch=0.65, size=0.2, pad=0.46, pin = 37, mask_clearance=-0.1, outer_only=True)
f.finish()

f = Footgen("QFN20_4x4")
f.qfn(pitch = 0.5, pins = 20, width = 3.0, padheight = 0.25, padwidth = 0.65, silk_xsize = 4.0)
f.thermal_pad(2.15, pin=21, copper_expansion = 0.2)
f.via_array(columns=3, pitch=1.05, size=0.2, pad=0.45, pin=21,
            mask_clearance=-0.1, outer_only=True)
f.finish()

f = Footgen("QFN24_4x4")
f.qfn(pitch = 0.5, pins = 24, width = 3.2, padheight = 0.25, padwidth = 0.6, silk_xsize = 4.0)
f.thermal_pad(2.6, pin=25)
f.via_array(columns=3, pitch=1.0, size=0.2, pad=0.5, pin=25)
f.finish()

# Dual pad QFN 24 - Analog Devices ADP2384
f = Footgen("CP-24-12")
f.qfn(pitch = 0.5, pins = 24, width = 3.2, padheight = 0.25, padwidth = 0.6, silk_xsize = 4.0)
f.thermal_pad(w=2.6, h=1.3, position=[0, -0.65], dots=[2,1], pin=25, coverage=0.6)
f.thermal_pad(w=2.6, h=0.85, position=[0, 0.875], dots=[2,1], pin=26, coverage=0.6)
f.via_array(columns=3, rows=1, pitch=1.0, size=0.2, pad=0.5, pin=25, position = [0,-0.65])
f.finish()

f = Footgen("QFN28_4x5")
f.qfn(pitch = 0.5, width=3.15, height=4.15, padheight=0.25, padwidth=0.7, pins = 28, pinswide = 6, silk_xsize = 4.0, silk_ysize = 5.0)
f.thermal_pad(w=2.6, h=3.6, pin=29, copper_expansion=0.1)
f.via_array(columns=5, rows=6, pitch=0.575, pitchy=0.665, size=0.2, pad=0.46, pin=29, mask_clearance=-0.1, outer_only=True)
f.finish()

f = Footgen("QFN20_5x5")
f.qfn(pitch = 0.65, pins = 20, width = 4.0, padheight = 0.35, padwidth = 0.7, silk_xsize = 5.0)
f.thermal_pad(3.15, pin=21)
f.via_array(columns=4, pitch=0.75, pin=21)
f.finish()

f = Footgen("PQFP48_7x7")
f.qfn(pitch = 0.5, pins = 48, width = 6.9, padheight = 0.3, padwidth = 1.5, silk_xsize = 7.0)
f.thermal_pad(6, pin=49, copper_expansion=0.3)
f.via_array(columns=5, pitch=1.2, size=0.3, pad=0.6, pin=49, mask_clearance = -0.1)
f.finish()

f = Footgen("qfn16_4x4")
f.qfn(pitch = 0.65, pins = 16, width = 3.1, padheight = 0.35, padwidth = 0.85, silk_xsize = 4.0)
f.thermal_pad(2.7, dots=[2,2])
f.via_array(columns=3, pitch=1.1, size=0.2, pad=0.5)
f.finish()

# Minicircuits MC1630-1
f = Footgen("MCL_MC1630-1")
f.so(pitch = 0.65, pins = 6, width = 1.2, padheight = 0.35, padwidth = 0.7)
f.thermal_pad(w=0.65, h=1.25, dots=[1,1], pin=7)
f.finish()

f = Footgen("LQFP48")
f.qfn(pitch = 0.5, pins = 48, width = 7.5, padheight = 0.25, padwidth = 0.9, silk_xsize = 7.0)
f.finish()

f = Footgen("LQFP64")
f.qfn(pitch = 0.5, pins = 64, width = 10.5, padheight = 0.25, padwidth = 0.9, silk_xsize = 10.0)
f.finish()

f = Footgen("VQFP100")
f.qfn(pitch = 0.5, pins = 100, width = 14.5, padheight = 0.25, padwidth = 0.9, silk_xsize = 14.0)
f.finish()
