import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase


class TestPortalPalettes(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        tmtool = self.portal.portal_themes
        if 'PortalTheme' in tmtool.objectIds():
           tmtool.manage_delObjects(['PortalTheme'])
        self.theme_container = tmtool.addPortalTheme(empty=1)

    def test_addPortalPalette_Color(self):
        theme_container = self.theme_container
        theme_container.addPortalPalette(type_name='Palette Color')
        theme_container.addPortalPalette(type_name='Palette Color')
        palettes = theme_container['palettes'].objectValues()
        palettenames = [getattr(s,'title') for s in palettes]
        self.assertEquals(['PaletteColor', 'PaletteColor1'], palettenames)
        for s in theme_container['palettes'].objectValues():
            self.assert_(s.aq_explicit.isPortalPalette())
            self.assert_(s.preview())

    def test_addPortalPalette_Border(self):
        theme_container = self.theme_container
        theme_container.addPortalPalette(type_name='Palette Border')
        theme_container.addPortalPalette(type_name='Palette Border')
        palettes = theme_container['palettes'].objectValues()
        palettenames = [getattr(s,'title') for s in palettes]
        self.assertEquals(['PaletteBorder', 'PaletteBorder1'], palettenames)
        for s in theme_container['palettes'].objectValues():
            self.assert_(s.aq_explicit.isPortalPalette())
            self.assert_(s.preview())


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPortalPalettes))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)

