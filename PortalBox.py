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
from cpsskins_utils import html_slimmer

BOX_LAYOUTS = {
# standard box
'standard': """<div class="title">%s</div><div class="body">%s</div>""",
# one frame
'one_frame': """<div class="body"><h4>%s</h4><br/>%s</div>""",
# no title no frame
'notitle_noframe': """<div class="body" style="border: none">%s</div>""",
# no title
'notitle': """<div class="body">%s</div>""",
# no frame
'noframe': """<div class="title" style="border: none">%s</div>
<div class="body" style="border: none">%s</div>""",
}

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

        if css:
            return css

    #
    # Rendering
    #
    security.declarePublic('render')
    def render(self, shield=0, **kw):
        """Renders the templet."""

        body = self.render_skin(shield=shield, **kw)
        body = html_slimmer(body)

        rendered_box = ''
        if body:
            # add the box frame
            rendered_box += '<div style="%s"><div class="%s">' % (
                            self.getCSSBoxLayoutStyle(),
                            self.getCSSBoxClass())
            # add the box decoration
            rendered_box += self.renderBoxLayout(boxlayout=self.boxlayout,
                                                 title=self.render_title(**kw),
                                                 body=body,
                                                )
            rendered_box += '</div></div>'
        return rendered_box

    security.declarePublic('renderBoxLayout')
    def renderBoxLayout(self, boxlayout='', title='', body='', **kw):
        """Render the box layout.
        """
        if boxlayout == 'standard': 
            return BOX_LAYOUTS['standard'] % (title, body)
        elif boxlayout == 'one_frame':
            return BOX_LAYOUTS['one_frame'] % (title, body)
        elif boxlayout == 'notitle':
            return BOX_LAYOUTS['notitle'] % body
        elif boxlayout == 'noframe':
            return BOX_LAYOUTS['noframe'] % (title, body)
        elif boxlayout == 'notitle_noframe':
            return BOX_LAYOUTS['notitle_noframe'] % body

        macro_path = self.restrictedTraverse('cpsskins_BoxLayouts/macros/%s' %\
                                             boxlayout, default=None)
        if macro_path is None:
            return ''

        rendered = self.cpsskins_renderBoxLayout(title=title,
                                                 body=body,
                                                 macro_path=macro_path,
                                                 **kw)
        return rendered

    security.declarePublic('render_title')
    def render_title(self, **kw):
        """Renders the templet's title."""

        title_source = self.title_source
        REQUEST = self.REQUEST
        mcat = REQUEST.get('cpsskins_mcat')

        title = ''

        if title_source == 'Templet title':
            title = self.title
            if mcat and self.box_title_i18n:
                title = mcat(title)

        elif title_source == 'Folder title':
            title = 'XXX'
            if mcat and self.box_title_i18n:
                title = mcat(title)

        elif title_source == 'Workflow state':
            context_obj = kw.get('context_obj')
            if context_obj is not None:
                wtool = getToolByName(self, 'portal_workflow')
                title = wtool.getInfoFor(context_obj, 'review_state','')

        elif title_source == 'Username':
            mtool = getToolByName(self, 'portal_membership')
            isAnon = mtool.isAnonymousUser()
            if isAnon:
                title = '_Guest_'
                if mcat:
                    title = mcat(title)
            else:
                member = mtool.getAuthenticatedMember()
                title = member.getUserName()

        return title

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
            params.append('user')

        if content in ['folders', 'about', 'related']:
            params.append('object:path')

        if content == 'actions':
            categories = self.action_categories + self.custom_action_categories
            cat_string = ','.join(categories)
            params.append('actions:' + cat_string)

        if content == 'pending':
            params.append('actions')

        if self.boxlayout in ['drawer', 'drawer_notitle']:
            params.append('boxstate')
                
        return params

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
