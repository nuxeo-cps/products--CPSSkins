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
  Base Style
"""

from Globals import InitializeClass, DTMLFile
from Acquisition import aq_base
from AccessControl import ClassSecurityInfo
from OFS.PropertyManager import PropertyManager
from OFS.SimpleItem import SimpleItem

from Products.CMFCore.DynamicType import DynamicType
from Products.CMFCore.utils import getToolByName

from CPSSkinsPermissions import ManageThemes
from cpsskins_utils import rebuild_properties, callAction, renderMeth, \
                           getFreeId, getFreeTitle, canonizeStyleTitle, \
                           verifyThemePerms, canonizeId

factory_type_information = (
    {'id': 'Base Style',
     'meta_type': 'Base Style',
     'description': ('A Base Style is the most basic style.'),
     'icon': 'style_icon.png',
     'product': 'CPSSkins',
     'factory': 'addBaseStyle',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'aliases': {
          '(Default)': 'cpsskins_style_view',
          'edit': 'cpsskins_edit_form', 
          'edit_form': 'cpsskins_edit_form', 
          'delete': 'cpsskins_object_delete', },
     'actions': (
         {'id': 'view',
          'name': 'View',
          'action': 'cpsskins_style_view',
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
         {'id': 'isportalstyle',
          'name': 'isportalstyle',
          'action': 'isPortalStyle',
          'visible': 0,
          'permissions': ()
         },
     ),
    },
)

class BaseStyle(DynamicType, PropertyManager, SimpleItem):
    """
    Base class for styles
    """

    meta_type = None
    portal_type = None

    isportalstyle = 1

    manage_options = ( PropertyManager.manage_options      # Properties
                     + ( {'label': 'Preview',
                         'action': 'manage_stylePreview'}, )
                     )

    security = ClassSecurityInfo()
    security.declarePublic('manage_stylePreview')
    manage_stylePreview = DTMLFile('zmi/manage_stylePreview', globals())

    _aliases = factory_type_information[0]['aliases']
    _actions = factory_type_information[0]['actions']

    _properties = (
        {'id': 'title', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Title'
        },
        {'id': 'default', 
         'type': 'boolean', 
         'mode': 'w', 
         'label': 'Default', 
         'category': 'none',
         'default': 0,
        },
    )

    def __init__(self, id, 
                 title= 'Style', 
                 default=0,
                 **kw):
        self.id = id
        self.title = title
        self.default = default
                                

    security.declarePublic('isPortalStyle')
    def isPortalStyle(self):
        """Returns True is this is a style."""
           
        return self.isportalstyle

    security.declarePublic('isDefaultStyle')
    def isDefaultStyle(self):
        """Returns True is this is a default style."""

        return getattr(self, 'default', None)
           
    security.declareProtected(ManageThemes, 'setAsDefault')
    def setAsDefault(self):
        """Sets as the default style name for a type."""
         
        tmtool = getToolByName(self, 'portal_themes')
        theme_container = tmtool.getPortalThemeRoot(self)
        meta_type = getattr(self, 'meta_type', None)
        if meta_type is not None:
            styles = theme_container.getStyles(meta_type=meta_type)
            for style in styles:
                style.default = 0
            self.default = 1
             
    security.declarePublic('getTitle')
    def getTitle(self):
        """Gets the style's title."""

        return getattr(self, 'title', None)

    security.declareProtected(ManageThemes, 'rebuild')
    def rebuild(self, **kw):
        """Rebuilds this style."""

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

        tmtool = getToolByName(self, 'portal_themes')
        theme_container = tmtool.getPortalThemeRoot(self)
        title = kw.get('title', None)
        current_title = self.getTitle()
        if title is None:
            title = current_title
        title = canonizeStyleTitle(title)
        if title != current_title:
            styles_dir = theme_container.getStylesFolder()
            title = getFreeTitle(styles_dir, title)
        self.findParents(newtitle=title)
        kw['title'] = title

        # remove unknown properties
        for prop in kw.keys():
            if self.hasProperty(prop):
                continue
            del kw[prop]

        self.manage_changeProperties(**kw)
        theme_container.expireCSSCache()

    security.declarePublic('getStyleImages')
    def getStyleImages(self):
        """Returns the list of images used by a style as a dictionary:
           {'id': <image id>, 
            'prop': <style's property>,
            'category': <icons|backgrounds|...>
           }
        """

        list = []
        for propid in self.propertyIds():
            prop_map = self.propertyMap()
            for obj in prop_map:            
                if obj['id'] == propid:                
                    image = obj.get('image', None)
                    if image:
                        value = getattr(self, propid)
                        if value == '':
                            continue
                        list.append({'id': value, 
                                     'prop': propid, 
                                     'category': image
                                    }
                        )
        return list

    security.declarePublic('findParents')
    def findParents(self, newtitle=None):
        """Find the style's parents.
           If the 'newtitle' parameter is passed, the style's title 
           will be updated in every object that uses the style.
        """

        style_title = self.getTitle()
        meta_type = self.meta_type

        tmtool = getToolByName(self, 'portal_themes')
        theme_container = tmtool.getPortalThemeRoot(self)
        parents = []

        for obj in theme_container.getPageBlocks():
            # page blocks
            for pm in aq_base(obj).propertyMap():
                if pm.get('style') != meta_type:
                    continue
                style_type = pm.get('id')
                style = getattr(obj, style_type, None)
                if style != style_title:
                    continue
                rebuild_properties(obj)
                parents.append(obj)
                if newtitle is None:
                    continue
                obj.edit(**{style_type:newtitle})

            # cell blocks
            for obj2 in obj.objectValues():
                for pm in aq_base(obj2).propertyMap():
                    if pm.get('style') != meta_type:
                        continue
                    style_type = pm.get('id')
                    style = getattr(obj2, style_type, None)
                    if style != style_title:
                        continue
                    rebuild_properties(obj2)
                    parents.append(obj2)
                    if newtitle is None:
                        continue
                    obj2.edit(**{style_type:newtitle})

        for pm in theme_container.propertyMap():
            if pm.get('style') != meta_type:
                continue
            style_type = pm.get('id')
            style = getattr(theme_container.aq_inner.aq_explicit, style_type, None)
            if style != style_title:
                continue
            rebuild_properties(theme_container)
            parents.append(theme_container)
            if newtitle is None:
                continue
            theme_container.edit(**{style_type:newtitle})

        return parents

    security.declarePublic('isOrphan')
    def isOrphan(self):
        """Returns True is the style is an orphan"""

        parents = self.findParents()
        if len(parents) == 0:
       	    return 1
        return None

    security.declareProtected(ManageThemes, 'copy_to_theme')
    def copy_to_theme(self, dest_theme=None, REQUEST=None):
        """Copies the style to another theme.
           returns the new object
        """

        if dest_theme is None:
            return self
        container = self.aq_parent

        tmtool = getToolByName(self, 'portal_themes')
        theme_container = tmtool.getPortalThemeRoot(self)
        dest_theme_container = tmtool.getThemeContainer(theme=dest_theme)
        if dest_theme_container is None:
            return self

        # save the default style
        meta_type = getattr(self, 'meta_type', None)
        default_style = dest_theme_container.getDefaultStyleByType(meta_type)

        # copy the style
        dest_container = dest_theme_container.getStylesFolder()
        cookie = container.manage_copyObjects(self.getId(), REQUEST=REQUEST)
        res = dest_container.manage_pasteObjects(cookie) 
        new_id = res[0]['new_id']            
        style = getattr(dest_container, new_id)
        verifyThemePerms(style)            
        newtitle = getFreeTitle(dest_container, style.getTitle())
        setattr(style, 'title', newtitle)

        # resets the default style
        if default_style is not None:
            default_style.setAsDefault()

        # copy the style's images as well
        for img in self.getStyleImages():
            category = img['category']
            image_dir = theme_container.getImageFolder(category=category)
            dest_image_dir = dest_container.getImageFolder(category=category)
            if image_dir is None:
                continue
            img_id = img['id']
            src_img = getattr(image_dir, img_id)
            dest_img = getattr(dest_image_dir, img_id, None)
            if dest_img:
                if dest_img.data == src_img.data:
                    continue
            cookie = image_dir.manage_copyObjects(img_id, REQUEST=REQUEST)
            res = dest_image_dir.manage_pasteObjects(cookie) 
            new_id = res[0]['new_id']            
            if new_id != img_id:
                style.edit({img['prop']:new_id})
        return style

    security.declareProtected(ManageThemes, 'duplicate')
    def duplicate(self):
        """Duplicate a Style."""
        
        tmtool = getToolByName(self, 'portal_themes')
        theme_container = tmtool.getThemeContainer()
        theme_container.invalidateCSSCache()
        container = self.aq_parent
        newid = getFreeId(container)
        container.manage_clone(self, newid)
        newobj = getattr(container, newid, None)
        newobj.rebuild()
        newtitle = getFreeTitle(container, self.getTitle())
        newobj.manage_changeProperties({'title':newtitle})
        verifyThemePerms(newobj)
        return newobj

    security.declarePublic('can_delete')
    def can_delete(self):
        """Can the style be deleted?"""

        return 1

    security.declarePublic('getInfo')
    def getInfo(self):
        """Returns some information about the style"""

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
        """Renders a preview of the style."""

        return renderMeth(self, 'preview_action', **kw)

    security.declarePublic('render')
    def render(self, **kw):
        """Renders the style."""

        return renderMeth(self, 'render_action', **kw)

InitializeClass(BaseStyle)

def addBaseStyle(dispatcher, id, REQUEST=None):
    """Add a Base Style."""
    ob = BaseStyle(id)
    container = dispatcher.Destination()
    container._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
