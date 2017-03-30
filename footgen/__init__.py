#!/usr/bin/python
# footgen.py
# Copyright (C) 2005-2016 Darrell Harmon
# Copyright (C) 2016 Levente Kovacs
# Generates footprints for PCB from text description
# The GPL applies only to the python scripts.
# the output of the program and the footprint definition files
# are public domain

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Patches and bug reports to darrell@dlharmon.com

import footgen.geda as geda
import footgen.kicad as kicad

import math

class Footgen(object):
    def __init__(self, name=None, output_format="kicad"):
        if "geda" in output_format:
            self.generator = geda.Generator(name)
            self.name = name + ".fp"
        else:
            self.generator = kicad.Generator(name)
            self.name = name + ".kicad_mod"
        self.add_pad = self.generator.add_pad
        self.silk_line = self.generator.silk_line

    def finish(self):
        fp = self.generator.finish()
        with open(self.name, "w") as f:
            f.write(fp)

    def thermal_pad(self, w, h=None, position = [0,0], coverage = 0.5, dots=[2,2], pin=None, copper_expansion=0):
        """ draw a thermal pad """
        if not h:
            h = w
        mask_clearance = -1*copper_expansion if copper_expansion else None
        self.add_pad(name = str(pin),
                     x = position[0],
                     y = position[1],
                     xsize = w + 2*copper_expansion,
                     ysize = h + 2*copper_expansion,
                     mask_clearance = mask_clearance,
                     paste = False
        )
        dotsizex = w/dots[0]
        dotsizey = h/dots[1]
        scale = math.sqrt(coverage)
        offsetx = dotsizex*(dots[0]-1)*-0.5
        offsety = dotsizey*(dots[1]-1)*-0.5
        for x in range(dots[0]):
            for y in range(dots[1]):
                self.add_pad(name = str(pin),
                             x = position[0] + x*dotsizex + offsetx,
                             y = position[1] + y*dotsizey + offsety,
                             xsize = dotsizex*scale,
                             ysize = dotsizey*scale)

    def via_array(self,
                  columns=None,
                  rows=None,
                  pitch = 1.0,
                  size = 0.3302,
                  pad = 0.7,
                  pin = None,
                  mask_clearance = None,
                  thermal='solid',
                  pitchy = None,
                  outer_only=False,
                  position = [0,0]):
        if not rows:
            rows = columns
        if not pitchy:
            pitchy = pitch
        for x in range(columns):
            for y in range(rows):
                if outer_only and (0 < x < columns - 1) and (0 < y < rows - 1):
                    continue
                self.add_pad(name = str(pin),
                             x = position[0] + (x-(columns-1)*0.5)*pitch,
                             y = position[1] + (y-(rows-1)*0.5)*pitchy,
                             diameter = pad,
                             mask_clearance = mask_clearance,
                             shape = "circle",
                             thermal=thermal,
                             drill = size
                         )

    def sm_pads(self,
                pitch = 0,
                width = None,
                height = None,
                pinswide = 0,
                pinshigh = 0,
                padwidth = 1,
                padheight = 1,
                square = True,
                silk_xsize = None,
                silk_ysize = None,
                silkwidth = 0.155,
                silk_pin1 = 'circle',
                prefix = ''):
        """Create pads for a dual or quad SM package.
        """

        left_x = -0.5*(width+padwidth)

        if pinshigh:
            rowlen = pitch * (pinshigh - 1)
            x = left_x
            y = 0 - rowlen*0.5
            for padnum in range (1, 1+pinshigh):
                self.add_pad(name = prefix+str(padnum),
                             x = x,
                             y = y,
                             xsize = padwidth,
                             ysize = padheight,
                             shape = 'rect' if square else 'oval')
                y += pitch
            x = 0 - left_x
            y = rowlen*0.5
            for padnum in range (pinshigh + pinswide + 1,
                                 2*pinshigh + pinswide + 1):
                self.add_pad(name = prefix+str(padnum),
                             x = x,
                             y = y,
                             xsize = padwidth,
                             ysize = padheight,
                             shape = 'rect' if square else 'oval')
                y -= pitch
        if pinswide:
            rowlen = pitch * (pinswide - 1)
            x = 0 - rowlen*0.5
            y = (height+padwidth)*0.5
            for padnum in range (pinshigh+1, pinshigh+1+pinswide):
                self.add_pad(prefix+str(padnum),
                             x = x,
                             y = y,
                             xsize = padheight,
                             ysize = padwidth,
                             shape = 'rect' if square else 'oval')
                x += pitch
            x = rowlen*0.5
            y = -0.5*(height+padwidth)
            for padnum in range (2*pinshigh+pinswide+1,
                                 2*pinshigh+pinswide+1+pinswide):
                self.add_pad(prefix+str(padnum),
                             x = x,
                             y = y,
                             xsize = padheight,
                             ysize = padwidth,
                             shape = 'rect' if square else 'oval')
                x -= pitch

        if not silk_xsize:
            return
        x_stop = 0.5*pitch*(pinswide-1) + .5*padheight + 2*silkwidth
        y_stop = 0.5*pitch*(pinshigh-1) + .5*padheight + 2*silkwidth
        if not silk_ysize:
            silk_ysize = silk_xsize
        x = 0.5*silk_xsize
        y = 0.5*silk_ysize
        croplength = 0.25
        if "circle" in silk_pin1:
            self.generator.silk_circle(
                -x-croplength,-y-croplength, croplength, width = silkwidth)
        else: # tick
            self.silk_line(
                -x, -y, -0.5*w-croplength, -0.5*h-croplength,
                width = silkwidth)
        self.silk_line(-x, -y, -x, -y_stop, width = silkwidth)
        self.silk_line(-x, -y, -x_stop, -y, width = silkwidth)
        self.silk_line(-x,  y, -x, y_stop, width = silkwidth)
        self.silk_line(-x,  y, -x_stop, y, width = silkwidth)
        self.silk_line( x, -y, x_stop, -y, width = silkwidth)
        self.silk_line( x, -y, x, -y_stop, width = silkwidth)
        self.silk_line( x,  y, x_stop, y, width = silkwidth)
        self.silk_line( x,  y, x, y_stop, width = silkwidth)

    def qfn(self,
            pitch = 0,
            width = 0,
            height = 0,
            padheight = 1,
            padwidth = 1,
            pins = 0,
            pinswide = 0,
            square = True,
            silk_xsize = None,
            silk_ysize = None,
            silkwidth = 0.155,
            silk_pin1 = 'circle',
            prefix=''):
        """
        Generate pads for a QFN or QFP type package
        arguments:
        pitch - pad pitch
        width - space between inside edges of pads in x
        height - (optional, defaults to width if 0) space between pads in y
        padheight -
        padwidth -
        pins - number of pins on part
        pinswide - (optional, defaults to pins/4 if 0) number of pins across
        top and bottom
        square - True: use square pads, False: use rounded pads
        prefix - prefix for pin names
        """
        if pinswide == 0:
            pinswide = pins/4
        if height == 0:
            height = width

        self.sm_pads(pitch = pitch,
                     width = width,
                     height = height,
                     pinswide = pinswide,
                     pinshigh = pins/2 - pinswide,
                     padwidth = padwidth,
                     padheight = padheight,
                     square = square,
                     silk_xsize = silk_xsize,
                     silk_ysize = silk_ysize,
                     silkwidth = 0.155,
                     silk_pin1 = 'circle',
                     prefix = prefix)

    def so(self,
           pitch = 0,
           width = 0,
           height = 0,
           pins = 0,
           padwidth = 1,
           padheight = 1,
           square=True):
        """ create a dual row surface mount footprint uses pins, padwidth, padheight, pitch """
        if pins % 2:
            raise Exception("Error, number of pins must be even")
        self.sm_pads(pitch = pitch,
                     width = width,
                     height = height,
                     pinswide = 0,
                     pinshigh = pins/2,
                     padwidth = padwidth,
                     padheight = padheight,
                     square = square)

    def soh(self, pitch = 0, width = 0, padwidth = 1, padheight = 1, pins = 0):
        """ create a dual row surface mount header """
        if pins % 2:
            raise Exception("Error, number of pins must be even")
        left_x = -0.5*(width+padwidth)
        # left going down
        rowlen = pitch * (pins/2 - 1)
        y = rowlen*-0.5
        for padnum in range (pins/2):
            self.add_pad(name = str(1+2*padnum),
                         x = left_x,
                         y = y,
                         xsize = padwidth,
                         ysize = padheight)
            self.add_pad(name = str(2+2*padnum),
                         x = -1.0*left_x,
                         y = y,
                         xsize = padwidth,
                         ysize = padheight)
            y += pitch

    def twopad(self, width, padwidth, padheight):
        """generate a two pad part, typically used for passives such
        as 0402, 0805, etc uses parameters width, padwidth, padheight
        """
        self.sm_pads(pitch = 1,
                     width = width,
                     height = 1,
                     pinswide = 0,
                     pinshigh = 1,
                     padwidth = padwidth,
                     padheight = padheight)

    def tabbed(self, pitch, pins, padwidth, padheight, tabwidth, tabheight, height):
        """ generate a part with a tab such as SOT-223 """
        totalheight = height+tabheight+padheight
        totalwidth = max(tabwidth, (pins-1)*pitch+padwidth)
        taby = -(totalheight-tabheight)*0.5
        padsy = -(padheight - totalheight)*0.5
        rowlen = pitch * (pins - 1)
        x = 0 - rowlen*0.5
        y = padsy
        for padnum in range (1, 1+pins):
            self.add_pad(name = str(padnum),
                         x = x,
                         y = y,
                         xsize = padwidth,
                         ysize = padheight)
            x += pitch
        self.add_pad(name = str(pins+1),
                     x = 0,
                     y = taby,
                     xsize = tabwidth,
                     ysize = tabheight)

    def dip(self,
            pitch,
            pins,
            drill,
            diameter,
            width,
            pin1shape="square",
            draw_silk=True,
            silkboxwidth = 0,
            silkboxheight = 0):
        """ DIP and headers, set width to 0 and pincount to 2x the desired for SIP"""
        y = -(pins*0.5-1.0)*pitch*0.5
        x = width*-0.5
        shape = 'rect' if pin1shape=='square' else 'circle'
        for pinnum in range (1,1+pins/2):
            self.add_pad(name = str(pinnum),
                         x = x,
                         y = y,
                         xsize = diameter,
                         ysize = diameter,
                         diameter = diameter,
                         drill = drill,
                         shape = shape)
            shape = 'circle'
            y += pitch
        y -= pitch
        x *= -1
        if width != 0:
            for pinnum in range (1+pins/2, pins+1):
                self.add_pad(name = str(pinnum),
                             x = x,
                             y = y,
                             drill = drill,
                             diameter = diameter,
                             shape = 'circle')
                y -= pitch
        if draw_silk == False:
            return
        silky = max(pins*pitch*0.25,silkboxheight*0.5)
        silkx = max((width+pitch)*0.5,silkboxwidth*0.5)
        self.box_corners(silkx,silky,-silkx,-silky)
        self.box_corners(-silkx,-silky,-silkx+pitch,-silky+pitch)

    def dih(self,
            pitch,
            pins,
            width,
            drill,
            diameter,
            silkboxwidth = 0,
            silkboxheight = 0,
            pin1shape="rect",
            draw_silk=True):
        """ like DIP, but numbered across and then down instead of counterclockwise """
        y = -(pins*0.5-1.0)*pitch*0.5
        x = width*0.5
        for pinnum in range (1,1+pins,2):
            self.add_pad(name = str(pinnum),
                         x = -x,
                         y = y,
                         diameter = diameter,
                         xsize = diameter,
                         ysize = diameter,
                         drill = drill,
                         shape = pin1shape if pinnum == 1 else 'circle')
            y += pitch
        if width != 0:
            y = -(pins/2-1)*pitch*0.5
            for pinnum in range (2,1+pins,2):
                self.add_pad(name = str(pinnum),
                             x = x,
                             y = y,
                             diameter = diameter,
                             xsize = diameter,
                             ysize = diameter,
                             drill = drill,
                             shape = 'circle')
                y += pitch
        if draw_silk == False:
            return
        silky = max(pins*pitch*0.25,silkboxheight*0.5)
        silkx = max((width+pitch)*0.5,silkboxwidth*0.5)
        self.box_corners(silkx,silky,-silkx,-silky)
        self.box_corners(-silkx,-silky,-silkx+pitch,-silky+pitch)

    def dihf(self,
            pitch,
            pins,
            width,
            drill,
            diameter,
            silkboxwidth = 0,
            silkboxheight = 0,
            pin1shape="rect",
            draw_silk=True):
        """ like DIP, but numbered across and then down instead of counterclockwise """
        y = -(pins*0.5-1.0)*pitch*0.5
        x = width*0.5
        for pinnum in range (1,1+pins,2):
            self.add_pad(name = str(pinnum),
                         x = x,
                         y = y,
                         diameter = diameter,
                         xsize = diameter,
                         ysize = diameter,
                         drill = drill,
                         shape = pin1shape if pinnum == 1 else 'circle')
            y += pitch
        if width != 0:
            y = -(pins/2-1)*pitch*0.5
            for pinnum in range (2,1+pins,2):
                self.add_pad(name = str(pinnum),
                         x = -x,
                         y = y,
                         diameter = diameter,
                         xsize = diameter,
                         ysize = diameter,
                         drill = drill,
                         shape = 'circle')
                y += pitch
        if draw_silk == False:
            return
        silky = max(pins*pitch*0.25,silkboxheight*0.5)
        silkx = max((width+pitch)*0.5,silkboxwidth*0.5)
        self.box_corners(silkx,silky,-silkx,-silky)
        self.box_corners(silkx,-silky,silkx-pitch,-silky+pitch)

    def sip(self, pitch, pins, drill, diameter, silkboxwidth=0, silkboxheight=0, pin1shape="square", draw_silk=True):
        """ generates a single in line through hole footprint """
        self.dip(pitch = pitch,
                 pins = pins*2,
                 width = 0,
                 drill = drill,
                 diameter = diameter,
                 silkboxwidth = silkboxwidth,
                 silkboxheight = silkboxheight,
                 pin1shape=pin1shape,
                 draw_silk=draw_silk)

    # BGA row names
    rowname = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K',
               'L', 'M', 'N', 'P', 'R', 'T', 'U', 'V', 'W', 'Y',
               'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AJ', 'AK',
               'AL', 'AM', 'AN', 'AP', 'AR', 'AT', 'AU', 'AV', 'AW', 'AY',
               'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BJ', 'BK',
               'BL', 'BM', 'BN', 'BP', 'BR', 'BT', 'BU', 'BV', 'BW', 'BY',
               'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CJ', 'CK',
               'CL', 'CM', 'CN', 'CP', 'CR', 'CT', 'CU', 'CV', 'CW', 'CY']

    # generate ball name from row and column (for BGA)
    def ballname(self, col, row):
        return self.rowname[row-1]+str(col)

    # find X and Y position of ball from name
    def ballpos(self, ball_name):
        col = int("".join(filter(str.isdigit, ball_name)))
        row = 1 + self.rowname.index("".join(filter(str.isalpha, ball_name)))
        return [col,row]

    # expand an expression such as B1:C5 to list of balls
    def expandexpr(self, inputbuf):
        # single ball has no :
        if inputbuf.find(":")==-1:
            return " \"" + inputbuf + "\""
        # multiple balls
        expanded = ""
        pos1 = self.ballpos(inputbuf[:inputbuf.find(":")])
        pos2 = self.ballpos(inputbuf[inputbuf.find(":")+1:])
        # Make sure order is increasing
        if pos1[0]>pos2[0]:
            tmp = pos1[0]
            pos1[0] = pos2[0]
            pos2[0] = tmp
        if pos1[1]>pos2[1]:
            tmp = pos1[1]
            pos1[1] = pos2[1]
            pos2[1] = tmp
        for col in range(pos1[0], pos2[0]+1):
            for row in range(pos1[1], pos2[1]+1):
                expanded = expanded + " " +"\""+ self.ballname(col, row)+"\""
        return expanded

    # expand list of balls to omit
    def expandomitlist(self, omitlist):
        expandedlist = ""
        tmpbuf = ""
        if not omitlist:
            return ""
        for character in omitlist:
            if character.isalpha() or character.isdigit() or character==":":
                tmpbuf = tmpbuf + character
            elif character == ',':
                expandedlist = expandedlist + self.expandexpr(tmpbuf)
                tmpbuf = ''
        #last value will be in tmpbuf
        expandedlist = expandedlist + self.expandexpr(tmpbuf)
        # debug: print expandedlist
        return expandedlist

    def bga(self, pitch, diameter, rows, columns = None, omit = ""):
        """ Generate a BGA footprint """
        if not columns:
            columns = rows
        # definitions needed to generate bga
        omitlist = self.expandomitlist(omit)
        width = (columns-1)*pitch+diameter
        height = (rows-1)*pitch+diameter
        # position of ball A1
        xoff = -1*((columns+1)*pitch*0.5)
        yoff = -1*((rows+1)*pitch*0.5)
        ypitch = pitch
        for row in range(1, rows+1):
            for col in range(1, 1+columns):
                if omitlist.find("\""+self.ballname(col,row)+"\"")==-1:
                    x = xoff + (pitch*col)
                    y = yoff + (ypitch*row)
                    self.add_pad(name = self.ballname(col,row),
                                 x = x,
                                 y = y,
                                 diameter = diameter,
                                 shape = 'circle')

    def silkbox(self,
                w=None,
                h=None,
                notch=None,
                silkwidth=0.155,
                arc=None,
                circle=None,
                nosides=False):

        h = h if h else w
        pullback = notch if notch else 0.0
        if notch is not None:
            self.silk_line(-0.5*w+pullback,
                           -0.5*h,
                           -0.5*w,
                           -0.5*h+pullback,
                           width = silkwidth)
        if arc is not None:
            self.generator.silk_arc(0,
                                    -0.5*h,
                                    arc,
                                    -0.5*h,
                                    180.0,
                                    width = silkwidth)
        if circle is not None:
            self.generator.silk_circle(-0.5*w+2*circle,
                                       -0.5*h+2*circle,
                                       circle,
                                       width = silkwidth)
        if not nosides:
            # left
            self.silk_line(-0.5*w,
                           -0.5*h+pullback,
                           -0.5*w,
                           0.5*h,
                           width = silkwidth)
            # right
            self.silk_line(0.5*w,
                           -0.5*h,
                           0.5*w,
                           0.5*h,
                           width = silkwidth)
        # bottom
        self.silk_line(-0.5*w,
                       0.5*h,
                       0.5*w,
                       0.5*h,
                       width = silkwidth)
        # top
        self.silk_line(-0.5*w+pullback,
                       -0.5*h,
                       0.5*w,
                       -0.5*h,
                       width = silkwidth)

    # draw silkscreen box
    def box_corners(self, x1, y1, x2, y2, width = 0.15):
        """ draw a silkscreen rectangle with corners x1,y1 and x2,y2 """
        self.silk_line(x1,y1,x2,y1, width = width)
        self.silk_line(x2,y1,x2,y2, width = width)
        self.silk_line(x2,y2,x1,y2, width = width)
        self.silk_line(x1,y2,x1,y1, width = width)

# some unit conversions to mm
mil = 0.0254
inch = 25.4
