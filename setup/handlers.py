
import os

from Globals import InitializeClass
from Globals import package_home

from Products.CMFCore.utils import getToolByName
from Products.CMFSetup.utils import ConfiguratorBase
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

_pkgdir = package_home(globals())
_xmldir = os.path.join(_pkgdir, 'xml')

_FILENAME = 'themes.xml'

def importPortalThemes(context):
    site = context.getSite()
    tmtool = getToolByName(site, 'portal_themes')
    ttic = ThemesToolImportConfigurator(site).__of__(site)
    # TODO

    return 'Portal themes imported'

def exportPortalThemes(context):
    """Export themes locate in the portal themes tool.
    """
    site = context.getSite()
    tmtool = getToolByName(site, 'portal_themes')
    themes = tmtool.getThemes()
    #ttec = ThemesToolExportConfigurator(site).__of__(site)
    #context.writeDataFile(_FILENAME, theme_xml, 'text/xml')

    tec = ThemeExportConfigurator(site).__of__(site)
    for theme in themes:
        theme_id = theme.getId()
        theme_filename = '%s.xml' % theme_id.replace(' ', '_')
        theme_xml = tec.generateXML(theme_id=theme_id)
        context.writeDataFile(theme_filename, theme_xml, 'text/xml', 'themes')
    return 'Portal themes exported'


class ThemesToolImportConfigurator(ConfiguratorBase):
    """ """

InitializeClass(ThemesToolImportConfigurator)


class ThemesToolExportConfigurator(ConfiguratorBase):
    """ """

InitializeClass(ThemesToolExportConfigurator)


class ThemeImportConfigurator(ConfiguratorBase):
    """ """

InitializeClass(ThemeImportConfigurator)


class ThemeExportConfigurator(ConfiguratorBase):
    """ """

    def _propertyMap(self):
        return {}

    def listThemeObjects(self, theme_id):
        """Return a sequence of mappings for theme objects.
        """
        tmtool = getToolByName(self._site, 'portal_themes')
        theme = tmtool.getThemeContainer(theme=theme_id)
        return self._extractObject(theme)['subobjects']

    def _getExportTemplate(self):
        return PageTemplateFile('themeExport.xml', _xmldir)

InitializeClass(ThemeExportConfigurator)
