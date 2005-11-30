
import os

from Globals import InitializeClass
from Globals import package_home

from Products.CMFCore.utils import getToolByName
from Products.CMFSetup.utils import ExportConfiguratorBase
from Products.CMFSetup.utils import ImportConfiguratorBase
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

_pkgdir = package_home(globals())
_xmldir = os.path.join(_pkgdir, 'xml')

_FILENAME = 'themes.xml'

#######################################################################
# Handlers
#######################################################################

def importThemesTool(context):
    """Import the theme tool's properties.
    """

def exportThemesTool(context):
    """Export the theme tool's properties.
    """

def importPortalThemes(context):
    site = context.getSite()
    tmtool = getToolByName(site, 'portal_themes')
    ttic = ThemeImportConfigurator(site).__of__(site)

    xml = context.readDataFile(_FILENAME)
    if xml is None:
        return 'Portal themes: Nothing to import.'

    #TODO
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

    context.writeDataFile(_FILENAME, themes_xml, 'text/xml')

    for theme in themes:
        theme_id = theme.getId()
        theme_filename = '%s.xml' % theme_id.replace(' ', '_')
        theme_xml = tec.generateXML(theme_id=theme_id)
        context.writeDataFile(theme_filename, theme_xml, 'text/xml', 'themes')
    return 'Portal themes exported'

#######################################################################
# Configurators
#######################################################################

class ThemesToolImportConfigurator(ImportConfiguratorBase):
    """ """

class ThemesToolExportConfigurator(ExportConfiguratorBase):
    """ """

class ThemeImportConfigurator(ImportConfiguratorBase):
    """ """

class ThemeExportConfigurator(ExportConfiguratorBase):
    """ """

    def _propertyMap(self):
        return {}

    def listThemeObjects(self, theme_id):
        """Return a sequence of mappings for theme objects.
        """
        tmtool = getToolByName(self._site, 'portal_themes')
        theme = tmtool.getThemeContainer(theme=theme_id)
        return self._extractObject(theme)['subobjects']

    def getThemes(self):
        """Return the list of themes.
        """
        return getToolByName(self._site, 'portal_themes').getThemes()

    def _getExportTemplate(self):
        return PageTemplateFile('themeExport.xml', _xmldir)


InitializeClass(ThemesToolImportConfigurator)
InitializeClass(ThemesToolExportConfigurator)
InitializeClass(ThemeImportConfigurator)
InitializeClass(ThemeExportConfigurator)
