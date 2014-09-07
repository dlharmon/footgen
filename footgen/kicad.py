#!/usr/bin/python
# footgen.py
# Copyright (C) 2005-2013 Darrell Harmon
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

# Added dih patch from David Carr - 8/28/2005 Darrell Harmon

# 1/6/2007
# Bugfix from David Carr to correct row and col reversal in BGA omitballs
# Several improvements sent to me by Peter Baxendale, with some modification
# by DLH: Square pin 1 on all through hole, optional inside silkscreen on
# SO parts with diagonal corner for pin 1, to enable use silkstyle = "inside",
# disabled by default or use silkstyle = "none"

# 9/28/2008
# Added patch by David Carr to add silkstyle="corners" option on qfp
# set silkboxwidth and silkboxheigh if using this style

# 9/28/2008
# Added refdesx and refdesy attributes which allow the reference designator to be positioned as desired
# Previously the reference designator was located at the origin. This is still the default.

# 9/29/2008
# Allow negative numbers in footprint definition file

# 10/22/2008
# added "skew" option to SO
# take out debug print for expandedlist

# 2/9/2009 DLH
# allow exposed pads on SO parts
# added "rect" option
# if "rect" is set, it will create a rectangular exposed pad. It must be >= to the ep value.
# It sets the height, and is only available in so at this time.

# 2/24/2009 DLH
# Added support for silkboxwidth and silkboxheight to sip, dip

# 4/29/2009
# Applied bugfix patch for dih from Levente Kovacs
# Applied patch adding dihf (double row receptacle) from Levente Kovacs

# 20120731 Stephen Ecob
# Changed fundamental units from centimils to nanometers
# Changed flags from integers to strings (as per newer format)
# Changed a few hard coded distances from values such as
# 1000, 4000 or 3940 (centimils) to 1000000nm.  These hard
# coded distances are still ugly, but now at least they are
# metric ugly instead of imperial ugly

# 20120830 Larry Doolittle
# Add attribute "lefthand" to support both genders of BGA connectors
# Embed the filename in the file, helps when inspecting the resulting PCB layout file
# Deleted trailing spaces

from footgen.generator import BaseGenerator

import warnings

