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

from Products.CMFCore.utils import getToolByName

from CPSSkinsPermissions import ManageThemes
from cpsskins_utils import getStyleList, getApplicableStylesFor

class StylableContent:
    """Stylable content
    """

    security = ClassSecurityInfo()

    security.declarePublic('listAreaColors')
    def listAreaColors(self):           
        """Returns a list of Area Color styles."""

        return getStyleList(self, 'Area Color')

    security.declarePublic('listAreaShapes')
    def listAreaShapes(self):           
        """Returns a list of Area Shape styles."""

        return getStyleList(self, 'Area Shape')

    security.declarePublic('listFontColors')
    def listFontColors(self):           
        """Returns a list of Font Color styles."""

        return getStyleList(self, 'Font Color')

    security.declarePublic('listFontShapes')
    def listFontShapes(self):           
        """Returns a list of Font Shape styles."""

        return getStyleList(self, 'Font Shape')

    security.declarePublic('listFormStyles')
    def listFormStyles(self):           
        """Returns a list of formstyles."""

        return getStyleList(self, 'Form Style')

    security.declarePublic('listBoxShapes')
    def listBoxShapes(self):           
        """ Returns a list of Portal Box Shape styles"""

        return getStyleList(self, 'Portal Box Shape')

    security.declarePublic('listBoxColors')
    def listBoxColors(self):           
        """ Returns a list of Portal Box Color styles"""

        return getStyleList(self, 'Portal Box Color')

    security.declarePublic('listBoxCorners')
    def listBoxCorners(self):           
        """ Returns a list of Box Corner styles"""

        return getStyleList(self, 'Box Corners')

    security.declarePublic('listTabStyles')
    def listTabStyles(self):           
        """ Returns a list of Portal Tab styles"""

        return getStyleList(self, 'Portal Tab Style')

    security.declarePublic('listCalendarStyles')
    def listCalendarStyles(self):           
        """ Returns a list of Calendar styles"""

        return getStyleList(self, 'Calendar Style')

    security.declarePublic('listCollapsibleMenuStyles')
    def listCollapsibleMenuStyles(self):           
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

    security.declarePublic('getStyle')
    def getStyle(self,  meta_type=None):
        """Get a style associated to this object by meta type.
        """
        tmtool = getToolByName(self, 'portal_themes')
        theme_container = tmtool.getPortalThemeRoot(self)
        for propid in self.propertyIds():
            for obj in self.propertyMap():
                if obj['id'] != propid:                
                    continue
                if obj.get('style', None) != meta_type:
                    continue
                style_title = getattr(self, propid, None)
                styles = theme_container.findStyles(title=style_title)
                if len(styles) > 0: 
                    return styles[0]

    security.declareProtected(ManageThemes, 'setStyle')
    def setStyle(self, style=None, meta_type=None):
        """Sets a style to this object."""

        if style is None:
            return
        prop_id = None 
        for propid in self.propertyIds():
            for obj in self.propertyMap():
                if obj['id'] != propid:
                    continue
                if obj.get('style', None) == meta_type:
                    prop_id = propid
                    break
        if prop_id is not None:
            self.manage_changeProperties(**{prop_id: style.getTitle()})
            self.expireCache()

InitializeClass(StylableContent)
