import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase

class TestPortalThemesTool(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        self.portal.REQUEST.SESSION = {}

    def test_check_meta_type(self):
        portal = self.portal
        tmtool = portal.portal_themes
        self.assertEquals(tmtool.meta_type, 'Portal Themes Tool')

    def test_theme_rebuild(self):
        tmtool = self.portal.portal_themes
        tmtool.rebuild()

    def test_setDefaultTheme(self):
        tmtool = self.portal.portal_themes
        tmtool.setDefaultTheme('empty')
        self.assertEquals(tmtool['theme1']['default'], 0)
        self.assertEquals(tmtool['empty']['default'], 1)

    def test_setDefaultTheme2(self):
        tmtool = self.portal.portal_themes
        tmtool.setDefaultTheme('theme1')
        self.assertEquals(tmtool['theme1']['default'], 1)
        self.assertEquals(tmtool['empty']['default'], 0)

        tmtool.setDefaultTheme('empty')
        self.assertEquals(tmtool.getDefaultThemeName(), 'empty')

        tmtool.setDefaultTheme('theme1')
        self.assertEquals(tmtool.getDefaultThemeName(), 'theme1')
            
    def test_getPortalThemeRoot(self):
        tmtool = self.portal.portal_themes
        theme = tmtool['theme1']
        for obj in theme.objectValues():
           self.assertEquals(tmtool.getPortalThemeRoot(object=obj), tmtool['theme1'])

    def test_getThemes(self):
        tmtool = self.portal.portal_themes
        self.failUnless('empty' not in tmtool.getThemes())
        self.failUnless('theme1' not in tmtool.getThemes())

    def test_getThemeContainer(self):
        tmtool = self.portal.portal_themes
        for themeid in ['theme1', 'empty']:
           self.assertEquals(tmtool.getThemeContainer(theme=themeid).getId(), themeid)
    
    def test_getThemeContainer_parent(self):
        tmtool = self.portal.portal_themes
        self.assertEquals(tmtool.getThemeContainer(parent=1), tmtool)

    def test_findStylesFor(self):
        tmtool = self.portal.portal_themes
        theme = tmtool['theme1']
        for obj in theme.objectValues():
           self.assertEquals(tmtool.findStylesFor(category='Area Color', object=obj)['title'],
           ['AreaColor4', 'AreaColor1', 'AreaColor2', 'AreaColor3', 'AreaColor5',
            'AreaColor', 'AreaColor6', 'AreaColor7', 'AreaColor8'])
           self.assertEquals(tmtool.findStylesFor(category='Area Shape', object=obj)['title'],
           ['AreaShape1', 'AreaShape2', 'AreaShape', 'AreaShape3', 'AreaShape4', 'AreaShape5'])
           self.assertEquals(tmtool.findStylesFor(category='Portal Box Color', object=obj)['title'], \
               ['PortalBoxColor2'])
           self.assertEquals(tmtool.findStylesFor(category='Portal Box Shape', object=obj)['title'], \
               ['PortalBoxShape1'])
           self.assertEquals(tmtool.findStylesFor(category='Font Color', object=obj)['title'], \
               ['FontColor1', 'FontColor2'])
           self.assertEquals(tmtool.findStylesFor(category='Font Shape', object=obj)['title'], \
                ['FontShape1'])

    def test_listPalettes(self):
        tmtool = self.portal.portal_themes
        theme = tmtool['theme1']
        for obj in theme.objectValues():
           self.assertEquals(tmtool.listPalettes(category='Palette Color', object=obj)['title'], \
               ['PaletteColor1', 'PaletteColor2'])
           self.assertEquals(tmtool.listPalettes(category='Palette Border', object=obj)['title'], \
               ['PaletteBorder1', 'PaletteBorder2'])

        

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPortalThemesTool))
    return suite
    
if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)

