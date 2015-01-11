#!/usr/bin/python
import footgen

f = footgen.Footgen("r_th")
f.pitch = 20.0
f.drill = 0.8
f.pins = 2
f.diameter = 1.2
f.sip(pin1shape="circle", draw_silk=False)
f.silkbox(w=2.0, h=16.0, notch=None, silkwidth=0.155)
f.finish()

f = footgen.Footgen("c_elec")
f.pitch = 5.0
f.drill = 1.0
f.pins = 2
f.diameter = 1.6
f.sip(pin1shape="square", draw_silk=False)
f.generator.silk_circle(0,0, 10.0/2)
f.finish()
