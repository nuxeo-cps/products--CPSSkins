import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase

class TestZPTSkins(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        tmtool = self.portal.portal_themes
        if 'PortalTheme' in tmtool.objectIds():
            tmtool.manage_delObjects(['PortalTheme'])
        self.theme_container = tmtool.addPortalTheme()
        self.portal.REQUEST.SESSION = {}
        self.portal.REQUEST.set('cpsskins_mcat', self.portal.cpsskins_getlocalizer())

    def test_1(self):
        self.assert_(self.portal.index_html())
        self.assert_(self.portal.login_form())
        self.assert_(self.portal.search_form())
        self.assert_(self.portal.reconfig_form())

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestZPTSkins))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)

