#!/usr/bin/python

from footgen import *
    
f = Footgen("MCL_FV1206")
f.add_pad("1", x=-1.625, y=0.0, xsize=1.04, ysize=1.8)
f.add_pad("3", x=1.625, y=0.0, xsize=1.04, ysize=1.8)
f.add_pad("2", x=0.0, y=0.9275, xsize=0.61, ysize=1.245)
f.add_pad("2", x=0.0, y=-0.9275, xsize=0.61, ysize=1.245)
f.finish()
