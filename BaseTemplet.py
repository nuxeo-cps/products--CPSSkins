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
  BaseTemplet
"""

import time
import md5

from Globals import InitializeClass, DTMLFile
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from OFS.PropertyManager import PropertyManager
from OFS.SimpleItem import SimpleItem

from Products.CMFCore.CMFCorePermissions import View
from Products.CMFCore.DynamicType import DynamicType
from Products.CMFCore.utils import getToolByName

from CPSSkinsPermissions import ManageThemes
from cpsskins_utils import rebuild_properties, callAction, \
                           getFreeId, verifyThemePerms, \
                           getObjectVisibility, canonizeId, \
                           getApplicableStylesFor, getStyleList, \
                           getAvailableLangs, getDefaultLang, html_slimmer


factory_type_information = (
    {'id': 'Base Templet',
     'meta_type': 'Base Templet',
     'description': ('A Base Templet is the most basic templet.'),
     'icon': 'templet_icon.gif',
     'product': 'CPSSkins',
     'factory': 'addBaseTemplet',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'aliases': {
          '(Default)': 'index_html',
          'view': 'cpsskins_templet_view',
          'edit': 'cpsskins_edit_form', 
          'edit_form': 'cpsskins_edit_form', },
     'actions': (
         {'id': 'view',
          'name': 'View',
          'action': 'cpsskins_templet_view',
          'visible': 1,
          'category': 'object',
          'permissions': (View,)
         },
         {'id': 'edit',
          'name': 'Edit',
          'action': 'cpsskins_edit_form',
          'visible': 1,
          'category': 'object',
          'permissions': (ManageThemes,)
         },
         {'id': 'isportaltemplet',
          'name': 'isportaltemplet',
          'action': 'isPortalTemplet',
          'visible': 0,
          'permissions': ()
         },
     ),
    },
)


class BaseTemplet(DynamicType, PropertyManager, SimpleItem):
    """
    Base class for templets.
    """

    meta_type = None
    portal_type = None

    isportaltemplet = 1

    manage_options = ( PropertyManager.manage_options     # Properties
                     + ( {'label': 'Preview',
                          'action': 'manage_templetPreview'}, )
                     )

    security = ClassSecurityInfo()
    security.declarePublic('manage_templetPreview')
    manage_templetPreview = DTMLFile('zmi/manage_templetPreview', globals())

    _aliases = factory_type_information[0]['aliases']
    _actions = factory_type_information[0]['actions']

    _properties = (
        {'id': 'title', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Title', 
         'category': 'general',
        },
        {'id': 'closed', 
         'type': 'boolean', 
         'mode': 'w', 
         'label': 'Closed', 
         'category': 'none',
         'default': 0,
        },
        {'id': 'cacheable', 
         'type': 'boolean', 
         'mode': 'w', 
         'label': 'Cacheable in RAM', 
         'category': 'Caching',
         'visible': 'isCacheable',
         'default': 0,
        },
        {'id': 'cache_lifetime', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Cache lifetime',  
         'category': 'Caching',
         'visible': 'isCached',
         'select_variable': 'LifetimeList',
         'default': '60',
         'i18n': 1,
         'i18n_prefix': '_option_lifetime_',
        },
        {'id': 'hidden_in_text_mode', 
         'type': 'boolean', 
         'mode': 'w', 
         'label': 'Hidden in text mode', 
         'category': 'visibility',
         'default': 0,
        },
        {'id': 'display_title_in_text_mode', 
         'type': 'boolean', 
         'mode': 'w', 
         'label': 'Display title in text mode', 
         'category': 'visibility',
         'default': 1,
        },
        {'id': 'xpos', 
         'type': 'int', 
         'mode': 'w', 
         'label': 'xpos',  
         'category': 'none',
        },
        {'id': 'align', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Horizontal alignment', 
         'select_variable': 'AlignList', 
         'category': 'layout',
         'visible': 'IsAlignable',
         'i18n': 1,
         'i18n_prefix': '_option_',
        },
        {'id': 'padding', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Templet padding', 
         'category': 'layout',
        },
        {'id': 'margin', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Templet margin',  
         'category': 'layout',
        },
        {'id': 'templet_height', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Templet height', 
         'category': 'layout',
        },
        {'id': 'fontcolor', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Font color', 
         'select_variable': 'FontColorsList', 
         'style': 'Font Color', 
         'category': 'style',
        },
        {'id': 'fontshape', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Font shape', 
         'select_variable': 'FontShapesList', 
         'style': 'Font Shape', 
         'category': 'style',
        },
        {'id': 'shape', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Templet shape', 
         'select_variable': 'AreaShapesList', 
         'style': 'Area Shape', 
         'category': 'style',
        },
        {'id': 'color', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Templet color', 
         'select_variable': 'AreaColorsList', 
         'style': 'Area Color',  
         'category': 'style',
        },
        {'id': 'formstyle', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Form style', 
         'select_variable': 'FormStyleList', 
         'style': 'Form Style',  
         'category': 'style',
        },
        {'id': 'visibility',  
         'type': 'selection',  
         'mode': 'w', 
         'label': 'Visibility criteria', 
         'select_variable': 'VisibilityList', 
         'category': 'visibility',
         'default': 'always',
         'i18n': 1,
         'i18n_prefix': '_option_',
        },
        {'id': 'visibility_paths',  
         'type': 'multiple selection',   
         'mode': 'w', 
         'label': 'The visibility paths', 
         'select_variable': 'cpsskins_listPaths', 
         'category': 'visibility',
         'visible': 'ShowVisibilityPaths',
        },
        {'id': 'languages', 
         'type': 'multiple selection', 
         'mode': 'w', 
         'label': 'The languages in which it is visible', 
         'select_variable': 'LanguagesList', 
         'category': 'visibility',
         'visible': 'LanguagesList',
        },
        {'id': 'esi_fragment', 
         'type': 'boolean', 
         'mode': 'w', 
         'label': 'ESI fragment', 
         'category': 'ESI',
         'visible': 'isESICacheable',
         'default': 0,
        },
     )

    #
    # RAM cache
    #
    cache_cleanup_date = 0

    # Edge-Side-Includes
    esi_code = """
      <esi:try>
        <esi:attempt>
          <esi:include src="%s/render?context_rurl=%s" onerror="continue" />
        </esi:attempt>
        <esi:except>
          <!--esi
           This spot is reserved
          -->
        </esi:except>
      </esi:try>
    """

    def __init__(self, id, 
                 title = 'Templet',
                 closed = 0,
                 cacheable = 0,
                 cache_lifetime = '60',
                 esi_fragment = 0,
                 hidden_in_text_mode = 0,
                 display_title_in_text_mode = 0,
                 visibility = 'always',
                 visibility_paths= [],
                 languages = [],
                 xpos = 0, 
                 align = 'left', 
                 templet_height = '',
                 padding = '0.5em', 
                 margin = '0.5em', 
                 fontshape = 'Arial',
                 fontcolor = 'Black',
                 shape = 'NoBorder',
                 color = 'Transparent',
                 formstyle = '',
                 **kw):
        self.id = id
        self.closed = closed
        self.cacheable = cacheable
        self.cache_lifetime = cache_lifetime
        self.esi_fragment = esi_fragment
        self.hidden_in_text_mode = hidden_in_text_mode
        self.display_title_in_text_mode = display_title_in_text_mode
        self.visibility = visibility
        self.visibility_paths = visibility_paths
        self.languages = languages
        self.title = title
        self.xpos = int(xpos)
        self.align = align
        self.templet_height = templet_height
        self.padding = padding
        self.margin = margin
        self.fontshape = fontshape
        self.fontcolor = fontcolor
        self.shape = shape
        self.color = color
        self.formstyle = formstyle
    
    security.declarePublic('getTitle')
    def getTitle(self):
        """Gets the templet's title."""
    
        return getattr(self, 'title', None)

    security.declarePublic('isPortalTemplet')
    def isPortalTemplet(self):
        """Returns True if this is a Templet."""
           
        return self.isportaltemplet

    security.declarePublic('isPortalBox')
    def isPortalBox(self):
        """Returns True if this is a Portal Box."""
           
        return None

    security.declarePublic('isPortalBoxGroup')
    def isPortalBoxGroup(self):
        """Returns True if this is a Portal Box Group."""
           
        return None

    security.declarePublic('isAlignable')
    def isAlignable(self):
        """Returns true if the Templet can be aligned horizontally."""

        return 1

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """Returns true if the Templet can be cached in RAM."""

        return 1

    security.declarePublic('isCached')
    def isCached(self):
        """Returns true if the Templet is being cached."""

        if self.isCacheable():
            return getattr(self, 'cacheable', 0)

    security.declarePublic('isESIFragment')
    def isESIFragment(self):
        """Returns true if the Templet is an ESI fragment
        """

        return self.esi_fragment

    security.declarePublic('isESICacheable')
    def isESICacheable(self):
        """Returns true if the Templet can become an ESI fragment. 
           ESI is expected to be globally enabled in the theme.
        """

        return self.ifESIEnabled()

    security.declarePublic('ifESIEnabled')
    def ifESIEnabled(self):
        """Returns true if ESI is enabled for this theme."""

        tmtool = getToolByName(self, 'portal_themes')
        theme_container = tmtool.getPortalThemeRoot(self)
        return getattr(theme_container, 'esi', 0)

    security.declarePublic('isRenderable')
    def isRenderable(self):
        """Returns true if the Templet can be rendered.
        """

        return 1

    security.declarePublic('ShowVisibilityPaths')
    def ShowVisibilityPaths(self):
        """Returns True if the visibility paths must be shown."""
           
        category = getattr(self, 'visibility', None)
        if category in ['everywhere_except_in',
                        'only_in',
                        'starting_from',
                        'up_till']:
            return 1

    security.declarePublic('AlignList')
    def AlignList(self):
        """Returns a list of alignments for this object."""

        list = ['left', 'center', 'right']
        return list

    #
    # CSS
    #
    security.declarePublic('getCSSLayoutStyle')
    def getCSSLayoutStyle(self):
        """Returns the CSS layout style for this Templet."""

        css = ''
        padding = self.padding
        height = self.templet_height

        if padding:
            css += 'padding:%s;' % padding
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
                    'Color%s FontColor%s FontShape%s' %\
                         (self.color,
                          self.fontcolor,
                          self.fontshape)
            elif level == 2:
                areaclass = \
                    'Shape%s Color%s FontColor%s FontShape%s FormStyle%s' %\
                         (self.shape,
                          self.color,
                          self.fontcolor,
                          self.fontshape,
                          self.formstyle)
        # rebuild the templet if some attributes are missing.
        # a simple page reload will display the correct results.
        except AttributeError:
            self.rebuild()
        return areaclass


    security.declarePublic('VisibilityList')
    def VisibilityList(self):
        """Returns a list of visibility criteria."""

        list = ['always', 
                'everywhere_except_in', 
                'only_in', 
                'starting_from', 
                'up_till', 
                'if_authenticated', 
                'if_anonymous', 
                'if_secure_connection' ]
        return list

    security.declareProtected(ManageThemes, 'getTempletPosition')
    def getTempletPosition(self):
        """Return the page block's ypos in the theme folder."""

        container = self.aq_parent
        return container.get_object_position(self.getId())

    security.declarePublic('getI18nProperties')
    def getI18nProperties(self):
        """Returns the list of i18n properties."""

        return []

    security.declareProtected(ManageThemes, 'rebuild')
    def rebuild(self, **kw):
        """Rebuilds this templet."""

        setperms = kw.get('setperms', 0)
        canonizeId(self)
        rebuild_properties(self)
        if setperms:
            verifyThemePerms(self)

    security.declarePublic('getVisibility')
    def getVisibility(self, REQUEST=None):
        """Returns True if the Templet is visible."""

        if self.closed:
            return None
        return getObjectVisibility(self, REQUEST)

    security.declarePublic('getApplicableStyles')
    def getApplicableStyles(self):
        """Returns the styles by meta type that are 
           applicable to this Templet
        """

        return getApplicableStylesFor(self)

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
        self.expireCache()
        
    security.declarePublic('moveleft_pos')
    def moveleft_pos(self):
        """Can the templet be moved to the left?"""

        if self.can_moveleft():
           return self.xpos -1 

    security.declarePublic('moveright_pos')
    def moveright_pos(self):
        """Returns the new position."""

        if self.can_moveright():
            return self.xpos + 1

    security.declarePublic('moveup_pos')
    def moveup_pos(self):
        """Returns the new position."""

        container = self.aq_parent
        this_pos = container.get_object_position(self.getId())
        newpos = -1
        for obj in container.objectValues():
            o = obj.aq_explicit
            if getattr(o, 'isportaltemplet', 0):
                if obj.xpos == self.xpos:
                    pos = container.get_object_position(obj.getId())
                    if pos > newpos and pos < this_pos:
                        newpos = pos
        return newpos

    security.declarePublic('movedown_pos')
    def movedown_pos(self):
        """Returns the new position."""

        container = self.aq_parent
        this_pos = container.get_object_position(self.getId())
        newpos = -1
        for obj in container.objectValues():
            o = obj.aq_explicit
            if getattr(o, 'isportaltemplet', 0):
                if obj.xpos == self.xpos:
                    pos = container.get_object_position(obj.getId())
                    if  pos > this_pos:
                        newpos = pos
                        break
        return newpos

    security.declarePublic('can_toggle')
    def can_toggle(self):
        """Can the templet be toggled (open/close)?"""

        if hasattr(self, 'closed'):
            return 1

    security.declarePublic('can_delete')
    def can_delete(self):
        """Can the templet be deleted?"""

        return 1

    security.declarePublic('can_moveup')
    def can_moveup(self):
        """Can the templet be moved up?"""

        # find a page block above it
        container = self.aq_parent
        if container.can_moveup():
            return 1

        # otherwise find a templet above it
        this_pos = container.get_object_position(self.getId())
        for obj in container.objectValues():
            o = obj.aq_explicit
            if getattr(o, 'isportaltemplet', 0):
               if obj.xpos == self.xpos:
                   pos = container.get_object_position(obj.getId())
                   if pos < this_pos:
                       return 1

    security.declarePublic('can_movedown')
    def can_movedown(self):
        """Can the templet be moved down?"""

        container = self.aq_parent
        if container.can_movedown():
            return 1

        container = self.aq_parent
        this_pos = container.get_object_position(self.getId())
        for obj in container.objectValues():
            o =  obj.aq_explicit
            if getattr(o, 'isportaltemplet', 0):
                if obj.xpos == self.xpos:
                    pos = container.get_object_position(obj.getId())
                    if pos > this_pos:
                        return 1

    security.declarePublic('can_moveright')
    def can_moveright(self):
        """Can the templet be moved to the right?"""

        container = self.aq_parent 
        maxcols = getattr(container, 'maxcols', None)
        if maxcols is None:
            return None
        if self.xpos < maxcols -1 :
            return 1

    security.declarePublic('can_moveleft')
    def can_moveleft(self):
        """Can the templet be moved to the left?"""

        if self.xpos > 0:
            return 1

    security.declareProtected(ManageThemes, 'toggle')
    def toggle(self):
        """Opens or closes the Templet."""
        
        self.closed = not self.closed

    security.declareProtected(ManageThemes, 'duplicate')
    def duplicate(self):
        """Duplicates a Templet."""
        
        tmtool = getToolByName(self, 'portal_themes')
        container = self.aq_parent
        src_ypos = container.get_object_position(self.getId())
        newid = getFreeId(container)
        container.manage_clone(self, newid)
        newobj  = getattr(container, newid, None)
        container.move_object_to_position(newobj.getId(), src_ypos + 1)

        # needed for the ImageBox 
        setattr(newobj, 'id', newid)
        verifyThemePerms(newobj)
        newobj.expireCache()
        return newobj

    security.declareProtected(ManageThemes, 'set_property')
    def set_property(self, prop=None, value=None):
        """Sets a property."""

        if value is None:
           return
     
        if not hasattr(self, prop):
           return
        setattr(self, prop, value)

    security.declareProtected(ManageThemes, 'move_to_pageblock')
    def move_to_pageblock(self, pageblock=None, 
                                xpos=None, ypos=None, REQUEST=None):
        """Move the templet to a given pageblock.
           Returns the instance of the object moved
        """

        tmtool = getToolByName(self, 'portal_themes')
        if pageblock is None:
            return
        if xpos is None:
            return
        if ypos is None:
            return
        id = self.getId()
        current_xpos = self.xpos
        new_xpos = int(xpos)
        self.xpos = new_xpos
        container = self.aq_parent
        src_pageblock = container.getId()
        theme_container = container.aq_parent
        current_ypos = container.get_object_position(self.getId())

        if pageblock == container.getId() and \
                        int(xpos) == current_xpos and \
                        int(ypos) == current_ypos:
            return

        for obj in theme_container.objectValues():
           if obj.getId() == pageblock:
               cookie = container.manage_cutObjects(self.getId(), 
                                                    REQUEST=REQUEST)
               res = obj.manage_pasteObjects(cookie) 
               new_id = res[0]['new_id']
               newpos = int(ypos) 
               if pageblock == src_pageblock:
                    if newpos > current_ypos and new_xpos != current_xpos:
                        newpos = newpos -1;
               obj.move_object_to_position(new_id, newpos)
               templet = getattr(obj, new_id)
               templet.expireCache()
               return templet


    security.declareProtected(ManageThemes, 'copy_to_theme')
    def copy_to_theme(self, dest_theme=None, REQUEST=None):
        """Copies the Templet to another theme.
           The copied object is placed into the first available Page Block.
           returns the copied object
        """

        tmtool = getToolByName(self, 'portal_themes')
        if dest_theme is None:
            return
        container = self.aq_parent
        dest_theme_container = tmtool.getThemeContainer(theme=dest_theme)
        if dest_theme_container is None:
            return
        
        pageblocks = dest_theme_container.getPageBlocks()
        if pageblocks:
            dest_container = pageblocks[0]
        else:
            return

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
  
        tmtool = getToolByName(self, 'portal_themes')
        container = self.aq_parent 
        if direction == 'left' and self.can_moveleft():
            self.xpos = self.moveleft_pos()
            templet = self
 
        if direction == 'right' and self.can_moveright():
            self.xpos = self.moveright_pos()
            templet = self

        if direction == 'up' and self.can_moveup():
            newpos = self.moveup_pos()
            if newpos >= 0:
                container.move_object_to_position(self.getId(), newpos)
                templet = self
            else:
                cookie = container.manage_cutObjects(self.getId(), 
                                                     REQUEST=REQUEST)
                pos =  container.moveup_pos()
                theme_container = container.aq_parent
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
                templet = self
            else:
                cookie = container.manage_cutObjects(self.getId(), 
                                                     REQUEST=REQUEST)
                pos =  container.movedown_pos()
                theme_container = container.aq_parent
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

        tmtool = getToolByName(self, 'portal_themes')
        if alignment in ['left', 'center', 'right']:
            self.set_property('align', alignment)
        self.expireCache()

    #
    # RAM Cache
    #
    security.declarePublic('getCacheParams')
    def getCacheParams(self):
        """Return a list of cache parameters"
        """
        return []

    security.declarePublic('getCustomCacheIndex')
    def getCustomCacheIndex(self, **kw):
        """Returns the RAM cache index as a tuple (var1, var2, ...)
        """

        # override this method in derived classes to pass a cache index
        return None

    security.declarePublic('getCacheIndex')
    def getCacheIndex(self, REQUEST=None, **kw):
        """Returns the RAM cache index as a tuple (var1, var2, ...)
        """
        if REQUEST is None:
            REQUEST = self.REQUEST

        def getOptions(param):
             """extract cache parameter options
             """
             res = []
             opts = param.split(':')[1].split(',')
             for opt in opts:
                 if opt[0] == '(' and opt[-1] == ')':
                     opt = getattr(self, opt[1:-1], None)
                     if opt is None:
                         continue
                     if isinstance(opt, ListType) or\
                        isinstance(opt, TupleType):
                         res.extend(opt)
                         continue
                 res.append(str(opt))
             return res

        context = kw.get('context_obj')
        params = self.getCacheParams()
        index = ()
        for param in params:
            index_string = ''
            prefix = param

            # current user
            if param == 'user':
                index_string = str(REQUEST.get('AUTHENTICATED_USER'))

            # current language
            elif param == 'lang':
                index_string = REQUEST.get('cpsskins_language', 'en')

            # current url
            if param == 'url':
                index_string = REQUEST.get('cpsskins_url')

            # CMF Actions
            elif param == 'actions':
                cmf_actions = REQUEST.get('cpsskins_cmfactions')
                if cmf_actions:
                    index_string = md5.new(str(cmf_actions)).hexdigest()

            elif param.startswith('actions:'):
                prefix = 'actions'
                cmf_actions = REQUEST.get('cpsskins_cmfactions')
                if cmf_actions:
                    categories = param.split(':')[1].split(',')
                    actions = [cmf_actions[x] for x in categories \
                               if cmf_actions.has_key(x)]
                    index_string = md5.new(str(actions)).hexdigest()

            # Workflow actions
            elif param == 'wf_actions':
                cmf_actions = REQUEST.get('cpsskins_cmfactions')
                wf_actions = cmf_actions.get('workflow', None)
                if wf_actions is not None:
                    index_string = md5.new(str(wf_actions)).hexdigest()

            # current object
            elif param.startswith('object:'):
                opts = getOptions(param)
                index_string = ''
                prefix = 'object'
                for opt in opts:
                    # object's published path
                    # including the method used to access the object
                    index_string += '_' + opt + ':'
                    if opt == 'published_path':
                        index_string += REQUEST.get('PATH_TRANSLATED')

                    # object's physical path
                    if opt == 'path':
                        index_string += '/'.join(context.getPhysicalPath())

            # box state
            elif param == 'boxstate':
                index_string = str(self.getBoxState())

            # current month
            elif param == 'month':
                month = REQUEST.get('month', None)
                if month is None:
                    ctool = getToolByName(self, 'portal_calendar', None)
                    if ctool and ctool.getUseSession() == "True":
                        session = REQUEST.get('SESSION', None)
                        if session:
                            month = session.get('calendar_month',  None)
                if month:
                    index_string = month

            # current year
            elif param == 'year':
                year = REQUEST.get('year', None)
                if year is None:
                    ctool = getToolByName(self, 'portal_calendar', None)
                    if ctool and ctool.getUseSession() == "True":
                        session = REQUEST.get('SESSION', None)
                        if session:
                            year = session.get('calendar_year',  None)
                if year:
                    index_string = year

            if index_string:
                index += (prefix + '_' + index_string,)

        # custom cache index
        # this is where we obtain the portlets cache index
        custom_index = self.getCustomCacheIndex(**kw)
        if custom_index is not None:
            index += custom_index
        return index

    security.declareProtected(ManageThemes, 'expireCache')
    def expireCache(self):
        """Expires the cache for this Templet.
 
           In a ZEO environment, the information will propagate
           between all ZEO instances as long as the Templet still
           exists.
        """

        self.cache_cleanup_date = time.time()

    #
    # Rendering
    #
    security.declarePublic('render')
    def render(self, shield=0,  **kw):
        """Render the templet."""

        fail = 0
        if getattr(aq_base(self), 'render_action', None) is not None:
            actionid = self.render_action
        else:
            fail = 1
 
        if not fail: 
            meth = getattr(self, actionid, None)
            if meth is not None:
                if shield:
                    # crash shield
                    try:
                        rendered = apply(meth, (), kw)
                    except:
                        # attempt to rebuild 
                        try:
                            self.rebuild()
                        # rebuild failed
                        except:
                            fail = 1
                        else:
                            # try again to render it ...
                            try:
                                rendered = apply(meth, (), kw)
                            # total failure
                            except:
                                fail = 1
                # no crash shield
                else:
                    rendered = apply(meth, (), kw)
            else:
                fail = 1

        if fail:
            rendered = self.cpsskins_brokentemplet(**kw)
        return html_slimmer(rendered)

    security.declarePublic('render_cache')
    def render_cache(self, shield=0, enable_esi=0, **kw):
        """Renders the cached version of the templet."""

        if enable_esi:
            if self.isESIFragment():
                return self.render_esi(**kw)

        if not self.cacheable:
            rendered = self.render(shield=shield, **kw)
        else:
            now = time.time()
            templet_path = self.getPhysicalPath()
            index = (templet_path, ) + self.getCacheIndex(**kw)
            cache = self.getTempletCache(create=1)
            last_cleanup = cache.getLastCleanup(id=templet_path)
            lifetime = getattr(self, 'cache_lifetime', 60)
            cleanup_date = getattr(self, 'cache_cleanup_date', 0)

            # ZEO
            if cleanup_date > last_cleanup:
                cache.delEntries(templet_path)

            rendered = None
            if last_cleanup is not None and now < last_cleanup + int(lifetime):
                rendered = cache.getEntry(index)
            else:
                cache.delEntries(templet_path)

            if rendered is None:
                rendered = self.render(shield=shield, **kw)
                cache.setEntry(index, rendered)

        return rendered

    security.declarePublic('render_js')
    def render_js(self, **kw):
        """Renders the javascript code used by the Templet."""

        if hasattr(self.aq_explicit, 'javascript_render_action'):
            actionid = self.javascript_render_action
            meth = getattr(self, actionid, None)
            if meth is not None:
                rendered = apply(meth, (), kw)
                return rendered  

    security.declarePublic('render_css')
    def render_css(self, **kw):
        """Renders the CSS code used by the Templet."""

        tmtool = getToolByName(self, 'portal_themes')
        theme_container = tmtool.getPortalThemeRoot(self)
        styles_dir = theme_container.getStylesFolder()

        css = ''
        for propid in self.propertyIds():
            prop_map = self.propertyMap()
            for obj in prop_map:            
                if obj['id'] == propid:                
                    if not obj.has_key('style'):
                        continue
                    style_type = obj.get('style')
                    this_style = getattr(self, propid)
                    style_obj = [s 
                                 for s in styles_dir.objectValues(style_type)
                                 if s.getTitle() == this_style]
                    if style_obj:
                        css += style_obj[0].render()
                    break
        return css

    security.declarePublic('render_esi')
    def render_esi(self, context_rurl=None, **kw):
        """Renders the ESI fragment code."""

        return self.esi_code % (self.absolute_url(), context_rurl)

    security.declarePublic('getStyle')
    def getStyle(self,  meta_type=None):
        """Gets a style associated to this Templet by meta type."""

        tmtool = getToolByName(self, 'portal_themes')
        theme_container = tmtool.getPortalThemeRoot(self)
        for propid in self.propertyIds():
            for obj in self.propertyMap():
                if obj['id'] != propid:                
                    continue
                if obj.get('style', None) != meta_type:
                    continue
                style_title = getattr(self, propid, None)
                styles = theme_container.findStyles(title=style_title)
                if len(styles) > 0: 
                    return styles[0]

    security.declareProtected(ManageThemes, 'setStyle')
    def setStyle(self, style=None, meta_type=None):
        """Sets a style to this Templet."""

        if style is None:
            return
        prop_id = None 
        for propid in self.propertyIds():
            for obj in self.propertyMap():
                if obj['id'] != propid:                
                    continue
                if obj.get('style', None) == meta_type:
                    prop_id = propid
                    break
        if prop_id is not None:
            self.manage_changeProperties(**{prop_id: style.getTitle()})
            self.expireCache()

    #
    # Theme properties
    #
    security.declarePublic('AreaColorsList')
    def AreaColorsList(self):           
        """Returns a list of Area Color styles."""

        return getStyleList(self, 'Area Color')

    security.declarePublic('AreaShapesList')
    def AreaShapesList(self):           
        """Returns a list of Area Shape styles."""

        return getStyleList(self, 'Area Shape')

    security.declarePublic('FontColorsList')
    def FontColorsList(self):           
        """Returns a list of Font Color styles."""

        return getStyleList(self, 'Font Color')

    security.declarePublic('FontShapesList')
    def FontShapesList(self):           
        """Returns a list of Font Shape styles."""

        return getStyleList(self, 'Font Shape')

    security.declarePublic('FormStyleList')
    def FormStyleList(self):           
        """Returns a list of formstyles."""

        return getStyleList(self, 'Form Style')

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """Returns true if the Templet is cacheable."""

        return getattr(self, 'cacheable', 0) 

    security.declarePublic('LanguagesList')
    def LanguagesList(self):           
        """Returns a list of languages."""

        return getAvailableLangs(self)

    security.declarePublic('LfetimeList')
    def LifetimeList(self):           
        """Returns a list of cache lifetimes in seconds."""

        list = ['10', '30', '60', '300', '600', '900', '1800', '3600']
        return list

    security.declarePublic('getDefaultLang')
    def getDefaultLang(self):
        """Returns the code name of the default language."""
           
        return getDefaultLang(self)

InitializeClass(BaseTemplet)

def addBaseTemplet(dispatcher, id, REQUEST=None):
    """Add a Base Templet."""
    ob = BaseTemplet(id)
    container = dispatcher.Destination()
    container._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
