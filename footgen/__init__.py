#!/usr/bin/python
# footgen.py
# Copyright (C) 2005-2013 Darrell Harmon
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
import re
import math

class Footgen():
    def __init__(self, name=None, output_format="kicad"):
        self.generator = None
        self.output_format = output_format
        self.new_footprint(name)
        self.generator.mask_clearance = 0.0762
        self.generator.clearance = 0.1524
        self.pitch = 0.5
        self.skew = 0.0
        self.pins = 4
        self.pinshigh = 0
        self.padwidth = None
        self.padheight = None
        self.pitch = None
        self.width = None
        self.height = None
        self.silkoffset = 0.5
        self.silkboxheight = 0
        self.silkboxwidth = 0
        self.tabheight = None
        self.tabwidth = None
        self.mirror = False # mirror the part about the Y axis, currently supported by BGA, DIH, DIP
        self.omitballs = "" # BGA
        self.diameter = 0
    def new_footprint(self, name=None):
        if "geda" in self.output_format:
            self.generator = geda.Generator(name)
            self.name = name + ".fp"
        else:
            self.generator = kicad.Generator(name)
            self.name = name + ".kicad_mod"
    def finish(self):
        fp = self.generator.finish()
        with open(self.name, "w") as f:
            f.write(fp)

    def add_pad(self, name, x, y, xsize, ysize):
        """ add a surface mount pad """
        self.generator.width = xsize
        self.generator.height = ysize
        self.generator.add_pad(x,y, name)

    def rowofpads(self, pos, whichway, startnum, numpads):
        """ draw a row of rectangular pads
        pos is the center position [x,y]
        whichway is "up" "down" "left" or "right" """
        rowlen = self.pitch * (numpads - 1)
        if whichway == "down":
            x = pos[0]
            y = pos[1] - rowlen*0.5
            self.generator.height = self.padheight
            self.generator.width = self.padwidth
            for padnum in range (startnum, startnum+numpads):
                self.generator.add_pad(x,y,str(padnum))
                y = y + self.pitch
        elif whichway == "up":
            x = pos[0]
            y = pos[1] + rowlen*0.5
            self.generator.height = self.padheight
            self.generator.width = self.padwidth
            for padnum in range (startnum, startnum+numpads):
                self.generator.add_pad(x,y,str(padnum))
                y = y - self.pitch
        elif whichway == "right":
            x = pos[0] - rowlen*0.5
            y = pos[1]
            self.generator.height = self.padwidth
            self.generator.width = self.padheight
            for padnum in range (startnum, startnum+numpads):
                self.generator.add_pad(x,y,str(padnum))
                x = x + self.pitch
        elif whichway == "left":
            x = pos[0] + rowlen*0.5
            y = pos[1]
            self.generator.height = self.padwidth
            self.generator.width = self.padheight
            for padnum in range (startnum, startnum+numpads):
                self.generator.add_pad(x,y,str(padnum))
                x = x - self.pitch

    def thermal_pad(self, w, h=None, position = [0,0], coverage = 0.5, dots=[2,2], pin=None):
        """ draw a thermal pad """
        if not h:
            h = w
        if not pin:
            pin = str(self.pins+1)
        self.generator.width = w
        self.generator.height = h
        self.generator.options_list = ["nopaste"]
        self.generator.add_pad(0,0,pin)
        self.generator.options_list = []
        dotsizex = w/dots[0]
        dotsizey = h/dots[1]
        scale = math.sqrt(coverage)
        self.generator.height = dotsizey*scale
        self.generator.width = dotsizex*scale
        offsetx = dotsizex*(dots[0]-1)*-0.5
        offsety = dotsizey*(dots[1]-1)*-0.5
        for x in range(dots[0]):
            for y in range(dots[1]):
                self.generator.add_pad(x*dotsizex+offsetx,y*dotsizey+offsety,str(self.pins+1))

    def via_array(self, columns=None, rows=None, pitch = None, size = 0.3302, pad = 0.7, pin = None):
        if not rows:
            rows = columns
        if not pin:
            pin = str(self.pins+1)
        self.generator.drill = size
        self.generator.diameter = pad
        print size, pad
        self.generator.options_list = ["circle"]
        for x in range(columns):
            for y in range(rows):
                self.generator.add_pad((x-(columns-1)*0.5)*pitch,(y-(rows-1)*0.5)*pitch,pin)

    def add_via(self, pin="1", x=0.0, y=0.0, size=0.3302, pad=0.7):
        """ add a single via to the footprint """
        oldopts = self.generator.options_list
        olddia = self.generator.diameter
        self.generator.drill = size
        self.generator.diameter = pad
        self.generator.options_list = ["circle"]
        self.generator.add_pad(x,y,pin)
        self.generator.options_list = oldopts
        self.generator.drill = 0
        self.generator.diameter = olddia

    def sm_pads(self):
        """ create pads for a dual or quad SM package """
        left_x = -0.5*(self.width+self.padwidth)
        dir_bottom = "right"
        dir_top = "left"
        if self.mirror:
            left_x *= -1
            dir_bottom = "left"
            dir_top = "right"
        #print self.name, self.padheight, self.padwidth, self.pinshigh
        if self.pinshigh:
            self.generator.height = self.padheight
            self.generator.width = self.padwidth
            # left going down
            rowlen = self.pitch * (self.pinshigh - 1)
            y = rowlen*-0.5
            for padnum in range (1, 1 + self.pinshigh):
                self.generator.add_pad(left_x,y,str(padnum))
                y += self.pitch
            # draw right side going up
            y = rowlen*0.5
            for padnum in range (self.pinshigh+self.pinswide+1, self.pinshigh*2+self.pinswide+1):
                self.generator.add_pad(-left_x,y,str(padnum))
                y -= self.pitch
        if self.pinswide:
            # draw bottom
            self.rowofpads([0,(self.height+self.padwidth)*0.5], dir_bottom, self.pinshigh+1, self.pinswide)
            # draw top
            self.rowofpads([0,-(self.height+self.padwidth)*0.5], dir_top, 2*self.pinshigh+self.pinswide+1, self.pinswide)

    def qfn(self):
        self.pinshigh = self.pins/4
        self.pinswide = self.pinshigh
        self.height = self.width
        self.sm_pads()

    def so(self):
        """ create a dual row surface mount footprint uses pins, padwidth, padheight, pitch """
        if self.pins % 2:
            raise Exception("Error, number of pins must be even")
        self.pinshigh = self.pins/2
        self.pinswide = 0
        self.sm_pads()

    def soh(self):
        """ create a dual row surface mount header """
        if self.pins % 2:
            raise Exception("Error, number of pins must be even")
        self.pinshigh = self.pins/2
        self.pinswide = 0
        left_x = -0.5*(self.width+self.padwidth)
        self.generator.height = self.padheight
        self.generator.width = self.padwidth
        # left going down
        rowlen = self.pitch * (self.pinshigh - 1)
        y = rowlen*-0.5
        for padnum in range (self.pinshigh):
            self.generator.add_pad(left_x,y,str(1+2*padnum))
            self.generator.add_pad(-1.0*left_x,y,str(2+2*padnum))
            y += self.pitch

    def twopad(self):
        """generate a two pad part, typically used for passives such
        as 0402, 0805, etc uses parameters width, padwidth, padheight
        """
        self.pinshigh = 1
        self.pinswide = 0
        self.height = 1
        self.pitch = 1
        self.sm_pads()

    def tabbed(self):
        """ generate a part with a tab such as SOT-223 """
        totalheight = self.height+self.tabheight+self.padheight
        totalwidth = max(self.tabwidth, (self.pins-1)*self.pitch+self.padwidth)
        taby = -(totalheight-self.tabheight)*0.5
        padsy = -(self.padheight - totalheight)*0.5
        self.rowofpads([0,padsy], "right", 1, self.pins)
        self.generator.height = self.tabheight
        self.generator.width = self.tabwidth
        self.generator.add_pad(0,taby,str(self.pins+1))

    def dip(self):
        """ DIP and headers, set width to 0 and pincount to 2x the desired for SIP"""
        self.generator.drill = self.drill
        self.generator.diameter = self.diameter
        self.generator.height = self.diameter
        self.generator.width = self.diameter
        self.generator.options_list = ["square"]
        y = -(self.pins*0.5-1.0)*self.pitch*0.5
        x = self.width*0.5
        if self.mirror:
            x *= -1
        for pinnum in range (1,1+self.pins/2):
            self.generator.add_pad(-x,y,str(pinnum))
            self.generator.options_list = ["circle"] # after pin 1 gets placed
            y += self.pitch
        y -= self.pitch
        if self.width != 0:
            for pinnum in range (1+self.pins/2, self.pins+1):
                self.generator.add_pad(x,y,str(pinnum))
                y -= self.pitch
        silky = max(self.pins*self.pitch*0.25,self.silkboxheight*0.5)
        silkx = max((self.width+self.pitch)*0.5,self.silkboxwidth*0.5)
        if self.mirror:
            silkx *= -1
        self.box_corners(silkx,silky,-silkx,-silky)
        self.box_corners(-silkx,-silky,-silkx+self.pitch,-silky+self.pitch)

    def dih(self):
        """ like DIP, but numbered across and then down instead of counterclockwise """
        self.generator.drill = self.drill
        self.generator.diameter = self.diameter
        self.generator.height = self.diameter
        self.generator.width = self.diameter
        y = -(self.pins*0.5-1.0)*self.pitch*0.5
        x = self.width*0.5
        for pinnum in range (1,1+self.pins,2):
            self.generator.add_pad(-x,y,str(pinnum))
            self.generator.options_list = ["circle"]
            y += self.pitch
        if self.width != 0:
            y = -(self.pins/2-1)*self.pitch*0.5
            for pinnum in range (2,1+self.pins,2):
                self.generator.add_pad(x,y,str(pinnum))
                y += self.pitch
        silky = max(self.pins*self.pitch*0.25,self.silkboxheight*0.5)
        silkx = max((self.width+self.pitch)*0.5,self.silkboxwidth*0.5)
        self.box_corners(silkx,silky,-silkx,-silky)
        self.box_corners(-silkx,-silky,-silkx+self.pitch,-silky+self.pitch)

    def sip(self):
        """ generates a single in line through hole footprint """
        self.width = 0
        self.pins *= 2
        self.dip()
        self.pins /= 2

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
    # expand B1:C5 to list of balls
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
    def bga(self, rows, columns = None, omit = ""):
        """ Generate a BGA footprint """
        if not columns:
            columns = rows
        # definitions needed to generate bga
        omitlist = self.expandomitlist(omit)
        width = (columns-1)*self.pitch+self.diameter
        height = (rows-1)*self.pitch+self.diameter
        # position of ball A1
        xoff = -1*((columns+1)*self.pitch*0.5)
        yoff = -1*((rows+1)*self.pitch*0.5)
        ypitch = self.pitch
        if self.mirror:
            yoff = -yoff
            ypitch = -ypitch
        self.generator.options_list.append("circle")
        self.generator.diameter = self.diameter
        for row in range(1, rows+1):
            for col in range(1, 1+columns):
                if omitlist.find("\""+self.ballname(col,row)+"\"")==-1:
                    x = xoff + (self.pitch*col)
                    y = yoff + (ypitch*row)
                    self.generator.add_pad(x, y, self.ballname(col,row))

    def silkbox(self, w=None, h=None, notch=None, silkwidth=0.155, arc=None, circle=None, nosides=False):
        self.generator.silkwidth = silkwidth
        if not h:
            h = w
        if notch:
            pullback = notch
        else:
            pullback = 0.0
        if notch:
            self.generator.silk_line(-0.5*w+pullback, -0.5*h, -0.5*w, -0.5*h+pullback)
        if arc:
            self.generator.silk_arc(0, -0.5*h, arc,-0.5*h, 180.0)
        if circle:
            self.generator.silk_circle(-0.5*w, -0.5*h-circle, circle)
        if not nosides:
            # left
            self.generator.silk_line(-0.5*w, -0.5*h+pullback, -0.5*w, 0.5*h)
            # right
            self.generator.silk_line(0.5*w, -0.5*h, 0.5*w, 0.5*h)
        # bottom
        self.generator.silk_line(-0.5*w, 0.5*h, 0.5*w, 0.5*h)
        # top
        self.generator.silk_line(-0.5*w+pullback, -0.5*h, 0.5*w, -0.5*h)



    # draw silkscreen box
    def box_corners(self, x1, y1, x2, y2):
        """ draw a silkscreen rectangle with corners x1,y1 and x2,y2 """
        self.generator.silk_line(x1,y1,x2,y1)
        self.generator.silk_line(x2,y1,x2,y2)
        self.generator.silk_line(x2,y2,x1,y2)
        self.generator.silk_line(x1,y2,x1,y1)

    def silk_line(self, x1, y1, x2, y2):
        """ draw a silkscreen line """
        self.generator.silk_line(x1,y1,x2,y2)

    def silk_crop(self, w=None, h=None, pin1="", croplength=0.25, silkwidth=0.155):
        x_stop = 0.5*self.pitch*(self.pinswide-1) + .5*self.padheight + 2*silkwidth
        y_stop = 0.5*self.pitch*(self.pinshigh-1) + .5*self.padheight + 2*silkwidth
        self.generator.silkwidth = silkwidth
        if not h:
            h = w
        x = 0.5*w
        y = 0.5*h
        if "circle" in pin1:
            self.generator.silk_circle(-x-croplength,-y-croplength, croplength)
        else: # tick
            self.generator.silk_line(-x, -y, -0.5*w-croplength, -0.5*h-croplength)
        self.generator.silk_line(-x, -y, -x, -y_stop)
        self.generator.silk_line(-x, -y, -x_stop, -y)
        self.generator.silk_line(-x,  y, -x, y_stop)
        self.generator.silk_line(-x,  y, -x_stop, y)
        self.generator.silk_line( x, -y, x_stop, -y)
        self.generator.silk_line( x, -y, x, -y_stop)
        self.generator.silk_line( x,  y, x_stop, y)
        self.generator.silk_line( x,  y, x, y_stop)

# some unit conversions to mm
mil = 0.0254
inch = 25.4
