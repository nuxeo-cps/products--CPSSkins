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
  Cell Block
  a Cell Block allows to display several Templets horizontally inside a Page Block.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.Folder import Folder

from Products.CMFCore.CMFCorePermissions import View
from Products.CMFCore.utils import getToolByName

from CPSSkinsPermissions import ManageThemes
from ThemeFolder import ThemeFolder
from cpsskins_utils import rebuild_properties, callAction, \
                           verifyThemePerms, canonizeId, \
                           isBroken, moveToLostAndFound

from PageBlockContent import PageBlockContent

factory_type_information = (
    {'id': 'Cell Block',
     'meta_type': 'Cell Block',
     'description': ('_cellblock_description_'),
     'icon': 'cellblock.gif',
     'product': 'CPSSkins',
     'factory': 'addCellBlock',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': {
          '(Default)': 'cpsskins_default_view',
          'view': 'cpsskins_default_view',
          'edit': 'cpsskins_edit_form', 
          'edit_form': 'cpsskins_edit_form', 
          'addtemplet': 'cpsskins_addtemplet_form', },
     'actions': (
         {'id': 'view',
          'name': 'View',
          'action': 'cpsskins_default_view',
          'permissions': (View,)
         },
         {'id': 'edit',
          'name': 'Edit',
          'action': 'cpsskins_edit_form',
          'permissions': (ManageThemes,)
         },
         {'id': 'addtemplet',
          'name': '_action_addtemplet_',
          'action': 'cpsskins_addtemplet_form',
          'visible': 0,
          'permissions': (ManageThemes,),
          'category': 'object'
         },
     ),
    },
)

