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
  Portal Tab Templet
  horizontal tabs displaying folders, actions, etc.
"""

from types import StringType
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BaseTemplet import BaseTemplet

factory_type_information = (
    {'id': 'Portal Tab Templet',
     'meta_type': 'Portal Tab Templet',
     'description': ('_portaltab_templet_description_'),
     'icon': 'portaltab_templet.png',
     'product': 'CPSSkins',
     'factory': 'addPortalTab',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseTemplet._aliases,
     'actions': BaseTemplet._actions,
    },
)

class PortalTab(BaseTemplet):
    """
    Portal Tab Templet.
    """
    meta_type = 'Portal Tab Templet'
    portal_type = 'Portal Tab Templet'

    render_method = 'cpsskins_portaltab'

    security = ClassSecurityInfo()

    _properties = BaseTemplet._properties + (
       {'id': 'content',
        'type': 'selection',
        'mode': 'w',
        'label': 'Portal box content',
        'select_variable': 'listDisplayModes',
        'category': 'general',
        'i18n': 1,
        'i18n_prefix': '_option_',
       },
       {'id': 'show_docs',
        'type': 'boolean',
        'mode': 'w',
        'label': 'Show documents in folders',
        'category': 'folders',
        'visible': 'ifFoldersCategory',
        'default': 0,
       },
       {'id': 'show_add_items',
        'type': 'boolean',
        'mode': 'w',
        'label': 'Show add items',
        'category': 'folders',
        'visible': 'ifFoldersCategory',
        'default': 1,
       },
       {'id': 'folder_items_i18n',
        'type': 'boolean',
        'mode': 'w',
        'label': 'Translate folder items',
        'default': 0,
        'category': 'folders',
        'visible': 'ifFoldersCategory'
       },
       {'id': 'level',
        'type': 'int',
        'mode': 'w',
        'label': 'Depth level',
        'category': 'folders',
        'visible': 'ifFoldersCategory'
       },
       {'id': 'base',
        'type': 'selection',
        'mode': 'w',
        'label': 'Hierarchy base',
        'category': 'folders',
        'select_variable': 'cpsskins_listFolderRoots',
        'visible': 'ifFoldersCategoryAndExistsBase'
       },
       {'id': 'base_path',
        'type': 'selection',
        'mode': 'w',
        'label': 'Base path',
        'category': 'folders',
        'select_variable': 'listPaths',
        'visible': 'ifFoldersCategory'
       },
       {'id': 'action_categories',
        'type': 'multiple selection',
        'mode': 'w',
        'label': 'Action categories',
        'select_variable': 'cpsskins_listActionCategories',
        'category': 'actions',
        'visible': 'ifActionsCategory'
       },
       {'id': 'custom_action_categories',
        'type': 'lines',
        'mode': 'w',
        'label': 'Custom action categories',
        'category': 'actions',
        'visible': 'ifActionsCategory'
       },
       {'id': 'invisible_actions',
        'type': 'lines',
        'mode': 'w',
        'label': 'Invisible actions',
        'category': 'actions',
        'visible': 'ifActionsCategory'
       },
       {'id': 'portaltabstyle',
        'type': 'selection',
        'mode': 'w',
        'label': 'Tab style',
        'select_variable': 'listTabStyles',
        'category': 'style',
        'style': 'Portal Tab Style'
       },
    )

    def __init__(self, id,
                 content = 'actions',
                 level = 0,
                 show_docs = 0,
                 show_add_items = 1,
                 action_categories = ['user', 'global'],
                 custom_action_categories = [],
                 invisible_actions = ['view',],
                 base_path = '/',
                 portaltabstyle = '',
                 base = [],
                 folder_items_i18n = 0,
                 **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.content = content
        self.level = level
        self.show_docs = show_docs
        self.show_add_items = show_add_items
        self.base_path = base_path
        self.action_categories = action_categories
        self.custom_action_categories = custom_action_categories
        self.invisible_actions = invisible_actions
        self.portaltabstyle = portaltabstyle
        self.base = base
        self.folder_items_i18n = folder_items_i18n

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return 1

    security.declarePublic('getCacheParams')
    def getCacheParams(self):
        """Return a list of cache parameters"
        """

        params = ['user']
        content = self.content

        if self.folder_items_i18n:
            params.append('lang')

        if content == 'folders':
            params.extend(['object:path', 'baseurl'])

        if content == 'actions':
            categories = self.action_categories + self.custom_action_categories
            cat_string = ','.join(categories)
            params.append('actions:' + cat_string)

        return params

    security.declarePublic('listDisplayModes')
    def listDisplayModes(self):
        """ Returns a list of contents for this Templet's body"""

        list = [ 'actions',
                 'folders' ]
        return list

    security.declarePublic('isAlignable')
    def isAlignable(self):
        """ Returns true if the Templet can be aligned horizontally """

        return None

    security.declarePublic('getI18nProperties')
    def getI18nProperties(self):
        """ Returns the list of i18n properties """

        return ['folder_items_i18n',]

    security.declarePublic('ifActionsCategory')
    def ifActionsCategory(self):
        """ Returns true if the box content is set 'actions' """

        if getattr(self, 'content', None) == 'actions':
            return 1
        return None

    security.declarePublic('ifFoldersCategory')
    def ifFoldersCategory(self):
        """ Returns true if the box content is set 'folders' """

        if getattr(self, 'content', None) == 'folders':
            return 1
        return None

    security.declarePublic('ifFoldersCategoryAndExistsBase')
    def ifFoldersCategoryAndExistsBase(self):
        """ Returns true if the box content is set 'folders'
            and if the folders have a base """

        if not self.ifFoldersCategory():
            return None

        if not self.cpsskins_ifExistsBase():
            return None
        return 1

    security.declarePublic('listPaths')
    def listPaths(self):
        """ Returns a list of paths """

        list = self.cpsskins_listPaths()
        if self.ifFoldersCategoryAndExistsBase():
            mount_points = self.cpsskins_getMountPoints()
            base = self.base
            if isinstance(base, StringType):
                if mount_points.has_key(base):
                    mount_point = mount_points[base]
                    list = [p for p in list if p.startswith(mount_point)]
        return list

InitializeClass(PortalTab)

def addPortalTab(dispatcher, id, REQUEST=None, **kw):
    """Add a Portal Tab Templet."""
    ob = PortalTab(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
