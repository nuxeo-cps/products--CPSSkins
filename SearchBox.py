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
  Search Box Templet
  a box with an input field to search the site.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BaseTemplet import BaseTemplet

factory_type_information = (
    {'id': 'Search Box Templet',
     'meta_type': 'Search Box Templet',
     'description': ('_searchbox_templet_description_'),
     'icon': 'searchbox_templet.png',
     'product': 'CPSSkins',
     'factory': 'addSearchBox',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseTemplet._aliases,
     'actions': BaseTemplet._actions,
    },
)

class SearchBox(BaseTemplet):
    """
    Search Box Templet.
    """
    meta_type = 'Search Box Templet'
    portal_type = 'Search Box Templet'

    render_method = 'cpsskins_searchbox'

    security = ClassSecurityInfo()

    _properties = BaseTemplet._properties + (
        {'id': 'style', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Style', 
         'select_variable': 'listLayoutModes',
         'i18n': 1, 
         'i18n_prefix': '_option_searchbox_'
        },
    )

    def __init__(self, id, 
                 style = 'advanced',
                 **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.style = style

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """Returns true if the Templet can be cached in RAM."""

        return 1

    security.declarePublic('getCacheParams')
    def getCacheParams(self):
        """Return a list of cache parameters"
        """
        params = ['lang']
        return params

    security.declarePublic('listLayoutModes')
    def listLayoutModes(self):
        """Returns a list of styles or layouts for this Templet."""

        list = ['advanced', 'compact']
        return list

InitializeClass(SearchBox)

def addSearchBox(dispatcher, id, REQUEST=None, **kw):
    """Add a Search Box Templet."""
    ob = SearchBox(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
