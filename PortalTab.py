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
  Portal Tab Templet
  horizontal tabs displaying folders, actions, etc.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BaseTemplet import BaseTemplet
from cpsskins_utils import getStyleList

import md5

factory_type_information = (
    {'id': 'Portal Tab Templet',
     'meta_type': 'Portal Tab Templet',
     'description': ('_portaltab_templet_description_'),
     'icon': 'portaltab_templet.gif',
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

    render_action = 'cpsskins_portaltab'

    security = ClassSecurityInfo()

    _properties = BaseTemplet._properties + (
       {'id': 'content', 
        'type': 'selection', 
        'mode': 'w', 
        'label': 'Portal box content', 
        'select_variable': 'ContentList', 
        'category': 'general',
        'i18n': 1,
       },
       {'id': 'show_docs', 
        'type': 'boolean', 
        'mode': 'w', 
        'label': 'Show documents in folders', 
        'category': 'folders', 
        'visible': 'IfFoldersCategory',
        'default': 0,
       },
       {'id': 'folder_items_i18n', 
        'type': 'boolean', 
        'mode': 'w', 
        'label': 'Translate folder items',
        'default': 0, 
        'category': 'folders', 
        'visible': 'IfFoldersCategory'
       },
       {'id': 'level', 
        'type': 'int', 
        'mode': 'w', 
        'label': 'Depth level', 
        'category': 'folders', 
        'visible': 'IfFoldersCategory'
       },
       {'id': 'base', 
        'type': 'selection', 
        'mode': 'w', 
        'label': 'Hierarchy base', 
        'category': 'folders', 
        'select_variable': 'cpsskins_listFolderRoots', 
        'visible': 'IfFoldersCategoryAndExistsBase'
       },
       {'id': 'base_path', 
        'type': 'selection', 
        'mode': 'w', 
        'label': 'Base path', 
        'category': 'folders', 
        'select_variable': 'PathsList', 
        'visible': 'IfFoldersCategory'
       },
       {'id': 'action_categories', 
        'type': 'multiple selection', 
        'mode': 'w', 
        'label': 'Action categories', 
        'select_variable': 'cpsskins_listActionCategories', 
        'category': 'actions', 
        'visible': 'IfActionsCategory'
       },
       {'id': 'custom_action_categories', 
        'type': 'lines', 
        'mode': 'w', 
        'label': 'Custom action categories', 
        'category': 'actions', 
        'visible': 'IfActionsCategory'
       },
       {'id': 'invisible_actions', 
        'type': 'lines', 
        'mode': 'w', 
        'label': 'Invisible actions', 
        'category': 'actions', 
        'visible': 'IfActionsCategory'
       },
       {'id': 'portaltabstyle', 
        'type': 'selection', 
        'mode': 'w', 
        'label': 'Tab style', 
        'select_variable': 'PortalTabStylesList', 
        'category': 'style', 
        'style': 'Portal Tab Style'
       },
    )

    def __init__(self, id,
                 content = 'actions', 
                 level = 0,
                 show_docs = 0,
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

    security.declarePublic('getCacheIndex')
    def getCacheIndex(self, REQUEST=None):
        """ returns the RAM cache index as a tuple (var1, var2, ...) """

        index = ()
        if REQUEST is None:
            REQUEST = self.REQUEST

        index += (str(REQUEST.get('AUTHENTICATED_USER')), )
        if getattr(self, 'folder_items_i18n', 0):
            index += (REQUEST.get('cpsskins_language', 'en'), )
        if getattr(self, 'content') == 'folders':
            index += (REQUEST.get('PATH_TRANSLATED', '/'), )
        if getattr(self, 'content') == 'actions':
            cmf_actions = REQUEST.get('cpsskins_cmfactions')
            if cmf_actions:         
                current_url = REQUEST.get('cpsskins_url')
                categories = getattr(self, 'action_categories', []) + \
                             getattr(self, 'custom_action_categories', [])
                actions = [cmf_actions[x] for x in categories \
                          if cmf_actions.has_key(x)]
                index += (md5.new(str(actions)).hexdigest(), )
                for actions_by_cat in actions:
                    for ac in actions_by_cat:
                        ac_url = ac.get('url')
                        if ac_url == current_url:
                             index += (ac_url, )
                             break  
        return index

    security.declarePublic('ContentList')
    def ContentList(self):           
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

    security.declarePublic('IfActionsCategory')
    def IfActionsCategory(self):           
        """ Returns true if the box content is set 'actions' """

        if getattr(self, 'content', None) == 'actions':
            return 1

    security.declarePublic('IfFoldersCategory')
    def IfFoldersCategory(self):           
        """ Returns true if the box content is set 'folders' """

        if getattr(self, 'content', None) == 'folders':
            return 1

    security.declarePublic('IfFoldersCategoryAndExistsBase')
    def IfFoldersCategoryAndExistsBase(self):           
        """ Returns true if the box content is set 'folders' 
            and if the folders have a base """

        if not self.IfFoldersCategory():
            return None

        if not self.cpsskins_ifExistsBase():
            return None
        return 1   

    security.declarePublic('PathsList')
    def PathsList(self):           
        """ Returns a list of paths """

        list = self.cpsskins_listPaths()
        if self.IfFoldersCategoryAndExistsBase():
            mount_points = self.cpsskins_getMountPoints()
            base = self.base  
            if type(base) == type(''):
                if mount_points.has_key(base):
                    mount_point = mount_points[base]
                    list = [p for p in list if p.startswith(mount_point)]
        return list 

    security.declarePublic('PortalTabStylesList')
    def PortalTabStylesList(self):           
        """ Returns a list of Portal Tab styles"""

        return getStyleList(self, 'Portal Tab Style')

InitializeClass(PortalTab)

def addPortalTab(dispatcher, id, REQUEST=None, **kw):
    """Add a Portal Tab Templet."""
    ob = PortalTab(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
