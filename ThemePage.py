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
  Theme Page
  a Theme Page is composed of Page Blocks.
  Page blocks are stacked on top of one another.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from OFS.Folder import Folder

from Products.CMFCore.utils import getToolByName

from CPSSkinsPermissions import ManageThemes
from ThemeFolder import ThemeFolder
from StylableContent import StylableContent

from cpsskins_utils import rebuild_properties, callAction, \
                           getFreeId, verifyThemePerms, canonizeId, \
                           isBroken, moveToLostAndFound

factory_type_information = (
    {'id': 'Theme Page',
     'meta_type': 'Theme Page',
     'description': ('_themepage_description_'),
     'icon': 'themepage.png',
     'product': 'CPSSkins',
     'factory': 'addThemePage',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': {
          '(Default)': 'cpsskins_default_view',
          'view': 'cpsskins_default_view',
          'edit': 'cpsskins_edit_form',
          'edit_form': 'cpsskins_edit_form',
          'addcontent': 'cpsskins_addcontent_form', },
     'actions': (
         {'id': 'view',
          'name': 'View',
          'action': 'cpsskins_default_view',
          'permissions': ()
         },
         {'id': 'edit',
          'name': 'Edit',
          'action': 'cpsskins_edit_form',
          'permissions': (ManageThemes,)
         },
         {'id': 'addcontent',
          'name': '_action_addcontent_',
          'action': 'cpsskins_addcontent_form',
          'visible': 0,
          'permissions': (ManageThemes,),
          'category': 'object'
         },
     ),
    },
)