class CellBlock(ThemeFolder, PageBlockContent):
    """
    Class for cell blocks.
    """

    meta_type = "Cell Block"
    portal_type = "Cell Block"

    iscellblock = 1

    manage_options = ( Folder.manage_options )

    security = ClassSecurityInfo()

    _properties = (
        {'id': 'title', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Title', 
         'category': 'general'
        },
        {'id': 'xpos', 
         'type': 'int', 
         'mode': 'w', 
         'label': 'xpos',  
         'category': 'none',
        },
        {'id': 'height', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Height', 
         'category': 'layout'
        },
        {'id': 'maxcols', 
         'type': 'int', 
         'mode': 'w', 
         'label': 'Number of columns', 
         'category': 'layout'
        },
        {'id': 'shape', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Shape', 
         'select_variable': 'AreaShapesList', 
         'style': 'Area Shape', 
         'category' : 'style'
        },
        {'id': 'color', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Color', 
         'select_variable': 'AreaColorsList', 
         'style': 'Area Color', 
         'category' : 'style'
        },
        {'id': 'margin', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Cellblock margin',  
         'category': 'layout',
        },
      )

    def __init__(self, id, 
                 title = '',
                 xpos = 0,
                 maxcols = 1,
                 height = '', 
                 color = '',
                 shape = '',
                 margin = '',
                 **kw):
        self.id = id
        self.title = title
        self.xpos = xpos
        self.maxcols = maxcols
        self.height = height
        self.color = color
        self.shape = shape
        self.margin = margin

    security.declarePublic('isCellBlock')
    def isCellBlock(self):
        """ is a Cell Block ? """   

        return self.iscellblock

    security.declarePublic('isRenderable')
    def isRenderable(self):
        """Returns true if the Cell Block can be rendered.
        """

        return 1

    security.declarePublic('isAlignable')
    def isAlignable(self):
        """Returns true if the Cell Block can be aligned horizontally."""

        return None

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """Returns true if the Templet can be cached in RAM."""

        return None

    security.declarePublic('render')
    def render(self, shield=0, **kw):
        """Render the templet."""

        return self.render_skin(shield=shield, **kw)

    security.declarePublic('render_skin')
    def render_skin(self, shield=0,  **kw):
        """Render the cellblock's skin."""

        return self.cpsskins_cellblock(**kw)

    security.declarePublic('render_cache')
    def render_cache(self, shield=0, enable_esi=0, **kw):
        """Renders the cached version of the templet."""

        return self.render(**kw)

    security.declarePublic('getIconRelative')
    def getIconRelative(self):
        """
        Gets the Icon path, relative to the portal.
        This is needed to catalog correctly in the presence of VHM.
        """
        return self.getIcon(1)

    security.declareProtected(ManageThemes, 'rebuild')
    def rebuild(self, **kw):
        """                  
        Rebuild this page block
        """              
                         
        setperms = kw.get('setperms', 0)
        canonizeId(self)
        rebuild_properties(self)
        if setperms:
            verifyThemePerms(self)

        for (id, o) in self.objectItems():
            o = o.aq_explicit
            if isBroken(o):
                self.manage_delObjects(id)
                continue
            if getattr(o, 'isportaltemplet', 0):
                o.rebuild(**kw)
                continue
            moveToLostAndFound(self, o)
 
    security.declarePrivate('getActions')
    def getActions(self):
        """Returns the list of actions"""

        atool = getToolByName(self, 'portal_actions')
        return atool.listFilteredActionsFor(self)

    security.declarePublic('getObjects')
    def getObjects(self, edit=0, REQUEST=None):
        """
        Gets all the objects inside a Page Block.
        Returns information about each cell (width, style, visibility, ...)
        """
 
        objects = {}
        contents = {}

        maxcols = self.maxcols
        for col in range(maxcols):
            contents[col] = []

        for obj in self.objectValues():
            xpos = getattr(obj, 'xpos', 0)
            if xpos and xpos >= maxcols:
                continue

            if getattr(obj, 'isportaltemplet', 0):
                contents[xpos].append(obj)
                continue

        for col in range(maxcols):
            objects[col] = {'contents': contents[col], 
                           }
        return objects

    security.declarePublic('getVisibility')
    def getVisibility(self, REQUEST=None, **kw):
        """Returns True if the Cell Block is visible."""

        return 1

    security.declareProtected(ManageThemes, 'getVerticalPosition')
    def getVerticalPosition(self):
        """Return the page block's ypos in the theme folder."""

        container = self.aq_parent
        return container.get_object_position(self.getId())

    #
    # CSS
    #
    security.declarePublic('getCSSLayoutStyle')
    def getCSSLayoutStyle(self):
        """Returns the CSS layout style for this CellBlock."""

        css = ''
        height = self.height

        if height:
            css += 'height:%s' % height
        return css

    security.declarePublic('getCSSAreaClass')
    def getCSSAreaClass(self, level=2):
        """Return the CSS area class for this Templet.
           level = 1 for CSS1 browsers
           level = 2 for CSS2 browsers
        """

        areaclass = ''
        try:
            if level == 1:
                areaclass = \
                    'Color%s' % self.color
            elif level == 2:
                areaclass = \
                    'Shape%s Color%s' %\
                         (self.shape,
                          self.color,
                         )
        except AttributeError:
            self.rebuild()
        return areaclass

    security.declareProtected(ManageThemes, 'edit_form')
    def edit_form(self, **kw):
        """
        Call the edit action.
        """
        return callAction(self, 'edit', **kw)

    security.declareProtected(ManageThemes, 'edit')
    def edit(self, **kw):
        """
        Default edit method, changes the properties.
        """

        # remove unknown properties
        for prop in kw.keys():
            if self.hasProperty(prop):
                continue
            del kw[prop]

        self.manage_changeProperties(**kw)

    security.declareProtected(ManageThemes, 'expireCache')
    def expireCache(self):
        """Expires the cache for this Templet.
 
           In a ZEO environment, the information will propagate
           between all ZEO instances as long as the Templet still
           exists.
        """

        # XXX
        pass

    #
    # properties 
    #
    security.declarePublic('AreaColorsList')
    def AreaColorsList(self):           
        """ Returns a list of Area Color styles"""

        tmtool = getToolByName(self, 'portal_themes')
        styles = tmtool.findStylesFor(category = 'Area Color', object=self)
        if styles: 
            return styles['title']

    security.declarePublic('AreaShapesList')
    def AreaShapesList(self):           
        """ Returns a list of Area Shape styles"""

        tmtool = getToolByName(self, 'portal_themes')
        styles = tmtool.findStylesFor(category = 'Area Shape', object=self)
        if styles: 
            return styles['title']

InitializeClass(CellBlock)

def addCellBlock(dispatcher, id, REQUEST=None, **kw):
    """Add a Cell Block."""
    ob = PageBlock(id)
    container = dispatcher.Destination()
    container._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
