import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase
from Products.CPSSkins.cpsskins_utils import getFreeTitle

class TestPortalTheme(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        portal = self.portal
        tmtool = portal.portal_themes
        tmtool.manage_delObjects(tmtool.objectIds())
        self.theme_container = tmtool.addPortalTheme()
        self.portal.REQUEST.SESSION = {}
        self.portal.REQUEST.set('cpsskins_mcat', self.portal.cpsskins_getlocalizer())

    def test_Theme_structure(self):
        portal = self.portal
        tmtool = portal.portal_themes
        theme_container = self.theme_container
        ids = self.theme_container.objectIds()
        self.assert_('PortalTheme' in tmtool.objectIds())
        self.assert_(theme_container.getId() == 'PortalTheme')
        self.assert_(theme_container.aq_explicit.isPortalTheme())
        self.assert_('icons' in ids)
        self.assert_('styles' in ids)
        self.assert_('backgrounds' in ids)
        self.assert_(self.portal.index_html())

    def test_addPageBlock(self):
        portal = self.portal
        tmtool = portal.portal_themes
        theme_container = tmtool.getThemeContainer(theme='PortalTheme')
        theme_container.addPageBlock()
        pbs = theme_container.getPageBlocks()
        self.assert_(len(pbs) == 2)
        
    def test_edit_theme(self):
        portal = self.portal
        tmtool = portal.portal_themes
        theme_container = self.theme_container
        kw = {}
        kw['title'] = 'new title'
        kw['theme_renderer'] = 'automatic'
        kw['margin'] = '1em'
        kw['align'] = 'center'
        kw['author'] = 'Author'
        kw['copyright'] = 'Copyright (c)'
        kw['license'] = 'as-is'
        theme_container.edit(**kw)
        self.assert_(theme_container['title'] == 'new title')
        self.assert_(theme_container['theme_renderer'] == 'automatic')
        self.assert_(theme_container['margin'] == '1em')
        self.assert_(theme_container['align'] == 'center')
        self.assert_(theme_container['author'] == 'Author')
        self.assert_(theme_container['copyright'] == 'Copyright (c)')
        self.assert_(theme_container['license'] == 'as-is')
      
    def test_theme_renderers(self):
        tmtool = self.portal.portal_themes
        tmtool.setDefaultTheme('theme1')
        for theme_renderer in tmtool.listThemeRenderers():
            self.theme_container.edit(theme_renderer=theme_renderer)
            self.assert_(self.portal.index_html())
       
    def test_theme_rebuild(self):
        self.theme_container.rebuild()

    def test_getStylesFolder(self):
        stylesfolder = self.theme_container.getStylesFolder()
        self.assert_(stylesfolder.getId(), 'styles')

    def test_findUncachedTemplets(self):
        theme_container = self.theme_container
        pageblock = theme_container.addPageBlock()
        templet1 = pageblock.addContent(type_name='Text Box Templet')
        templet2 = pageblock.addContent(type_name='Text Box Templet')
        templet1.cacheable = 1
        templet2.cacheable = 0
        uncached_templets = theme_container.findUncachedTemplets()
        self.assert_(templet1 not in uncached_templets)
        self.assert_(templet2 in uncached_templets)
        templet1.cacheable = 0
        uncached_templets = theme_container.findUncachedTemplets()
        self.assert_(templet1 in uncached_templets)
        self.assert_(templet2 in uncached_templets)

    def test_findOrphanedStyles_a(self):
        theme_container = self.theme_container
        theme_container.addPortalStyle(type_name='Area Color')
        theme_container.addPortalStyle(type_name='Area Shape')
        orphaned_styles = theme_container.findOrphanedStyles()
        orphaned_styles_titles = [getattr(s, 'title') for s in orphaned_styles]
        self.assertEquals(orphaned_styles_titles, ['AreaColor', 'AreaShape'])

    def test_findOrphanedStyles_b(self):
        theme_container = self.theme_container
        theme_container.addPortalStyle(type_name='Area Color')
        theme_container.addPortalStyle(type_name='Area Shape')
        pageblock = theme_container.addPageBlock()
        templet = pageblock.addContent(type_name='Text Box Templet')
        prop_dict = {}
        prop_dict['shape'] = 'AreaShape'
        templet.manage_changeProperties(prop_dict)
        self.assertEquals(getattr(templet, 'shape'), 'AreaShape')
        orphaned_styles = theme_container.findOrphanedStyles()
        orphaned_styles_titles = [getattr(s, 'title') for s in orphaned_styles]
        self.assertEquals(orphaned_styles_titles, ['AreaColor'])
    
    def test_findStyles_a(self):
        theme_container = self.theme_container
        theme_container.addPortalStyle(type_name='Area Color')
        theme_container.addPortalStyle(type_name='Area Color')
        styles = theme_container.findStyles()
        styles_titles = [getattr(s, 'title') for s in styles]
        self.assertEquals(styles_titles, ['AreaColor', 'AreaColor1'])

    def test_renderCSS(self):
        theme_container = self.theme_container
        theme_container.addPortalStyle(type_name='Area Color')
        theme_container.addPortalStyle(type_name='Area Color')
        theme_container.addPortalStyle(type_name='Area Shape')
        self.assert_(theme_container.renderCSS())

    def test_renderJS(self):
        portal = self.portal
        tmtool = portal.portal_themes
        theme_container = tmtool.getThemeContainer(theme='PortalTheme')
        pageblock = theme_container.addPageBlock()
        pageblock.addContent(type_name="Calendar Templet")
        self.assert_(theme_container.renderJS())

    def test_findStyles_b(self):
        theme_container = self.theme_container
        theme_container.addPortalStyle(type_name='Area Color')
        theme_container.addPortalStyle(type_name='Area Color')
        theme_container.addPortalStyle(type_name='Area Shape')
        styles = theme_container.findStyles(meta_type='Area Color')
        styles_titles = [getattr(s, 'title') for s in styles]
        self.assertEquals(styles_titles, ['AreaColor', 'AreaColor1'])
        styles = theme_container.findStyles(meta_type='Area Shape')
        styles_titles = [getattr(s, 'title') for s in styles]
        self.assertEquals(styles_titles, ['AreaShape'])

    def test_getFreeTitle(self):
        theme_container = self.theme_container
        theme_container.addPortalStyle(type_name='Area Color')
        theme_container.addPortalStyle(type_name='Area Shape')
        stylesfolder = theme_container.getStylesFolder()
        title1 =  getFreeTitle(stylesfolder, 'AreaColor')
        title2 =  getFreeTitle(stylesfolder, 'AreaColor1')
        title3 =  getFreeTitle(stylesfolder)
        self.assertEquals(title1, 'AreaColor1')
        self.assertEquals(title2, 'AreaColor1')
        self.assertEquals(title3, 'Noname')
 
    def test_getInvisibleTemplets(self):
        theme_container = self.theme_container
        pageblock = theme_container.addPageBlock()
        templet1 = pageblock.addContent(type_name='Text Box Templet', xpos=int(0))
        templet2 = pageblock.addContent(type_name='Action Box Templet', xpos=int(2))
        templet3 = pageblock.addContent(type_name='Search Box Templet', xpos=int(3))
        templet4 = pageblock.addContent(type_name='Portal Box Templet', xpos=int(0))
        templet5 = pageblock.addContent(type_name='Portal Box Templet', xpos=int(0))
        templet6 = pageblock.addContent(type_name='Portal Box Group Templet', xpos=int(0))
        pageblock.maxcols = 1
        templet4.closed = 1
        invisible_templets = theme_container.getInvisibleTemplets()
        invisible_templets_titles = [getattr(t, 'title') for t in invisible_templets]
        self.assertEquals(invisible_templets_titles, 
                ['Portal Box Templet', 'Search Box Templet', 'Action Box Templet'])
    
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPortalTheme))
    return suite
    
if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)
 
