# footgen
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

# list of all options handled previously
OLDSTYLE_OPTION_MAPPING = [
    ("round", "round"),
    ("cir", "circle"),
    ("bot", "bottom"),
    ("nopaste", "nopaste"),
    ("noplate", "noplate"),
    ("masked", "masked"),
]

class OptionsTranslator(object):
    """Translates the `options` attribute in old scripts to the new
    `options_list`.
    """

    @property
    def options(self):
        """Return the options as a string.
        """
        return ', '.join(self.options_list)

    @options.setter
    def options(self, options):
        self.options_list = []
        for option, canonical_name in OLDSTYLE_OPTION_MAPPING:
            if options.find(option) != -1:
                self.options_list.append(canonical_name)
