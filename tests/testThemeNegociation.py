import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase

from Testing import ZopeTestCase

from Products.CPSSkins.PortalThemesTool import CPSSKINS_THEME_COOKIE_ID, \
                                               VIEW_MODE_SESSION_KEY

class TestGetThemes(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        self.REQUEST = self.portal.REQUEST
        self.REQUEST.SESSION = {}
        self.REQUEST.cookies = {}
        self.REQUEST.form = {}
        self.tmtool = self.portal.portal_themes

    def test_printable(self):
        self.REQUEST.form['pp'] = '1'
        theme = self.tmtool.getRequestedThemeAndPageName()
        self.assert_(theme == ('printable', None))

    def test_form(self):
        self.REQUEST.form['theme'] = 'theme'
        theme = self.tmtool.getRequestedThemeAndPageName()
        self.assert_(theme == ('theme', None))

    def test_cookie_theme(self):
        self.REQUEST.cookies[CPSSKINS_THEME_COOKIE_ID] = 'theme'
        theme = self.tmtool.getRequestedThemeAndPageName()
        self.assert_(theme == ('theme', None))
        self.REQUEST.cookies[CPSSKINS_THEME_COOKIE_ID] = 'theme+page'
        theme = self.tmtool.getRequestedThemeAndPageName()
        self.assert_(theme == ('theme', 'page'))

    def test_session(self):
        self.tmtool.setViewMode(theme='theme')
        theme = self.tmtool.getRequestedThemeAndPageName(editing=1)
        self.assert_(theme == ('theme', None))
        # the session info is only read in editing mode
        theme = self.tmtool.getRequestedThemeAndPageName()
        self.assert_(theme != ('theme', None))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGetThemes))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)
