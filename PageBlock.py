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
  Page Block
  a Page Block is composed of Cells (columns). 
  The visual appearance of a Cell can be modified by using Cell Stylers, 
  Cell Sizers and Cell Hiders.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.Folder import Folder

from Products.CMFCore.CMFCorePermissions import View
from Products.CMFCore.utils import getToolByName

from CPSSkinsPermissions import ManageThemes
from ThemeFolder import ThemeFolder
from StylableContent import StylableContent

from cpsskins_utils import rebuild_properties, callAction, \
                           getFreeId, verifyThemePerms, canonizeId, \
                           isBroken, moveToLostAndFound

factory_type_information = (
    {'id': 'Page Block',
     'meta_type': 'Page Block',
     'description': ('_pageblock_description_'),
     'icon': 'pageblock.png',
     'product': 'CPSSkins',
     'factory': 'addPageBlock',
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
          'permissions': (View,)
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

class PageBlock(ThemeFolder, StylableContent):
    """
    Class for page blocks.
    """

    meta_type = "Page Block"
    portal_type = "Page Block"

    isportalpageblock = 1

    manage_options = ( Folder.manage_options )

    security = ClassSecurityInfo()

    _properties = (
        {'id': 'title', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Title', 
         'category': 'general'
        },
        {'id': 'closed', 
         'type': 'boolean', 
         'mode': 'w', 
         'label': 'Closed', 
         'category': 'none',
         'default': 0
        },
        {'id': 'width', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Width', 
         'category': 'general' 
        },
        {'id': 'height', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Height', 
         'category': 'general'
        },
        {'id': 'maxcols', 
         'type': 'int', 
         'mode': 'w', 
         'label': 'Number of columns', 
         'category': 'general'
        },
        {'id': 'shape', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Shape', 
         'select_variable': 'AreaShapesList', 
         'style': 'Area Shape', 
         'category' : 'general'
        },
        {'id': 'color', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Color', 
         'select_variable': 'AreaColorsList', 
         'style': 'Area Color', 
         'category' : 'general'
        },
      )

    # XXX to be fixed: title
    def __init__(self, id, 
                 title = '',
                 closed = 0,
                 maxcols = 1,
                 width = '100%', 
                 height = '', 
                 shape = 'NoBorder', 
                 color = 'Transparent', 
                 **kw):
        self.id = id
        self.title = title
        self.closed = closed
        self.maxcols = maxcols
        self.width = width
        self.height = height
        self.shape = shape
        self.color = color

    security.declarePublic('isPortalPageBlock')
    def isPortalPageBlock(self):
        """ is Portal Page Block ? """   

        return self.isportalpageblock

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
            if getattr(o, 'iscellmodifier', 0):
                o.rebuild(**kw)
                continue
            if getattr(o, 'iscellblock', 0):
                o.rebuild(**kw)
                continue
            moveToLostAndFound(self, o)

    security.declarePrivate('getActions')
    def getActions(self):
        """Returns the list of actions"""

        atool = getToolByName(self, 'portal_actions')
        return atool.listFilteredActionsFor(self)

    security.declareProtected(ManageThemes, 'add_content_form')
    def add_content_form(self, **kw):
        """
        Call the add content action.
        """
        return callAction(self, 'addcontent', **kw)

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
        del kw['type_name']

        xpos = kw.get('xpos', 0)
        ypos = kw.get('ypos', 0)

        kw['title'] = type_name
        ypos = int(ypos)
        if ypos == 0:
            newpos = ypos 
        else:
            newpos = ypos + 1

        id = getFreeId(self)
        self.invokeFactory(type_name, id, **kw)
        content = getattr(self.aq_explicit, id, None)
        if content is not None:
            self.move_object_to_position(content.getId(), newpos)
            content.xpos = int(xpos)
            verifyThemePerms(content)
            theme_container.expireCSSCache()
            theme_container.expireJSCache()
            return content
        return None

    security.declareProtected(ManageThemes, 'addCellHider')
    def addCellHider(self, **kw):
        """
        Add a Cell Hider. Returns the Cell Hider's id.
        """

        id = getFreeId(self)
        cellhider_xpos = kw.get('xpos', None)
        if cellhider_xpos is not None:
            self.invokeFactory('Cell Hider', id, xpos=int(cellhider_xpos))
            cellhider = getattr(self.aq_explicit, id, None)
            if cellhider is not None:
                verifyThemePerms(cellhider)
                return cellhider
        return None

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
            cellsizer = getattr(self.aq_explicit, id, None)
            if cellwidth is not None:
                cellsizer.edit(cellwidth=cellwidth)
            if cellsizer is not None:
                verifyThemePerms(cellsizer)
                return cellsizer
        return None

    security.declareProtected(ManageThemes, 'addCellStyler')
    def addCellStyler(self, **kw):
        """
        Add a Cell Styler. Returns the Cell Styler's id.
        """

        id = getFreeId(self)
        cellstyler_xpos = kw.get('xpos', None)
        if cellstyler_xpos is not None:
            self.invokeFactory('Cell Styler', id, xpos=int(cellstyler_xpos))
            cellstyler = getattr(self.aq_explicit, id, None)
            if cellstyler is not None:
                verifyThemePerms(cellstyler)
                return cellstyler
        return None

    security.declareProtected(ManageThemes, 'moveCell')
    def moveCell(self, **kw):
        """
        Move a cell into a given direction.
        """

        xpos = kw.get('xpos', None)
        dir = kw.get('dir', None)

        if xpos is None or dir not in ['left', 'right']:
            return None
        
        delta = 0
        if dir == 'left' and int(xpos) > 0:
            delta = -1
        
        if dir == 'right' and int(xpos) <= int(self.maxcols):
            delta = +1

        if delta == 0:
            return None

        objects_src = []
        for obj in self.objectValues():
            if hasattr(obj, 'xpos') and int(obj.xpos) == int(xpos):
                objects_src.append(obj)

        objects_dest = []
        for obj in self.objectValues():
            if hasattr(obj, 'xpos') and int(obj.xpos) == int(xpos) + delta:
                objects_dest.append(obj)

        for obj in objects_src:
            obj.xpos = obj.xpos + delta

        for obj in objects_dest:
            obj.xpos = obj.xpos - delta
        return None

    security.declarePublic('getObjects')
    def getObjects(self, edit=0, **kw):
        """
        Gets all the objects inside a Page Block.
        Returns information about each cell (width, style, visibility, ...)
        """
 
        objects = {}
        contents = {}
        cellstyler = {}
        cellsizer = {}
        cellhider = {}
        cellvisibility = {}

        maxcols = self.maxcols
        for col in range(maxcols):
            contents[col] = []
            cellstyler[col] = None
            cellsizer[col] = None
            cellhider[col] = None
            cellvisibility[col] = 1

        for obj in self.objectValues():
            xpos = getattr(obj, 'xpos', 0)
            if xpos and xpos >= maxcols:
                continue
            if getattr(obj, 'iscellhider', 0):
                cellvisibility[xpos] = obj.getVisibility(**kw)
                cellhider[xpos] = obj
                continue

            if cellvisibility[xpos] or edit:
                if getattr(obj, 'isportaltemplet', 0):
                    if obj.getVisibility(**kw) or edit:
                        contents[xpos].append(obj)
                        continue

                if getattr(obj, 'iscellblock', 0):
                    contents[xpos].append(obj)
                    continue

                if getattr(obj, 'iscellsizer', 0):
                    cellsizer[xpos] = obj
                    continue

                if getattr(obj, 'iscellstyler', 0):
                    cellstyler[xpos] = obj

        for col in range(maxcols):
            if edit or cellvisibility[col]:
                objects[col] = {'contents': contents[col], 
                                'cellsizer': cellsizer[col], 
                                'cellstyler': cellstyler[col],
                                'cellhider': cellhider[col],
                               }
        return objects

    security.declarePublic('getTemplets')
    def getTemplets(self):
        """Get the list of Templets
        """
        templets = []
        for obj in self.objectValues():
            o = obj.aq_explicit
            if getattr(o, 'isportaltemplet', 0):
                templets.append(obj)
            if getattr(o, 'iscellblock', 0):
                templets.extend(obj.getTemplets())
        return templets

    #
    # CSS
    #
    security.declarePublic('getCSSAreaClass')
    def getCSSAreaClass(self):
        """Returns the CSS area class for this Page Block."""

        areaclass = None
        shape = self.shape
        color = self.color
        areaclass = []
        if shape:
            areaclass.append('shape%s' % shape)
        if color:
            areaclass.append('color%s' % color)
        return ' '.join(areaclass)

    security.declarePublic('can_toggle')
    def can_toggle(self):
        """
        Can the page block be toggled ( open/close ) ?
        """

        return self.can_delete()

    security.declarePublic('can_delete')
    def can_delete(self):
        """ Can the page block be deleted ?
            Not if it contains a 'main content' templet
        """
           
        for obj in self.objectValues():
            o = obj.aq_explicit
            if getattr(o, 'ismaincontent', 0):
                return None
        return 1

    security.declareProtected(ManageThemes, 'toggle')
    def toggle(self):
        """
        Open / close the page block
        """

        self.closed = not self.closed

    security.declareProtected(ManageThemes, 'getVerticalPosition')
    def getVerticalPosition(self):
        """ 
        Return the page block's ypos in the theme folder
        """

        container = self.aq_parent
        return container.get_object_position(self.getId())

    security.declareProtected(ManageThemes, 'move')
    def move(self, direction=None):
        """
        Move the page block into a direction
        """

        container = self.aq_parent

        if direction == 'up' and self.can_moveup():
            newpos = self.moveup_pos()
            return container.move_object_to_position(self.getId(), newpos)

        if direction == 'down' and self.can_movedown():
            newpos = self.movedown_pos()
            return container.move_object_to_position(self.getId(), newpos)
        return None

    security.declareProtected(ManageThemes, 'moveup')
    def moveup(self):
        """
        Move the page block up
        """

        return self.move('up')

    security.declareProtected(ManageThemes, 'movedown')
    def movedown(self):
        """
        Move the page block down
        """

        return self.move('down')

    security.declareProtected(ManageThemes, 'movetop')
    def movetop(self):
        """
        Move the page block to the top of the canvas
        """

        ypos_list = [p.getVerticalPosition() for p in self.getPageBlocks()]
        top_ypos = min(ypos_list)
        self.move_object_to_position(self.getId(), top_ypos)

    security.declarePublic('can_moveup')
    def can_moveup(self):
        """
        Can the page block be moved up?
        """

        container = self.aq_parent
        this_pos = container.get_object_position(self.getId())
        for obj in container.objectValues():
            o = obj.aq_explicit
            if getattr(o, 'isportalpageblock', 0):
                pos = container.get_object_position(obj.getId())
                if pos < this_pos:
                    return 1
        return None

    security.declarePublic('can_movedown')
    def can_movedown(self):
        """
        Can the page block be moved down?
        """

        container = self.aq_parent
        this_pos = container.get_object_position(self.getId())
        for obj in container.objectValues():
            o = obj.aq_explicit
            if getattr(o, 'isportalpageblock', 0):
                pos = container.get_object_position(obj.getId())
                if pos > this_pos:
                    return 1
        return None

    security.declarePublic('moveup_pos')
    def moveup_pos(self):
        """
        Return the new position
        """

        container = self.aq_parent
        this_pos = container.get_object_position(self.getId())
        newpos = -1
        for obj in container.objectValues():
            o = obj.aq_explicit
            if getattr(o, 'isportalpageblock', 0):
                pos = container.get_object_position(obj.getId())
                if pos > newpos and pos < this_pos:
                    newpos = pos

        if newpos >= 0:
            return newpos
        return None

    security.declarePublic('movedown_pos')
    def movedown_pos(self):
        """
        Return the new position
        """
          
        container = self.aq_parent
        this_pos = container.get_object_position(self.getId())
        for obj in container.objectValues():
            o = obj.aq_explicit
            if getattr(o, 'isportalpageblock', 0):
                pos = container.get_object_position(obj.getId())
                if pos > this_pos:
                    return pos
        return None

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

    security.declareProtected(ManageThemes, 'delete')
    def delete(self):
        """
        Delete the page block 
        """

        theme_container = self.aq_parent
        theme_container.manage_delObjects(self.getId())

InitializeClass(PageBlock)

def addPageBlock(dispatcher, id, REQUEST=None, **kw):
    """Add a Page Block."""
    ob = PageBlock(id)
    container = dispatcher.Destination()
    container._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
