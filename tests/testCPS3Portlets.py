import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase
from Testing import ZopeTestCase

class TestPortlets(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        tmtool = self.portal.portal_themes
        tmtool.manage_delObjects(tmtool.objectIds())
        self.theme_container = tmtool.addPortalTheme(empty=1)
        self.pageblock = self.theme_container.addPageBlock()

    def test_Portlet_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Portlet Box Templet')
        self.assertEquals('Portlet Box Templet', getattr(templet, 'title'))
        self.assert_(templet.aq_explicit.isPortalTemplet())
 
def test_suite():
    suite = unittest.TestSuite()
    target = os.environ.get('CPSSKINS_TARGET', 'CMF')
    if target == 'CPS3':
        suite.addTest(unittest.makeSuite(TestPortlets))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)

