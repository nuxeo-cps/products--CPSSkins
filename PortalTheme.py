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
  Portal Theme
  a Portal Theme modifies the appearance and the layout of the portal. 
  The Theme layout is composed of horizontal Page Blocks.
"""

# RAM Cache
TEMPLET_RAMCACHE_ID = 'templets'
CSS_RAMCACHE_ID = 'css'
JS_RAMCACHE_ID = 'js'

# Thumbnails
THUMBNAIL_WIDTH = 200
THUMBNAIL_HEIGHT = 160
THUMBNAIL_IMAGE_FORMAT = 'PNG'

import string
import time

isPILAvailable = 1
try:
    import PIL.Image
except ImportError:
    isPILAvailable = 0

from Acquisition import aq_base
from Globals import InitializeClass, DTMLFile
from AccessControl import ClassSecurityInfo

from Products.CMFCore.CMFCorePermissions import View
from Products.CMFCore.utils import getToolByName

from RAMCache import SimpleRAMCache, RAMCache
from ThemeFolder import ThemeFolder
from CPSSkinsPermissions import ManageThemes
from StylableContent import StylableContent

from cpsskins_utils import rebuild_properties, callAction, css_slimmer, \
                           getFreeId, verifyThemePerms, canonizeId, \
                           isBroken, moveToLostAndFound, setCacheHeaders

factory_type_information = (
    {'id': 'Portal Theme',
     'meta_type': 'Portal Theme',
     'description': ('_portaltheme_description_'),
     'icon': 'portaltheme.png',
     'product': 'CPSSkins',
     'factory': 'addPortalTheme',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': {              
          '(Default)': 'cpsskins_theme_view',
          'view': 'cpsskins_theme_view',
          'edit': 'cpsskins_edit_form', 
          'edit': 'cpsskins_edit_form', 
          'edit_styles': 'cpsskins_edit_styles', 
          'edit_palettes': 'cpsskins_edit_palettes', 
          'edit_images': 'cpsskins_edit_images',
          'manage_cache': 'cpsskins_cache_manager',
          'manage_themes': 'cpsskins_themes_manager',
     },
     'actions': (
         {'id': 'view',
          'name': 'View',
          'action': 'cpsskins_theme_view',
          'permissions': (View,)
         },
         {'id': 'edit',
          'name': '_Edit_',
          'action': 'cpsskins_edit_form',
          'visible': 0,
          'permissions': (ManageThemes,)
         },
         {'id': 'edit_styles',
          'name': '_Edit styles_',
          'action': 'cpsskins_edit_styles',
          'visible': 0,
          'permissions': (ManageThemes,)
         },
         {'id': 'edit_palettes',
          'name': '_Edit palettes_',
          'action': 'cpsskins_edit_palettes',
          'visible': 0,
          'permissions': (ManageThemes,)
         },
         {'id': 'edit_images',
          'name': '_Edit images_',
          'action': 'cpsskins_edit_images',
          'visible': 0,
          'permissions': (ManageThemes,)
         },
         {'id': 'manage_cache',
          'name': '_Cache manager_',
          'action': 'cpsskins_cache_manager',
          'visible': 0,
          'permissions': (ManageThemes,)
         },
         {'id': 'manage_themes',
          'name': '_Themes manager_',
          'action': 'cpsskins_themes_manager',
          'visible': 0,
          'permissions': (ManageThemes,)
         },
     )
    },
)

SHORTCUT_ICON_HTML = """
<link rel="icon" href="%s" type="%s" />
<link rel="shortcut icon" type="image/x-icon" href="%s" type="%s" />
"""

class PortalTheme(ThemeFolder, StylableContent):
    """
    Class for Portal Themes.
    """

    meta_type = "Portal Theme"
    portal_type = "Portal Theme"

    isportaltheme = 1

    manage_options = ( ThemeFolder.manage_options[0:1] +
                       ThemeFolder.manage_options[2:3] +
                       ( {'label': 'Rebuild',
                          'action': 'manage_themeRebuild'},
                         {'label': 'RAM Cache',
                          'action': 'manage_RAMCache'}, )
                     )

    security = ClassSecurityInfo()

    security.declareProtected(ManageThemes, 'manage_themeRebuild')
    manage_themeRebuild = DTMLFile('zmi/manage_themeRebuild', globals())
    security.declareProtected(ManageThemes, 'manage_RAMCache')
    manage_RAMCache = DTMLFile('zmi/manage_RAMCache', globals())

    _properties = (
        {'id': 'title', 
         'type':'string', 
         'mode':'w', 
         'label':'Title', 
         'category': 'general'
        },
        {'id': 'margin', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Margin', 
         'category': 'layout'
        },
        {'id': 'default', 
         'type': 'boolean', 
         'mode': 'w', 
         'label': 'Default', 
         'category': 'none',
         'default': 0,
        },
        {'id': 'esi', 
         'type': 'boolean', 
         'mode': 'w', 
         'label': 'Enable ESI', 
         'category': 'general',
         'default': 0,
        },
        {'id': 'align', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Align', 
         'select_variable': 'AlignList', 
         'category': 'layout',
         'i18n': 1,
         'i18n_prefix': '_option_',
        },
        {'id': 'color', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Area background color', 
         'select_variable': 'AreaColorsList', 
         'style': 'Area Color',
         'category': 'style'
        },
        {'id': 'shortcut_icon', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Shortcut icon', 
         'select_variable': 'cpsskins_listIcons',  
         'category': 'style', 
         'image' : 'icons'
        },
        {'id': 'theme_renderer', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Theme renderer', 
         'select_variable' : 'listThemeRenderers',  
         'category': 'general',
         'i18n': 1, 
         'i18n_prefix': '_option_',
        },
        {'id': 'preview',
         'type': 'selection',
         'mode': 'w',
         'label': 'Preview',
         'select_variable': 'cpsskins_listThumbnails',
         'category': 'about',
         'image' : 'thumbnails'
        },
        {'id': 'author', 
         'type': 'text', 
         'mode': 'w', 
         'label': 'Author', 
         'category' : 'about'
        },
        {'id': 'copyright', 
         'type': 'text', 
         'mode': 'w', 
         'label': 'Copyright', 
         'category': 'about'
        },
        {'id': 'license', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'License', 
         'category': 'about'
        },
    )


    # RAM Cache
    caches = {}
    css_cache_cleanup_date = 0
    js_cache_cleanup_date = 0

    def __init__(self, id, 
                 title = 'Portal Theme',
                 color = 'Transparent',
                 align = 'center',
                 margin = '0.5em',
                 default = 0,
                 esi = 0,
                 shortcut_icon = '',
                 theme_renderer = 'default',
                 author = '',
                 copyright = '',
                 license = '',
                 preview = '',
                 **kw):
        self.id = id
        self.title = title
        self.color = color
        self.align = align
        self.margin = margin
        self.default = default
        self.esi = esi
        self.shortcut_icon = shortcut_icon
        self.theme_renderer = theme_renderer
        self.author = author
        self.copyright = copyright
        self.license = license
        self.preview = preview

    security.declarePublic('getTitle')
    def getTitle(self):
        """ Returns the theme's title """

        return self.title

    security.declarePublic('getURL')
    def getURL(self):
        """ Returns the theme's title """

        return self.absolute_url()

    security.declarePublic('isPortalTheme')
    def isPortalTheme(self):
        """ is a portal theme """
           
        return self.isportaltheme

    security.declarePublic('isDefaultTheme')
    def isDefaultTheme(self):
        """ is a default theme ? """

        return getattr(self, 'default', None)

    security.declarePublic('AlignList')
    def AlignList(self):
        """ Returns a list of alignments for this object"""

        list = ['left', 'center', 'right']
        return list

    security.declarePublic('listThemeRenderers')
    def listThemeRenderers(self):
        """ returns the list of theme renderers """

        tmtool = getToolByName(self, 'portal_themes')
        return tmtool.listThemeRenderers()

    security.declareProtected(ManageThemes, 'manage_rebuild')
    def manage_rebuild(self, setperms=0, REQUEST=None):
        """
        Rebuild this theme
        """

        self.rebuild(setperms=setperms)
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(self.absolute_url() + '/manage_main')

    security.declareProtected(ManageThemes, 'createThemeSkeleton')
    def createThemeSkeleton(self):
        """
        Creates a theme skeleton
        """

        themefolders = self.cpsskins_listImageCategories()
        themefolders.extend(['styles', 'palettes'])

        for themefolder in themefolders:
            self.invokeFactory('Theme Folder', id=themefolder)

    security.declareProtected(ManageThemes, 'rebuild')
    def rebuild(self, **kw):
        """
        Rebuild the theme
        """

        tmtool = getToolByName(self, 'portal_themes')
        setperms = kw.get('setperms', 0)
        canonizeId(self)
        rebuild_properties(self) 
        if setperms:
            verifyThemePerms(self)

        # check the presence of theme folders
        themefolders = self.cpsskins_listImageCategories()
        themefolders.extend(['styles', 'palettes'])

        for themefolder in themefolders:
            backupid = themefolder + '-bak'
            objs = self.objectIds()
            if backupid in objs:
                self.manage_delObjects([backupid])

            if themefolder not in objs:
                self.invokeFactory('Theme Folder', id=themefolder)
                continue
        
            else:
                folder = getattr(self.aq_explicit, themefolder)
                f = folder.aq_explicit
                if getattr(f, 'isthemefolder', 0):
                    continue

                self.manage_renameObjects([themefolder], [backupid])
                backup_folder = getattr(self.aq_explicit, backupid)
                objects = backup_folder.objectIds()
                cookie = backup_folder.manage_cutObjects(objects)
                self.invokeFactory('Theme Folder', themefolder)
                new_folder = getattr(self.aq_explcit, themefolder, None)
                if new_folder is not None:
                    new_folder.manage_pasteObjects(cookie)
                    self.manage_delObjects([backupid])

        # move disallowed objects to lost+found
        for (id, o) in self.objectItems():
            o = o.aq_explicit
            if getattr(o, 'isportalpageblock', 0):
                continue
            if getattr(o, 'isthemefolder', 0):
                continue
            moveToLostAndFound(self, o)
        
        for obj in self.getPageBlocks():
            obj.rebuild(**kw)
        
        for obj in self.findStyles():
            obj.rebuild(**kw)

        styles_dir = self.getStylesFolder()
        for (id, obj) in styles_dir.objectItems():
            obj = obj.aq_explicit
            if isBroken(obj):
                styles_dir.manage_delObjects(id)
                continue
            if getattr(obj, 'isportalstyle', 0):
                continue
            moveToLostAndFound(self, obj)

        palettes_dir = self.getPalettesFolder()
        for (id, obj) in palettes_dir.objectItems():
            obj = obj.aq_explicit
            if isBroken(obj):
                palettes_dir.manage_delObjects(id)
                continue
            if getattr(obj, 'isportalpalette', 0):
                continue
            moveToLostAndFound(self, obj)

        for themefolder in themefolders:
            obj = getattr(self.aq_explicit, themefolder, None)
            if obj is not None and setperms:
                 verifyThemePerms(obj)

        self.clearCache()

    #
    # Rendering
    #

    security.declarePublic('renderIcon')
    def renderIcon(self):
        """ Generates the shortcut icon for this theme."""

        shortcut_icon = self.shortcut_icon
        if shortcut_icon:
            icon_dir = getattr(self, 'icons', None)
            if icon_dir is not None:
                icon_obj = getattr(icon_dir, shortcut_icon, None);
                if icon_obj is not None:
                    path = '/' + icon_obj.absolute_url(1)
                    mimetype = icon_obj.content_type
                    return SHORTCUT_ICON_HTML % (path, mimetype, path, mimetype)


    security.declarePublic('renderCSS')
    def renderCSS(self, **kw):
        """ Generates the CSS file for this theme """

        REQUEST = self.REQUEST
        kw.update(REQUEST.form)

        setCacheHeaders(self, css=1, **kw)

        cache = self.getCSSCache(create=1)
        index = tuple(kw.items())

        cleanup_date = getattr(self, 'css_cache_cleanup_date', 0)
        last_update = cache.getLastUpdate()
        if last_update < cleanup_date:
           cache.invalidate()

        css = cache.getEntry(index)

        if css is None:
            styles_dir = self.getStylesFolder()
            if styles_dir is None:
                return
            css = ''
            for obj in styles_dir.objectValues():
                o = obj.aq_explicit
                if getattr(o, 'isportalstyle', 0):
                    try:
                        css += obj.render(**kw) 
                    except:
                        pass
            css = css_slimmer(css)
            cache.setEntry(index, css)
        return css

    security.declarePublic('renderJS')
    def renderJS(self, REQUEST=None, **kw):
        """ Generates the javascript code for this theme """

        if REQUEST is not None:
            kw.update(REQUEST.form)

        cache = self.getJSCache(create=1)
        index = tuple(kw.items())

        cleanup_date = getattr(self, 'js_cache_cleanup_date', 0)
        last_update = cache.getLastUpdate()
        if last_update < cleanup_date:
           cache.invalidate()

        js = cache.getEntry(index)

        if js is None:
            js = ''
            done_types = []
            for templet in self.getTemplets():
                ti = templet.getTypeInfo()
                if ti is None:
                    continue
                templet_type = ti.getId()
                if templet_type in done_types:
                    continue
                done_types.append(templet_type)
                js_code = templet.render_js(**kw)
                if js_code:
                    js += js_code
            cache.setEntry(index, js)
        return js  

    #
    # RAM Cache
    #
    security.declareProtected(ManageThemes, 'clearCache')
    def clearCache(self, REQUEST=None, **kw):
        """Clears the local RAM caches."""

        templetcache = self.getTempletCache()
        if templetcache is not None:
            templetcache.invalidate()

        csscache = self.getCSSCache()
        if csscache is not None:
            csscache.invalidate()
        
        jscache = self.getJSCache()
        if jscache is not None:
            jscache.invalidate()

    security.declareProtected(ManageThemes, 'expireCSSCache')
    def expireCSSCache(self):
        """Expires the CSS RAM cache for this theme.
 
           In a ZEO environment, the information will propagate
           between all ZEO instances as long as the theme still
           exists.
        """

        self.css_cache_cleanup_date = time.time()

    security.declareProtected(ManageThemes, 'expireJSCache')
    def expireJSCache(self):
        """Expires the JS RAM cache for this theme.
 
           In a ZEO environment, the information will propagate
           between all ZEO instances as long as the theme still
           exists.
        """

        self.js_cache_cleanup_date = time.time()

    #
    # Theme objects
    #
    security.declarePublic('getPageBlocks')
    def getPageBlocks(self):
        """ returns a list of page blocks sorted by ypos"""

        return self.objectValues('Page Block')

    security.declarePublic('getSlots')
    def getSlots(self):
        """Return the list of slots used in this theme.
        """

        slots = []
        for templet in self.getTemplets():
            if getattr(aq_base(templet), 'isportalboxgroup', 0):
                slots.append(templet.getSlot())
        return slots

    security.declarePublic('getStyles')
    def getStyles(self, meta_type=None):
        """ returns a list of styles by meta type"""

        styles_dir = self.getStylesFolder()
        return styles_dir.objectValues(meta_type)

    security.declarePublic('getStylesFolder')
    def getStylesFolder(self):
        """
        Returns the styles folder object 
        """

        id = 'styles'
        folder = getattr(self.aq_explicit, id, None)
        if folder is not None:
            f = folder.aq_explicit
            if not getattr(f, 'isthemefolder', 0):
                return None
        return getattr(self, id, None)

    security.declarePublic('getPalettesFolder')
    def getPalettesFolder(self):
        """                 
        Returns the palettes folder object 
        """                 
                            
        id = 'palettes'
        folder = getattr(self.aq_explicit, id, None)
        if folder is not None:
            f = folder.aq_explicit
            if not getattr(f, 'isthemefolder', 0):
                return None 
        return getattr(self, id, None)

    security.declarePublic('getDefaultStyle')
    def getDefaultStyle(self, meta_type=None):
        """ Gets the default style name by type
        """
 
        styles = self.getStyles(meta_type=meta_type) 
        for style in styles:
           if style.isDefaultStyle():
               return getattr(style, 'title', None)
        if styles:
           return getattr(styles[0], 'title', None)

    security.declareProtected(ManageThemes, 'getLostAndFoundFolder')
    def getLostAndFoundFolder(self, create=0):
        """
        Returns the 'lost+found' folder. 
        """

        id = 'LOST-AND-FOUND'
        folder = getattr(self.aq_explicit, id, None)
        exists = 0
        if folder is not None:
            if getattr(folder.aq_explicit, 'isthemefolder', 0):
               exists = 1 
        if not exists and create:
            self.invokeFactory('Theme Folder', id)
        return getattr(self.aq_explicit, id, None)

    security.declarePublic('getImageFolder')
    def getImageFolder(self, category=None):
        """
        Returns the image folder by category 
        """

        if category not in self.cpsskins_listImageCategories():
            return None
        id = category
        folder = getattr(self.aq_explicit, id, None)
        if folder is not None:
            f = folder.aq_explicit
            if not getattr(f, 'isthemefolder', 0):
                return None
        return getattr(self, id, None)

    security.declarePublic('findStyles')
    def findStyles(self, title=None, meta_type=None):
        """
        Returns a list of style(s) that has/have a given title or meta type
        """

        styles_dir = self.getStylesFolder()
        list = []
        for (id, o) in styles_dir.objectItems():
            o = o.aq_explicit
            if not getattr(o, 'isportalstyle', 0):
                continue

            if title is not None:
                if getattr(o, 'title', None) != title:
                    continue

            if meta_type is not None:
                if getattr(o, 'meta_type', None) != meta_type:
                    continue

            list.append(o)
        return list 

    security.declarePublic('findIdenticalStyles')
    def findIdenticalStyles(self):
        """
        Returns a dictionary of identical styles by type
        """

        dict = {}
        tmtool = getToolByName(self, 'portal_themes')
        for style_type in tmtool.listStyleTypes():
            meta_type = style_type.getId()
            identical_styles = self.findIdenticalStylesByType(meta_type=meta_type)
            if identical_styles:
                dict[meta_type] = identical_styles
        return dict

    security.declarePublic('getDefaultStyleByType')
    def getDefaultStyleByType(self, meta_type=None):
        """
        Returns the default style if it exists.
        """

        if meta_type is None:
            return 
 
        for style in self.findStyles(meta_type=meta_type):
            if style.aq_explicit.isDefaultStyle():
                return style


    security.declarePublic('findIdenticalStylesByType')
    def findIdenticalStylesByType(self, meta_type=None):
        """
        Returns a list of a list of styles that have identical properties
        """

        if meta_type is None:
            return 
 
        groups = []
        props = []
        for style in self.findStyles(meta_type=meta_type):
            # XXX: does it have to be rebuilt?
            style.rebuild()
            #
            properties = style.propertyValues()[1:]
            for i in range(len(groups)):
                group = groups[i]
                if properties == props[i]: 
                     groups[i].append(style)
                     break
    
            groups.append([style])
            props.append(properties)
        final_groups = []
        for group in groups:
            if len(group) > 1:
                final_groups.append(group)
        return final_groups

    security.declarePublic('findUncachedTemplets')
    def findUncachedTemplets(self):
        """
        Returns a list of uncached Templets
        """

        list = []
        for templet in self.getTemplets():
            templet = templet.aq_explicit
            if templet.isCacheable():
                if not getattr(templet, 'cacheable', 0):
                    list.append(templet)
        return list

    security.declareProtected(ManageThemes, 'addPageBlock')
    def addPageBlock(self, **kw):
        """
        Add a Page Block. Returns the Page Block object
        """

        id = getFreeId(self)
        self.invokeFactory('Page Block', title='PageBlock', id=id)
        pageblock = getattr(self.aq_explicit, id, None)
        if pageblock is not None:
            ypos = kw.get('pageblock_ypos', None)
            if ypos:
                self.move_object_to_position(pageblock.getId(), int(ypos))
            return pageblock

    security.declareProtected(ManageThemes, 'addPortalPalette')
    def addPortalPalette(self, **kw):
        """
        Add a Portal Palette. Returns the Portal Palette's id
        """
      
        type_name = kw.get('type_name', None)
        if type_name is None:
            return
        type = string.replace(type_name, ' ', '') 

        title = kw.get('title', type)
        value = kw.get('value', None)

        del kw['type_name']
        if kw.has_key('title'):
            del kw['title']
        if kw.has_key('value'):
            del kw['value']

        palettes_dir = self.getPalettesFolder()
        if palettes_dir is None:
            return None

        titles = [getattr(obj, 'title', None) \
                  for obj in palettes_dir.objectValues()]

        i = 0
        while 1:
           if title not in titles:
               break 
           i = i + 1
           title = type + str(i)
           if titles is None: 
               break

        id = getFreeId(self)
        palettes_dir.invokeFactory(type_name, id, title=title, **kw)
        palette = getattr(palettes_dir.aq_explicit, id, None)
        if palette is not None:
            if value:
                setattr(palette, 'value', value)
            verifyThemePerms(palette)
            return palette

    security.declareProtected(ManageThemes, 'addPortalStyle')
    def addPortalStyle(self, **kw):
        """
        Add a Portal Style. Returns the Portal Style's id
        """
      
        tmtool = getToolByName(self, 'portal_themes')
        type_name = kw.get('type_name', None)
        if type_name is None:
            return
        type = string.replace(type_name, ' ', '') 

        title = kw.get('title', type)

        del kw['type_name']
        if kw.has_key('title'):
            del kw['title']

        styles_dir = self.getStylesFolder()
        if styles_dir is None:
            return None

        titles = [getattr(obj, 'title', None) \
                  for obj in styles_dir.objectValues()]

        i = 0
        while 1:
           if title not in titles:
               break 
           i = i + 1
           title = type + str(i)
           if titles is None: 
               break

        id = getFreeId(self)
        styles_dir.invokeFactory(type_name, id, title=title, **kw)
        style = getattr(styles_dir.aq_explicit, id, None)
        if style is not None:
            verifyThemePerms(style)
            self.expireCSSCache()
            return style

    security.declareProtected(ManageThemes, 'editPortalImage')
    def editPortalImage(self, **kw):
        """
        Edit a Portal Image.
        """

        file = kw.get('file', None)
        if file is None:
            return

        imagecat = kw.get('imagecat', '')
        if imagecat not in self.cpsskins_listImageCategories():
            return

        # rebuild the theme to create the image folders.
        if imagecat not in self.objectIds():
            self.rebuild()

        images_dir = getattr(self, imagecat, None)
        if images_dir is None:
            return

        id = kw.get('id', None)
        if id is None:
            return

        img = getattr(images_dir, id, None)
        if img is None:
            return
        # create a thumbnail
        if imagecat == 'thumbnails':
            file = self._createThumbnail(file)
        img.manage_upload(file)

        self.expireCSSCache()
        return img

    security.declareProtected(ManageThemes, 'addPortalImage')
    def addPortalImage(self, **kw):
        """
        Add a Portal Image.
        """

        imagecat = kw.get('imagecat', '')
        if imagecat not in self.cpsskins_listImageCategories():
            return

        images_dir = getattr(self, imagecat, None)
        if images_dir is None:
            return

        file = kw.get('file', None)
        if file is None:
            return

        fn = file.filename
        title = string.split(fn, '/')[-1]
        title = string.split(fn, '\\')[-1]
        id = title

        ids = images_dir.objectIds()
        prefix = title.split('.')[0]
        if imagecat == 'thumbnails':
            ext = THUMBNAIL_IMAGE_FORMAT
        else:
            ext = title.split('.')[1]

        i = 0
        while 1:
           i = i + 1
           if ids is None: 
               break
           if id not in ids:
               break 
           id = prefix + str(i) + '.' + ext

        title = id
        cmfdefault = images_dir.manage_addProduct['CMFDefault']
        cmfdefault.manage_addContent(id=id, type='Portal Image')

        img = getattr(images_dir, id, None)
        kw['id'] = id
        self.editPortalImage(**kw)
        img.manage_changeProperties(title=title)

        return img

    security.declareProtected(ManageThemes, 'findOrphanedStyles')
    def findOrphanedStyles(self, **kw):
        """
        Returns the list of styles that are not used.
        """

        stylesfolder = self.getStylesFolder()
        list = []
        for style in stylesfolder.objectValues():
             if hasattr(style.aq_explicit, 'isOrphan'):
                 if style.isOrphan():
                     list.append(style)
        return list

    security.declareProtected(ManageThemes, 'getTemplets')
    def getTemplets(self):
        """
        Returns the list of templets.
        """

        pageblocks = self.getPageBlocks()
        templets = []
        for pageblock in pageblocks:
             maxcols = getattr(pageblock, 'maxcols', None)
             pageblock_closed = pageblock.closed
             if maxcols is not None:
                 maxcols = int(maxcols)
             for obj in pageblock.objectValues():
                 o = obj.aq_explicit
                 if getattr(o, 'isportaltemplet', 0):
                     templets.append(obj)
        return templets 

    security.declareProtected(ManageThemes, 'getTempletByPath')
    def getTempletByPath(self, templet_path=None):
        """
        Returns a Templet by its physical path.
        """

        if templet_path is None:
            return None
        return self.unrestrictedTraverse(templet_path, default=None)

    security.declareProtected(ManageThemes, 'getI18nTemplets')
    def getI18nTemplets(self, **kw):
        """
        Returns the list of templets that are translated
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
        """
        Returns the list of invisible templets.
        """

        invisible_templets = []
        pageblocks = self.getPageBlocks()
        for pageblock in pageblocks:
             maxcols = getattr(pageblock, 'maxcols', None)
             pageblock_closed = pageblock.closed
             if maxcols is not None:
                 maxcols = int(maxcols)
             for obj in pageblock.objectValues():
                 o = obj.aq_explicit
                 if getattr(o, 'isportaltemplet', 0):
                     if obj.closed:
                         invisible_templets.append(obj)
                         continue
                     if pageblock_closed:
                         invisible_templets.append(obj)
                         continue
                     xpos = getattr(obj, 'xpos', None)
                     if xpos is not None and xpos >= maxcols:
                         invisible_templets.append(obj)
        return invisible_templets

    #
    # Action aliases
    #
    security.declareProtected(ManageThemes, 'edit_form')
    def edit_form(self, **kw):
        """
        Call the 'edit' action.
        """
        return callAction(self, 'edit', **kw)

    security.declareProtected(ManageThemes, 'edit_styles')
    def edit_styles(self, **kw):
        """
        Call the 'edit styles' action.
        """
        return callAction(self, 'edit_styles', **kw)

    security.declareProtected(ManageThemes, 'edit_palettes')
    def edit_palettes(self, **kw):
        """
        Call the 'edit palettes' action.
        """
        return callAction(self, 'edit_palettes', **kw)

    security.declareProtected(ManageThemes, 'edit_images')
    def edit_images(self, **kw):
        """
        Call the 'edit styles' action.
        """
        return callAction(self, 'edit_images', **kw)

    security.declareProtected(ManageThemes, 'manage_cache')
    def manage_cache(self, **kw):
        """
        Call the 'manage cache' action.
        """
        return callAction(self, 'manage_cache', **kw)

    security.declareProtected(ManageThemes, 'manage_themes')
    def manage_themes(self, **kw):
        """
        Call the 'manage themes' action.
        """
        return callAction(self, 'manage_themes', **kw)

    #
    # Local methods
    #
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

    security.declarePublic( 'get_object_position')
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

    #
    # RAM Cache
    #
    security.declareProtected('Manage Themes', 'manage_clearCacheOrphans')
    def manage_clearCacheOrphans(self, REQUEST=None):
        """Removes orphaned objects from the cache."""

        orphans = self.findCacheOrphans()
        for orphan in orphans:
            self.invalidateCacheEntriesById(orphan)

        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(self.absolute_url() + '/manage_RAMCache')

    security.declareProtected('Manage Themes', 'manage_clearCache')
    def manage_clearCache(self, REQUEST=None):
        """Clears the local RAM cache."""

        self.clearCache()

        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(self.absolute_url() + '/manage_RAMCache')

    security.declareProtected('Manage Themes', 'invalidateCacheEntriesById')
    def invalidateCacheEntriesById(self, obid=None, REQUEST=None):
        """Removes local cache entries that match a given Templet id.
           This method can be used to clean orphaned cache entries.

           In a ZEO environment only the local RAM cache entries will be erased.
           If the Templet still exists then 'templet.expireCache()' should be used
           instead in order to propagate the information between ZEO instances.
        """
                                                
        cache = self.getTempletCache()
        if cache is None:                       
            return                              
        cache.delEntries(obid)

    security.declareProtected(ManageThemes, 'invalidateCSSCache')
    def invalidateCSSCache(self):
        """Invalidates the CSS RAM Cache.

           In a ZEO environment only the local RAM cache will be invalidated.
           Use 'theme.expireCSSCache()' to propagate the information between
           all ZEO instances.
        """
   
        cache = self.getCSSCache()
        if cache is None:                       
            return                              
        cache.invalidate()
        
    security.declareProtected(ManageThemes, 'invalidateJSCache')
    def invalidateJSCache(self, ob=None):
        """Invalidates the JavaScript RAM Cache.

           In a ZEO environment only the local RAM cache will be invalidated.
           Use 'theme.expireJSCache()' to propagate the information between
           all ZEO instances.
        """
   
        cache = self.getJSCache()
        if cache is None:                       
            return                              
        cache.invalidate()

    security.declarePublic('findCacheOrphans')
    def findCacheOrphans(self):
        """
        Returns the list of object ids that are in the cache
        but that no longer exist.
        """

        cache = self.getTempletCache()
        if cache is None:
            return []
        templets = self.getTemplets()
        cached_templets_paths = [t.getPhysicalPath() for t in templets \
                                 if getattr(t, 'cacheable')]
        orphans = []
        for index, entry in cache.getEntries():
            templet_path = index[0]
            if templet_path not in (cached_templets_paths + orphans):
                orphans.append(templet_path)
        return orphans

    security.declarePublic('getCacheStats')
    def getCacheStats(self):
        """
        Returns statistics about the cache.
        """
 
        cache = self.getTempletCache()
        if cache is None:
            return 

        stats = cache.getStats()
        count = stats['count']
        hits = stats['hits']
        size = stats['size']

        if count > 0:
            effectivity = 100 * hits / count
        else:
            effectivity = 100
  
        return {'effectivity': effectivity, 
                'size': size, }

    security.declarePublic('getCacheReport')
    def getCacheReport(self):
        """
        Returns detailed statistics about the cache.
        """

        cache = self.getTempletCache()
        if cache is None:
            return  
        return cache.getReport()
                    
    security.declarePublic('getCacheSize')
    def getCacheSize(self):
        """         
        Returns the size of the cache.
        """         
                    
        size = 0
        templetcache = self.getTempletCache()
        if templetcache is not None:
            size += templetcache.getSize()
        csscache = self.getCSSCache()
        if csscache is not None:
            size += csscache.getSize()
        jscache = self.getJSCache()
        if jscache is not None:
            size += jscache.getSize()
        return size 

    security.declarePublic('getTempletCache')
    def getTempletCache(self, create=0):
        """Returns the Templet RAM cache object"""

        cacheid = '_'.join((TEMPLET_RAMCACHE_ID,) + self.getPhysicalPath()[1:])
        try:
            return self.caches[cacheid]
        except KeyError:
            cache = RAMCache()
            self.caches[cacheid] = cache
            return cache

    security.declarePublic('getCSSCache')
    def getCSSCache(self, create=0):
        """ Returns the CSS RAM cache object"""

        cacheid = '_'.join((CSS_RAMCACHE_ID,) + self.getPhysicalPath()[1:])
        try:
            return self.caches[cacheid]
        except KeyError:
            cache = SimpleRAMCache()
            self.caches[cacheid] = cache
            return cache

    security.declarePublic('getJSCache')
    def getJSCache(self, create=0):
        """ Returns the javascript RAM cache object"""
                 
        cacheid = '_'.join((JS_RAMCACHE_ID,) + self.getPhysicalPath()[1:])
        try:
            return self.caches[cacheid]
        except KeyError:
            cache = SimpleRAMCache()
            self.caches[cacheid] = cache
            return cache

    #
    # Private
    #
    security.declarePrivate('_createThumbnail')
    def _createThumbnail(self, file=None):
        """Create a thumbnail image.
        """

        if file is None:
            return

        width, height = THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT
        if isPILAvailable:
            try:
                img = PIL.Image.open(file)
            except IOError:
                pass
            else:
                image = img.resize((width, height), PIL.Image.ANTIALIAS)
                file.seek(0)
                image.save(file, THUMBNAIL_IMAGE_FORMAT)
        return file


InitializeClass(PortalTheme)

def addPortalTheme(dispatcher, id, REQUEST=None):
    """Add a Portal Theme."""
    ob = PortalTheme(id)
    container = dispatcher.Destination()
    container._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
