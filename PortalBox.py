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
# $Id$

__author__ = "Jean-Marc Orliaguet <jmo@ita.chalmers.se>"

"""
  Portal Box
  a generic box that displays actions, folders, an about box,
  a login box, an info box, etc.
"""

from types import StringType
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName

from BaseTemplet import BaseTemplet
from SimpleBox import SimpleBox
from cpsskins_utils import html_slimmer

factory_type_information = (
    {'id': 'Portal Box Templet',
     'meta_type': 'Portal Box Templet',
     'description': ('_portalbox_templet_description_'),
     'icon': 'portalbox_templet.png',
     'product': 'CPSSkins',
     'factory': 'addPortalBox',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseTemplet._aliases,
     'actions': BaseTemplet._actions,
    },
)

class PortalBox(BaseTemplet, SimpleBox):
    """
    Portal Box Templet.
    """
    meta_type = 'Portal Box Templet'
    portal_type = 'Portal Box Templet'

    render_method = 'cpsskins_portalbox'

    security = ClassSecurityInfo()

    _properties = BaseTemplet._properties + \
                  SimpleBox._properties + (
       {'id': 'title_source',
        'type': 'selection',
         'mode': 'w',
         'label': 'Portal box title source',
         'select_variable': 'listTitleSources',
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
        'visible': 'ifCanTranslateTitleSource'
       },
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
       {'id': 'display_hidden_folders',
        'type': 'boolean',
        'mode': 'w',
        'label': 'Display hidden folders',
        'category': 'folders',
        'visible': 'ifFoldersCategory',
        'default': 0,
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
       {'id': 'orientation',
        'type': 'selection',
        'mode': 'w',
        'label': 'List orientation',
        'select_variable': 'listOrientations',
        'category': 'layout',
        'i18n': 1,
        'i18n_prefix': '_option_',
       },
       {'id': 'info',
        'type': 'text',
        'mode': 'w',
        'label': 'Info text',
        'category': 'general',
        'visible': 'ifInfoCategory'
       },
    )

    def __init__(self, id,
                 content = 'actions',
                 level = 0,
                 title_source = 'Templet title',
                 show_docs = 0,
                 display_hidden_folders = 0,
                 action_categories = ['user', 'global'],
                 custom_action_categories = [],
                 invisible_actions = ['view',],
                 base_path = '/',
                 orientation = 'vertical',
                 info = 'Info here',
                 base = [],
                 folder_items_i18n = 0,
                 box_title_i18n = 0,
                 **kw):
        BaseTemplet.__init__(self, id, **kw)
        SimpleBox.__init__(self, **kw)
        self.content = content
        self.level = level
        self.show_docs = show_docs
        self.display_hidden_folders = display_hidden_folders
        self.base_path = base_path
        self.title_source = title_source
        self.action_categories = action_categories
        self.custom_action_categories = custom_action_categories
        self.invisible_actions = invisible_actions
        self.orientation = orientation
        self.info = info
        self.base = base
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
    # CSS
    #
    def getCSSBoxLayoutStyle(self):
        """Returns the CSS layout style for this boxes."""

        css = ''
        padding = self.padding
        if padding:
            if padding not in ('0', '0pt', '0in', '0pc', '0mm',
                               '0cm', '0px', '0em', '0ex'):
                css += 'padding:%s;' % padding
        return css

    #
    # Rendering
    #
    security.declarePublic('render')
    def render(self, shield=0, **kw):
        """Renders the templet."""

        body = self.render_skin(shield=shield, **kw)
        body = html_slimmer(body)

        rendered_box = []
        if body:
            # add the box frame
            boxstyle = self.getCSSBoxLayoutStyle()
            if boxstyle:
                rendered_box.extend('<div style="%s">' % boxstyle)
            rendered_box.extend('<div class="%s">' % self.getCSSBoxClass())

            # add the box decoration
            rendered_box.extend(
                self.renderBoxLayout(
                    boxlayout=self.boxlayout,
                    title=self.render_title(**kw),
                    body=body, **kw))
            rendered_box.extend('</div>')
            if boxstyle:
                rendered_box.extend('</div>')
        return ''.join(rendered_box)

    security.declarePublic('render_title')
    def render_title(self, **kw):
        """Renders the templet's title."""

        macro = self.cpsskins_portalbox_macros
        kw.update({
            'title_source': self.title_source,
            'box_title_i18n': self.box_title_i18n,
            })
        return macro(**kw)

    #
    # RAM Cache
    #
    security.declarePublic('getCacheParams')
    def getCacheParams(self):
        """Return a list of cache parameters"
        """
        params = []
        title_source = self.title_source
        content = self.content

        if self.folder_items_i18n or self.box_title_i18n or\
           title_source == 'Workflow state' or \
           content in ['actions', 'login']:
            params.append('lang')

        if content in ['folders', 'related', 'recent',
                       'events', 'login', 'pending'] \
           or title_source in ['Workflow state', 'Username']:
            params.extend(['user', 'baseurl'])

        if content in ['folders', 'about', 'related']:
            params.append('object:path')

        elif content == 'actions':
            categories = self.action_categories
            custom_categories = self.custom_action_categories
            if custom_categories and custom_categories[0]:
                categories += custom_categories
            cat_string = ','.join(categories)
            params.append('actions:' + cat_string)

        if self.boxlayout in ['drawer', 'drawer_notitle']:
            params.append('boxstate')

        return params

    security.declarePublic('listTitleSources')
    def listTitleSources(self):
        """ Returns a list of contents for this Templet's title"""

        list = ['Templet title',
                 'Workflow state',
                 'Username',
                 'Folder title']
        return list

    security.declarePublic('listDisplayModes')
    def listDisplayModes(self):
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

    security.declarePublic('listOrientations')
    def listOrientations(self):
        """ Returns a list of orientations for this Templet"""

        list = ['horizontal', 'vertical']
        return list


    security.declarePublic('getI18nProperties')
    def getI18nProperties(self):
        """ Returns the list of i18n properties """

        return ['box_title_i18n', 'folder_items_i18n']

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

    security.declarePublic('ifInfoCategory')
    def ifInfoCategory(self):
        """ Returns true if the box content is set 'info' """

        if getattr(self, 'content', None) == 'info':
            return 1
        return None

    security.declarePublic('listPaths')
    def listPaths(self):
        """ Returns a list of paths """

        list = self.cpsskins_listPaths()
        if self.cpsskins_ifExistsBase():
            mount_points = self.cpsskins_getMountPoints()
            base = self.base
            if isinstance(base, StringType):
                if mount_points.has_key(base):
                    mount_point = mount_points[base]
                    list = [p for p in list if p.startswith(mount_point)]
        return list

    security.declarePublic('ifCanTranslateTitleSource')
    def ifCanTranslateTitleSource(self):
        """ Returns true if the title source can be translated """

        if getattr(self, 'title_source', None) in \
                      ['Templet title', 'Folder title']:
            return 1
        return None

    security.declarePublic('getBoxState')
    def getBoxState(self, REQUEST=None):
        """ Returns the box state """

        tmtool = getToolByName(self, 'portal_themes')
        if REQUEST is None:
            REQUEST = self.REQUEST
        theme, page = tmtool.getEffectiveThemeAndPageName()
        boxid = self.getId()
        cookie_name = 'cpsskins_%s_%s_%s' % (theme, page, boxid)

        if REQUEST is not None:
            state = REQUEST.cookies.get(cookie_name, None)
            return state
        return None

    security.declarePublic('listBoxLayouts')
    def listBoxLayouts(self):
        """Return a list of layouts for this Templet.
        """

        return self.cpsskins_listBoxLayouts('PortalBox')

InitializeClass(PortalBox)

def addPortalBox(dispatcher, id, REQUEST=None, **kw):
    """Add an Portal Box Templet."""
    ob = PortalBox(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
