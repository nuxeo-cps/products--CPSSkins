# Copyright (c) 2003-2005 Chalmers University of Technology
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
  Cell Sizer
  a Cell Sizer sets the width of a cell.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BaseCellModifier import BaseCellModifier
from CPSSkinsPermissions import ManageThemes

factory_type_information = (
    {'id': 'Cell Sizer',
     'meta_type': 'Cell Sizer',
     'description': ('_cellsizer_description_'),
     'icon': 'cell_sizer.png',
     'product': 'CPSSkins',
     'factory': 'addCellSizer',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseCellModifier._aliases,
     'actions': BaseCellModifier._actions,
    },
)

class CellSizer(BaseCellModifier):
    """
    Cell Sizer.
    """
    meta_type = 'Cell Sizer'
    portal_type = 'Cell Sizer'

    iscellsizer = 1

    security = ClassSecurityInfo()

    _properties = BaseCellModifier._properties + (
        {'id': 'cellwidth',
         'type': 'string',
         'mode': 'w',
         'label': 'Cell width'
        },
    )

    def __init__(self, id,
                       cellwidth = '25%',
                       **kw):
        apply(BaseCellModifier.__init__, (self, id), kw)
        self.cellwidth = cellwidth

    security.declarePublic('isCellSizer')
    def isCellSizer(self):

        return self.iscellsizer

    security.declareProtected(ManageThemes, 'edit')
    def edit(self, **kw):
        """Default edit method, changes the properties."""

        # remove unknown properties
        for prop in kw.keys():
            if self.hasProperty(prop):
                continue
            del kw[prop]

        if kw.get('cellwidth') == '':
            del kw['cellwidth']
        self.manage_changeProperties(**kw)

    security.declarePublic('getCSSLayoutStyle')
    def getCSSLayoutStyle(self, level=2):
        """Return the CSS layout style for this cell
        """

        if level == 1:
            return ''
        cellwidth = self.cellwidth
        if cellwidth:
            return 'width:%s' % cellwidth
        return ''

InitializeClass(CellSizer)

def addCellSizer(dispatcher, id, REQUEST=None, **kw):
    """Add a Cell Sizer."""
    ob = CellSizer(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
