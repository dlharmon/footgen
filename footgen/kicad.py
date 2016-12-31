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

class Generator():
    def __init__(self, part, mask_margin = None, clearance = None, zone_connect=None): # part name
        self.part = part
        self.mirror = ""
        self.fp = "(module {} (layer F.Cu)\n".format(part)
        self.fp += "  (at 0 0)\n"
        if mask_margin:
            self.fp += "  (solder_mask_margin {})\n".format(mask_margin)
        if clearance:
            self.fp += "  (clearance {})\n".format(clearance)
        if zone_connect:
            self.fp += "  (zone_connect 2)\n"
        self.fp += "  (attr smd)"
        self.fp += "  (fp_text reference U1 (at 0 -1.27) (layer F.SilkS) (effects (font (size 0.7 0.7) (thickness 0.127))))\n"
        self.fp += "  (fp_text value value (at 0 1.27) (layer F.SilkS) hide (effects (font (size 0.7 0.7) (thickness 0.127))))\n"
        return
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
                plated = True,
                thermal = None,
                layer=None,
                mirror = "",
                angle=0,
                shape="rect"):
        if "x" in self.mirror:
            x *= -1.0
        if "y" in self.mirror:
            y *= -1.0
        if "cir" in shape:
            shape = "circle"
            xsize = diameter
            ysize = diameter
        if "round" in shape:
            shape = "oval"
        if angle != 0:
            atstring = "(at {:.6f} {:.6f} {:.6f})".format(x, y, angle)
        else:
            atstring = "(at {:.6f} {:.6f})".format(x, y)
        side = "B" if bottom else "F"
        padtype = "smd"
        if masked:
            layers = " (layers {0}.Cu)".format(side)
        elif not paste:
            layers = " (layers {0}.Cu {0}.Mask)".format(side)
        else:
            layers = " (layers {0}.Cu {0}.Mask {0}.Paste)".format(side)
        if layer != None:
            layers = " (layers {})".format(layer)
        drillstring = ""
        if drill > 0:
            drillstring = " (drill {:.6f})".format(drill)
            if plated:
                padtype = "thru_hole"
            else:
                padtype = "np_thru_hole"
            layers = " (layers *.Cu *.Mask)"
        self.fp += "  (pad {} {} {} {} (size {:.6f} {:.6f}){}".format(
            name, padtype, shape, atstring, xsize, ysize, drillstring)
        self.fp += layers
        if mask_clearance:
            self.fp += "(solder_mask_margin {:.6f})".format(mask_clearance)
        if thermal == 'solid':
            self.fp += "(zone_connect 2)"
        self.fp += ")\n"
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
    def silk_line(self, x1, y1, x2, y2, layer='F.SilkS', width = 0.15):
        if "x" in self.mirror:
            x1 *= -1.0
            x2 *= -1.0
        if "y" in self.mirror:
            y1 *= -1.0
            y2 *= -1.0
        self.fp += "  (fp_line (start {:.6f} {:.6f}) (end {:.6f} {:.6f}) (layer {}) (width {:.6f}))\n".format(
            x1, y1, x2, y2, layer, width)
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
        self.fp += "  (fp_arc (start {:.6f} {:.6f}) (end {:.6f} {:.6f}) (angle {:.6f}) (layer {}) (width {:.6f}))\n".format(
            x1, y1, x2, y2, angle, layer, width)
    def silk_circle(self, x, y, radius, layer = 'F.SilkS', width = 0.15):
        if "x" in self.mirror:
            x *= -1.0
        if "y" in self.mirror:
            y *= -1.0
        # DC ox oy fx fy w  DC Xcentre Ycentre Xpoint Ypoint Width Layer
        self.fp += "  (fp_circle (center {:.6f} {:.6f}) (end {:.6f} {:.6f}) (layer {}) (width {:.6f}))\n".format(
            x,y,x,y+radius,layer, width)
    def finish(self):
        self.fp += ")\n"
        return self.fp
