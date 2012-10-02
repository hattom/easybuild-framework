##
# Copyright 2009-2012 Stijn De Weirdt
# Copyright 2010 Dries Verdegem
# Copyright 2010-2012 Kenneth Hoste
# Copyright 2011 Pieter De Baets
# Copyright 2011-2012 Jens Timmerman
#
# This file is part of EasyBuild,
# originally created by the HPC team of the University of Ghent (http://ugent.be/hpc).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for building and installing netCDF-Fortran, implemented as an easyblock
"""

import os

import easybuild.tools.environment as env
import easybuild.tools.toolkit as toolkit
from easybuild.easyblocks.configuremake import EB_ConfigureMake  #@UnresolvedImport


class EB_netCDF_minus_Fortran(EB_ConfigureMake):
    """Support for building/installing the netCDF-Fortran library"""

    def configure_step(self):
        """Configure build: set config options and configure"""

        if self.get_toolkit().opts['pic']:
            self.updatecfg('configopts', "--with-pic")

        self.updatecfg('configopts', 'FCFLAGS="%s" FC="%s"' % (os.getenv('FFLAGS'), os.getenv('F90')))

        # add -DgFortran to CPPFLAGS when building with GCC
        if self.get_toolkit().comp_family() == toolkit.GCC:
            env.set('CPPFLAGS', "%s -DgFortran" % os.getenv('CPPFLAGS'))

        super(self.__class__, self).configure_step()

    def sanity_check_step(self):
        """
        Custom sanity check for netCDF-Fortran
        """
        if not self.getcfg('sanityCheckPaths'):

            self.setcfg('sanityCheckPaths',{
                                            'files': ["bin/nf-config"] +
                                                     ["lib/%s" % x for x in ["libnetcdff.so", "libnetcdff.a"]] +
                                                     ["include/%s" % x for x in ["netcdf.inc", "netcdf.mod",
                                                                                 "typesizes.mod"]],
                                            'dirs': []
                                           })

            self.log.info("Customized sanity check paths: %s" % self.getcfg('sanityCheckPaths'))

        super(self.__class__, self).sanity_check_step()
