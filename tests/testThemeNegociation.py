import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase

from Testing import ZopeTestCase

from Products.CPSSkins.PortalThemesTool import CPSSKINS_THEME_COOKIE_ID, \
                                               VIEW_MODE_SESSION_KEY, \
                                               CPSSKINS_LOCAL_THEME_ID

class TestGetThemes(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        self.login('cpsskins_root')
        self.REQUEST = self.portal.REQUEST
        self.REQUEST.SESSION = {}
        self.REQUEST.cookies = {}
        self.REQUEST.form = {}
        self.tmtool = self.portal.portal_themes

    def beforeTearDown(self):
        self.logout()

    def test_printable(self):
        self.REQUEST.form['pp'] = '1'
        theme = self.tmtool.getRequestedThemeAndPageName()
        self.assert_(theme == ('printable', None))

    def test_form_1(self):
        self.REQUEST.form['theme'] = 'theme'
        theme = self.tmtool.getRequestedThemeAndPageName()
        self.assert_(theme == ('theme', None))

    def test_form_2(self):
        self.REQUEST.form['theme'] = 'theme+page'
        theme = self.tmtool.getRequestedThemeAndPageName()
        self.assert_(theme == ('theme', 'page'))

    def test_form_3(self):
        self.REQUEST.form['theme'] = 'theme+page1'
        self.REQUEST.form['page'] = 'page2'
        theme = self.tmtool.getRequestedThemeAndPageName()
        self.assert_(theme == ('theme', 'page1'))

    def test_cookie_theme_1(self):
        self.REQUEST.cookies[CPSSKINS_THEME_COOKIE_ID] = 'theme'
        theme = self.tmtool.getRequestedThemeAndPageName()
        self.assert_(theme == ('theme', None))

    def test_cookie_theme_2(self):
        self.REQUEST.cookies[CPSSKINS_THEME_COOKIE_ID] = 'theme+page'
        theme = self.tmtool.getRequestedThemeAndPageName()
        self.assert_(theme == ('theme', 'page'))

    def test_session_1(self):
        self.tmtool.setViewMode(theme='theme')
        theme = self.tmtool.getRequestedThemeAndPageName(editing=1)
        self.assert_(theme == ('theme', None))

    def test_session_2(self):
        self.tmtool.setViewMode(theme='theme', page='page')
        theme = self.tmtool.getRequestedThemeAndPageName(editing=1)
        self.assert_(theme == ('theme', 'page'))

    def test_session_3(self):
        self.tmtool.setViewMode(theme='theme+page1', page='page2')
        theme = self.tmtool.getRequestedThemeAndPageName(editing=1)
        self.assert_(theme == ('theme', 'page1'))

    def test_session_3(self):
        # the session info is only read in editing mode
        theme = self.tmtool.getRequestedThemeAndPageName()
        self.assert_(theme != ('theme', None))

    def test_local_theme_1(self):
        self.portal.invokeFactory(type_name='Folder', id='folder')
        folder = self.portal.folder
        value = 'theme'
        folder.manage_addProperty(CPSSKINS_LOCAL_THEME_ID, value, 'string')
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=folder)
        self.assert_(theme == ('theme', None))

    def test_local_theme_2(self):
        self.portal.invokeFactory(type_name='Folder', id='folder')
        folder = self.portal.folder
        value = 'theme+page'
        folder.manage_addProperty(CPSSKINS_LOCAL_THEME_ID, value, 'string')
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=folder)
        self.assert_(theme == ('theme', 'page'))

    def test_local_theme_3(self):
        self.portal.invokeFactory(type_name='Folder', id='folder')
        folder = self.portal.folder
        folder.invokeFactory(type_name='Folder', id='subfolder')
        subfolder = self.portal.folder.subfolder
        value = 'theme'
        folder.manage_addProperty(CPSSKINS_LOCAL_THEME_ID, value, 'string')
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=folder)
        self.assert_(theme == ('theme', None))
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=subfolder)
        self.assert_(theme == ('theme', None))

    def test_local_theme_4(self):
        self.portal.invokeFactory(type_name='Folder', id='folder')
        folder = self.portal.folder
        folder.invokeFactory(type_name='Folder', id='subfolder')
        subfolder = self.portal.folder.subfolder
        value = '1-1:theme'
        folder.manage_addProperty(CPSSKINS_LOCAL_THEME_ID, value, 'string')
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=folder)
        self.assert_(theme != ('theme', None))
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=subfolder)
        self.assert_(theme == ('theme', None))

    def test_local_theme_5(self):
        self.portal.invokeFactory(type_name='Folder', id='folder')
        folder = self.portal.folder
        folder.invokeFactory(type_name='Folder', id='subfolder')
        subfolder = self.portal.folder.subfolder
        value = ['1-1:theme2', '0-0:theme1']
        folder.manage_addProperty(CPSSKINS_LOCAL_THEME_ID, value, 'lines')
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=folder)
        self.assert_(theme == ('theme1', None))
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=subfolder)
        self.assert_(theme == ('theme2', None))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGetThemes))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)
