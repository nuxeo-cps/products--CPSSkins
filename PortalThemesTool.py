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
  PortalThemesTool
"""

import os
import md5
from os.path import join, isfile
from urllib import urlopen
from DateTime import DateTime

from Globals import InitializeClass, DTMLFile
from AccessControl import ClassSecurityInfo, Unauthorized
from ZODB.PersistentList import PersistentList

from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore.ActionInformation import ActionInformation
from Products.CMFCore.Expression import Expression
from Products.CMFCore.utils import getToolByName

from ThemeFolder import ThemeFolder
from CPSSkinsPermissions import ManageThemes
from cpsskins_utils import getFreeId
import QuickImporter

CPSSKINS_THEME_COOKIE_NAME = 'cpsskins_theme'

STATUS_NO_THEME_INFO = 0
STATUS_THEME_INSTALL_OK = 1
STATUS_THEME_INSTALL_FAILED = 2
STATUS_THEME_RETRIEVE_FAILED = 3
STATUS_THEME_REBUILD_FAILED = 4
STATUS_NO_NEW_THEME = 5
STATUS_NEW_THEME_AVAILABLE = 6

class PortalThemesTool(ThemeFolder, ActionProviderBase):
    """
    Portal Themes Tool
    """

    id = 'portal_themes'
    meta_type = 'Portal Themes Tool'
    portal_type = 'Portal Themes Tool'

    _actions = (
        ActionInformation(
            id='configThemes',
            title='_action_themes_reconfig_',
            description='Configure Portal Themes',
            action=Expression(
                text='string: ${portal_url}/cpsskins_themes_reconfig_form'),
                permissions=('View',),
                category='global',
                condition='python: member and portal.portal_membership.checkPermission(\'Manage Themes\', portal.portal_themes)',
                visible=1, 
        ),
    )            

    security = ClassSecurityInfo()

    manage_options = ( ThemeFolder.manage_options[0:1]
                     + ( {'label': 'Default theme', 
		          'action': 'manage_selectDefaultTheme'}, )
                     + ( {'label' : 'External Themes', 
		          'action' : 'manage_externalThemes' }, )
                     + ( {'label': 'Rebuild', 
		          'action': 'manage_themesRebuild'}, )
                     + ( {'label' : 'Overview', 
		          'action' : 'manage_overview' }, )
                     + ( {'label' : 'RAM Cache', 
		          'action' : 'manage_RAMCaches' }, )
                     + ActionProviderBase.manage_options 
                     )

    def __init__(self):
        ThemeFolder.__init__(self, self.id)
        self.externalthemes = PersistentList()

    #
    #   ActionProvider interface
    #
    security.declarePublic('listActions')
    def listActions(self, info=None):
        """
        Return actions provided via tool.
        """
        return self._actions 

    #
    # ZMI
    #
    security.declareProtected(ManageThemes, 'manage_externalThemes')
    manage_externalThemes = DTMLFile('zmi/manage_externalThemes', globals())

    security.declareProtected(ManageThemes, 'manage_selectDefaultTheme')
    manage_selectDefaultTheme = DTMLFile('zmi/manage_selectDefaultTheme', 
                                          globals())
    security.declareProtected(ManageThemes, 'manage_themesRebuild')
    manage_themesRebuild = DTMLFile('zmi/manage_themesRebuild', globals())

    security.declareProtected(ManageThemes, 'manage_overview')
    manage_overview = DTMLFile('zmi/explainPortalThemesTool', globals())

    security.declareProtected(ManageThemes, 'manage_RAMCaches')
    manage_RAMCaches = DTMLFile('zmi/manage_RAMCaches', globals())

    #
    # Public API
    #
    security.declarePublic('getThemeCookieID')
    def getThemeCookieID(self):
        """ Gets the cookie ID used to set themes """
        return CPSSKINS_THEME_COOKIE_NAME

    security.declarePublic('getPortalThemeRoot')
    def getPortalThemeRoot(self, object=None):
        """ Gets the portal theme root container of a given object """

        if object is None:
            return
        rurl = object.absolute_url(relative=1)
        path = rurl.split('/')
        path_length = len(path)
    
        for p in range(0,path_length):
            if path[p] == 'portal_themes' and p < path_length - 1:
                theme_name = path[p+1]
                theme_container = self.getThemeContainer(theme=theme_name)
                return theme_container     

        o = object.aq_explicit
        if getattr(o, 'isportaltheme', 0):
            return object

    security.declarePublic('findStylesFor')
    def findStylesFor(self, category=None, object=None, title=None ):
        """ Gets the list of available styles:
            - by meta type ('category') 
            - for a given object ('object') 
            - that has a given title ('title') [optional]
        """

        style = {}
        title_list = []
        object_list = []
        if object is None:
             return

        themeroot = self.getPortalThemeRoot(object)
        if themeroot is None:
             return

        styles_dir = getattr(themeroot, 'styles', None)
        if styles_dir is None:
            return

        for obj in styles_dir.objectValues():
            if getattr(obj, 'meta_type', None) == category:
                if title:
                    obj_title = obj.getTitle()
                    if obj_title != title:
                        continue
                title_list.append(obj.title)
                object_list.append(obj)

        style['title'] = title_list
        style['object'] = object_list
        return style

    security.declarePublic('listPalettes')
    def listPalettes(self, category=None, object=None ):
        """ Gets the list of available palettes for a given object"""

        palette = {}
        title_list = []
        object_list = []
        if object is None:
             return

        themeroot = self.getPortalThemeRoot(object)
        if themeroot is None:
             return

        palettes_dir = getattr(themeroot, 'palettes', None)
        if palettes_dir is None:
            return

        for obj in palettes_dir.objectValues():
            if getattr(obj.aq_explicit, 'meta_type', None) == category:
                title_list.append(obj.title)
                object_list.append(obj)

        palette['title'] = title_list
        palette['object'] = object_list
        return palette

    security.declarePublic('listStyleTypes')
    def listStyleTypes(self):
        """Gets the list of style types.
           Returns the type information.
        """

        list = []
        for ti in self.portal_types.listTypeInfo():
            if ti.getActionById('isportalstyle', None):
                list.append(ti)
        return list

    security.declarePublic('listStyleMetaTypes')
    def listStyleMetaTypes(self):
        """Gets the list of style meta types."""

        return [s.Metatype() for s in self.listStyleTypes()]

    security.declarePublic('getPageBlocks')
    def getPageBlocks(self, theme=None):
        """Returns a list of page blocks sorted in vertical order."""

        theme_container =  self.getEffectiveThemeContainer(theme=theme)
        if theme_container is None:
            return None
        return theme_container.getPageBlocks()

    security.declarePublic('listThemeRenderers')
    def listThemeRenderers(self):
        """ returns the list of theme renderers """

        renderers = ['default', 
                     'compatible', 
                     'textonly', 
                     'automatic', 
                     'profiler']
        return renderers

    security.declarePublic('getThemeRenderer')
    def getThemeRenderer(self, theme_renderer=None, REQUEST=None):
        """ returns the name of the theme renderer """

        if theme_renderer is None:
            theme_renderer = 'default'

        if theme_renderer not in self.listThemeRenderers():
            theme_renderer = 'default'

        if theme_renderer == 'automatic':
            theme_renderer = 'default'
            info = self.cpsskins_browser_detection(REQUEST=REQUEST)
            browser = info[0]
            version = info[1]
            if browser in ['Netscape']:
                theme_renderer = 'compatible'
            if browser in ['Lynx', 'Links']:
                theme_renderer = 'textonly'

        return theme_renderer
    
    security.declarePublic('getThemeContainer')
    def getThemeContainer(self, theme=None, parent=None ):
        """Gets the themes container.
           - theme = 'printable' | 'default' | ... 
           - theme = None : will return the first available theme
           - parent = 1 : returns the 'themes' folder
        """

        portal_themes = getToolByName(self, 'portal_themes')
        if parent:
            return portal_themes

        themes = self.objectIds()
        if theme is not None and theme in themes:
            return getattr(portal_themes, theme, None)

        if themes:
            default_theme = self.getDefaultThemeName()
            return getattr(portal_themes, default_theme, None)

    security.declarePublic('getDefaultThemeName')
    def getDefaultThemeName(self, REQUEST=None):
        """ gets the default theme
        """
 
        themes =  self.getThemes() 
        for theme in themes:
           if theme.isDefaultTheme():
               return theme.getId()
        if themes:
           return themes[0].getId()

    security.declareProtected('Manage Themes', 'setDefaultTheme')
    def setDefaultTheme(self, default_theme=None, REQUEST=None):
        """ sets the default theme. 
        """
 
        themes =  self.getThemes() 
        for theme in themes:
             if theme.getId() == default_theme:
                theme.default = 1
             else:
                theme.default = 0

        msg = 'Settings updated'
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(self.absolute_url() + \
                '/manage_selectDefaultTheme?manage_tabs_message=' + msg)
 
    security.declarePublic('getRequestedThemeName')
    def getRequestedThemeName(self, REQUEST=None):
        """Gets the name of the requested theme by checking 
           if there is a 'cpsskins_theme' cookie, ?pp=1, or ?theme=...
        """

        if REQUEST is None:
            return

        if hasattr(REQUEST, 'pp'):
            return 'printable'

        if hasattr(REQUEST, 'theme'):
            return REQUEST.form['theme']

        if hasattr(REQUEST, 'cpsskins_theme'):
            return REQUEST['cpsskins_theme']

        if hasattr(REQUEST, CPSSKINS_THEME_COOKIE_NAME):
            return REQUEST.cookies[CPSSKINS_THEME_COOKIE_NAME]

        return self.getDefaultThemeName()

    def getEffectiveThemeContainer(self, theme=None):
        """Gets a theme container by theme name - if available.
        """

        if theme is not None:
            # theme explicitly specified
            theme_container = self.getThemeContainer(theme=theme)
            if theme_container is not None:
                return theme_container

        default_theme_container = self.getThemeContainer(theme='default')
        return default_theme_container

    security.declarePublic('getThemes')
    def getThemes(self):
        """Gets the list of global themes ('default', 'printable', ... )
           returns a list of names.
        """
     
        themes_container = self.getThemeContainer(parent=1)
        theme_list = []

        if themes_container:
           theme_list = themes_container.objectValues('Portal Theme')

        return theme_list

    security.declarePublic('getIconFor')
    def getIconFor(self, category, id):
        """ Returns an action icon - based on CMFActionsIcons
        """
        icons = {}
        actionicons = getToolByName(self, 'portal_actionicons', None)

        if actionicons:
            try:
               iconinfo = actionicons.getActionIcon(category, id)
            except:
               pass
            else:
               return iconinfo

    security.declarePublic('getIconsInfo')
    def getIconsInfo(self, actions=None, ):
        """ Returns action icons as a dictionary - based on CMFActionsIcons
        """

        icons = {}
        actionicons = getToolByName(self, 'portal_actionicons', None)
        if actionicons:
            for action in actions:
                if action.find(':') == -1:
                    continue
                category, id = action.split(':')
                try:
                    icon_path = actionicons.getActionIcon(category, id)
                    try:
                        iconobj = self.restrictedTraverse(icon_path)
                    except:
                        continue
                    icon = icons.setdefault( (category, id),
                               {'path': icon_path, 
                                'url': iconobj.absolute_url(),
                                'width': iconobj.width,
                                'height': iconobj.height,
                                }
                    )
                except:
                    pass
        return icons

    security.declareProtected(ManageThemes, 'delObject')
    def delObject(self, object=None):
        """ Deletes an object """
 
        if object is None:
           return

        container = object.aq_parent
        theme_container = self.getPortalThemeRoot(object)

        mtool = getToolByName(self, 'portal_membership')
        if not mtool.checkPermission(ManageThemes, container):
            raise Unauthorized
        container.manage_delObjects(object.getId())

        theme_container.expireCSSCache()
        theme_container.expireJSCache()

    security.declareProtected(ManageThemes, 'addPortalTheme')
    def addPortalTheme(self, empty=0, **kw):
        """ Creates a new Portal Theme. Returns the theme's id. 
            If 'empty' is set to 1, the theme will be empty, 
            otherwise a minimal theme will be created.
        """
        
        id = kw.get('id', 'PortalTheme')
        new_id = getFreeId(self, try_id=id)
        cpsskins = self.manage_addProduct['CPSSkins']
        cpsskins.manage_addContent(id=new_id, type='Portal Theme')
        theme = getattr(self, new_id, None)
        theme.createThemeSkeleton()

        if empty:
            return theme
        pageblock = theme.addPageBlock()
        if pageblock is not None:
           maincontent = pageblock.addTemplet(type_name='Main Content Templet')
        pageblock.edit(maxcols=int(3))
        maincontent.edit(xpos=int(1))
        col1 = pageblock.addCellSizer(xpos=int(0))
        col2 = pageblock.addCellSizer(xpos=int(1))
        col3 = pageblock.addCellSizer(xpos=int(2))
        col1.edit(cellwidth='20%') 
        col2.edit(cellwidth='60%') 
        col3.edit(cellwidth='20%') 
        return theme
      
    #
    # Theme management
    #
    security.declareProtected(ManageThemes, 'manage_clearCaches')
    def manage_clearCaches(self, REQUEST=None):
        """
        Clear the RAM caches.
        """

        for theme in self.getThemes():
            theme.clearCache()

        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(REQUEST['HTTP_REFERER'])

    security.declareProtected(ManageThemes, 'getCachesSize')
    def getCachesSize(self):
        """Returns the total RAM caches size""" 

        size = 0
        for theme in self.getThemes():
            size += theme.getCacheSize()
        return size

    security.declareProtected(ManageThemes, 'importTheme')
    def importTheme(self, file=None, REQUEST=None):
        """ Imports a theme from a .zexp file
            Returns the its id
        """

        if file is None:
            return

        tmp_id = getFreeId(self, try_id='tmp')
        self.invokeFactory('Theme Folder', id=tmp_id)
        tmp_dir = getattr(self.aq_explicit, tmp_id, None)
        if tmp_dir is None:
           return 

        try:
            QuickImporter.manage_doQuickImport(tmp_dir, file, \
                             set_owner=0, leave=0, REQUEST=None)
        except:
            return

        theme_id = tmp_dir.objectIds()[0]
        new_id = getFreeId(self, try_id=theme_id)
        if new_id != theme_id: 
           tmp_dir.manage_renameObjects([theme_id], [new_id])

        cookie = tmp_dir.manage_cutObjects([new_id])
        self.manage_pasteObjects(cookie)
        self.manage_delObjects(tmp_id)
        return new_id

    security.declareProtected(ManageThemes, 'manage_rebuild')
    def manage_rebuild(self, REQUEST=None, **kw):
        """
        Rebuild this theme
        """

        if REQUEST is not None:
            kw.update(REQUEST.form)
        self.rebuild(**kw)
        self.manage_permission(ManageThemes, \
            ('Manager', 'Owner', 'ThemeManager'), \
             acquire=0)
        self.reindexObjectSecurity()

        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(self.absolute_url() + '/manage_main')

    security.declareProtected(ManageThemes, 'rebuild')
    def rebuild(self, **kw):
        """
        Rebuild all the themes
        """

        for obj in self.objectValues('Portal Theme'):
            obj.rebuild(**kw)

    #
    # External Themes
    #
    security.declarePublic('getStatusMsgs')
    def getStatusMsgs(self):
        """ get the status codes """
        
        info = {STATUS_NO_THEME_INFO: '',
                STATUS_THEME_INSTALL_OK: 'Theme installed',
                STATUS_THEME_INSTALL_FAILED: 'FAILED',
                STATUS_THEME_RETRIEVE_FAILED: 'NOT FOUND',
                STATUS_THEME_REBUILD_FAILED: 'THEME REBUILD FAILED',
                STATUS_NO_NEW_THEME: 'OK',
                STATUS_NEW_THEME_AVAILABLE: 'New theme available!',
               }
        return info

    security.declareProtected('Manage portal', 'getExternalThemes')
    def getExternalThemes(self):
        """ gets a list of external themes """
        
        if not hasattr(self, 'externalthemes'):
            self.externalthemes = PersistentList()
        return self.externalthemes
        
    security.declarePublic('getExternalThemeIds')
    def getExternalThemeIds(self, REQUEST=None):
        """ get external theme ids """
        
        externalthemes = self.getExternalThemes()
        return [t['themeid'] for t in externalthemes]

    security.declareProtected('Manage portal', 'manage_changeExternalThemes')
    def manage_changeExternalThemes(self, form={}, REQUEST=None):
        """ updates a list external themes """
     
        form = form.copy()
        if REQUEST is not None:
            form.update(REQUEST.form)
        keys = form.get('keys')
        len_keys = form.get('len_keys')

        if keys is not None:
            themeids = form.get('themeids')
            themeurls = form.get('themeurls')
            if len_keys == 1:
                themeids = [themeids]
                themeurls = [themeurls]
            externalthemes = self.externalthemes
            for key in keys:
                key = eval(key)
                themeid = key['themeid']
                themeurl = themeurls[themeids.index(themeid)]
                if themeurl.startswith('http://') or \
                   themeurl.startswith('https://') or \
                   themeurl.startswith('ftp://'):
                    index = externalthemes.index(key)
                    externalthemes[index] = {'themeid': themeid, 
                                             'themeurl': themeurl, 
                                             'status': STATUS_NO_THEME_INFO, 
                                             'updated': ''}
            self.externalthemes = externalthemes

        msg = 'Settings updated'
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(self.absolute_url() + \
                '/manage_externalThemes?manage_tabs_message=' + msg)

    security.declareProtected('Manage portal', 'manage_delExternalThemes')
    def manage_delExternalThemes(self, form={}, REQUEST=None):
        """ updates a list external themes """
     
        form = form.copy()
        if REQUEST is not None:
            form.update(REQUEST.form)
        keys = form.get('keys')

        if keys is not None:
            externalthemes = self.externalthemes
            for key in keys:
                key = eval(key)
                index = externalthemes.index(key)
                del externalthemes[index]
            self.externalthemes = externalthemes

        msg = 'Settings updated'
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(self.absolute_url() + \
                '/manage_externalThemes?manage_tabs_message=' + msg)


    security.declareProtected(ManageThemes, 'manage_addExternalTheme')
    def manage_addExternalTheme(self, themeid=None, themeurl=None,
                                REQUEST=None):
        """
        Adds an external theme
        """
  
        msg = ''
        error = 0
        externalthemes = self.externalthemes
      
        themeids = [t['themeid'] for t in externalthemes]
        if not themeid.isalnum(): 
            msg += '\n- The theme ID is invalid'
            error = 1

        if themeid in themeids: 
            msg += '\n- The theme ID is already in use'
            error = 1

        if not (themeurl.startswith('http://') or \
                themeurl.startswith('https://') or \
                themeurl.startswith('ftp://')): 
            msg += '\n- The theme URL must start with \
                    http://, https:// or ftp:// ...'
            error = 1

        if not error:
            externalthemes = self.getExternalThemes()
            externalthemes.append({'themeid': themeid, 
                                   'themeurl': themeurl, 
                                   'updated': '', 
                                   'status': STATUS_NO_THEME_INFO})
            self.externalthemes = externalthemes
            msg = 'Settings updated'

        if error:
            msg = 'ERROR:' + msg

        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(self.absolute_url() + \
                '/manage_externalThemes?manage_tabs_message=' + msg)

    security.declareProtected(ManageThemes, 'installExternalTheme')
    def installExternalTheme(self, theme=None, REQUEST=None):
        """ retrieves and installs an external theme 
            return the theme information """


        themeid = theme.get('themeid', None)
        themeurl = theme.get('themeurl', None)
        md5sum = theme.get('md5sum', None)
        if themeid is None or themeurl is None:
            return None

        try:
            f = urlopen(themeurl)
            zexp_data = f.read()
        except:
            return None

        new_md5sum = md5.new(zexp_data).hexdigest()
        theme['md5sum'] = new_md5sum
        if new_md5sum == md5sum:
            return None
        
        # Installing external theme
        default_theme = self.getDefaultThemeName()

        filename = 'cpsskins_theme_%s.zexp' % themeid
        filepath = join(INSTANCE_HOME, 'import', \
                        'cpsskins_theme_%s.zexp' % themeid)
        writefile = open(filepath, "wb")
        writefile.write(zexp_data)
        writefile.close()
        
        tmp_id = getFreeId(self, try_id='tmp')
        self.invokeFactory('Theme Folder', id=tmp_id)
        tmp_dir = getattr(self.aq_explicit, tmp_id, None)
        if tmp_dir is None:
           return None

        tmp_dir.manage_importObject(file=filename, set_owner=0)
        if themeid in self.objectIds():
            self.manage_delObjects(themeid)

        current_id = tmp_dir.objectIds()[0]
        if current_id != themeid: 
           tmp_dir.manage_renameObjects([current_id], [themeid])

        cookie = tmp_dir.manage_cutObjects([themeid])
        self.manage_pasteObjects(cookie)
        self.manage_delObjects(tmp_id)

        if isfile(filepath):
            os.remove(filepath)

        new_theme = getattr(self, themeid, None)
        if new_theme is not None:
            theme['updated'] = DateTime().ISO()
            try:
                new_theme.rebuild(setperms=1)
            except:
                theme['status'] = STATUS_THEME_REBUILD_FAILED
            else:
                theme['status'] = STATUS_THEME_INSTALL_OK
        else:
            theme['status'] = STATUS_THEME_INSTALL_FAILED

        return self.setDefaultTheme(default_theme)

    security.declareProtected(ManageThemes, 'manage_synchronizeExternalThemes')
    def manage_synchronizeExternalThemes(self, REQUEST=None):
        """ synchronizes external themes """

        themes = []
        new_themes = 0
        for theme in self.externalthemes:
            themeid = theme.get('themeid', None)
            themeurl = theme.get('themeurl', None)
            md5sum = theme.get('md5sum', None)

            try:
                f = urlopen(themeurl)
                zexp_data = f.read()
            except:
                theme['status'] = STATUS_THEME_RETRIEVE_FAILED
            else:
                new_md5sum = md5.new(zexp_data).hexdigest()
                if new_md5sum == md5sum:
                    if theme['status'] == STATUS_NO_THEME_INFO:
                        theme['status'] = STATUS_NO_NEW_THEME
                else:
                    theme['status'] = STATUS_NEW_THEME_AVAILABLE
                    new_themes += 1
            themes.append(theme)
        self.externalthemes = themes

        if new_themes == 1:
            msg = '1 theme can be updated.'
        elif new_themes > 1:
            msg = '%s themes can be updated.' % new_themes
        else: 
            msg = 'All themes are up-to-date.'
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(self.absolute_url() + \
                '/manage_externalThemes?manage_tabs_message=' + msg)

    security.declareProtected(ManageThemes, 'manage_updateExternalThemes')
    def manage_updateExternalThemes(self, force=0, REQUEST=None):
        """ updates external themes """

        for theme in self.externalthemes:
            if force == 1:
                theme['md5sum'] = STATUS_NO_THEME_INFO
            res = self.installExternalTheme(theme=theme)
            if res is not None:
                theme = res

        msg = 'Themes have been updated'
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(self.absolute_url() + \
                '/manage_externalThemes?manage_tabs_message=' + msg)

    security.declareProtected(ManageThemes, 'manage_forceupdateExternalThemes')
    def manage_forceupdateExternalThemes(self, REQUEST=None):
        """ updates external themes, invalidates checksums """

        self.manage_updateExternalThemes(force=1)
        return self.manage_externalThemes(themeid='', themeurl='', \
                    manage_tabs_message='Themes have been updated')

InitializeClass(PortalThemesTool)
