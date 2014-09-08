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

import warnings

class BaseGenerator(object):
    """Base class for all backends.

    This mainly supplies shared code: translation of the old- and
    newstyle options interfaces, sanitation and handling of option
    lists.
    """

    @property
    def options(self):
        """Translates the `options` attribute used in old scripts to the new
        `options_list`.

        Only the options valid for the old interface may be supplied by
        this method.
        """
        return ', '.join(self.options_list)

    @options.setter
    def options(self, options):
        self.options_list = []
        for option, canonical_name in OLDSTYLE_OPTION_MAPPING:
            # check for the options the same way the old code used to
            # do, therfore ensuring backwards compatibility
            if options.find(option) != -1:
                self.options_list.append(canonical_name)

    def _sanitize_options(self, name):
        # make sure options are unique
        self.options_list = list(set(self.options_list))

        # warn on contradictory options
        # XXX: actually I believe we should set one as the default (circle)
        # and only supply square explicitely as a flag.
        if "circle" in self.options_list and "square" in self.options_list:
            warnings.warn("square and circle options given for pad {}.\n"
                          "Default to square".fomrat(name))

    def _unhandled_options(self):
        # some thoughts on improving this: check the options with an
        # interface, which lists the handled options, but this is TODO
        # for a future refactoring IMO.
        res = []
        for option in self.options_list:
            # XXX: add options here that are handled explicitely in
            # the backends (instead of being passed on to the
            # underlying tool)
            if option not in ("circle", "square", "bottom", "round",
                              "noplate", "masked"):
                res.append(option)
        return res
