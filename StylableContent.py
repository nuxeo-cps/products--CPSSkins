# Copyright (c) 2003-2004 Chalmers University of Technology
# Authors: Jean-Marc Orliaguet <jmo@ita.chalmers.se>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#

__author__ = "Jean-Marc Orliaguet <jmo@ita.chalmers.se>"

"""
  Base class for stylable content
"""

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from cpsskins_utils import getStyleList, getApplicableStylesFor

class StylableContent:
    """Stylable content
    """

    security = ClassSecurityInfo()

    security.declarePublic('AreaColorsList')
    def AreaColorsList(self):           
        """Returns a list of Area Color styles."""

        return getStyleList(self, 'Area Color')

    security.declarePublic('AreaShapesList')
    def AreaShapesList(self):           
        """Returns a list of Area Shape styles."""

        return getStyleList(self, 'Area Shape')

    security.declarePublic('FontColorsList')
    def FontColorsList(self):           
        """Returns a list of Font Color styles."""

        return getStyleList(self, 'Font Color')

    security.declarePublic('FontShapesList')
    def FontShapesList(self):           
        """Returns a list of Font Shape styles."""

        return getStyleList(self, 'Font Shape')

    security.declarePublic('FormStyleList')
    def FormStyleList(self):           
        """Returns a list of formstyles."""

        return getStyleList(self, 'Form Style')

    security.declarePublic('BoxShapesList')
    def BoxShapesList(self):           
        """ Returns a list of Portal Box Shape styles"""

        return getStyleList(self, 'Portal Box Shape')

    security.declarePublic('BoxColorsList')
    def BoxColorsList(self):           
        """ Returns a list of Portal Box Color styles"""

        return getStyleList(self, 'Portal Box Color')

    security.declarePublic('BoxCornersList')
    def BoxCornersList(self):           
        """ Returns a list of Box Corner styles"""

        return getStyleList(self, 'Box Corners')

    security.declarePublic('PortalTabStylesList')
    def PortalTabStylesList(self):           
        """ Returns a list of Portal Tab styles"""

        return getStyleList(self, 'Portal Tab Style')

    security.declarePublic('CalendarStylesList')
    def CalendarStylesList(self):           
        """ Returns a list of Calendar styles"""

        return getStyleList(self, 'Calendar Style')

    security.declarePublic('CollapsibleMenuStylesList')
    def CollapsibleMenuStylesList(self):           
        """ Returns a list of Collapsible Menu styles"""

        return getStyleList(self, 'Collapsible Menu Style')

    #
    #
    #
    security.declarePublic('getApplicableStyles')
    def getApplicableStyles(self):
        """Returns the styles by meta type that are 
           applicable to this Templet
        """

        return getApplicableStylesFor(self)

InitializeClass(StylableContent)
