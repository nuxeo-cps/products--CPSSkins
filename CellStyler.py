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
  Cell Styler
  a Cell Styler modifies the style of a cell.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName

from BaseCellModifier import BaseCellModifier
from cpsskins_utils import getApplicableStylesFor

factory_type_information = (
    {'id': 'Cell Styler',
     'meta_type': 'Cell Styler',
     'description': ('_cellstyler_description_'),
     'icon': 'cell_styler.gif',
     'product': 'CPSSkins',
     'factory': 'addCellStyler',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseCellModifier._aliases,
     'actions': BaseCellModifier._actions,
    },
)

class CellStyler(BaseCellModifier):
    """
    Cell Styler.
    """
    meta_type = 'Cell Styler'
    portal_type = 'Cell Styler'
    security = ClassSecurityInfo()

    iscellstyler = 1

    _properties = BaseCellModifier._properties + (
        {'id': 'shape', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Shape', 
         'select_variable': 'AreaShapesList',
         'style' : 'Area Shape'
        },
        {'id': 'color', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Color', 
         'select_variable': 'AreaColorsList',
         'style' : 'Area Color'
        },
    )

    def __init__(self, id, 
                 shape = 'NoBorder', 
                 color = 'Transparent', 
                 **kw):
        apply(BaseCellModifier.__init__, (self, id), kw)
        self.shape = shape
        self.color = color

    security.declarePublic('isCellStyler')
    def isCellStyler(self):
        """ Is this a cell styler? """   
        return 1

    security.declarePublic('getCSSCellClass')
    def getCSSCellClass(self, level=2):
        """Return the CSS area class for this cell
        """

        if level == 1:
            cellclass = 'Color%s' % self.color

        elif level == 2:
            cellclass = 'Shape%s Color%s' % \
                        (self.shape, 
                         self.color)
        return cellclass

    security.declarePublic('getApplicableStyles')
    def getApplicableStyles(self):
        """ Returns the styles by meta type that are 
            applicable to this Cell Styler
        """
        return getApplicableStylesFor(self)

    security.declarePublic('AreaColorsList')
    def AreaColorsList(self):           
        """ Returns a list of Area Color styles"""

        tmtool = getToolByName(self, 'portal_themes') 
        styles = tmtool.findStylesFor(category = 'Area Color', object=self)
        if styles: 
            return styles['title']

    security.declarePublic('AreaShapesList')
    def AreaShapesList(self):           
        """ Returns a list of Area Shape styles"""

        tmtool = getToolByName(self, 'portal_themes')
        styles = tmtool.findStylesFor(category = 'Area Shape', object=self)
        if styles: 
            return styles['title']

InitializeClass(CellStyler)

def addCellStyler(dispatcher, id, REQUEST=None, **kw):
    """Add a Cell Styler."""
    ob = CellStyler(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
