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
  Language Templet
  a language selector.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BaseTemplet import BaseTemplet

factory_type_information = (
    {'id': 'Language Templet',
     'meta_type': 'Language Templet',
     'description': ('_language_templet_description_'),
     'icon': 'language_templet.png',
     'product': 'CPSSkins',
     'factory': 'addLanguage',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseTemplet._aliases,
     'actions': BaseTemplet._actions,
    },
)

class Language(BaseTemplet):
    """
    Language Templet.
    """
    meta_type = 'Language Templet'
    portal_type = 'Language Templet'

    render_method = 'cpsskins_language'

    security = ClassSecurityInfo()

    _properties = BaseTemplet._properties + (
        {'id': 'style',
         'type': 'selection',
         'mode': 'w',
         'label': 'Appearance',
         'select_variable': 'listLayoutModes',
         'i18n': 1,
         'i18n_prefix': '_option_',
        },
        {'id': 'hide_current_lang',
         'type': 'boolean',
         'mode': 'w',
         'label': 'Hide current language',
         'default': 0,
        },
    )

    def __init__(self, id,
                 style = 'flags',
                 hide_current_lang = 0,
                 **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.style = style
        self.hide_current_lang = hide_current_lang

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return 1

    security.declarePublic('getCacheParams')
    def getCacheParams(self):
        """Return a list of cache parameters"
        """
        params = ['lang']
        return params

    security.declarePublic('listLayoutModes')
    def listLayoutModes(self):
        """ Returns a list of styles or layouts for this Templet"""

        list = ['flags', 'dropdown list', 'language names']
        return list

InitializeClass(Language)

def addLanguage(dispatcher, id, REQUEST=None, **kw):
    """Add a Language Templet."""
    ob = Language(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