class ThemePage(ThemeFolder, StylableContent):
    """
    Class for theme pages.
    """

    meta_type = "Theme Page"
    portal_type = "Theme Page"
    isportalthemepage = 1

    manage_options = (Folder.manage_options)

    security = ClassSecurityInfo()

    _properties = (
        {'id': 'title',
         'type': 'string',
         'mode': 'w',
         'label': 'Title',
         'category': 'general'
        },
        {'id': 'default',
         'type': 'boolean',
         'mode': 'w',
         'label': 'Default page',
         'category': 'general',
         'default': 0,
        },
        {'id': 'preview',
         'type': 'selection',
         'mode': 'w',
         'label': 'Preview',
         'select_variable': 'cpsskins_listThumbnails',
         'category': 'general',
         'image' : 'thumbnails'
        },
        {'id': 'renderer',
         'type': 'selection',
         'mode': 'w',
         'label': 'Page renderer',
         'select_variable' : 'listPageRenderers',
         'category': 'general',
         'i18n': 1,
         'i18n_prefix': '_option_',
        },
        {'id': 'align',
         'type': 'selection',
         'mode': 'w',
         'label': 'Align',
         'select_variable': 'listHorizontalAlignments',
         'category': 'layout',
         'i18n': 1,
         'i18n_prefix': '_option_',
        },
        {'id': 'shape',
         'type': 'selection',
         'mode': 'w',
         'label': 'Shape',
         'select_variable': 'listAreaShapes',
         'style': 'Area Shape',
         'category' : 'style'
        },
        {'id': 'color',
         'type': 'selection',
         'mode': 'w',
         'label': 'Color',
         'select_variable': 'listAreaColors',
         'style': 'Area Color',
         'category' : 'style'
        },
        {'id': 'margin',
         'type': 'string',
         'mode': 'w',
         'label': 'Margin',
         'category' : 'layout'
        },
      )

    def __init__(self, id,
                 title = '',
                 renderer = 'default',
                 align = '',
                 shape = '',
                 color = '',
                 margin = '0.5em',
                 default = 0,
                 preview = '',
                 **kw):
        self.id = id
        self.title = title
        self.renderer = renderer
        self.align = align
        self.shape = shape
        self.color = color
        self.margin = margin
        self.default = default
        self.preview = preview

    security.declarePublic('isPortalThemePage')
    def isPortalThemePage(self):
        """ is Portal Theme Page ? """

        return self.isportalthemepage

    security.declarePublic('getIconRelative')
    def getIconRelative(self):
        """
        Gets the Icon path, relative to the portal.
        This is needed to catalog correctly in the presence of VHM.
        """
        return self.getIcon(1)

    security.declarePublic('isDefaultPage')
    def isDefaultPage(self):
        """ is a default page ? """

        return getattr(self, 'default', None)

    security.declareProtected('Manage Themes', 'setAsDefault')
    def setAsDefault(self):
        """Set as the default page
        """
        theme_container = self.getContainer()
        theme_container.setDefaultPage(default_page=self.getId())

    #
    # Properties
    #
    security.declarePublic('isAlignable')
    def isAlignable(self):
        """ Returns true if the page can be aligned horizontally """

        return 1

    security.declarePublic('listHorizontalAlignments')
    def listHorizontalAlignments(self):
        """ Returns a list of alignments for this object"""

        list = ['left', 'center', 'right']
        return list

    security.declarePublic('listPageRenderers')
    def listPageRenderers(self):
        """ returns the list of page renderers """

        tmtool = getToolByName(self, 'portal_themes')
        return tmtool.listPageRenderers()

    #
    # CSS
    #
    security.declarePublic('getCSSLayoutStyle')
    def getCSSLayoutStyle(self):
        """Returns the CSS layout style for this theme."""

        align = self.align
        if align == 'left':
            return 'margin-left:0px;margin-right:auto;'

        elif align == 'right':
            return 'margin-left:auto;margin-right:0px;'

        elif align == 'center':
            return 'margin-left:auto;margin-right:auto;'
        return ''

    #
    # Rendering
    #
    security.declarePublic('render')
    def render(self, **kw):
        """Render the page"""

        rendered = []
        kw['layout_style'] = self.getCSSLayoutStyle()
        for pageblock in self.getPageBlocks(**kw):
            rendered.append(pageblock.render(**kw))
        return ''.join(rendered)

    #
    # Actions
    #
    security.declareProtected(ManageThemes, 'change_alignment')
    def change_alignment(self, alignment=None):
        """Aligns the templet."""

        if alignment in self.listHorizontalAlignments():
            self.setProperty('align', alignment)

    security.declarePrivate('getActions')
    def getActions(self):
        """Returns the list of actions"""

        atool = getToolByName(self, 'portal_actions')
        return atool.listFilteredActionsFor(self)

    security.declareProtected(ManageThemes, 'edit_form')
    def edit_form(self, **kw):
        """
        Call the edit action.
        """
        return callAction(self, 'edit', **kw)

    security.declareProtected(ManageThemes, 'setProperty')
    def setProperty(self, prop=None, value=None):
        """Sets a property."""

        if value is not None and self.hasProperty(prop):
            self.manage_changeProperties(**{prop:value})
    #
    # Factories
    #
    security.declareProtected(ManageThemes, 'addPageBlock')
    def addPageBlock(self, **kw):
        """Add a Page Block. Returns the Page Block object
        """
        id = getFreeId(self)
        self.invokeFactory('Page Block', title='Page Block', id=id)
        pageblock = getattr(self.aq_inner.aq_explicit, id, None)
        if pageblock is not None:
            ypos = kw.get('pageblock_ypos', None)
            if ypos:
                self.move_object_to_position(pageblock.getId(), int(ypos))
            return pageblock
        return None

    #
    # Pagelets (page elements)
    #
    security.declarePublic('getPageBlocks')
    def getPageBlocks(self, filter=1, **kw):
        """Returns a list of page blocks sorted by ypos
        """
        pageblocks = self.objectValues('Page Block')
        if not filter:
            return pageblocks
        return [p for p in pageblocks if not p.closed and p.maxcols]

    security.declarePublic('getTemplets')
    def getTemplets(self):
        """Get the list of Templets
        """
        templets = []
        for pageblock in self.getPageBlocks():
            templets.extend(pageblock.getTemplets())
        return templets

    security.declareProtected(ManageThemes, 'getI18nTemplets')
    def getI18nTemplets(self, **kw):
        """Returns the list of templets that are translated
        """
        i18n_templets = []
        for templet in self.getTemplets():
            for prop_id in templet.getI18nProperties():
                if getattr(templet, prop_id, 0) == 1 and \
                           templet not in i18n_templets:
                    i18n_templets.append(templet)
        return i18n_templets

    security.declareProtected(ManageThemes, 'getInvisibleTemplets')
    def getInvisibleTemplets(self, **kw):
        """Returns the list of invisible templets.
        """
        invisible_templets = []
        pageblocks = self.getPageBlocks()
        for pageblock in pageblocks:
            invisible_templets.extend(pageblock.getInvisibleTemplets())
        return invisible_templets

    # slots
    security.declarePublic('getSlots')
    def getSlots(self):
        """Return the list of slots used in this theme.
        """
        slots = []
        for templet in self.getTemplets():
            if getattr(aq_base(templet), 'isportalboxgroup', 0):
                slots.append(templet.getSlot())
        return slots

    #
    # RAM Cache
    #
    security.declareProtected(ManageThemes, 'expireCache')
    def expireCache(self):
        """Expires the cache for this page.
        """

        # pages are not cacheable
        pass

    #
    # Theme management
    #
    security.declareProtected(ManageThemes, 'rebuild')
    def rebuild(self, **kw):
        """Rebuild this theme page
        """
        setperms = kw.get('setperms', 0)
        canonizeId(self)
        rebuild_properties(self)
        if setperms:
            verifyThemePerms(self)

        for (id, o) in self.objectItems():
            if isBroken(aq_base(o)):
                self.manage_delObjects(id)
                continue
            if getattr(aq_base(o), 'isportalpageblock', 0):
                o.rebuild(**kw)
                continue
            moveToLostAndFound(self, o)

    security.declareProtected(ManageThemes, 'edit')
    def edit(self, **kw):
        """Default edit method, changes the properties.
        """

        # remove unknown properties
        for prop in kw.keys():
            if self.hasProperty(prop):
                continue
            del kw[prop]
        self.manage_changeProperties(**kw)

        # default page
        if kw.get('default', 0):
            theme_container = self.getContainer()
            theme_container.setDefaultPage(default_page=self.getId())

    security.declareProtected(ManageThemes, 'delete')
    def delete(self):
        """Delete the page block
        """
        theme_container = self.getContainer()
        theme_container.manage_delObjects(self.getId())

    security.declareProtected(ManageThemes, 'duplicate')
    def duplicate(self):
        """Duplicate this page
        """
        container = self.getContainer()
        newid = getFreeId(container)
        container.manage_clone(self, newid)
        newobj = getattr(container, newid, None)
        verifyThemePerms(newobj)
        # do not make the new page a default page
        newobj.default = 0
        return newobj

InitializeClass(ThemePage)

def addThemePage(dispatcher, id, REQUEST=None, **kw):
    """Add a Theme Page."""
    ob = ThemePage(id, **kw)
    container = dispatcher.Destination()
    container._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
