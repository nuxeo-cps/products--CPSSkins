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
  Cell Hider
  a Cell Hider controls the visibility of a cell.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BaseCellModifier import BaseCellModifier
from cpsskins_utils import getObjectVisibility, getAvailableLangs

factory_type_information = (
    {'id': 'Cell Hider',
     'meta_type': 'Cell Hider',
     'description': ('_cellhider_description_'),
     'icon': 'cell_hider.png',
     'product': 'CPSSkins',
     'factory': 'addCellHider',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseCellModifier._aliases,
     'actions': BaseCellModifier._actions,
    },
)

class CellHider(BaseCellModifier):
    """
    Cell Hider.
    """
    meta_type = 'Cell Hider'
    portal_type = 'Cell Hider'

    iscellhider = 1

    security = ClassSecurityInfo()

    _properties = BaseCellModifier._properties + (
        {'id': 'visibility',
         'type': 'selection',
         'mode': 'w',
         'label': 'Visibility criteria',
         'select_variable': 'listVisibilityModes',
         'category': 'general'
        },
        {'id': 'visibility_paths',
         'type': 'multiple selection',
         'mode': 'w',
         'label': 'The visibility paths',
         'select_variable': 'cpsskins_listPaths',
         'category': 'general',
         'visible': 'showVisibilityPaths'
        },
        {'id': 'languages',
         'type': 'multiple selection',
         'mode': 'w',
         'label': 'The languages in which it is visible',
         'select_variable': 'listLanguages',
         'category': 'general',
         'visible': 'listLanguages'
        },
    )

    def __init__(self, id,
                 visibility = 'always',
                 visibility_paths= [],
                 languages = [],
                 **kw):

        apply(BaseCellModifier.__init__, (self, id), kw)
        self.visibility = visibility
        self.visibility_paths = visibility_paths
        self.languages = languages

    security.declarePublic('isCellHider')
    def isCellHider(self):
        """ is a cell hider ?"""

        return self.iscellhider

    security.declarePublic('showVisibilityPaths')
    def showVisibilityPaths(self):
        """ returns true if the visibility paths must be shown """

        category = getattr(self, 'visibility', None)
        if category in ['everywhere_except_in',
                        'only_in',
                        'starting_from',
                        'up_till']:
            return 1
        return None

    security.declarePublic('getVisibility')
    def getVisibility(self, **kw):
        """ Return 1 if the object is visible in this context """

        return getObjectVisibility(self, **kw)

    security.declarePublic('listVisibilityModes')
    def listVisibilityModes(self):
        """ Returns a list of visibility criteria """

        list = ['always',
                'everywhere_except_in',
                'only_in',
                'starting_from',
                'up_till',
                'if_authenticated',
                'if_anonymous',
                'if_secure_connection' ]
        return list

    security.declarePublic('listLanguages')
    def listLanguages(self):
        """ Returns a list of languages """

        return getAvailableLangs(self)

InitializeClass(CellHider)

def addCellHider(dispatcher, id, REQUEST=None, **kw):
    """Add a Cell Hider."""
    ob = CellHider(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
