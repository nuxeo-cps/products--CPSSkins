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
  Portal Box
  a generic box that displays actions, folders, an about box,
  a login box, an info box, etc.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName

from BaseTemplet import BaseTemplet

import md5 

factory_type_information = (
    {'id': 'Portal Box Templet',
     'meta_type': 'Portal Box Templet',
     'description': ('_portalbox_templet_description_'),
     'icon': 'portalbox_templet.gif',
     'product': 'CPSSkins',
     'factory': 'addPortalBox',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseTemplet._aliases,
     'actions': BaseTemplet._actions,
    },
)

class PortalBox(BaseTemplet):
    """
    Portal Box Templet.
    """
    meta_type = 'Portal Box Templet'
    portal_type = 'Portal Box Templet'

    render_action = 'cpsskins_portalbox'

    security = ClassSecurityInfo()

    _properties = BaseTemplet._properties + (
       {'id': 'title_source', 
        'type': 'selection', 
         'mode': 'w', 
         'label': 'Portal box title source', 
         'select_variable': 'TitleSourceList', 
         'category': 'general',
         'i18n': 1,
         'i18n_prefix': '_option_',
       },
       {'id': 'box_title_i18n', 
        'type': 'boolean', 
        'mode': 'w', 
        'label': 'Translate the box title',
        'default': 0, 
        'category': 'general', 
        'visible': 'IfCanTranslateTitleSource'
       },
       {'id': 'content', 
        'type': 'selection', 
        'mode': 'w', 
        'label': 'Portal box content', 
        'select_variable': 'ContentList', 
        'category': 'general',
        'i18n': 1,
        'i18n_prefix': '_option_',
       },
       {'id': 'show_action_icons', 
        'type': 'boolean', 
        'mode': 'w', 
        'label': 'Show action icons', 
        'category': 'actions', 
        'visible': 'IfActionsCategory',
        'default': 0
       },
       {'id': 'show_docs', 
        'type': 'boolean', 
        'mode': 'w', 
        'label': 'Show documents in folders', 
        'category': 'folders', 
        'visible': 'IfFoldersCategory',
        'default': 0,
       },
       {'id': 'display_hidden_folders', 
        'type': 'boolean', 
        'mode': 'w', 
        'label': 'Display hidden folders', 
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
       {'id': 'boxlayout', 
        'type': 'selection', 
        'mode': 'w', 
        'label': 'Box layout', 
        'category': 'layout', 
        'select_variable': 'BoxLayoutList',
        'i18n': 1,
        'i18n_prefix': '_option_',
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
       {'id': 'orientation', 
        'type': 'selection', 
        'mode': 'w', 
        'label': 'List orientation', 
        'select_variable': 'OrientationList', 
        'category': 'layout',
        'i18n': 1,
        'i18n_prefix': '_option_',
       },
       {'id': 'boxshape', 
        'type': 'selection', 
        'mode': 'w', 
        'label': 'Box shape', 
        'select_variable': 'BoxShapesList', 
        'category': 'style', 
        'style': 'Portal Box Shape'
       },
       {'id': 'boxcolor', 
        'type': 'selection', 
        'mode': 'w', 
        'label': 'Box color', 
        'select_variable': 'BoxColorsList', 
        'category': 'style', 
        'style': 'Portal Box Color'
       },
       {'id': 'info', 
        'type': 'text', 
        'mode': 'w', 
        'label': 'Info text', 
        'category': 'general', 
        'visible': 'IfInfoCategory'
       },
    )

    def __init__(self, id,
                 content = 'actions', 
                 level = 0,
                 title_source = 'Templet title',
                 show_action_icons = 0,
                 show_docs = 0,
                 display_hidden_folders = 0,
                 action_categories = ['user', 'global'],
                 custom_action_categories = [],
                 invisible_actions = ['view',],
                 base_path = '/',
                 orientation = 'vertical',
                 boxshape = '', 
                 boxcolor = '', 
                 info = 'Info here',
                 base = [],
                 boxlayout = 'standard',
                 folder_items_i18n = 0,
                 box_title_i18n = 0,
                 **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.content = content
        self.level = level
        self.show_action_icons = show_action_icons
        self.show_docs = show_docs
        self.display_hidden_folders = display_hidden_folders
        self.base_path = base_path
        self.title_source = title_source
        self.action_categories = action_categories
        self.custom_action_categories = custom_action_categories
        self.invisible_actions = invisible_actions
        self.orientation = orientation
        self.boxshape = boxshape
        self.boxcolor = boxcolor
        self.info = info
        self.base = base
        self.boxlayout = boxlayout
        self.folder_items_i18n = folder_items_i18n
        self.box_title_i18n = box_title_i18n

    security.declarePublic('isPortalBox')
    def isPortalBox(self):
        """ This templet is a Portal Box """
           
        return 1

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return 1

    #
    # RAM Cache
    #
    security.declarePublic('getCacheIndex')
    def getCacheIndex(self, REQUEST=None):
        """ returns the RAM cache index as a tuple (var1, var2, ...) """

        index = ()
        if REQUEST is None:
            REQUEST = self.REQUEST

        title_source = getattr(self, 'title_source')
        content = getattr(self, 'content')
          
        if getattr(self, 'folder_items_i18n', 0) or \
           getattr(self, 'box_title_i18n', 0) or \
           title_source == 'Workflow state' or \
           content in ['actions', 'login']:
            index += (REQUEST.get('cpsskins_language', 'en'), )

        if content in ['folders', 'related', 'recent', 'events', 
                       'login', 'pending'] \
           or title_source in ['Workflow state', 'Username']:
           index += (str(REQUEST.get('AUTHENTICATED_USER')), )

        if content in ['folders', 'about', 'related']:
            index += (REQUEST.get('PATH_TRANSLATED', '/'), )

        if content == 'actions':
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
                        ac_url = ac.get('url').strip()
                        if ac_url == current_url:
                             index += (ac_url, )
                             break

        if content == 'pending':
            cmf_actions = REQUEST.get('cpsskins_cmfactions')
            if cmf_actions:
                wf_actions = cmf_actions.get('workflow', None)
                if wf_actions is not None:
                    index += (md5.new(str(wf_actions)).hexdigest(), )

        if getattr(self, 'boxlayout', None) in ['drawer', \
                                                'drawer_notitle']:
            if self.getBoxState():
                index += (int(1), )
        return index

    security.declarePublic('TitleSourceList')
    def TitleSourceList(self):           
        """ Returns a list of contents for this Templet's title"""
                                   
        list = ['Templet title', 
                 'Workflow state', 
                 'Username',
                 'Folder title']
        return list  

    security.declarePublic('ContentList')
    def ContentList(self):           
        """ Returns a list of contents for this Templet's body"""

        list = ['actions', 
                'folders', 
                'about', 
                'login', 
                'info', 
                'related', 
                'recent', 
                'events',
                'pending',
                'language']
        return list

    security.declarePublic('OrientationList')
    def OrientationList(self):           
        """ Returns a list of orientations for this Templet"""
                                   
        list = ['horizontal', 'vertical']
        return list  

    security.declarePublic('BoxLayoutList')
    def BoxLayoutList(self):           
        """ Returns a list of orientations for this Templet"""

        layouts = ['standard', 
                   'one_frame', 
                   'notitle', 
                   'no_frames', 
                   'notitle_noframe',
                   'drawer',
                   'drawer_notitle']
        return layouts

    security.declarePublic('getI18nProperties')
    def getI18nProperties(self):
        """ Returns the list of i18n properties """

        return ['box_title_i18n', 'folder_items_i18n']

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

    security.declarePublic('IfInfoCategory')
    def IfInfoCategory(self):           
        """ Returns true if the box content is set 'info' """
                         
        if getattr(self, 'content', None) == 'info':
            return 1    

    security.declarePublic('PathsList')
    def PathsList(self):           
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

    security.declarePublic('IfCanTranslateTitleSource')
    def IfCanTranslateTitleSource(self):           
        """ Returns true if the title source can be translated """
                         
        if getattr(self, 'title_source', None) in \
                      ['Templet title', 'Folder title']:
            return 1

    security.declarePublic('BoxShapesList')
    def BoxShapesList(self):           
        """ Returns a list of Portal Box Shape styles"""

        tmtool = getToolByName(self, 'portal_themes')
        styles = tmtool.findStylesFor('Portal Box Shape', self)
        if styles: 
            return styles['title']

    security.declarePublic('BoxColorsList')
    def BoxColorsList(self):           
        """ Returns a list of Portal Box Color styles"""

        tmtool = getToolByName(self, 'portal_themes')
        styles = tmtool.findStylesFor('Portal Box Color', self)
        if styles: 
            return styles['title']

    security.declarePublic('getBoxState')
    def getBoxState(self, REQUEST=None):           
        """ Returns the box state """

        tmtool = getToolByName(self, 'portal_themes')
        if REQUEST is None:
            REQUEST = self.REQUEST
        current_theme = tmtool.getRequestedThemeName(REQUEST=REQUEST)
        boxid = self.getId()
        cookie_name = 'cpsskins_%s_%s' % (current_theme, boxid)

        if REQUEST is not None:
            state = REQUEST.cookies.get(cookie_name, None)
            return state

InitializeClass(PortalBox)

def addPortalBox(dispatcher, id, REQUEST=None, **kw):
    """Add an Portal Box Templet."""
    ob = PortalBox(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