class Generator(BaseGenerator):
    def __init__(self, part): # part name
        self.options_list = [] # "circle" circle pad (BGA) "round" rounded corners "bottom" on bottom of board
        self.diameter = 1.0 # used for circular pads, mm
        self.width = 1.0 # pad x dimension or silk width
        self.height = 1.0 # pad y dimension
        self.drill = 0.0 # drill diameter
        self.angle = 0.0 # rotation - only kicad
        self.clearance = 0.2
        self.mask_clearance = False
        self.part = part
        self.silkwidth = 0.15
        self.mirror = ""
        self.silklayer = "F.SilkS"
        self.fp = "(module {} (layer F.Cu)\n".format(part)
        self.fp += "  (at 0 0)\n"
        self.fp += "  (descr DocString)\n"
        self.fp += "  (tags Keywords)\n"
        self.fp += "  (path 50705C0D)\n"
        self.fp += "  (solder_mask_margin 0)\n"
        self.fp += "  (clearance 0)\n"
        self.fp += "  (attr smd)"
        self.fp += "  (fp_text reference U1 (at 0 -1.27) (layer F.SilkS)\n"
        self.fp += "    (effects (font (size 0.7 0.7) (thickness 0.127)))\n"
        self.fp += "  )\n"
        self.fp += "  (fp_text value value (at 0 1.27) (layer F.SilkS) hide\n"
        self.fp += "    (effects (font (size 0.7 0.7) (thickness 0.127)))\n"
        self.fp += "  )\n"
        return
    # nm, degrees
    def add_pad(self, x, y, name, layer = None):
        self._sanitize_options(name)

        unhandled = self._unhandled_options()
        if unhandled:
            warnings.warn('kicad backend ingnoring unkown options "{}" for pad {}\n'.format(', '.join(unhandled), name))

        if "x" in self.mirror:
            x *= -1.0
        if "y" in self.mirror:
            y *= -1.0
        shape = "rect"
        if "circle" in self.options_list:
            shape = "circle"
            self.width = self.diameter
            self.height = self.diameter
        elif "round" in self.options_list:
            shape = "oval"
        if(self.angle != 0):
            atstring = "(at {:.6f} {:.6f} {:.6f})".format(x, y, self.angle)
        else:
            atstring = "(at {:.6f} {:.6f})".format(x, y)
        if layer != None:
            padtype = "smd"
            layers = "    (layers {})\n".format(layer)
        elif "masked" in self.options_list:
            padtype = "smd"
            if "bottom" in self.options_list:
                layers = "    (layers B.Cu)\n"
            else:
                layers = "    (layers F.Cu)\n"
        elif "nopaste" in self.options_list:
            padtype = "smd"
            if "bottom" in self.options_list:
                layers = "    (layers B.Cu B.Mask)\n"
            else:
                layers = "    (layers F.Cu F.Mask)\n"
        else:
            padtype = "smd"
            if "bottom" in self.options_list:
                layers = "    (layers B.Cu B.Mask B.Paste)\n"
            else:
                layers = "    (layers F.Cu F.Mask F.Paste)\n"
        drillstring = ""
        if self.drill > 0:
            drillstring = " (drill {:.6f})".format(self.drill)
            if"noplate" in self.options_list:
                padtype = "thru_hole"
            else:
                padtype = "np_thru_hole"
            layers = "    (layers *.Cu *.Mask)\n"
        self.fp += "  (pad {} {} {} {} (size {:.6f} {:.6f}){}\n".format(name, padtype, shape, atstring, self.width, self.height, drillstring)
        self.fp += layers
        if self.mask_clearance:
            self.fp += "(solder_mask_margin {:.6f})".format(self.mask_clearance)
        self.fp += "  )\n"
        return

    def add_polygon(self, points, layer="F.Cu", width = 0.0):
        polystring = "(fp_poly (pts\n"
        for p in points:
            if "x" in self.mirror:
                p[0] *= -1.0
            if "y" in self.mirror:
                p[1] *= -1.0
            polystring += "\t(xy {:.6f} {:.6f})\n".format(p[0], p[1])
        polystring += ") (layer {}) (width {:.6f}) )\n".format(layer, width)
        self.fp += polystring

    # draw silkscreen line
    def silk_line(self, x1, y1, x2, y2):
        if "x" in self.mirror:
            x1 *= -1.0
            x2 *= -1.0
        if "y" in self.mirror:
            y1 *= -1.0
            y2 *= -1.0
        self.fp += "  (fp_line (start {:.6f} {:.6f}) (end {:.6f} {:.6f}) (layer {}) (width {:.6f}))\n".format(x1, y1, x2, y2, self.silklayer, self.silkwidth)
    def silk_arc(self, x1, y1, x2, y2, angle):
        if "x" in self.mirror:
            x1 *= -1.0
            x2 *= -1.0
        if "y" in self.mirror:
            y1 *= -1.0
            y2 *= -1.0
        self.fp += "  (fp_arc (start {:.6f} {:.6f}) (end {:.6f} {:.6f}) (angle {:.6f}) (layer {}) (width {:.6f}))\n".format(x1, y1, x2, y2, angle, self.silklayer, self.silkwidth)
    def silk_circle(self, x, y, radius):
        if "x" in self.mirror:
            x *= -1.0
        if "y" in self.mirror:
            y *= -1.0
        # DC ox oy fx fy w  DC Xcentre Ycentre Xpoint Ypoint Width Layer
        self.fp += "  (fp_circle (center {:.6f} {:.6f}) (end {:.6f} {:.6f}) (layer {}) (width {:.6f}))\n".format(x,y,x,y+radius,self.silklayer, self.silkwidth)
    def finish(self):
        self.fp += ")\n"
        return self.fp
