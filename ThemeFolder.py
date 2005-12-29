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
  Theme Folder
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Acquisition import aq_parent, aq_inner, aq_base

from Products.CMFCore.PortalFolder import PortalFolder

from CPSSkinsPermissions import ManageThemes
from Products.CPSSkins.cpsskins_utils import getFreeTitle

from Products.CPSSkins.interfaces import implements
from Products.CPSSkins.interfaces import IThemeFolder


factory_type_information = (
    {'id': 'Theme Folder',
     'meta_type': 'Theme Folder',
     'description': ('A Theme Folder contain theme items.'),
     'icon': 'themefolder.png',
     'product': 'CPSSkins',
     'factory': 'addThemeFolder',
     'filter_content_types': 0,
     'immediate_view': '',
     'global_allow': 0,
     'actions': (
         {'id': 'view',
          'name': 'View',
          'action': 'folder_view',
          'permissions': ()
         },
    ),
   },
)

class ThemeFolder(PortalFolder):
    """
    Class for Theme Folder.
    """

    implements(IThemeFolder)

    meta_type = "Theme Folder"
    portal_type = "Theme Folder"
    isthemefolder = 1

    manage_options = ( PortalFolder.manage_options[0:3] )

    security = ClassSecurityInfo()

    description = ''

    def __init__(self, id, title = ''):
        self.id = id
        self.title = title

    security.declarePublic('isThemeFolder')
    def isThemeFolder(self):
        """ is Theme Folder? """

        return self.isthemefolder

    #
    # Order support
    #
    security.declarePublic('get_object_position')
    def get_object_position(self, id):
        """ Gets the objects' position in an ordered folder
        """
        i = 0
        for obj in self._objects:
            if obj['id'] == id:
                return i
            i = i+1
        # If the object was not found, throw an error.
        raise 'ObjectNotFound', 'The object with the id "%s" does not exist.' % id

    security.declareProtected(ManageThemes, 'move_object_to_position')
    def move_object_to_position(self, id, newpos):
        """ Sets the objects' position in an ordered folder
        """
        oldpos = self.get_object_position(id)
        if (newpos < 0 or newpos == oldpos or newpos >= len(self._objects)):
            return None
        obj = self._objects[oldpos]
        objects = list(self._objects)
        del objects[oldpos]
        objects.insert(newpos, obj)
        self._objects = tuple(objects)
        return 1

    security.declarePublic('getContainer')
    def getContainer(self):
        """Return the folder's container"""

        return aq_parent(aq_inner(self))

    security.declareProtected(ManageThemes, 'cutObjects')
    def cutObjects(self, ids=[], REQUEST=None):
        """Cut a list of objects
        """
        if REQUEST is None:
            REQUEST = self.REQUEST
        self.manage_cutObjects(ids, REQUEST)

        RESPONSE = REQUEST.RESPONSE
        redirect_url = REQUEST['HTTP_REFERER']
        RESPONSE.redirect(redirect_url)

    security.declareProtected(ManageThemes, 'copyObjects')
    def copyObjects(self, ids=[], REQUEST=None):
        """Copy a list of objects
        """

        if REQUEST is None:
            REQUEST = self.REQUEST
        self.manage_copyObjects(ids, REQUEST)

        RESPONSE = REQUEST.RESPONSE
        redirect_url = REQUEST['HTTP_REFERER']
        RESPONSE.redirect(redirect_url)

    security.declareProtected(ManageThemes, 'pasteObjects')
    def pasteObjects(self, REQUEST=None):
        """Paste a list of objects
        """
        if REQUEST is None:
            REQUEST = self.REQUEST

        if REQUEST.has_key('__cp'):
            cp = REQUEST['__cp']
        if cp is not None:
            result = self.manage_pasteObjects(cp)

            # style titles should be unique
            container = self
            for res in result:
                new_id = res['new_id']
                obj = getattr(self.aq_inner.aq_explicit, new_id, None)
                if obj is None:
                    continue
                if getattr(aq_base(obj), 'isportalstyle', 0):
                    title = obj.getTitle()
                    newtitle = getFreeTitle(container=container,
                        title=title,
                        type_name=obj.meta_type,
                        exclude_self=1)
                    obj.manage_changeProperties(title=newtitle)

        RESPONSE = REQUEST.RESPONSE
        redirect_url = REQUEST['HTTP_REFERER']
        RESPONSE.redirect(redirect_url)

    security.declareProtected(ManageThemes, 'deleteObjects')
    def deleteObjects(self, ids=[], REQUEST=None):
        """Delete a list of objects
        """
        if REQUEST is None:
            REQUEST = self.REQUEST
        self.manage_delObjects(ids)

        RESPONSE = REQUEST.RESPONSE
        redirect_url = REQUEST['HTTP_REFERER']
        RESPONSE.redirect(redirect_url)

    security.declareProtected(ManageThemes, 'getPastableObjects')
    def getPastableObjects(self, meta_type=None, REQUEST=None):
        """Returns a list of objects from the clipboard that can
           be pasted into this folder.
        """

        if REQUEST is None:
            REQUEST = self.REQUEST

        if meta_type is None:
            return []

        try:
            items = self.cb_dataItems()
        except (KeyError, AttributeError):
            items = []

        pastableItems = [item for item in items
            if item.meta_type == meta_type]
        if len(pastableItems) < len(items):
            pastableItems = []
        return pastableItems


InitializeClass(ThemeFolder)

def addThemeFolder(dispatcher, id, REQUEST=None, **kw):
    """Add a Theme Folder."""
    ob = ThemeFolder(id, **kw)
    container = dispatcher.Destination()
    container._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
