# (C) Copyright 2003-2005 Chalmers University of Technology
# (C) Copyright 2007 Nuxeo SAS <http://nuxeo.com>
# Authors:
# Jean-Marc Orliaguet <jmo@ita.chalmers.se>
# M.-A. Darche <madarche@nuxeo.com>
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
  Cell Block
  a Cell Block allows to display several Templets horizontally
  inside a Page Block.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from OFS.Folder import Folder

from Products.CMFCore.utils import getToolByName

from CPSSkinsPermissions import ManageThemes
from ThemeFolder import ThemeFolder
from cpsskins_utils import rebuild_properties, callAction, \
                           getFreeId, \
                           verifyThemePerms, canonizeId, \
                           isBroken, moveToLostAndFound

from PageBlockContent import PageBlockContent
from StylableContent import StylableContent

factory_type_information = (
    {'id': 'Cell Block',
     'meta_type': 'Cell Block',
     'description': ('_cellblock_description_'),
     'icon': 'cellblock.png',
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
         {'id': 'iscellblock',
          'name': 'iscellblock',
          'action': 'iscellblock',
          'visible': 0,
          'permissions': ()
         },
     ),
    },
)

class CellBlock(ThemeFolder, PageBlockContent, StylableContent):
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
        {'id': 'margin',
         'type': 'string',
         'mode': 'w',
         'label': 'Cellblock margin',
         'category': 'layout',
        },
        {'id': 'hidden_empty',
         'type': 'boolean',
         'mode': 'w',
         'label': 'Hidden if empty',
         'category': 'layout'
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
      )

    # This variable is to know if we should hide this cell block if all
    # contained cells haven't any content. There is a choice here because
    # sometimes it might be interesting to have empty cells when those
    # empty cells are used to have a background image or for layout purpose.
    #
    # BBB will be changed in CPS 3.5.
    # This is set to False as a default to not break existing themes rendering,
    # but a saner default should be True. This will be changed in CPS 3.5.
    hidden_empty = False

    def __init__(self, id,
                 title = '',
                 xpos = 0,
                 maxcols = 2,
                 height = '',
                 color = '',
                 shape = '',
                 margin = '',
                 hidden_empty = False,
                 **kw):
        self.id = id
        self.title = title
        self.xpos = xpos
        self.maxcols = maxcols
        self.height = height
        self.color = color
        self.shape = shape
        self.margin = margin
        self.hidden_empty = hidden_empty

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
    def render_skin(self, editing=0, textonly=0, **kw):
        """Render the cellblock's skin."""

        # edit mode
        if editing:
            return self.cpsskins_cellblock_edit(**kw)
        # text mode
        if textonly:
            return self.cpsskins_cellblock_textonly(**kw)
        return self.cpsskins_cellblock(**kw)

    security.declarePublic('render_cache')
    def render_cache(self, **kw):
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

        for (id, obj) in self.objectItems():
            if isBroken(aq_base(obj)):
                self.manage_delObjects(id)
                continue
            if getattr(aq_base(obj), 'isportaltemplet', 0):
                obj.rebuild(**kw)
                continue
            if getattr(aq_base(obj), 'iscellmodifier', 0):
                obj.rebuild(**kw)
                continue
            moveToLostAndFound(self, obj)

    security.declarePrivate('getActions')
    def getActions(self):
        """Returns the list of actions"""

        atool = getToolByName(self, 'portal_actions')
        return atool.listFilteredActionsFor(self)

    security.declarePublic('getObjects')
    def getObjects(self, edit=0, **kw):
        """
        Gets all the objects inside a Page Block.
        Returns information about each cell (width, style, visibility, ...)
        """

        objects = {}
        contents = {}
        cellsizer = {}

        maxcols = self.maxcols
        for col in range(maxcols):
            contents[col] = []
            cellsizer[col] = None

        for obj in self.objectValues():
            o = aq_base(obj)
            xpos = getattr(o, 'xpos', 0)
            if xpos and xpos >= maxcols:
                continue

            if getattr(o, 'isportaltemplet', 0):
                contents[xpos].append(obj)
                continue

            if getattr(o, 'iscellsizer', 0):
                cellsizer[xpos] = obj
                continue

        for col in range(maxcols):
            objects[col] = {'contents': contents[col],
                            'cellsizer': cellsizer[col],
                           }
        return objects

    security.declarePublic('getTemplets')
    def getTemplets(self):
        """Get the list of Templets
        """
        templets = []
        for obj in self.objectValues():
            if getattr(aq_base(obj), 'isportaltemplet', 0):
                templets.append(obj)
        return templets

    security.declareProtected(ManageThemes, 'getInvisibleTemplets')
    def getInvisibleTemplets(self, **kw):
        """Returns the list of invisible templets.
        """

        invisible_templets = []
        container = self.getContainer()
        if self.xpos >= container.maxcols:
            invisible_templets.extend(self.getTemplets())
        return invisible_templets

    security.declarePublic('getVisibility')
    def getVisibility(self, **kw):
        """Returns True if the Cell Block is visible."""

        return 1

    security.declareProtected(ManageThemes, 'getVerticalPosition')
    def getVerticalPosition(self):
        """Return the page block's ypos in the theme folder."""

        container = self.getContainer()
        return container.get_object_position(self.getId())

    #
    # CSS
    #
    security.declarePublic('getCSSMarginStyle')
    def getCSSMarginStyle(self):
        """Returns the CSS margin style for this Templet."""

        margin = self.margin
        if margin:
            if margin not in ('0', '0pt', '0in', '0pc', '0mm',
                              '0cm', '0px', '0em', '0ex'):
                return 'padding: %s' % margin
        return ''

    security.declarePublic('getCSSLayoutStyle')
    def getCSSLayoutStyle(self, level=2):
        """Returns the CSS layout style for this CellBlock."""

        if level == 1:
            return ''
        css = ''
        height = self.height
        if height:
            css = 'height:%s' % height
        return css

    security.declarePublic('getCSSClass')
    def getCSSClass(self, level=2):
        """Return the CSS area class for this Templet.
           level = 1 for CSS1 browsers
           level = 2 for CSS2 browsers
        """

        areaclass = ''
        try:
            if level == 1:
                areaclass = \
                    'color%s' % self.color
            elif level == 2:
                areaclass = \
                    'shape%s color%s' %\
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

    security.declareProtected(ManageThemes, 'addContent')
    def addContent(self, **kw):
        """
        Add content. Returns the id
        """

        tmtool = getToolByName(self, 'portal_themes')
        theme_container = tmtool.getPortalThemeRoot(self)
        type_name = kw.get('type_name', None)
        if type_name is None:
            return None

        # Cell block cannot be added inside cell blocks
        # add it inside the container instead
        if type_name == self.meta_type:
            kw['xpos'] = self.xpos
            kw['ypos'] = self.getVerticalPosition()
            container = self.getContainer()
            return container.addContent(**kw)

        del kw['type_name']
        xpos = kw.get('xpos', 0)
        ypos = kw.get('ypos', 0)
        title = kw.get('title')
        if title is None:
            kw['title'] = type_name
        ypos = int(ypos)
        if ypos == 0:
            newpos = ypos
        else:
            newpos = ypos + 1

        id = getFreeId(self)
        self.invokeFactory(type_name, id, **kw)
        content = getattr(self.aq_inner.aq_explicit, id, None)
        if content is not None:
            self.move_object_to_position(content.getId(), newpos)
            content.xpos = int(xpos)
            verifyThemePerms(content)
            theme_container.expireCSSCache()
            theme_container.expireJSCache()
            return content
        return None

    security.declareProtected(ManageThemes, 'expireCache')
    def expireCache(self):
        """Expires the cache for this Templet.

           In a ZEO environment, the information will propagate
           between all ZEO instances as long as the Templet still
           exists.
        """

        # XXX
        pass

    security.declareProtected(ManageThemes, 'addCellSizer')
    def addCellSizer(self, **kw):
        """
        Add a Cell Sizer. Returns the Cell Sizer's id.
        """

        id = getFreeId(self)
        cellsizer_xpos = kw.get('xpos', None)
        cellwidth = kw.get('cellwidth', None)
        if cellsizer_xpos is not None:
            self.invokeFactory('Cell Sizer', id, xpos=int(cellsizer_xpos))
            cellsizer = getattr(self.aq_inner.aq_explicit, id, None)
            if cellwidth is not None:
                cellsizer.edit(cellwidth=cellwidth)
            if cellsizer is not None:
                verifyThemePerms(cellsizer)
                return cellsizer
        return None

InitializeClass(CellBlock)

def addCellBlock(dispatcher, id, REQUEST=None, **kw):
    """Add a Cell Block."""
    ob = CellBlock(id, **kw)
    container = dispatcher.Destination()
    container._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
