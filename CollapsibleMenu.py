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
  Collapsible Menu Templet
  a collapsible menu that shows folder items.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BaseTemplet import BaseTemplet

factory_type_information = (
    {'id': 'Collapsible Menu Templet',
     'meta_type': 'Collapsible Menu Templet',
     'description': ('_collapsiblemenu_templet_description_'),
     'icon': 'collapsiblemenu_templet.png',
     'product': 'CPSSkins',
     'factory': 'addCollapsibleMenu',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseTemplet._aliases,
     'actions': BaseTemplet._actions,
    },
)

class CollapsibleMenu(BaseTemplet):
    """
    Collapsible Menu Templet.
    """
    meta_type = 'Collapsible Menu Templet'
    portal_type = 'Collapsible Menu Templet'

    render_method = 'cpsskins_collapsiblemenu'

    security = ClassSecurityInfo()

    _properties = BaseTemplet._properties + (
       {'id': 'show_docs', 
        'type': 'boolean', 
        'mode': 'w', 
        'label': 'Show documents in folders', 
        'category': 'general',
        'default': 0
       },
       {'id': 'folder_items_i18n', 
        'type': 'boolean', 
        'mode': 'w', 
        'label': 'Translate folder items',
        'default': 0, 
        'category': 'folders', 
       },
       {'id': 'display_hidden_folders', 
        'type': 'boolean', 
        'mode': 'w', 
        'label': 'Display hidden folders', 
        'category': 'folders', 
        'default': 0,
       }, 
       {'id': 'max_items', 
        'type': 'int', 
        'mode': 'w', 
        'label': 'Maximum number of items', 
        'category': 'general'
       },
       {'id': 'level', 
        'type':'int', 
        'mode':'w', 
        'label': 'Depth level', 
        'category': 'folders'
       },
       {'id':'base', 
        'type':'selection', 
        'mode':'w',  
        'label': 'Hierarchy base', 
        'category': 'folders', 
        'select_variable': 'cpsskins_listFolderRoots',
        'visible': 'cpsskins_ifExistsBase'
       },
       {'id':'base_path', 
        'type':'selection', 
        'mode':'w', 
        'label': 'Base path', 
        'category': 'folders', 
        'select_variable': 'listPaths'
       },
       {'id': 'collapsiblemenu_style', 
        'type': 'selection', 
        'mode': 'w', 
        'label': 'Collapsible Menu Style', 
        'select_variable': 'listCollapsibleMenuStyles', 
        'category': 'style',
        'style': 'Collapsible Menu Style'
       },
    )

    def __init__(self, id, 
                       folder_items_i18n = 0,
                       display_hidden_folders = 0,
                       show_docs = 1,
                       max_items = 10,
                       base_path = '/',
                       level = 1,
                       base = '',
                       collapsiblemenu_style = '',
                       **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.folder_items_i18n = folder_items_i18n
        self.display_hidden_folders = display_hidden_folders
        self.show_docs = show_docs
        self.max_items = max_items
        self.level = level
        self.base_path = base_path
        self.base = base
        self.collapsiblemenu_style = collapsiblemenu_style

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return 1

    security.declarePublic('getCacheParams')
    def getCacheParams(self):
        """Return a list of cache parameters"
        """
        params = ['user', 'url']
        if self.folder_items_i18n:
            params.append('lang')
        return params

    security.declarePublic('listPaths')
    def listPaths(self):           
        """ Returns a list of paths """

        list = self.cpsskins_listPaths()
        if self.cpsskins_ifExistsBase():
            mount_points = self.cpsskins_getMountPoints()
            base = self.base  
            if type(base) == type(''):
                if mount_points.has_key(base):
                    mount_point = mount_points[base]
                    list = [p for p in list if p.startswith(mount_point)]
        return list 

    security.declarePublic('getI18nProperties')
    def getI18nProperties(self):
        """ Returns the list of i18n properties """

        return ['folder_items_i18n']

InitializeClass(CollapsibleMenu)

def addCollapsibleMenu(dispatcher, id, REQUEST=None, **kw):
    """Add an Collapsible Menu Templet."""
    ob = CollapsibleMenu(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
