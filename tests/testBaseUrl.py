import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase

class TestBaseUrl(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        tmtool = self.portal.portal_themes
        tmtool.manage_delObjects(tmtool.objectIds())
        self.theme_container = tmtool.addPortalTheme(empty=1)
        self.pageblock = self.theme_container.addPageBlock()
        self.REQUEST = self.portal.REQUEST

    def test_no_rewrite(self):
        self.REQUEST.set('PATH_INFO', '/site/url')
        base_url = self.portal.cpsskins_getBaseUrl()
        expected = self.portal.portal_url.getPortalPath() + '/'
        self.assert_(base_url == expected)

    def test_rewrite(self):
        self.REQUEST.set('PATH_INFO',
            '/VirtualHostBase/http/localhost:80/site/VirtualHostRoot/url')
        base_url = self.portal.cpsskins_getBaseUrl()
        expected = '/'
        self.assert_(base_url == expected)

    def test_rewrite_vh(self):
        self.REQUEST.set('PATH_INFO',
            '/VirtualHostBase/http/localhost:80/site/VirtualHostRoot/_vh_site/url')
        base_url = self.portal.cpsskins_getBaseUrl()
        expected = '/site/'
        self.assert_(base_url == expected)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBaseUrl))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)
