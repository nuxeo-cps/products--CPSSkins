import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase

def isCMF15():
    try:
        from Products.CMFCore import permissions
    except ImportError:
        return 0
    return 1

class TestZPTSkins(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        tmtool = self.portal.portal_themes
        if 'PortalTheme' in tmtool.objectIds():
            tmtool.manage_delObjects(['PortalTheme'])
        self.theme_container = tmtool.addPortalTheme()
        self.portal.REQUEST.SESSION = {}
        self.portal.REQUEST.set('cpsskins_mcat', tmtool.getTranslationService())

    def test_1(self):
        self.assert_(self.portal.index_html())

    def test_2(self):
        self.assert_(self.portal.login_form())

    def test_3(self):
        self.assert_(self.portal.search_form())

def test_suite():
    suite = unittest.TestSuite()
    if not isCMF15():
        suite.addTest(unittest.makeSuite(TestZPTSkins))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)

