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
  Breadcrumbs Templet
  a navigation trail from the top level of the site to the current page.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BaseTemplet import BaseTemplet

factory_type_information = (
    {'id': 'Breadcrumbs Templet',
     'meta_type': 'Breadcrumbs Templet',
     'description': ('_breadcrumbs_templet_description_'),
     'icon': 'breadcrumbs_templet.png',
     'product': 'CPSSkins',
     'factory': 'addBreadcrumbs',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases':  BaseTemplet._aliases,
     'actions':  BaseTemplet._actions,
    },
)

class Breadcrumbs(BaseTemplet):
    """
    Breadcrumbs Templet.
    """
    meta_type = 'Breadcrumbs Templet'
    portal_type = 'Breadcrumbs Templet'

    render_action = 'cpsskins_breadcrumbs'

    security = ClassSecurityInfo()

    _properties = BaseTemplet._properties + (
        {'id': 'show_icon', 
         'type': 'boolean', 
         'mode': 'w', 
         'label': 'Display a contextual icon',
         'default': 0, 
        },
        {'id': 'separator_start', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Start string',
        },
        {'id': 'separator_repeat', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Repeat string'
        },
        {'id': 'separator_end', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'End string'
        },
        {'id': 'i18n', 
         'type': 'boolean', 
         'mode': 'w', 
         'label': 'Translate the breadcrumbs',
         'default': 0, 
        },
        )

    def __init__(self, id, 
                       show_icon = 0,
                       separator_start = '_You are here:_',
                       separator_repeat = '&raquo;',
                       separator_end = '',
                       i18n = 0,
                       **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.show_icon = show_icon
        self.separator_start = separator_start
        self.separator_repeat = separator_repeat
        self.separator_end = separator_end
        self.i18n = i18n

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return 1

    security.declarePublic('getCacheParams')
    def getCacheParams(self):
        """Return a list of cache parameters"
        """
        params = ['user', 'url']
        if self.i18n:
            params.append('lang')
        return params

    security.declarePublic('getI18nProperties')
    def getI18nProperties(self):
        """ Returns the list of i18n properties """

        return ['i18n']

InitializeClass(Breadcrumbs)

def addBreadcrumbs(dispatcher, id, REQUEST=None, **kw):
    """Add a Breadcrumbs Templet."""
    ob = Breadcrumbs(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
