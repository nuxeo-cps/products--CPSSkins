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
  Base Palette
"""

from Globals import InitializeClass, DTMLFile
from AccessControl import ClassSecurityInfo
from OFS.PropertyManager import PropertyManager
from OFS.SimpleItem import SimpleItem

from Products.CMFCore.DynamicType import DynamicType

from CPSSkinsPermissions import ManageThemes
from cpsskins_utils import callAction, renderMeth

factory_type_information = (
    {'id': 'Base Palette',
     'meta_type': 'Base Palette',
     'description': ('A Base Palette is the most basic palette.'),
     'icon': 'palette_icon.png',
     'product': 'CPSSkins',
     'factory': 'addBasePalette',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'aliases': {
          '(Default)': 'cpsskins_palette_view',
          'edit': 'cpsskins_edit_form', 
          'edit_form': 'cpsskins_edit_form', 
          'delete': 'cpsskins_object_delete', },
     'actions': (
         {'id': 'view',
          'name': 'View',
          'action': 'cpsskins_palette_view',
          'permissions': ()
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
         {'id': 'isportalpalette',
          'name': 'isportalpalette',
          'action': 'isPortalPalette',
          'visible': 0,
          'permissions': ()
         },
     ),
    },
)

class BasePalette(DynamicType, PropertyManager, SimpleItem):
    """
    Base class for palettes
    """

    meta_type = None
    portal_type = None

    isportalpalette = 1

    manage_options = ( PropertyManager.manage_options  # Properties
                     + ( {'label': 'Preview',
                          'action': 'manage_palettePreview'}, )
                     )

    security = ClassSecurityInfo()
    security.declarePublic( 'manage_palettePreview')
    manage_palettePreview = DTMLFile('zmi/manage_palettePreview', globals())

    _aliases = factory_type_information[0]['aliases']
    _actions = factory_type_information[0]['actions']

    _properties = (
        {'id': 'title', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Title'
        },
    )

    def __init__(self, id, 
                 title= 'Palette', 
                 **kw):
        self.id = id
        self.title = title

    security.declarePublic('isPortalPalette')
    def isPortalPalette(self):
        """Returns True is this is a palette."""
           
        return self.isportalpalette

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

    security.declarePublic( 'can_delete')
    def can_delete(self):
        """Can the palette be deleted?"""

        return 1

    security.declarePublic('getInfo')
    def getInfo(self):
        """Returns information about the palette"""

        infoblock = {}
        actions_list = ['delete']
        ti = self.getTypeInfo()
        for actionid in actions_list:  
            actioninfo = {}
            if actionid == 'delete':
                actioninfo['can_delete'] = self.can_delete()
            action = ti.getActionById(actionid)
            obj = self.unrestrictedTraverse(action, default=None)
            if obj is None:
                continue
            actioninfo['url']  = self.absolute_url() + '/' + obj.getId()
            infoblock[actionid] = actioninfo
        return infoblock 

    security.declareProtected(ManageThemes, 'preview')
    def preview(self, **kw):    
        """Renders a preview of the palette."""

        return renderMeth(self, 'preview_method', **kw)

InitializeClass(BasePalette)

def addBasePalette(dispatcher, id, REQUEST=None):
    """Add a Base Palette."""
    ob = BasePalette(id)
    container = dispatcher.Destination()
    container._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
