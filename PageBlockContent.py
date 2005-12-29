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
  Page Block content
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base, aq_inner, aq_parent
from OFS.PropertyManager import PropertyManager
from OFS.SimpleItem import SimpleItem

from Products.CMFCore.DynamicType import DynamicType
from Products.CMFCore.utils import getToolByName

from CPSSkinsPermissions import ManageThemes
from cpsskins_utils import getFreeId, verifyThemePerms

from zope.interface import implements
from Products.CPSSkins.interfaces import IPageBlockContent


class PageBlockContent(DynamicType, PropertyManager, SimpleItem):
    """
    Page Block Content
    """

    implements(IPageBlockContent)

    security = ClassSecurityInfo()

    security.declareProtected(ManageThemes, 'getVerticalPosition')
    def getVerticalPosition(self):
        """Return the object's ypos position."""

        container = self.getContainer()
        return container.get_object_position(self.getId())

    security.declarePublic('moveleft_pos')
    def moveleft_pos(self):
        """Can the templet be moved to the left?"""

        if self.can_moveleft():
            return self.xpos -1
        return None

    security.declarePublic('moveright_pos')
    def moveright_pos(self):
        """Returns the new position."""

        if self.can_moveright():
            return self.xpos + 1
        return None

    security.declarePublic('moveup_pos')
    def moveup_pos(self):
        """Returns the new position."""

        container = self.getContainer()
        this_pos = self.getVerticalPosition()
        newpos = -1
        for obj in container.objectValues():
            o = aq_base(obj)
            if not (getattr(o, 'isportaltemplet', 0) or \
                    getattr(o, 'iscellblock', 0)):
                continue
            if obj.xpos != self.xpos:
                continue
            pos = obj.getVerticalPosition()
            if pos > newpos and pos < this_pos:
                newpos = pos
        return newpos

    security.declarePublic('movedown_pos')
    def movedown_pos(self):
        """Returns the new position."""

        container = self.getContainer()
        this_pos = self.getVerticalPosition()
        newpos = -1
        for obj in container.objectValues():
            o = aq_base(obj)
            if not (getattr(o, 'isportaltemplet', 0) or \
                    getattr(o, 'iscellblock', 0)):
                continue
            if obj.xpos != self.xpos:
                continue
            pos = obj.getVerticalPosition()
            if  pos > this_pos:
                newpos = pos
                break
        return newpos

    security.declarePublic('can_delete')
    def can_delete(self):
        """Can the templet be deleted?"""

        return 1

    security.declarePublic('can_moveup')
    def can_moveup(self):
        """Can the templet be moved up?"""

        # find a page block above it
        container = self.getContainer()
        if container.can_moveup():
            return 1

        # otherwise find a templet above it
        this_pos = self.getVerticalPosition()
        for obj in container.objectValues():
            o = aq_base(obj)
            if not (getattr(o, 'isportaltemplet', 0) or \
                    getattr(o, 'iscellblock', 0)):
                continue
            if obj.xpos != self.xpos:
                continue
            pos = obj.getVerticalPosition()
            if pos < this_pos:
                return 1
        return None

    security.declarePublic('can_movedown')
    def can_movedown(self):
        """Can the templet be moved down?"""

        container = self.getContainer()
        if container.can_movedown():
            return 1

        this_pos = self.getVerticalPosition()
        for obj in container.objectValues():
            o = aq_base(obj)
            if not (getattr(o, 'isportaltemplet', 0) or \
                    getattr(o, 'iscellblock', 0)):
                continue
            if obj.xpos != self.xpos:
                continue
            pos = obj.getVerticalPosition()
            if pos > this_pos:
                return 1
        return None

    security.declarePublic('can_moveright')
    def can_moveright(self):
        """Can the templet be moved to the right?"""

        container = self.getContainer()
        maxcols = getattr(container, 'maxcols', None)
        if maxcols is None:
            return None
        if self.xpos < maxcols -1 :
            return 1
        return None

    security.declarePublic('can_moveleft')
    def can_moveleft(self):
        """Can the templet be moved to the left?"""

        if self.xpos > 0:
            return 1
        return None

    security.declareProtected(ManageThemes, 'duplicate')
    def duplicate(self):
        """Duplicates a Templet."""

        container = self.getContainer()
        src_ypos = self.getVerticalPosition()
        newid = getFreeId(container)
        container.manage_clone(self, newid)
        newobj = getattr(container, newid, None)
        container.move_object_to_position(newobj.getId(), src_ypos + 1)

        # if the Templet is a portlet box create a new Templet
        # setting the portlet_id to None and calling the edit() method
        # forces the creation of a new portlet

        # XXX: should be rewritten as templet.duplicatePortlet()
        if getattr(aq_base(newobj), 'isportletbox', 0):
            newobj.setPortletId(portlet_id=None)
            newobj.edit(**{'portlet_type': newobj.portlet_type})

        # needed for the ImageBox
        setattr(newobj, 'id', newid)
        verifyThemePerms(newobj)
        newobj.expireCache()
        return newobj

    security.declareProtected(ManageThemes, 'move_to_block')
    def move_to_block(self, dest_block=None,
                            xpos=None, ypos=None, REQUEST=None):
        """Move the object to a given block.
           Returns the instance of the object that has been moved
        """

        utool = getToolByName(self, 'portal_url')

        if xpos is None:
            return None
        if ypos is None:
            return None

        current_xpos = self.xpos
        new_xpos = int(xpos)
        self.xpos = new_xpos

        src_container = self.getContainer()
        src_block = utool.getRelativeUrl(src_container)
        if dest_block is None:
            dest_block = src_block

        current_ypos = self.getVerticalPosition()

        if dest_block == src_block and \
                        int(xpos) == current_xpos and \
                        int(ypos) == current_ypos:
            return None

        dest_container = self.unrestrictedTraverse(dest_block, default=None)

        if dest_container is not None:
            cookie = src_container.manage_copyObjects([self.getId()])
            res = dest_container.manage_pasteObjects(cookie)
            new_id = res[0]['new_id']
            newpos = int(ypos)
            if dest_block == src_block:
                if newpos > current_ypos:
                    newpos += 1
            dest_container.move_object_to_position(new_id, newpos)
            content = getattr(dest_container, new_id, None)
            if content is None:
                return None
            src_container.manage_delObjects([self.getId()])
            verifyThemePerms(content)
            content.expireCache()
            return content
        return None

    security.declareProtected(ManageThemes, 'copy_to_theme')
    def copy_to_theme(self, dest_theme=None, dest_page=None, REQUEST=None):
        """Copies the Templet to another theme.
           The copied object is placed into the first available Page Block.
           returns the copied object
        """

        tmtool = getToolByName(self, 'portal_themes')
        # the destination theme is mandatory
        if dest_theme is None:
            return None

        # the destination page is mandatory
        if dest_page is None:
            return None

        # give up if the specified theme does not exist
        dest_theme_container = tmtool.getThemeContainer(dest_theme)
        if dest_theme_container is None:
            return None

        # give up if the specified page does not exist
        dest_page_container = dest_theme_container.getPageContainer(dest_page)
        if dest_page_container is None:
            return None

        # make sure that the destination page has page blocks
        # otherwise create one on the fly
        pageblocks = dest_page_container.getPageBlocks()
        if len(pageblocks) > 0:
            dest_container = pageblocks[0]
        else:
            dest_container = dest_page_container.addPageBlock()

        # copy the content to the destination container
        container = self.getContainer()
        cookie = container.manage_copyObjects(self.getId(), REQUEST=REQUEST)
        res = dest_container.manage_pasteObjects(cookie)
        new_id = res[0]['new_id']
        templet = getattr(dest_container, new_id)
        verifyThemePerms(templet)
        templet.xpos = 0
        templet.ypos = 0
        templet.expireCache()
        dest_container.expireCSSCache()
        dest_container.expireJSCache()
        return templet

    security.declareProtected(ManageThemes, 'move')
    def move(self, direction=None, REQUEST=None, **kw):
        """Moves the templet into a direction
           Returns the instance of the moved object
        """

        templet = self
        container = self.getContainer()
        if direction == 'left' and self.can_moveleft():
            self.xpos = self.moveleft_pos()

        if direction == 'right' and self.can_moveright():
            self.xpos = self.moveright_pos()

        if direction == 'up' and self.can_moveup():
            newpos = self.moveup_pos()
            if newpos >= 0:
                container.move_object_to_position(self.getId(), newpos)
            else:
                cookie = container.manage_cutObjects(self.getId(),
                                                     REQUEST=REQUEST)
                pos =  container.moveup_pos()
                theme_container = container.getContainer()
                for obj in theme_container.objectValues():
                    if theme_container.get_object_position(obj.getId()) == pos:
                        obj.manage_pasteObjects(cookie)
                        maxcols = getattr(obj, 'maxcols', None)
                        if maxcols is not None and self.xpos > maxcols-1:
                            self.xpos = maxcols - 1
                        templet = getattr(obj, self.getId(), None)

        if direction == 'down' and self.can_movedown():
            newpos = self.movedown_pos()
            if newpos >= 0:
                container.move_object_to_position(self.getId(), newpos)
            else:
                cookie = container.manage_cutObjects(self.getId(),
                                                     REQUEST=REQUEST)
                pos =  container.movedown_pos()
                theme_container = container.getContainer()
                for obj in theme_container.objectValues():
                    if theme_container.get_object_position(obj.getId()) == pos:
                        obj.manage_pasteObjects(cookie)
                        newobj =  getattr(obj, self.getId(), None)
                        obj.move_object_to_position(newobj.getId(), int(0))

                        maxcols = getattr(obj, 'maxcols', None)
                        if maxcols is not None and self.xpos > maxcols-1:
                            self.xpos = maxcols - 1
                        templet = newobj
        templet.expireCache()
        return templet

    security.declareProtected(ManageThemes, 'moveleft')
    def moveleft(self):
        """Moves the templet to the left.
           Returns the instance of the moved object
        """

        return self.move(direction='left')

    security.declareProtected(ManageThemes, 'moveright')
    def moveright(self):
        """Moves the templet to the right.
           Returns the instance of the moved object
        """

        return self.move(direction='right')

    security.declareProtected(ManageThemes, 'moveup')
    def moveup(self):
        """Moves the templet upwards
           Returns the instance of the moved object
        """

        return self.move(direction='up')

    security.declareProtected(ManageThemes, 'movedown')
    def movedown(self):
        """Moves the templet downwards.
           Returns the instance of the moved object
        """

        return self.move(direction='down')

    security.declareProtected(ManageThemes, 'change_alignment')
    def change_alignment(self, alignment=None):
        """Aligns the templet."""

        if alignment in self.listHorizontalAlignments():
            self.setProperty('align', alignment)

    security.declareProtected(ManageThemes, 'setProperty')
    def setProperty(self, prop=None, value=None):
        """Sets a property."""

        if value is not None and self.hasProperty(prop):
            self.manage_changeProperties(**{prop:value})
            self.expireCache()

    security.declarePublic('getContainer')
    def getContainer(self):
        """Return the content's container"""

        return aq_parent(aq_inner(self))

    security.declarePublic('getPage')
    def getPage(self):
        """Return the content's page"""

        return aq_parent(aq_inner(aq_parent(aq_inner(self))))

    #
    # Properties
    #
    security.declarePublic('listHorizontalAlignments')
    def listHorizontalAlignments(self):
        """Returns a list of alignments for this object."""

        list = ['left', 'center', 'right', 'justify']
        return list

InitializeClass(PageBlockContent)
