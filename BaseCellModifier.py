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
  Base Cell Modifier
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.PropertyManager import PropertyManager
from OFS.SimpleItem import SimpleItem

from Products.CMFCore.CMFCorePermissions import View
from Products.CMFCore.DynamicType import DynamicType

from CPSSkinsPermissions import ManageThemes
from cpsskins_utils import rebuild_properties, callAction, \
                           verifyThemePerms, canonizeId

factory_type_information = (
    {'id': 'Base Cell Modifier',
     'meta_type': 'Base CellModifier',
     'description': ('A Base Cell Modifier is the most basic cell modifier.'),
     'icon': 'skinner_icon.gif',
     'product': 'CPSSkins',
     'factory': 'addBaseCellModifier',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'aliases': {
          '(Default)': 'cpsskins_default_view',
          'view': 'cpsskins_default_view',
          'edit': 'cpsskins_edit_form', 
          'edit_form': 'cpsskins_edit_form', },
     'actions':  (
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
         {'id': 'delete',
          'name': 'Delete',
          'action': 'cpsskins_object_delete',
          'visible': 0,
          'permissions': (ManageThemes,)
         },
     ),
    },
)

class BaseCellModifier(DynamicType, PropertyManager, SimpleItem):
    """
    Base class for cell modifiers.
    """

    meta_type = None
    portal_type = None

    iscellmodifier = 1

    manage_options = ( PropertyManager.manage_options  # Properties
                     )

    security = ClassSecurityInfo()
    _aliases = factory_type_information[0]['aliases']
    _actions = factory_type_information[0]['actions']

    _properties = (
        {'id': 'xpos', 
         'type': 'int', 
         'mode': 'w', 
         'label': 'Xpos', 
         'category': 'none'
        },
    )


    def __init__(self, id, 
                 xpos = int(0), 
                 **kw):
        self.id = id
        self.xpos = xpos
 
    security.declarePublic('isCellModifier')
    def isCellModifier(self):
        """Returns true if this is a Cell Modifier"""
           
        return self.iscellmodifier

    security.declareProtected(ManageThemes, 'rebuild')
    def rebuild(self, **kw):
        """Rebuild this cell modifier."""               

        setperms = kw.get('setperms', 0)
        canonizeId(self)
        rebuild_properties(self)
        if setperms:
            verifyThemePerms(self)

    security.declareProtected(ManageThemes, 'edit_form')
    def edit_form(self, **kw):
        """Call the edit action."""

        return callAction(self, 'edit', **kw)

    security.declareProtected(ManageThemes, 'edit')
    def edit(self, **kw):
        """Default edit method, changes the properties."""

        # remove unknown properties
        for prop in kw.keys():
            if self.hasProperty(prop):
                continue
            del kw[prop]

        self.manage_changeProperties(**kw)

    security.declarePublic('getInfo')
    def getInfo(self):
        """Returns some action information."""

        infoblock = {}
        actions_list = ['delete', 'edit']

        ti = self.getTypeInfo()
        for actionid in actions_list:  
            actioninfo = {}
            if actionid == 'delete':
                actioninfo['can_delete'] = self.can_delete()
            try:
                action = ti.getActionById(actionid)
                actioninfo['url']  = self.absolute_url() + '/' + \
                                     self.restrictedTraverse(action).getId()
            except:
                continue
            infoblock[actionid] = actioninfo
        return infoblock

    security.declarePublic('can_delete')
    def can_delete(self):
        """Can the cell sizer be deleted ?"""
           
        return 1

InitializeClass(BaseCellModifier)

def addBaseCellModifier(dispatcher, id, REQUEST=None):
    """Add a Base Cell Modifier."""
    ob = BaseCellModifier(id)
    container = dispatcher.Destination()
    container._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
