import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase
from Testing import ZopeTestCase

from Products.CPSSkins import tests
TEST_IMG = os.path.join(tests.__path__[0], 'TestImage.jpg')

class TestTemplets(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        tmtool = self.portal.portal_themes
        tmtool.manage_delObjects(tmtool.objectIds())
        self.theme_container = tmtool.addPortalTheme(empty=1)
        self.pageblock = self.theme_container.addPageBlock()
        atool = self.portal.portal_actions
        self.portal.REQUEST.SESSION = {}
        self.portal.REQUEST.set('cpsskins_mcat', self.portal.cpsskins_getlocalizer())
        self.portal.REQUEST.set('cpsskins_cmfactions', atool.listFilteredActionsFor(self.portal))
        self.portal.REQUEST.set('cpsskins_language', 'en')

    def test_MainContent_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Main Content Templet')
        self.assertEquals('Main Content Templet', getattr(templet, 'title'))
        self.assert_(templet.aq_explicit.isPortalTemplet())

    def test_SearchBox_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Search Box Templet')
        self.assertEquals('Search Box Templet', getattr(templet, 'title'))
        self.assert_(templet.aq_explicit.isPortalTemplet())
        self.assertEquals(templet.getApplicableStyles(), \
            [{'meta_type': 'Font Color', 'id': 'fontcolor'}, \
             {'meta_type': 'Font Shape', 'id': 'fontshape'}, \
             {'meta_type': 'Area Shape', 'id': 'shape'}, \
             {'meta_type': 'Area Color', 'id': 'color'}] )
        for style in templet.StyleList():
            templet.style = style
            self.assert_(templet.render())

    def test_TextBox_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Text Box Templet')
        self.assertEquals('Text Box Templet', getattr(templet, 'title'))
        self.assert_(templet.aq_explicit.isPortalTemplet())
        self.assertEquals(templet.getApplicableStyles(), \
            [{'meta_type': 'Font Color', 'id': 'fontcolor'}, \
             {'meta_type': 'Font Shape', 'id': 'fontshape'}, \
             {'meta_type': 'Area Shape', 'id': 'shape'}, \
             {'meta_type': 'Area Color', 'id': 'color'}] )
        self.assert_(templet.render())

    def test_TextBox_Templet_text_format(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Text Box Templet')
        templet.text = '<h2>Welcome to CPSSkins!</h2>'
        for text_format in templet.TextFormatList():
            templet.text_format = text_format
            templet.i18n = 1
            self.assert_(templet.render())
            templet.i18n = 0
            self.assert_(templet.render())

    def test_PortalBox_Templet_Styles(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Portal Box Templet')
        self.assertEquals('Portal Box Templet', getattr(templet, 'title'))
        self.assert_(templet.aq_explicit.isPortalTemplet())
        self.assert_(templet.aq_explicit.isPortalBox())
        self.assertEquals(templet.getApplicableStyles(), \
            [{'meta_type': 'Font Color', 'id': 'fontcolor'}, \
             {'meta_type': 'Font Shape', 'id': 'fontshape'}, \
             {'meta_type': 'Area Shape', 'id': 'shape'}, \
             {'meta_type': 'Area Color', 'id': 'color'}, \
             {'meta_type': 'Portal Box Shape', 'id': 'boxshape'}, \
             {'meta_type': 'Portal Box Color', 'id': 'boxcolor'}] )
        for content in templet.ContentList():
            templet.content = content 
            self.assert_(templet.render())

    def test_PortalBox_Templet_title_source(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Portal Box Templet')
        self.assertEquals('Portal Box Templet', getattr(templet, 'title'))
        for title_source in templet.TitleSourceList():
            templet.title_source = title_source
            templet.box_title_i18n = 1
            self.assert_(templet.render())
            templet.box_title_i18n = 0 
            self.assert_(templet.render())

    def test_PortalBox_Templet_layouts(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Portal Box Templet')
        self.assertEquals('Portal Box Templet', getattr(templet, 'title'))
        for boxlayout in templet.BoxLayoutList():
            templet.boxlayout = boxlayout
            self.assert_(templet.render())

    def test_PortalBox_Templet_folder_items_i18n(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Portal Box Templet')
        templet.content = 'folders'
        templet.folder_items_i18n = 1
        self.assert_(templet.render())
        templet.folder_items_i18n = 0
        self.assert_(templet.render())

    def test_PortalBoxGroup_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Portal Box Group Templet')
        self.assertEquals('Portal Box Group Templet', getattr(templet, 'title'))
        self.assert_(templet.aq_explicit.isPortalTemplet())
        self.assertEquals(templet.getApplicableStyles(), \
            [{'meta_type': 'Font Color', 'id': 'fontcolor'}, \
             {'meta_type': 'Font Shape', 'id': 'fontshape'}, \
             {'meta_type': 'Area Shape', 'id': 'shape'}, \
             {'meta_type': 'Area Color', 'id': 'color'}, \
             {'meta_type': 'Portal Box Shape', 'id': 'boxshape'}, \
             {'meta_type': 'Portal Box Color', 'id': 'boxcolor'}] )

    def test_Language_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Language Templet')
        self.assertEquals('Language Templet', getattr(templet, 'title'))
        self.assert_(templet.aq_explicit.isPortalTemplet())
        self.assertEquals(templet.getApplicableStyles(), \
            [{'meta_type': 'Font Color', 'id': 'fontcolor'}, \
             {'meta_type': 'Font Shape', 'id': 'fontshape'}, \
             {'meta_type': 'Area Shape', 'id': 'shape'}, \
             {'meta_type': 'Area Color', 'id': 'color'}] )
        self.assert_(templet.render())

    def test_ThemeChooser_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Theme Chooser Templet')
        self.assertEquals('Theme Chooser Templet', getattr(templet, 'title'))
        self.assert_(templet.aq_explicit.isPortalTemplet())
        self.assertEquals(templet.getApplicableStyles(), \
            [{'meta_type': 'Font Color', 'id': 'fontcolor'}, \
             {'meta_type': 'Font Shape', 'id': 'fontshape'}, \
             {'meta_type': 'Area Shape', 'id': 'shape'}, \
             {'meta_type': 'Area Color', 'id': 'color'}] )
        self.assert_(templet.render())

    def test_ImageBox_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Image Box Templet')
        self.assert_(templet.aq_explicit.isPortalTemplet())
        self.assert_(templet.aq_explicit.isImageBox())
        self.assertEquals(templet.getApplicableStyles(), \
            [{'meta_type': 'Font Color', 'id': 'fontcolor'}, \
             {'meta_type': 'Font Shape', 'id': 'fontshape'}, \
             {'meta_type': 'Area Shape', 'id': 'shape'}, \
             {'meta_type': 'Area Color', 'id': 'color'}] )
        self.assert_(templet.render())
        templet.internal_link = 'http://site.com'
        self.assert_(templet.render())
        templet.use_internal_link = 1
        self.assert_(templet.render())
        templet.caption = 'caption'
        self.assert_(templet.render())

    def test_ImageBox_Templet_upload(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Image Box Templet')
        templet.i18n = 0
        imagefile = open(TEST_IMG, 'rb')
        templet.manage_upload(imagefile)
        imagefile.close()

        self.assert_(templet.size, 2694)
        self.assert_(templet.width, 70)
        self.assert_(templet.height, 70)
        self.assert_(templet.content_type, 'image/jpeg')


    def test_FlashBox_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Flash Box Templet')
        self.assert_(templet.aq_explicit.isPortalTemplet())
        self.assert_(templet.aq_explicit.isFlashBox())
        self.assertEquals(templet.getApplicableStyles(), \
            [{'meta_type': 'Font Color', 'id': 'fontcolor'}, \
             {'meta_type': 'Font Shape', 'id': 'fontshape'}, \
             {'meta_type': 'Area Shape', 'id': 'shape'}, \
             {'meta_type': 'Area Color', 'id': 'color'}] )
        self.assert_(templet.render())

    def test_Breadcrumbs_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Breadcrumbs Templet')
        self.assertEquals('Breadcrumbs Templet', getattr(templet, 'title'))
        self.assert_(templet.aq_explicit.isPortalTemplet())
        self.assertEquals(templet.getApplicableStyles(), \
            [{'meta_type': 'Font Color', 'id': 'fontcolor'}, \
             {'meta_type': 'Font Shape', 'id': 'fontshape'}, \
             {'meta_type': 'Area Shape', 'id': 'shape'}, \
             {'meta_type': 'Area Color', 'id': 'color'}] )
        templet.show_icon = 0
        self.assert_(templet.render())
        templet.separator_start = 'start'
        self.assert_(templet.render())
        templet.separator_repeat = 'repeat'
        self.assert_(templet.render())
        templet.separator_end = 'end'
        self.assert_(templet.render())
        templet.show_icon = 1
        self.assert_(templet.render())

    def test_ActionBox_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Action Box Templet')
        self.assertEquals('Action Box Templet', getattr(templet, 'title'))
        self.assert_(templet.aq_explicit.isPortalTemplet())
        self.assertEquals(templet.getApplicableStyles(), \
            [{'meta_type': 'Font Color', 'id': 'fontcolor'}, \
             {'meta_type': 'Font Shape', 'id': 'fontshape'}, \
             {'meta_type': 'Area Shape', 'id': 'shape'}, \
             {'meta_type': 'Area Color', 'id': 'color'}] )
        for style in templet.OrientationList():
            templet.style = style
            self.assert_(templet.render())
        for style in templet.StyleList():
            templet.style = style
            self.assert_(templet.render())

    def test_Document_Info_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Document Info Templet')
        self.assertEquals('Document Info Templet', getattr(templet, 'title'))
        self.assert_(templet.aq_explicit.isPortalTemplet())
        self.assertEquals(templet.getApplicableStyles(), \
            [{'meta_type': 'Font Color', 'id': 'fontcolor'}, \
             {'meta_type': 'Font Shape', 'id': 'fontshape'}, \
             {'meta_type': 'Area Shape', 'id': 'shape'}, \
             {'meta_type': 'Area Color', 'id': 'color'}] )
        for content in templet.ContentList():
            templet.content = content 
            self.assert_(templet.render())
        

    def test_CollapsibleMenu_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Collapsible Menu Templet')
        self.assertEquals('Collapsible Menu Templet', getattr(templet, 'title'))
        self.assert_(templet.aq_explicit.isPortalTemplet())
        self.assertEquals(templet.getApplicableStyles(), \
            [{'meta_type': 'Font Color', 'id': 'fontcolor'}, \
             {'meta_type': 'Font Shape', 'id': 'fontshape'}, \
             {'meta_type': 'Area Shape', 'id': 'shape'}, \
             {'meta_type': 'Area Color', 'id': 'color'}, \
             {'meta_type': 'Collapsible Menu Style', 'id': 'collapsiblemenu_style'}] )
        self.assert_(templet.render())

    def test_PortalTab_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Portal Tab Templet')
        self.assertEquals('Portal Tab Templet', getattr(templet, 'title'))
        self.assert_(templet.aq_explicit.isPortalTemplet())
        self.assertEquals(templet.getApplicableStyles(), \
            [{'meta_type': 'Font Color', 'id': 'fontcolor'}, \
             {'meta_type': 'Font Shape', 'id': 'fontshape'}, \
             {'meta_type': 'Area Shape', 'id': 'shape'}, \
             {'meta_type': 'Area Color', 'id': 'color'}, \
             {'meta_type': 'Portal Tab Style', 'id': 'portaltabstyle'}]  )
        for content in templet.ContentList():
            templet.content = content 
            self.assert_(templet.render())

    def test_PortalTab_Templet_folder_items_i18n(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Portal Tab Templet')
        templet.content = 'folders'
        self.assert_(templet.render())
        templet.folder_items_i18n = 0
        self.assert_(templet.render())
        templet.folder_items_i18n = 1


    def test_Calendar_Templet(self):
        if 'portal_calendar' in self.portal.objectIds():
           pageblock = self.pageblock
           templet = pageblock.addTemplet(type_name='Calendar Templet')
           self.assertEquals('Calendar Templet', getattr(templet, 'title'))
           self.assert_(templet.aq_explicit.isPortalTemplet())
           self.assertEquals(templet.getApplicableStyles(), \
               [{'meta_type': 'Font Color', 'id': 'fontcolor'}, \
                {'meta_type': 'Font Shape', 'id': 'fontshape'}, \
                {'meta_type': 'Area Shape', 'id': 'shape'}, \
                {'meta_type': 'Area Color', 'id': 'color'}, \
                {'meta_type': 'Calendar Style', 'id': 'calendar_style'}] )
           self.assert_(templet.render())
           templet.show_month = 0
           self.assert_(templet.render())
           templet.show_year = 0
           self.assert_(templet.render())
           templet.show_weekdays = 0
           self.assert_(templet.render())
           templet.show_preview = 0
           self.assert_(templet.render())


    def test_Templet_alignment(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Text Box Templet')
        templet.change_alignment('left')
        self.assertEquals(getattr(templet, 'align'), 'left')
        templet.change_alignment('center')
        self.assertEquals(getattr(templet, 'align'), 'center')
        templet.change_alignment('right')
        self.assertEquals(getattr(templet, 'align'), 'right')
        templet.change_alignment('dummy')
        self.assertEquals(getattr(templet, 'align'), 'right')

    def test_move_to_pageblock(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Text Box Templet')
        dest_pageblock = self.theme_container.addPageBlock()
        templet.move_to_pageblock(dest_pageblock, int(0), int(1))
        templet.move_to_pageblock(pageblock, int(0), int(0))

    def test_Templet_duplicate(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Text Box Templet')
        templet.duplicate()
        templets = pageblock.objectValues()
        templet_titles = [t.getTitle() for t in templets]
        self.assertEquals(templet_titles, \
                         ['Text Box Templet', 'Text Box Templet'])
      
    def test_Templet_toggle(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Text Box Templet')
        state = templet.closed
        templet.toggle()
        self.assertEquals(templet.closed, not state)

    def test_getTempletPosition(self):
        pageblock = self.pageblock
        templet1 = pageblock.addTemplet(type_name='Text Box Templet', \
                                        ypos=int(0))
        templet2 = pageblock.addTemplet(type_name='Text Box Templet', \
                                        ypos=int(1))
        templet3 = pageblock.addTemplet(type_name='Text Box Templet', \
                                        ypos=int(2))
        pos1 = templet1.getTempletPosition()
        pos2 = templet2.getTempletPosition()
        pos3 = templet3.getTempletPosition()
        self.assertEquals(pos1, int(0))
        self.assertEquals(pos2, int(1))
        self.assertEquals(pos3, int(2))

    def test_Templet_rebuild(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Text Box Templet', \
                                       ypos=int(0))
        templet.rebuild()

    def test_setStyle(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Text Box Templet', \
                                       ypos=int(0))
        style = self.theme_container.addPortalStyle(type_name='Area Color')
        templet.setStyle(style, meta_type='Area Color')        
        self.assert_(templet.color == style.getTitle())

    def test_getStyle(self):
        pageblock = self.pageblock
        templet = pageblock.addTemplet(type_name='Text Box Templet', \
                                       ypos=int(0))
        style = self.theme_container.addPortalStyle(type_name='Area Color')
        templet.color = style.getTitle()
        found_style = templet.getStyle(meta_type='Area Color')        
        self.assert_(templet.color == found_style.getTitle())

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTemplets))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)

