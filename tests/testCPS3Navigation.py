import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase
from Testing import ZopeTestCase

class TestNavigation(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        self.login('cpsskins_root')
        self.portal.REQUEST.SESSION = {}
        self.sections = self.portal['sections'] 
        for s in ['section1', 'section2']:
            self.sections.invokeFactory(type_name='Section', id=s)
        self.section1 = getattr(self.sections, 'section1')
        for s in ['sub1', 'sub2', 'sub3']:
            self.section1.invokeFactory(type_name='Section', id=s)
        self.sub1 = getattr(self.section1, 'sub1')
        for s in ['sub11', 'sub12']:
            self.sub1.invokeFactory(type_name='Section', id=s)
        self.sub2 = getattr(self.section1, 'sub2')
        for s in ['sub21']:
            self.sub2.invokeFactory(type_name='Section', id=s)


    def test_1(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=0, base='sections', show_docs=0, base_path='/sections/', context_obj=self.sections)
        results={'create_url': '', 'menuentries': []}
        self.assert_(menuentries, results)

    def test_2(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=1, base='sections', show_docs=0, base_path='/sections/', context_obj=self.sections)
        results={'create_url': 'http://nohost/portal/sections/folder_factories',
        'menuentries': [{'title': 'section1',
        'url': 'http://nohost/portal/sections/section1',
        'selected': 0,
        'folderish': 1,
        'id': 'section1',
        'icon': 'section_icon.gif'},
        {'title': 'section2',
        'url': 'http://nohost/portal/sections/section2',
        'selected': 0,
        'folderish': 1,
        'id': 'section2',
        'icon': 'section_icon.gif'}]}
        self.assert_(menuentries, results)

    def test_3(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=1, base='sections', show_docs=0, base_path='/sections/section1', context_obj=self.sections)
        results={'create_url': '', 'menuentries': []}
        self.assert_(menuentries, results)

    def test_4(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=0, base='sections', show_docs=0, base_path='/sections/section2', context_obj=self.sections)
        results={'create_url': 'http://nohost/portal/sections/folder_factories',
        'menuentries': [{'title': 'section1',
        'url': 'http://nohost/portal/sections/section1',
        'selected': 0,
        'folderish': 1,
        'id': 'section1',
        'icon': 'section_icon.gif'},
        {'title': 'section2',
        'url': 'http://nohost/portal/sections/section2',
        'selected': 0,
        'folderish': 1,
        'id': 'section2',
        'icon': 'section_icon.gif'}]}
        self.assert_(menuentries, results)

    def test_5(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=0, base='sections', show_docs=0, base_path='/sections/', context_obj=self.section1)
        results={'create_url': '', 'menuentries': []}
        self.assert_(menuentries, results)

    def test_6(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=1, base='sections', show_docs=0, base_path='/sections/', context_obj=self.section1)
        results={'create_url': 'http://nohost/portal/sections/folder_factories',
        'menuentries': [{'title': 'section1',
        'url': 'http://nohost/portal/sections/section1',
        'selected': 1,
        'folderish': 1,
        'id': 'section1',
        'icon': 'section_icon.gif'},
        {'title': 'section2',
        'url': 'http://nohost/portal/sections/section2',
        'selected': 0,
        'folderish': 1,
        'id': 'section2',
        'icon': 'section_icon.gif'}]}
        self.assert_(menuentries, results)

    def test_7(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=1, base='sections', show_docs=0, base_path='/sections/section1', context_obj=self.section1)
        results={'create_url': '',
        'menuentries': [{'title': 'sub1',
        'url': 'http://nohost/portal/sections/section1/sub1',
        'selected': 0,
        'folderish': 1,
        'id': 'sub1',
        'icon': 'section_icon.gif'},
        {'title': 'sub2',
        'url': 'http://nohost/portal/sections/section1/sub2',
        'selected': 0,
        'folderish': 1,
        'id': 'sub2',
        'icon': 'section_icon.gif'},
        {'title': 'sub3',
        'url': 'http://nohost/portal/sections/section1/sub3',
        'selected': 0,
        'folderish': 1,
        'id': 'sub3',
        'icon': 'section_icon.gif'}]}
        self.assert_(menuentries, results)

    def test_8(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=1, base='sections', show_docs=0, base_path='/sections/section2', context_obj=self.section1)
        results={'create_url': '',
        'menuentries': [{'title': 'sub1',
        'url': 'http://nohost/portal/sections/section1/sub1',
        'selected': 0,
        'folderish': 1,
        'id': 'sub1',
        'icon': 'section_icon.gif'},
        {'title': 'sub2',
        'url': 'http://nohost/portal/sections/section1/sub2',
        'selected': 0,
        'folderish': 1,
        'id': 'sub2',
        'icon': 'section_icon.gif'},
        {'title': 'sub3',
        'url': 'http://nohost/portal/sections/section1/sub3',
        'selected': 0,
        'folderish': 1,
        'id': 'sub3',
        'icon': 'section_icon.gif'}]}
        self.assert_(menuentries, results)

    def test_9(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=0, base='sections', show_docs=0, base_path='/sections/', context_obj=self.sub1)
        results={'create_url': '', 'menuentries': []}
        self.assert_(menuentries, results)

    def test_10(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=1, base='sections', show_docs=0, base_path='/sections/', context_obj=self.sub1)
        results={'create_url': 'http://nohost/portal/sections/folder_factories',
        'menuentries': [{'title': 'section1',
        'url': 'http://nohost/portal/sections/section1',
        'selected': 1,
        'folderish': 1,
        'id': 'section1',
        'icon': 'section_icon.gif'},
        {'title': 'section2',
        'url': 'http://nohost/portal/sections/section2',
        'selected': 0,
        'folderish': 1,
        'id': 'section2',
        'icon': 'section_icon.gif'}]}
        self.assert_(menuentries, results)

    def test_11(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=1, base='sections', show_docs=0, base_path='/sections/section1', context_obj=self.sub1)
        results={'create_url': 'http://nohost/portal/sections/section1/folder_factories',
        'menuentries': [{'title': 'sub1',
        'url': 'http://nohost/portal/sections/section1/sub1',
        'selected': 1,
        'folderish': 1,
        'id': 'sub1',
        'icon': 'section_icon.gif'},
        {'title': 'sub2',
        'url': 'http://nohost/portal/sections/section1/sub2',
        'selected': 0,
        'folderish': 1,
        'id': 'sub2',
        'icon': 'section_icon.gif'},
        {'title': 'sub3',
        'url': 'http://nohost/portal/sections/section1/sub3',
        'selected': 0,
        'folderish': 1,
        'id': 'sub3',
        'icon': 'section_icon.gif'}]}
        self.assert_(menuentries, results)

    def test_12(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=1, base='sections', show_docs=0, base_path='/sections/section2', context_obj=self.sub1)
        results={'create_url': '',
        'menuentries': [{'title': 'sub1',
        'url': 'http://nohost/portal/sections/section1/sub1',
        'selected': 1,
        'folderish': 1,
        'id': 'sub1',
        'icon': 'section_icon.gif'},
        {'title': 'sub2',
        'url': 'http://nohost/portal/sections/section1/sub2',
        'selected': 0,
        'folderish': 1,
        'id': 'sub2',
        'icon': 'section_icon.gif'},
        {'title': 'sub3',
        'url': 'http://nohost/portal/sections/section1/sub3',
        'selected': 0,
        'folderish': 1,
        'id': 'sub3',
        'icon': 'section_icon.gif'}]}
        self.assert_(menuentries, results)

    def test_13(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=0, base='sections', show_docs=0, base_path='/sections/', context_obj=self.sub2)
        results={'create_url': '', 'menuentries': []}
        self.assert_(menuentries, results)


    def test_14(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=1, base='sections', show_docs=0, base_path='/sections/', context_obj=self.sub2)
        results={'create_url': 'http://nohost/portal/sections/folder_factories',
        'menuentries': [{'title': 'section1',
        'url': 'http://nohost/portal/sections/section1',
        'selected': 1,
        'folderish': 1,
        'id': 'section1',
        'icon': 'section_icon.gif'},
        {'title': 'section2',
        'url': 'http://nohost/portal/sections/section2',
        'selected': 0,
        'folderish': 1,
        'id': 'section2',
        'icon': 'section_icon.gif'}]}
        self.assert_(menuentries, results)


    def test_15(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=1, base='sections', show_docs=0, base_path='/sections/section1', context_obj=self.sub2)
        results={'create_url': 'http://nohost/portal/sections/section1/folder_factories',
        'menuentries': [{'title': 'sub1',
        'url': 'http://nohost/portal/sections/section1/sub1',
        'selected': 0,
        'folderish': 1,
        'id': 'sub1',
        'icon': 'section_icon.gif'},
        {'title': 'sub2',
        'url': 'http://nohost/portal/sections/section1/sub2',
        'selected': 1,
        'folderish': 1,
        'id': 'sub2',
        'icon': 'section_icon.gif'},
        {'title': 'sub3',
        'url': 'http://nohost/portal/sections/section1/sub3',
        'selected': 0,
        'folderish': 1,
        'id': 'sub3',
        'icon': 'section_icon.gif'}]}
        self.assert_(menuentries, results)

    def test_16(self):
        menuentries = self.portal.cpsskins_getNavigationInfo(level=1, base='sections', show_docs=0, base_path='/sections/section2', context_obj=self.sub2)
        results={'create_url': '',
        'menuentries': [{'title': 'sub1',
        'url': 'http://nohost/portal/sections/section1/sub1',
        'selected': 0,
        'folderish': 1,
        'id': 'sub1',
        'icon': 'section_icon.gif'},
        {'title': 'sub2',
        'url': 'http://nohost/portal/sections/section1/sub2',
        'selected': 1,
        'folderish': 1,
        'id': 'sub2',
        'icon': 'section_icon.gif'},
        {'title': 'sub3',
        'url': 'http://nohost/portal/sections/section1/sub3',
        'selected': 0,
        'folderish': 1,
        'id': 'sub3',
        'icon': 'section_icon.gif'}]}
        self.assert_(menuentries, results)

def test_suite():
    suite = unittest.TestSuite()
    target = os.environ.get('CPSSKINS_TARGET', 'CMF')
    if target == 'CPS3':
        suite.addTest(unittest.makeSuite(TestNavigation))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)

