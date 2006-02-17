import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase

from Testing import ZopeTestCase

from Products.CPSSkins.PortalThemesTool import CPSSKINS_THEME_COOKIE_ID, \
                                               CPSSKINS_LOCAL_THEME_ID

class TestGetThemes(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        CPSSkinsTestCase.CPSSkinsTestCase.afterSetUp(self)
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
        if self.folder_root:
            testfolder = getattr(self.portal, self.folder_root)
        else:
            testfolder = self.portal
        testfolder.invokeFactory(type_name=self.folder_type, id='folder')
        folder = getattr(testfolder, 'folder')
        value = 'theme'
        folder.manage_addProperty(CPSSKINS_LOCAL_THEME_ID, value, 'string')
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=folder)
        self.assert_(theme == ('theme', None))

    def test_local_theme_2(self):
        if self.folder_root:
            testfolder = getattr(self.portal, self.folder_root)
        else:
            testfolder = self.portal
        testfolder.invokeFactory(type_name=self.folder_type, id='folder')
        folder = getattr(testfolder, 'folder')
        value = 'theme+page'
        folder.manage_addProperty(CPSSKINS_LOCAL_THEME_ID, value, 'string')
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=folder)
        self.assert_(theme == ('theme', 'page'))

    def test_local_theme_3(self):
        if self.folder_root:
            testfolder = getattr(self.portal, self.folder_root)
        else:
            testfolder = self.portal
        testfolder.invokeFactory(type_name=self.folder_type, id='folder')
        folder = getattr(testfolder, 'folder')
        folder.invokeFactory(type_name=self.folder_type, id='subfolder')
        subfolder = getattr(folder, 'subfolder')
        value = 'theme'
        folder.manage_addProperty(CPSSKINS_LOCAL_THEME_ID, value, 'string')
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=folder)
        self.assert_(theme == ('theme', None))
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=subfolder)
        self.assert_(theme == ('theme', None))

    def test_local_theme_4(self):
        if self.folder_root:
            testfolder = getattr(self.portal, self.folder_root)
        else:
            testfolder = self.portal
        testfolder.invokeFactory(type_name=self.folder_type, id='folder')
        folder = getattr(testfolder, 'folder')
        folder.invokeFactory(type_name=self.folder_type, id='subfolder')
        subfolder = getattr(folder, 'subfolder')
        value = '1-1:theme'
        folder.manage_addProperty(CPSSKINS_LOCAL_THEME_ID, value, 'string')
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=folder)
        self.assert_(theme != ('theme', None))
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=subfolder)
        self.assert_(theme == ('theme', None))

    def test_local_theme_5(self):
        if self.folder_root:
            testfolder = getattr(self.portal, self.folder_root)
        else:
            testfolder = self.portal
        testfolder.invokeFactory(type_name=self.folder_type, id='folder')
        folder = getattr(testfolder, 'folder')
        folder.invokeFactory(type_name=self.folder_type, id='subfolder')
        subfolder = getattr(folder, 'subfolder')
        value = ['1-1:theme2', '0-0:theme1']
        folder.manage_addProperty(CPSSKINS_LOCAL_THEME_ID, value, 'lines')
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=folder)
        self.assert_(theme == ('theme1', None))
        theme = self.tmtool.getRequestedThemeAndPageName(context_obj=subfolder)
        self.assert_(theme == ('theme2', None))

    def test_local_theme_6(self):
        self.tmtool.setDefaultTheme('printable')
        portal = self.portal
        value = ['1-0:theme1+page1']
        folder_id = self.folder_root
        if not folder_id:
            folder_id = 'folder'
            portal.invokeFactory(type_name=self.folder_type,
                                 id=folder_id)
        testfolder = getattr(portal, folder_id)

        portal.manage_addProperty(CPSSKINS_LOCAL_THEME_ID, value, 'lines')
        theme = self.tmtool.getRequestedThemeAndPageName(
                                          context_obj=portal)
        self.assert_(theme == ('printable', None))
        theme = self.tmtool.getRequestedThemeAndPageName(
                                          context_obj=testfolder)
        self.assert_(theme == ('theme1', 'page1'))

tests=[]
target = os.environ.get('CPSSKINS_TARGET', 'CMF')
if target == 'CPS3':
    class testCPS3(TestGetThemes):
        folder_type = 'Workspace'
        folder_root = 'workspaces'
    tests.append(testCPS3)
else:
    class testCMF(TestGetThemes):
        folder_type = 'Folder'
        folder_root = ''
    tests.append(testCMF)

def test_suite():
    suite = unittest.TestSuite()
    for test in tests:
        suite.addTest(unittest.makeSuite(test))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)
