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

import warnings
import math

masked_suppressed = False

class Generator():
    def __init__(self, part): # part name
        self.mirror = ""
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

    # mm, degrees
    def add_pad(self,
                name,
                x,
                y,
                xsize=None,
                ysize=None,
                diameter=None,
                masked = False,
                bottom = False,
                paste = True,
                drill = 0,
                mask_clearance = None,
                clearance = None,
                plated = True,
                thermal = None,
                layer=None,
                mirror = "",
                angle=0,
                shape="rect"):
        if masked:
            global masked_suppress
            if not masked_suppress:
                warnings.warn("masked option for pad {} ignored, not valid in gEDA/pcb\n"
                              "Future masked warnings suppressed".format(name))
                masked_suppress = True

        if mask_clearance == None:
            mask_clearance = self.mask_clearance
        if clearance == None:
            clearance = self.clearance

        flags = ""

        if 'cir' in shape:
            xsize = diameter
            ysize = diameter
        elif "round" in shape:
            pass
        else:
            flags = 'square'

        if not paste:
            if flags != "":
                flags += ", "
            flags += "nopaste"

        if layer and "B" in layer:
            if flags != "":
                flags += ", "
            flags += "onsolder"

        if not plated:
            if flags != "":
                flags += ", "
            flags += "hole"

        if "x" in mirror:
            x *= -1.0
        if "y" in mirror:
            y *= -1.0

        if drill > 0:
            self.fp += '\tPin[ {0:d}nm {1:d}nm {2:d}nm {3:d}nm {4:d}nm {5:d}nm '.format(
                *self.mm_to_geda(x, y, xsize, clearance*2, mask_clearance+xsize, drill))
        else:
            linewidth = min(ysize, xsize)
            linelength = abs(ysize - xsize)
            if ysize > xsize:
                # vertical pad
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
            self.fp += '\tPad[{0:d}nm {1:d}nm {2:d}nm {3:d}nm {4:d}nm {5:d}nm {6:d}nm '.format(
                *self.mm_to_geda(x1, y1, x2, y2, linewidth, self.clearance*2, self.mask_clearance+linewidth))
        self.fp += '"{name:s}" "{name:s}" "{flags:s}"]\n'.format(name=name, flags=flags)

    def silk_line(self, x1, y1, x2, y2, layer='F.SilkS', width = 0.15):
        if "x" in self.mirror:
            x1 *= -1.0
            x2 *= -1.0
        if "y" in self.mirror:
            y1 *= -1.0
            y2 *= -1.0
        self.fp += '\tElementLine [{0:d}nm {1:d}nm {2:d}nm {3:d}nm {4:d}nm]\n'.format(
            *self.mm_to_geda(x1, y1, x2, y2, width)
        )

    def _silk_arc(self, cx, cy, half_width, half_height, start, delta, width):
        self.fp += '\tElementArc [{0:d}nm {1:d}nm {2:d}nm {3:d}nm {start:d} {delta:d} {4:d}nm]\n'.format(
            *self.mm_to_geda(cx, cy, half_width, half_height, width),
            start=int(round(start)), delta=int(round(delta))
        )

    def silk_arc(self, x1, y1, x2, y2, angle, layer = 'F.SilkS', width = 0.15):
        # x1,y1 is the center of the circle that is the basis of the arc
	# x2,y2 is the starting point of the arc
        # angle is the clock wise length of the arc
        if "x" in self.mirror:
            x1 *= -1.0
            x2 *= -1.0
        if "y" in self.mirror:
            y1 *= -1.0
            y2 *= -1.0

        dx, dy = x2-x1, y2-y1

        # radius of the circle of which the arc is a part
        r = math.sqrt(dx*dx + dy*dy)
        # start angle
        start = math.degrees(math.atan2(dy, dx))
        self._silk_arc(x1, y1, r, r, start, angle, width)

    def silk_circle(self, x, y, radius, layer = 'F.SilkS', width = 0.15):
        if "x" in self.mirror:
            x *= -1.0
        if "y" in self.mirror:
            y *= -1.0
        self._silk_arc(x, y, radius, radius, 0, 360, width)

    def finish(self):
        self.fp += ")\n"
        return self.fp
