import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import time
import CPSSkinsTestCase

class TestRAMCache(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        tmtool = self.portal.portal_themes
        tmtool.manage_delObjects(tmtool.objectIds())
        self.theme_container = tmtool.addPortalTheme()
        self.page_container = self.theme_container.addThemePage()
        self.pageblock = self.page_container.addPageBlock()
        self.templet = self.pageblock.addContent(type_name='Text Box Templet')
        self.templet.text = str(range(1000))
        self.cache = self.templet.getTempletCache()
        self.cache.invalidate()

    def test_clearCache(self):
        templet = self.templet
        cache = self.cache
        templet.cacheable = 1
        templet.render_cache()
        self.assert_(cache.getSize() > 0)
        self.theme_container.clearCache()
        self.assert_(cache.getSize() == 0)

    def test_getCacheStats(self):
        templet = self.templet
        theme_container = self.theme_container
        cache = self.cache
        templet.cache_lifetime = 3600
        templet.cacheable = 1
        templet.render_cache()
        stats = self.theme_container.getCacheStats()
        self.assert_(stats['size'] == cache.getSize())
        cache.invalidate()
        stats = self.theme_container.getCacheStats()
        self.assert_(stats['size'] == 0)

    def test_getCacheSize(self):
        cache = self.cache
        templet = self.templet
        size = self.theme_container.getCacheSize()
        self.assert_(size == 0)
        templet.cache_lifetime = 3600
        templet.cacheable = 1
        templet.render_cache()
        size = self.theme_container.getCacheSize()
        self.assert_(size == cache.getSize())

    def test_isCached(self):
        templet = self.templet
        templet.cacheable = 1
        self.assert_(templet.isCached())
        templet.cacheable = 0
        self.assert_(not templet.isCached())

    def test_getLastCleanup(self):
        cache = self.cache
        templet = self.templet
        templet.cacheable = 1
        templet_path = templet.getPhysicalPath()
        templet.cache_lifetime = 3600
        self.assert_(cache.getLastCleanup(id=templet_path) is None)
        templet.render_cache()
        self.assert_(cache.getLastCleanup(id=templet_path) is not None)

    def test_expireCache(self):
        cache = self.cache
        templet = self.templet
        templet.cacheable = 1
        templet_path = templet.getPhysicalPath()
        templet.cache_lifetime = int(3600)
        templet.render_cache()
        last_cleanup1 = cache.getLastCleanup(id=templet_path)
        self.assert_(cache.getSize() > 0)
        templet.expireCache()
        time.sleep(0.1)
        last_cleanup2 = cache.getLastCleanup(id=templet_path)
        time.sleep(0.1)
        templet.render_cache()
        time.sleep(0.1)
        last_cleanup3 = cache.getLastCleanup(id=templet_path)
        self.assert_(last_cleanup2 == last_cleanup1)
        self.assert_(last_cleanup3 > last_cleanup2)

    def test_getCacheReport(self):
        templet = self.templet
        templet.cacheable = 1
        templet.cache_lifetime = int(3600)
        templet_path = templet.getPhysicalPath()
        cache = self.cache
        templet.render_cache()
        report = self.theme_container.getCacheReport()
        templet_report = report[templet_path]
        self.assert_(templet_report['count'] == 1)
        self.assert_(templet_report['last_cleanup'] == cache.getLastCleanup(id=templet_path))
        cache.invalidate()
        report = self.theme_container.getCacheReport()
        self.assert_(len(report.keys()) == 0)
        templet.render_cache()
        report = self.theme_container.getCacheReport()
        self.assert_(len(report.keys()) == 1)
        self.assert_(templet_path in report.keys())

    def test_CSSCache(self):
        theme_container = self.theme_container
        theme_container.expireCSSCache()
        style1 = theme_container.addPortalStyle(type_name='Area Color')
        time.sleep(0.1)
        css_render_1 = theme_container.renderCSS()
        style2 = theme_container.addPortalStyle(type_name='Area Shape')
        time.sleep(0.1)
        css_render_2 = theme_container.renderCSS()
        self.assert_(css_render_1 != css_render_2)
        style2.edit(**{'Area_border_style': 'solid'})
        time.sleep(0.1)
        css_render_3 = theme_container.renderCSS()
        style2.edit(**{'Area_border_style': 'dotted'})
        time.sleep(0.1)
        css_render_4 = theme_container.renderCSS()
        self.assert_(css_render_3 != css_render_4)
        style2.edit(**{'Area_border_style': 'solid'})
        time.sleep(0.1)
        css_render_5 = theme_container.renderCSS()
        self.assert_(css_render_3 == css_render_5)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRAMCache))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)

