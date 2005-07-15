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
  PortalThemesTool
"""

import os
import md5
from os.path import basename, join, isfile
from urllib import urlopen
from DateTime import DateTime

from Globals import InitializeClass, DTMLFile
from AccessControl import ClassSecurityInfo, Unauthorized
from Acquisition import aq_base, aq_parent, aq_inner
from types import StringType, TupleType

from Globals import PersistentMapping
try: from ZODB.PersistentList import PersistentList
except ImportError: from persistent.list import PersistentList

from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore.ActionInformation import ActionInformation
from Products.CMFCore.Expression import Expression
from Products.CMFCore.utils import getToolByName

from ThemeFolder import ThemeFolder
from CPSSkinsPermissions import ManageThemes
from cpsskins_utils import getFreeId
from QuickImporter import manage_doQuickImport, _deleteFileInImportDirectory, \
                          _writeFileInImportDirectory

# Theme negociation
CPSSKINS_THEME_COOKIE_ID = 'cpsskins_theme'
CPSSKINS_LOCAL_THEME_ID = '.cpsskins_theme'

# External themes
STATUS_NO_THEME_INFO = 0
STATUS_THEME_INSTALL_OK = 1
STATUS_THEME_INSTALL_FAILED = 2
STATUS_THEME_RETRIEVE_FAILED = 3
STATUS_THEME_REBUILD_FAILED = 4
STATUS_NO_NEW_THEME = 5
STATUS_NEW_THEME_AVAILABLE = 6

VIEW_MODE_SESSION_KEY = 'cpsskins_view_mode'

# Actions
THEME_CONFIG_ACTION_ID = 'configThemes'
THEME_CONFIG_ACTION_CATEGORY = 'global'
DEFAULT_ACCESSKEY = '*'

class PortalThemesTool(ThemeFolder, ActionProviderBase):
    """
    Portal Themes Tool
    """

    id = 'portal_themes'
    meta_type = 'Portal Themes Tool'
    portal_type = 'Portal Themes Tool'

    _actions = (
        ActionInformation(
            id=THEME_CONFIG_ACTION_ID,
            title='_action_themes_reconfig_',
            description='Configure Portal Themes',
            action=Expression(
                text='string:${portal_url}/cpsskins_themes_reconfig_form'),
                permissions=('View',),
                category=THEME_CONFIG_ACTION_CATEGORY,
                condition='python: member and portal.portal_membership.checkPermission(\'Manage Themes\', portal.portal_themes)',
                visible=1),
    )

    security = ClassSecurityInfo()

    manage_options = ( ThemeFolder.manage_options[0:1]
                     + ( {'label': 'Default theme',
                          'action': 'manage_selectDefaultTheme'}, )
                     + ( {'label' : 'External Themes',
                          'action' : 'manage_externalThemes' }, )
                     + ( {'label' : 'Method Themes',
                          'action' : 'manage_methodThemes' }, )
                     + ( {'label': 'Rebuild',
                          'action': 'manage_themesRebuild'}, )
                     + ( {'label' : 'Overview',
                          'action' : 'manage_overview' }, )
                     + ( {'label' : 'RAM Cache',
                          'action' : 'manage_RAMCaches' }, )
                     + ( {'label' : 'Options',
                          'action' : 'manage_configureOptions' }, )
                     + ActionProviderBase.manage_options
                     )

    def __init__(self):
        ThemeFolder.__init__(self, self.id)
        self.externalthemes = PersistentList()
        self.method_themes = PersistentMapping()
        self.debug_mode = 0
        self.accesskey = DEFAULT_ACCESSKEY

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

    security.declareProtected(ManageThemes, 'manage_methodThemes')
    manage_methodThemes = DTMLFile('zmi/manage_methodThemes', globals())

    security.declareProtected(ManageThemes, 'manage_selectDefaultTheme')
    manage_selectDefaultTheme = DTMLFile('zmi/manage_selectDefaultTheme',
                                          globals())
    security.declareProtected(ManageThemes, 'manage_themesRebuild')
    manage_themesRebuild = DTMLFile('zmi/manage_themesRebuild', globals())

    security.declareProtected(ManageThemes, 'manage_configureOptions')
    manage_configureOptions = DTMLFile('zmi/manage_configureOptions', globals())

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
        return CPSSKINS_THEME_COOKIE_ID

    #
    # Session management
    #
    security.declarePublic('getViewMode')
    def getViewMode(self):
        """ Gets the current view mode """

        session = self.REQUEST.SESSION
        if session.has_key(VIEW_MODE_SESSION_KEY):
            return session[VIEW_MODE_SESSION_KEY]
        return {}

    security.declarePublic('setViewMode')
    def setViewMode(self, reload=0, **kw):
        """ Sets the current view mode """

        REQUEST = self.REQUEST
        kw.update(REQUEST.form)

        session = REQUEST.SESSION
        session_dict = session.get(VIEW_MODE_SESSION_KEY, {})

        fullscreen = kw.get('fullscreen')
        if fullscreen in ['0', '1']:
            session_dict['fullscreen'] = int(fullscreen)

        for param in ['themes_panel',
                      'portlets_panel',
                      'selected_portlet',
                      'selected_content',
                      'portlets_override',
                      'edited_url',
                      'clipboard',
                      'theme',
                      'page',
                      'edit_mode',
                      'current_url',
                      'scrollx',
                      'scrolly',
                      'current_url']:
            if kw.has_key(param):
                session_dict[param] = kw[param]

        session[VIEW_MODE_SESSION_KEY] = session_dict

        # reload the page
        if reload and REQUEST is not None:
            redirect_url = REQUEST['HTTP_REFERER']
            if '?' in redirect_url:
                redirect_url = redirect_url.split('?')[0]
            REQUEST.RESPONSE.redirect(redirect_url)

    security.declarePublic('clearViewMode')
    def clearViewMode(self, *args):
        """ clear view modes """

        REQUEST = self.REQUEST
        session = REQUEST.SESSION
        session_dict = session.get(VIEW_MODE_SESSION_KEY, {})

        for k in args:
            if k not in session_dict.keys():
                continue
            del session_dict[k]

        session[VIEW_MODE_SESSION_KEY] = session_dict

    security.declarePublic('getPortalThemeRoot')
    def getPortalThemeRoot(self, object=None):
        """ Gets the portal theme root container of a given object """

        if object is None:
            return None
        rurl = object.absolute_url(relative=1)
        path = rurl.split('/')
        path_length = len(path)
        for p in range(0,path_length):
            if path[p] == 'portal_themes' and p < path_length - 1:
                theme_name = path[p+1]
                theme_container = self.getThemeContainer(theme=theme_name)
                return theme_container
        if getattr(object.aq_inner.aq_explicit, 'isportaltheme', 0):
            return object
        return None

    security.declarePublic('getContextObj')
    def getContextObj(self, context=None):
        """Return the context object
        """
        context_obj = None
        REQUEST = self.REQUEST
        context_rurl = REQUEST.form.get('context_rurl')

        if context_rurl is not None:
            utool = getToolByName(self, 'portal_url')
            portal_url = utool(relative=1)
            if portal_url != '/':
                portal_url = '/' + portal_url
            context_obj = self.unrestrictedTraverse(
                portal_url + context_rurl, default=None)

        if context_obj is None:
            context_obj = REQUEST.get('context_obj', context)

        return context_obj

    security.declarePublic('findStylesFor')
    def findStylesFor(self, category=None, object=None, title=None):
        """ Gets the list of available styles:
            - by meta type ('category')
            - for a given object ('object')
            - that has a given title ('title') [optional]
        """
        style = {}
        title_list = []
        object_list = []
        if object is None:
            return []
        themeroot = self.getPortalThemeRoot(object)
        if themeroot is None:
            return []
        styles_dir = getattr(themeroot, 'styles', None)
        if styles_dir is None:
            return []
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
    def listPalettes(self, category=None, object=None):
        """ Gets the list of available palettes for a given object"""

        palette = {}
        title_list = []
        object_list = []
        if object is None:
            return None

        themeroot = self.getPortalThemeRoot(object)
        if themeroot is None:
            return None

        palettes_dir = getattr(themeroot, 'palettes', None)
        if palettes_dir is None:
            return None

        for obj in palettes_dir.objectValues():
            if getattr(aq_base(obj), 'meta_type', None) != category:
                continue
            title_list.append(obj.title)
            object_list.append(obj)

        palette['title'] = title_list
        palette['object'] = object_list
        return palette

    security.declarePublic('listPaletteTypes')
    def listPaletteTypes(self):
        """Gets the list of palette types.
           Returns the type information.
        """

        list = []
        for ti in self.portal_types.listTypeInfo():
            if ti.getActionById('isportalpalette', None):
                list.append(ti)
        return list

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

    security.declarePublic('listPageRenderers')
    def listPageRenderers(self):
        """ returns the list of page renderers """

        renderers = ['default',
                     'compatible',
                     'textonly',
                     'automatic',
                     'profiler']
        return renderers

    security.declarePublic('getPageRenderer')
    def getPageRenderer(self, page_renderer_id=None, tableless=0, macroless=0):
        """ returns the name of the page renderer"""

        if page_renderer_id is None:
            page_renderer_id = 'default'

        elif page_renderer_id not in self.listPageRenderers():
            page_renderer_id = 'default'

        elif page_renderer_id == 'automatic':
            page_renderer_id = 'default'
            info = self.cpsskins_browser_detection()
            browser = info[0]
            version = info[1]
            if browser in ['Netscape']:
                page_renderer_id = 'compatible'
            if browser in ['Lynx', 'Links']:
                page_renderer_id = 'textonly'

        if page_renderer_id == 'default':
            if macroless:
                page_renderer_id = 'macroless'

            elif tableless:
                page_renderer_id = 'tableless'

        return page_renderer_id

    security.declarePublic('getThemeContainer')
    def getThemeContainer(self, theme=None, parent=None):
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
        return None

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
        return None

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

    #
    # Themes by URL
    #
    security.declarePublic('getThemeByMethod')
    def getThemeByMethod(self, meth=None):
        """Returns a theme + page by the method name (zpt, py, dtml, ...)
        """

        method_themes = self.method_themes
        if meth in method_themes.keys():
            return method_themes[meth]

    #
    # Local themes
    #
    security.declarePublic('getLocalThemeID')
    def getLocalThemeID(self):
        """Return the id of the attribute used to identify local themes.
        """

        return CPSSKINS_LOCAL_THEME_ID

    security.declarePublic('getLocalThemeName')
    def getLocalThemeName(self, **kw):
        """Return the name of a local theme in a given context.

           Local themes are obtained from folder attributes, i.e.
           - as the property of a folder (one theme per line)
           - as an object located in the folder that is callable and
             that returns a tuple.

           Local themes are computed by collecting all theme information
           from the portal to the context folder.

           The format for describing themes is:
           - simply a string containing the theme id.

           - 'n-m:theme'

           where:
           - 'theme' is the theme id
           - (n, m) is a couple with n <= m that describes the interval
             inside which the theme will be used.
             (0, 0) means the current folder and all subfolders
             (1, 0) means all subfolders below the current folder
             (1, 1) means the subfolders of level 1
             (0, 1) means the folder and the subfolders of level 1
             (n, n) means the subfolders of level n
             ...

           Examples:
           * with a folder property called '.cpsskins_theme':

             - lines with intervals:

               0-1:theme1
               2-4:theme2
               6-0:theme3

             - string with interval:

               0-1:theme1

             - string without interval:

               theme1

           * with a script called '.cpsskins_theme.py' placed in a folder:

             - tuple with intervals:

               return ('0-1:theme1', '2-4:theme2', '6-0:theme3')

             - string with interval:

               return '0-1:theme'

             - string without interval:

               return 'theme'

        """

        context = kw.get('context_obj')
        if context is None:
            return None

        # Find bottom-most folder:
        obj = context
        bmf = None
        while 1:
            if obj.isPrincipiaFolderish and \
                not obj.getId().startswith('.'):
                bmf = obj
                break
            parent = aq_parent(aq_inner(obj))
            if not obj or parent == obj:
                break
            obj = parent
        if bmf is None:
            bmf = context

        # get themes from the root to current path
        utool = getToolByName(self, 'portal_url')
        portal = utool.getPortalObject()
        level = len(utool.getRelativeContentPath(bmf))

        ob = bmf
        objs = []
        while ob is not None:
            objs.append(ob)
            # move to the parent
            ob = aq_parent(aq_inner(ob))
            if ob is portal:
                break

        # we revert the list since we want to start from the portal and move
        # to the current object, i.e. local themes if they apply to a given
        # folder override the themes set in the folders above.
        objs.reverse()

        # get the local theme
        localtheme = None
        for obj in objs:
            level -= 1
            theme = self._getLocalTheme(folder=obj, level=level)
            if theme is not None:
                localtheme = theme
            # we continue since the local theme can be still be overriden.
        return localtheme

    security.declarePublic('getLocalThemes')
    def getLocalThemes(self, folder=None, **kw):
        """Return the list of local themes in a given context.
        """

        if folder is None:
            return []

        local_theme_id = self.getLocalThemeID()
        if getattr(aq_base(folder), local_theme_id, None) is None:
            return []

        theme_obj = getattr(folder, local_theme_id)
        if theme_obj and callable(theme_obj):
            theme_obj = apply(theme_obj, ())
        if isinstance(theme_obj, StringType):
            theme_obj = (theme_obj, )
        if not isinstance(theme_obj, TupleType):
            return []

        themes = []
        for l in theme_obj:
            if ':' not in l:
                themes.append(((0,0), l))
                continue
            nm, theme = l.split(':')
            if '-' not in nm:
                continue
            n, m = nm.split('-')
            themes.append(((int(n), int(m)), theme))
        return themes

    security.declarePrivate('_getLocalTheme')
    def _getLocalTheme(self, folder=None, level=None):
        """ Return the name of the first theme assigned to a given level
            relative to a folder.
        """

        if level is None:
            return None

        themes = self.getLocalThemes(folder=folder)
        if themes is None:
            return None

        level = int(level)
        for (n, m), theme in themes:
            if n > 0 and n > level:
                continue
            if m > 0 and m < level:
                continue
            return theme

        return None

    security.declarePublic('getLocalThemesAncestor')
    def getLocalThemesAncestor(self, context=None):
        """Return the first ancestor folder in a given context
           in which local themes are defined.
        """

        if context is None:
            return None

        local_theme_id = self.getLocalThemeID()
        # nothing is acquired
        if getattr(context, local_theme_id, None) is None:
            return None
        # we want an ancestor
        if context.hasProperty(local_theme_id):
            return None

        container = context
        while 1:
            try:
                container = aq_parent(aq_inner(container))
            except AttributeError:
                break
            # check for an object in the container
            try:
                container_ids = container.objectIds()
            except AttributeError:
                pass
            else:
                if local_theme_id in container_ids:
                    return container
            # check for a property of the container
            try:
                prop = container.hasProperty(local_theme_id)
            except AttributeError:
                pass
            else:
                if prop:
                    return container
        return None

    #
    # Theme and page negociation
    #
    security.declarePrivate('_extractThemeAndPageName')
    def _extractThemeAndPageName(self, theme=None, page=None):
        """Extract the theme name
        """
        theme_id = theme
        page_id = page
        if theme and '+' in theme:
            theme_id, page_id = theme.split('+')
        return theme_id, page_id

    security.declarePublic('getRequestedThemeAndPageName')
    def getRequestedThemeAndPageName(self, **kw):
        """Gets the name of the requested theme and page by checking a series
           of URL parameters, variables, folder attributes, cookies, ...
        """

        REQUEST = self.REQUEST
        FORM = REQUEST.form
        # selected by writing ?pp=1 in the URL
        if FORM.get('pp') == '1':
            return 'printable', None

        # selected by writing ?theme=... in the URL
        # (+page)
        theme = FORM.get('theme')
        page = FORM.get('page')
        if (theme is not None) or (page is not None):
            return self._extractThemeAndPageName(theme, page)

        if int(kw.get('editing', 0)) == 1:
            # session variable (used in edition mode)
            view_mode = self.getViewMode()
            theme = view_mode.get('theme')
            page = view_mode.get('page')
            if (theme is not None) or (page is not None):
                return self._extractThemeAndPageName(theme, page)

        # cookie (theme + page)
        theme_cookie_id = self.getThemeCookieID()
        theme = REQUEST.cookies.get(theme_cookie_id)
        if theme is not None:
            return self._extractThemeAndPageName(theme, None)

        # method themes (theme + page)
        published = REQUEST.get('PUBLISHED')
        if published is not None:
            try:
                published = published.getId()
            except AttributeError:
                pass
            else:
                theme = self.getThemeByMethod(published)
                if theme is not None:
                    return self._extractThemeAndPageName(theme, None)

        # local theme + page
        theme = self.getLocalThemeName(**kw)
        if theme is not None:
            return self._extractThemeAndPageName(theme, None)

        # default theme, page not specified
        return self.getDefaultThemeName(), None

    security.declarePublic('getEffectiveThemeAndPageName')
    def getEffectiveThemeAndPageName(self, **kw):
        """Get the name of the effective theme and page, i.e. a requested
        theme that effectively exists and a page existing in this theme.
        Otherwise return the name of the default theme and of the default page.
        """
        theme, page = self.getRequestedThemeAndPageName(**kw)
        # theme
        if theme not in self.getThemeNames():
            theme = self.getDefaultThemeName()
        # page
        theme_container = self.getThemeContainer(theme)
        if page not in theme_container.getPageNames():
            page = theme_container.getDefaultPageName()

        # the theme has no page - use the default theme
        if page is None:
            theme = self.getDefaultThemeName()
            theme_container = self.getThemeContainer(theme)
            page = theme_container.getDefaultPageName()
        return theme, page

    security.declarePublic('getThemes')
    def getThemes(self):
        """Gets the list of themes as objects.
        """
        themes_container = self.getThemeContainer(parent=1)
        theme_list = []
        if themes_container:
            theme_list = themes_container.objectValues('Portal Theme')
        return theme_list

    security.declarePublic('getThemeNames')
    def getThemeNames(self):
        """Gets the list of themes by theme id.
        """
        return [t.getId() for t in self.getThemes()]

    security.declarePublic('getThemeAndPageNames')
    def getThemeAndPageNames(self):
        """Return the list of theme and page names
        """
        list = []
        for theme in self.getThemes():
            for page in theme.getPages():
                list.append(
                    '%s+%s' % (theme.getId(), page.getId()))
        return list

    security.declarePublic('getCurrentUrl')
    def getCurrentUrl(self, REQUEST=None):
        """Get the current url
        """

        if REQUEST is None:
            REQUEST = self.REQUEST

        request_url = REQUEST.get('URL', None)
        query_string = REQUEST.get('QUERY_STRING', None)

        if request_url.endswith('/index_html'):
            request_url = request_url[:-11]
        if query_string:
            request_url += '?' + query_string
        return request_url

    security.declarePublic('getCurrentLang')
    def getCurrentLang(self):
        """Get the current language
        """

        # Localizer (CMF, Plone1, CPS3)
        localizer = getattr(self, 'Localizer', None)
        if localizer is not None:
            return localizer.get_selected_language()

        # PloneLanguageTool (Plone2)
        ptool = getToolByName(self, 'portal_languages', None)
        if ptool is not None:
            boundLanguages = ptool.getLanguageBindings()
            if boundLanguages:
                return boundLanguages[0]

        # Portal messages (CPS2)
        mcat = getToolByName(self, 'portal_messages', None)
        if mcat is not None:
            return mcat.get_selected_language()

        # PlacelessTranslation service
        REQUEST = self.REQUEST
        if REQUEST is not None:
            accept_language = REQUEST.get('HTTP_ACCEPT_LANGUAGE')
            if accept_language:
                accept_language = accept_language.split(',')
                if len(accept_language) > 0:
                    return accept_language[0]

        return 'en'

    security.declarePublic('getIconFor')
    def getIconFor(self, category, id):
        """ Returns an action icon - based on CMFActionsIcons
        """
        icons = {}
        actionicons = getToolByName(self, 'portal_actionicons', None)
        if actionicons is not None:
            try:
                iconinfo = actionicons.getActionIcon(category, id)
            except KeyError:
                return None
            else:
                return iconinfo

    security.declarePublic('getIconsInfo')
    def getIconsInfo(self, actions=None):
        """ Returns action icons as a dictionary - based on CMFActionsIcons
        """

        icons = {}
        actionicons = getToolByName(self, 'portal_actionicons', None)
        if actionicons is not None:
            for action in actions:
                if ':' not in action:
                    continue
                category, id = action.split(':')
                try:
                    icon_path = actionicons.getActionIcon(category, id)
                except KeyError:
                    continue
                iconobj = self.unrestrictedTraverse(icon_path, default=None)
                if iconobj is None:
                    continue
                icon = icons.setdefault((category, id), {
                    'path': icon_path,
                    'url': iconobj.absolute_url(),
                    'width': iconobj.width,
                    'height': iconobj.height,
                    })
        return icons

    security.declareProtected(ManageThemes, 'delObject')
    def delObject(self, object=None):
        """ Deletes an object """

        if object is None:
            return

        container = aq_parent(aq_inner(object))
        theme_container = self.getPortalThemeRoot(object)

        # the object is a style
        # remove the references
        if getattr(aq_base(object), 'isportalstyle', 0):
            object.findParents(newtitle='')

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
        themepage = theme.addThemePage()
        pageblock = themepage.addPageBlock()
        if pageblock is not None:
            maincontent = pageblock.addContent(type_name='Main Content Templet')
            maincontent.edit(xpos=int(1))
        pageblock.edit(maxcols=int(3))
        col1 = pageblock.addCellSizer(xpos=int(0))
        col2 = pageblock.addCellSizer(xpos=int(1))
        col3 = pageblock.addCellSizer(xpos=int(2))
        col1.edit(cellwidth='20%')
        col2.edit(cellwidth='60%')
        col3.edit(cellwidth='20%')
        return theme

    security.declarePublic('getTranslationService')
    def getTranslationService(self, root=0, cat=''):
        """Return the translation service
        """
        # CMF / Plone1 / CPS3
        localizer = getToolByName(self, 'Localizer', None)
        if localizer is not None:
            if root:
                return localizer
            if cat:
                return getattr(localizer, cat, None)

            # Localizer without translation service
            ts = getToolByName(self, 'translation_service', None)
            if ts is None:
                return getattr(localizer, 'default', None)

        # CPS2
        portal_messages = getToolByName(self, 'portal_messages', None)
        if portal_messages is not None:
            return portal_messages

        return None

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
            REQUEST.RESPONSE.redirect(self.absolute_url() + '/manage_RAMCaches')

    security.declareProtected(ManageThemes, 'getCachesSize')
    def getCachesSize(self):
        """Returns the total RAM caches size"""

        size = 0
        for theme in self.getThemes():
            size += theme.getCacheSize()
        return size

    security.declareProtected(ManageThemes, 'importTheme')
    def importTheme(self, file=None, REQUEST=None):
        """Import a theme from a .zexp file.
        Return its id
        """

        if file is None:
            return None

        tmp_dir = self._getTemporaryThemeFolder()
        if tmp_dir is None:
            return None

        manage_doQuickImport(
            tmp_dir,
            file,
            set_owner=0,
            leave=0,
            REQUEST=None)

        theme_id = tmp_dir.objectIds()[0]
        new_id = getFreeId(self, try_id=theme_id)
        if new_id != theme_id:
            tmp_dir.manage_renameObjects([theme_id], [new_id])

        cookie = tmp_dir.manage_cutObjects([new_id])
        self.manage_pasteObjects(cookie)
        self.manage_delObjects(tmp_dir.getId())
        return new_id

    security.declareProtected(ManageThemes, 'manage_xmlImport')
    def manage_xmlImport(self, file, options, plugin='CPSSkinsImporter',
                         REQUEST=None):
        """Import a theme from a zip file in XML format (CPSIO)
        """

        psm = ''
        io_tool = getToolByName(self, 'portal_io', None)
        if io_tool is None:
            return

        utool = getToolByName(self, 'portal_url')
        portal = utool.getPortalObject()

        filename = basename(file.filename)
        _writeFileInImportDirectory(file, filename)

        importer = io_tool.getImportPlugin(plugin, portal)
        try:
            importer.setOptions(filename, options=options)
            importer.importFile()
            importer.finalize()
            psm = 'cpsio_psm_import_successful'
        except (ValueError, IOError), err:
            psm = err
        _deleteFileInImportDirectory(filename)
        return psm

    security.declareProtected(ManageThemes, 'manage_rebuild')
    def manage_rebuild(self, REQUEST=None, **kw):
        """
        Rebuild this theme
        """
        if REQUEST is not None:
            kw.update(REQUEST.form)

        self.rebuild(**kw)

        self.manage_permission(
            ManageThemes,
            ('Manager', 'Owner', 'ThemeManager'),
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
    # Access key
    #
    security.declarePublic('getDefaultAccessKey')
    def getDefaultAccessKey(self):
        """Return the value of the default access key
        """

        return DEFAULT_ACCESSKEY

    security.declarePublic('getAccessKey')
    def getAccessKey(self):
        """Return the value of the key used to access the tool
        """

        return self.accesskey

    security.declarePublic('renderAccessKey')
    def renderAccessKey(self, actions=[], **kw):
        """Render the access key html markup
        """

        rendered = ''

        if not actions:
            atool = getToolByName(self, 'portal_actions')
            actions = atool.listFilteredActionsFor(self)

        actions_by_cat = actions.get(THEME_CONFIG_ACTION_CATEGORY)
        if actions_by_cat is None:
            return rendered
        theme_manage_action = [
            ac for ac in actions_by_cat
            if ac.get('id') == THEME_CONFIG_ACTION_ID]

        if len(theme_manage_action) > 0:
            action = theme_manage_action[0]
        else:
            return rendered

        rendered = '<a href="%s" accesskey="%s"></a>' % \
            (action['url'], self.getAccessKey())
        return rendered

    security.declarePublic('renderAccessKeys')
    def renderAccessKeys(self, **kw):
        """Render all access keys
        """
        rendered = self.renderAccessKey(**kw)
        # CPSPortlets
        ptltool = getToolByName(self, 'portal_cpsportlets', None)
        if ptltool is not None:
            try:
                rendered += ptltool.renderAccessKey(**kw)
            except AttributeError:
                pass
        return rendered

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
        except IOError:
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

        tmp_dir = self._getTemporaryThemeFolder()
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
        self.manage_delObjects(tmp_dir.getId())

        if isfile(filepath):
            os.remove(filepath)

        new_theme = getattr(self, themeid, None)
        if new_theme is not None:
            new_theme.rebuild(setperms=1)
            theme['updated'] = DateTime().ISO()
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
            themeurl = theme.get('themeurl', None)
            md5sum = theme.get('md5sum', None)

            try:
                f = urlopen(themeurl)
                zexp_data = f.read()
            except IOError:
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

    security.declareProtected(ManageThemes, 'manage_switchDebugMode')
    def manage_switchDebugMode(self, REQUEST=None):
        """Turn the debug mode on / off"""

        self.debug_mode = not self.debug_mode
        if REQUEST is not None:
            return self.manage_configureOptions(
                manage_tabs_message='Settings updated')

    security.declareProtected(ManageThemes, 'manage_setAccessKey')
    def manage_setAccessKey(self, accesskey='', REQUEST=None):
        """Set the access key"""

        if accesskey == '':
            return
        self.accesskey = str(accesskey)[0]
        if REQUEST is not None:
            return self.manage_configureOptions(
                manage_tabs_message='Settings updated')

    security.declareProtected(ManageThemes, 'manage_setMethodThemes')
    def manage_setMethodThemes(self, form={}, REQUEST=None):
        """Set the method themes"""

        form = form.copy()
        if REQUEST is not None:
            form.update(REQUEST.form)

        err = ''
        changed = 0
        for k, v in form.items():
            if k.startswith('update_'):
                index = int(k[len('update_'):])
                meth = form['method_%s' % index].strip()
                theme = form['theme_%s' % index].strip()
                theme_container = self.getThemeContainer(theme=theme)
                if theme_container.getId() != theme:
                    err = "WARNING: Theme '%s' not found" % theme
                    continue
                page = form['page_%s' % index].strip()
                page_container = theme_container.getPageContainer(page=page)
                if page_container is None and page != '':
                    err = "WARNING: Page '%s' not found in the '%s' theme" \
                          % (page, theme)
                    page = ''
                theme_page = theme
                if page:
                    theme_page += '+' + page
                self.method_themes[meth] = theme_page
                changed = 1

            if k.startswith('remove_'):
                index = int(k[len('remove_'):])
                meth = form['method_%s' % index]
                del self.method_themes[meth]
                changed = 1

        if changed:
            self._p_changed = 1

        if REQUEST is not None:
            return self.manage_methodThemes(
                manage_tabs_message='Settings updated. %s' % err)

    security.declareProtected(ManageThemes, 'hasExternalEditor')
    def hasExternalEditor(self):
        """Return true if the External Editor is installed"""

        try:
            from Products import ExternalEditor
        except ImportError:
            return None
        else:
            return 1


    #
    # Private
    #
    security.declarePrivate('_getTemporaryThemeFolder')
    def _getTemporaryThemeFolder(self):
        """ Creates a temporary theme folder
        """
        tmp_id = getFreeId(self, try_id='tmp')
        self.invokeFactory('Theme Folder', id=tmp_id)
        return getattr(self, tmp_id, None)

InitializeClass(PortalThemesTool)
