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
  Theme Chooser Templet
  a theme selector for visitors (cookies must be enabled).
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BaseTemplet import BaseTemplet

factory_type_information = (
    {'id': 'Theme Chooser Templet',
     'meta_type': 'Theme Chooser Templet',
     'description': ('_themechooser_templet_description_'),
     'icon': 'themechooser_templet.gif',
     'product': 'CPSSkins',
     'factory': 'addThemeChooser',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseTemplet._aliases,
     'actions': BaseTemplet._actions,
    },
)

class ThemeChooser(BaseTemplet):
    """
    Theme Chooser Templet.
    """
    meta_type = 'Theme Chooser Templet'
    portal_type = 'Theme Chooser Templet'

    render_action = 'cpsskins_themechooser'

    security = ClassSecurityInfo()

    _properties = BaseTemplet._properties + (
        {'id': 'themes', 
         'type': 'multiple selection', 
         'mode': 'w', 
         'label': 'Selectable themes', 
         'select_variable': 'cpsskins_listGlobalThemes'
        },
    )

    def __init__(self, id, 
                 themes = [],
                 **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.themes = themes

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return 1

    security.declarePublic('getCacheParams')
    def getCacheParams(self):
        """Return a list of cache parameters"
        """

        return []

InitializeClass(ThemeChooser)

def addThemeChooser(dispatcher, id, REQUEST=None, **kw):
    """Add a Theme Chooser Templet."""
    ob = ThemeChooser(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
