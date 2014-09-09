#!/usr/bin/python
# footgen.py
# Copyright (C) 2005-2007 Darrell Harmon
# Generates footprints for PCB from text description
# The GPL applies only to the python scripts.
# the output of the program and the footprint definition files
# are public domain
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from footgen.generator import BaseGenerator

import warnings
import math
import itertools

nopaste_suppress = False
round_suppress = False

class Generator(BaseGenerator):
    def __init__(self, part): # part name
        self.options_list = [] # "cir" circle pad (BGA) "round" rounded corners "bottom" on bottom of board
        self.diameter = 1 # used for circular pads, mm
        self.width = 1 # pad x dimension or silk width
        self.height = 1 # pad y dimension
        self.drill = 0 # drill diameter
        self.angle = 0 # rotation - only kicad
        self.clearance = 0.2
        self.silkwidth = 0.15
        self.mask_clearance = 0.075
        self.part = part
        refdesy = 0
        refdesx = 0
        self.fp = 'Element["" "{part}" "" "" 1000 1000 {:d}nm {:d}nm 0 100 ""]\n(\n'.format(
            part=part, *self.mm_to_geda(refdesx, -1.0-refdesy)
        )

    def mm_to_geda(self, *mm):
        return (int(round(value * 1.0e6)) for value in mm)

    def _add_pin(self, x, y, name, flags):
        self.fp += '\tPin[ {0:d}nm {1:d}nm {2:d}nm {3:d}nm {4:d}nm {5:d}nm "{name:s}" "{name:s}" "{flags:s}"]\n'.format(
            *self.mm_to_geda(x, y, self.diameter, self.clearance*2,
                             self.mask_clearance+self.diameter, self.drill),
            name=name,flags=flags
        )

    def _add_pad(self, x, y, name, flags):
        linewidth = min(self.height,self.width)
        linelength = abs(self.height-self.width)

        if self.height > self.width:
            # vertcal pad
            x1 = x
            x2 = x
            y1 = y - linelength/2
            y2 = y + linelength/2
        else:
            # horizontal pad
            x1 = x - linelength/2
            x2 = x + linelength/2
            y1 = y
            y2 = y
        self.fp += '\tPad[{0:d}nm {1:d}nm {2:d}nm {3:d}nm {4:d}nm {5:d}nm {6:d}nm "{name:s}" "{name:s}" "{flags:s}"]\n'.format(
            *self.mm_to_geda(x1, y1, x2, y2, linewidth, self.clearance*2,
                             self.mask_clearance+linewidth),
            name=name, flags=flags
        )

    def add_pad(self, x, y, name):
        self._sanitize_options(name)

        if "nopaste" in self.options_list:
            global nopaste_suppress
            if not nopaste_suppress:
                warnings.warn("nopaste option for pad {} ignored, not valid in gEDA/pcb\n"
                              "Future nopaste warnings suppressed".format(name))
                nopaste_suppress = True

        if "round" in self.options_list:
            global round_suppress
            if not round_suppress:
                warnings.warn("round option for pad {} ignored, not valid in gEDA/pcb\n"
                              "Future round warnings suppressed".format(name))
                round_suppress = True

        flag_list = []
        if "circle" in self.options_list:
            pass
        elif "square" in self.options_list:
            flag_list.append("square")

        flags = ', '.join(itertools.chain(flag_list, self._unhandled_options()))

        if self.drill > 0:
            self._add_pin(x, y, name, flags)
        else:
            self._add_pad(x, y, name, flags)

    def silk_line(self, x1, y1, x2, y2):
        self.fp += '\tElementLine [{0:d}nm {1:d}nm {2:d}nm {3:d}nm {4:d}nm]\n'.format(
            *self.mm_to_geda(x1, y1, x2, y2, self.silkwidth)
        )

    def _silk_arc(self, cx, cy, half_width, half_height, start, delta):
        self.fp += '\tElementArc [{0:d}nm {1:d}nm {2:d}nm {3:d}nm {start:d} {delta:d} {4:d}nm]\n'.format(
            *self.mm_to_geda(cx, cy, half_width, half_height, self.silkwidth),
            start=int(round(start)), delta=int(round(delta))
        )

    def silk_arc(self, x1, y1, x2, y2, angle):
        dx, dy = x1-x2, y1-y2
        alpha = math.radians(angle)
        d = math.sqrt(dx*dx + dy*dy)

        # radius of the circle of which the arc is a part
        r = d / (2.0 * math.sin(math.pi - alpha/2))
        H = d / math.tan(math.pi - alpha/2)

        # center point
        cx, cy = (x1 + x2)/2.0 - H*dy/d, (x1 + y2)/2.0 + H*dx/d

        # start angle
        start = math.degrees(math.atan2(y1-cy, x1-cx))

        self._silk_arc(cx, cy, r, r, start, angle)

    def silk_circle(self, x, y, radius):
        self._silk_arc(x, y, radius, radius, 0, 360)

    def finish(self):
        self.fp += ")\n"
        return self.fp
