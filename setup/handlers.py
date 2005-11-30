# Copyright (c) 2003-2005 Chalmers University of Technology
# Authors: Jean-Marc Orliaguet <mailto:jmo@ita.chalmers.se>
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

import os

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass, package_home

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManagePortal
from Products.CMFSetup.utils import ExportConfiguratorBase
from Products.CMFSetup.utils import ImportConfiguratorBase
from Products.CMFSetup.utils import KEY
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

_pkgdir = package_home(globals())
_xmldir = os.path.join(_pkgdir, 'xml')

_TOOL_FILENAME = 'themestool.xml'
_THEMES_FILENAME = 'themes.xml'

#
# Handlers
#

def importThemesTool(context):
    """Import the theme tool's properties.
    """
    site = context.getSite()
    tmtool = getToolByName(site, 'portal_themes')
    if context.shouldPurge():
        # steps to follow to remove old settings
        pass

    body = context.readDataFile(_TOOL_FILENAME)
    if body is None:
        return 'Themes tool: Nothing to import.'

    ttic = ThemesToolImportConfigurator(site)
    tm_info = ttic.parseXML(body)

    tmtool.accesskey = tm_info['accesskey']
    tmtool.debug_mode = int(tm_info['debug_mode'])

    # TODO: convert to list / dicts
    #tmtool.externalthemes = tm_info['externalthemes']
    #tmtool.method_themes = tm_info['method_themes']

    return 'Themes tool settings imported.'

def exportThemesTool(context):
    """Export the theme tool's properties.
    """
    site = context.getSite()
    ttec = ThemesToolExportConfigurator(site).__of__(site)
    text = ttec.generateXML()
    context.writeDataFile(_TOOL_FILENAME, text, 'text/xml' )

    return 'Theme tool settings exported.'

def importPortalThemes(context):
    site = context.getSite()
    tmtool = getToolByName(site, 'portal_themes')
    ttic = ThemeImportConfigurator(site).__of__(site)

    if context.shouldPurge():
        # steps to follow to remove old settings
        pass

    xml = context.readDataFile(_THEMES_FILENAME)
    if xml is None:
        return 'Portal themes: Nothing to import.'

    print xml
    return 'Portal themes imported'

def exportPortalThemes(context):
    """Export themes locate in the portal themes tool.
    """
    site = context.getSite()
    tmtool = getToolByName(site, 'portal_themes')
    themes = tmtool.getThemes()

    tec = ThemeExportConfigurator(site).__of__(site)
    themes_xml = tec.generateXML()

    context.writeDataFile(_THEMES_FILENAME, themes_xml, 'text/xml')

    for theme in themes:
        theme_id = theme.getId()
        theme_filename = '%s.xml' % theme_id.replace(' ', '_')
        theme_xml = tec.generateXML(theme_id=theme_id)
        context.writeDataFile(theme_filename, theme_xml, 'text/xml', 'themes')

    return 'Portal themes exported'

#
# Configurators
#

class ThemesToolImportConfigurator(ImportConfiguratorBase):

    def _getImportMapping(self):
        return {
          'object': {
              'accesskey': {},
              'debug_mode': {},
              'externalthemes': {},
              'method_themes': {}
              }
          }

InitializeClass(ThemesToolImportConfigurator)


class ThemesToolExportConfigurator(ExportConfiguratorBase):
    security = ClassSecurityInfo()

    security.declareProtected(ManagePortal, 'getToolInfo')
    def getToolInfo( self ):
        """Get information about the tool
        """
        tmtool = getToolByName(self._site, 'portal_themes')
        config = {}
        config['accesskey'] = tmtool.getAccessKey()
        config['debug_mode'] = tmtool.debug_mode
        config['externalthemes'] = tmtool.getExternalThemes()
        config['method_themes'] = tmtool.method_themes
        return config

    def _getExportTemplate(self):
        return PageTemplateFile('tmtoolExport.xml', _xmldir)

InitializeClass(ThemesToolExportConfigurator)


class ThemeImportConfigurator(ImportConfiguratorBase):
    """ """

InitializeClass(ThemeImportConfigurator)


class ThemeExportConfigurator(ExportConfiguratorBase):
    security = ClassSecurityInfo()

    security.declareProtected(ManagePortal, 'listThemeObjects')
    def listThemeObjects(self, theme_id):
        """Return a sequence of mappings for theme objects.
        """
        tmtool = getToolByName(self._site, 'portal_themes')
        theme = tmtool.getThemeContainer(theme=theme_id)
        return self._extractObject(theme)['subobjects']

    security.declareProtected(ManagePortal, 'getThemes')
    def getThemes(self):
        """Return the list of themes.
        """
        return getToolByName(self._site, 'portal_themes').getThemes()

    def _getExportTemplate(self):
        return PageTemplateFile('themeExport.xml', _xmldir)

    def _propertyMap(self):
        return {}

InitializeClass(ThemeExportConfigurator)

