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

import footgen.kicad as kicad

class Footgen(object):
    def __init__(self, name=None, output_format="kicad"):
        self.generator = kicad.Generator(name)
        self.name = name + ".kicad_mod"
        self.add_pad = self.generator.add_pad
        self.silk_line = self.generator.silk_line

    def finish(self):
        fp = self.generator.finish()
        with open(self.name, "w") as f:
            f.write(fp)

# some unit conversions to mm
mil = 0.0254
inch = 25.4
