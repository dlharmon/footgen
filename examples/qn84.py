#!/usr/bin/python

from footgen import *

f = Footgen("QN84")
f.qfn(pitch=0.5, pins=48, width=6.2, padheight=0.25, padwidth=0.5, silk_xsize=7.0, prefix = 'A')
f.qfn(pitch=0.5, pins=36, width=4.9, padheight=0.25, padwidth=0.4, prefix = 'B')
f.thermal_pad(2.5, pin='G')
f.via_array(columns=2, pitch=2.0, size=0.2, pad=0.5, pin = 'G')
f.finish()
