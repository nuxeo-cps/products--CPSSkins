import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase

class TestPortalStyles(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        tmtool = self.portal.portal_themes
        if 'PortalTheme' in tmtool.objectIds():
           tmtool.manage_delObjects(['PortalTheme'])
        self.theme_container = tmtool.addPortalTheme(empty=1)

    def test_addPortalStyle_Color(self):
        theme_container = self.theme_container
        theme_container.addPortalStyle(type_name='Area Color')
        theme_container.addPortalStyle(type_name='Area Color')
        styles = theme_container['styles'].objectValues()
        stylenames = [getattr(s,'title') for s in styles]
        self.assertEquals(['AreaColor', 'AreaColor1'], stylenames)
        for s in theme_container['styles'].objectValues():
            self.assert_(s.aq_explicit.isPortalStyle())
            self.assert_(s.render())
            self.assert_(s.preview())

    def test_addPortalStyle_Shape(self):
        theme_container = self.theme_container
        theme_container.addPortalStyle(type_name='Area Shape')
        theme_container.addPortalStyle(type_name='Area Shape')
        styles = theme_container['styles'].objectValues()
        stylenames = [getattr(s,'title') for s in styles]
        self.assertEquals(['AreaShape', 'AreaShape1'], stylenames)
        for s in theme_container['styles'].objectValues():
            self.assert_(s.aq_explicit.isPortalStyle())
            self.assert_(s.render())
            self.assert_(s.preview())

    def test_addPortalStyle_BoxShape(self):
        theme_container = self.theme_container
        theme_container.addPortalStyle(type_name='Portal Box Shape')
        theme_container.addPortalStyle(type_name='Portal Box Shape')
        styles = theme_container['styles'].objectValues()
        stylenames = [getattr(s,'title') for s in styles]
        self.assertEquals(['PortalBoxShape', 'PortalBoxShape1'], stylenames)
        for s in theme_container['styles'].objectValues():
            self.assert_(s.aq_explicit.isPortalStyle())
            self.assert_(s.render())
            self.assert_(s.preview())

    def test_addPortalStyle_BoxColor(self):
        theme_container = self.theme_container
        theme_container.addPortalStyle(type_name='Portal Box Color')
        theme_container.addPortalStyle(type_name='Portal Box Color')
        styles = theme_container['styles'].objectValues()
        stylenames = [getattr(s,'title') for s in styles]
        self.assertEquals(['PortalBoxColor', 'PortalBoxColor1'], stylenames)
        for s in theme_container['styles'].objectValues():
            self.assert_(s.aq_explicit.isPortalStyle())
            self.assert_(s.render())
            self.assert_(s.preview())

    def test_addPortalStyle_FontColor(self):
        theme_container = self.theme_container
        theme_container.addPortalStyle(type_name='Font Color')
        theme_container.addPortalStyle(type_name='Font Color')
        styles = theme_container['styles'].objectValues()
        stylenames = [getattr(s,'title') for s in styles]
        self.assertEquals(['FontColor', 'FontColor1'], stylenames)
        for s in theme_container['styles'].objectValues():
            self.assert_(s.aq_explicit.isPortalStyle())
            self.assert_(s.render())
            self.assert_(s.preview())

    def test_addPortalStyle_FontShape(self):
        theme_container = self.theme_container
        theme_container.addPortalStyle(type_name='Font Shape')
        theme_container.addPortalStyle(type_name='Font Shape')
        styles = theme_container['styles'].objectValues()
        stylenames = [getattr(s,'title') for s in styles]
        self.assertEquals(['FontShape', 'FontShape1'], stylenames)
        for s in theme_container['styles'].objectValues():
            self.assert_(s.aq_explicit.isPortalStyle())
            self.assert_(s.render())
            self.assert_(s.preview())

    def test_addPortalStyle_CollapsibleMenuStyle(self):
        theme_container = self.theme_container
        theme_container.addPortalStyle(type_name='Collapsible Menu Style')
        theme_container.addPortalStyle(type_name='Collapsible Menu Style')
        styles = theme_container['styles'].objectValues()
        stylenames = [getattr(s,'title') for s in styles]
        self.assertEquals(['CollapsibleMenuStyle', 'CollapsibleMenuStyle1'], stylenames)
        for s in theme_container['styles'].objectValues():
            self.assert_(s.aq_explicit.isPortalStyle())
            self.assert_(s.render())
            self.assert_(s.preview())

    def test_addPortalStyle_CalendarStyle(self):
        if 'portal_calendar' in self.portal.objectIds():
            theme_container = self.theme_container
            theme_container.addPortalStyle(type_name='Calendar Style')
            theme_container.addPortalStyle(type_name='Calendar Style')
            styles = theme_container['styles'].objectValues()
            stylenames = [getattr(s,'title') for s in styles]
            self.assertEquals(['CalendarStyle', 'CalendarStyle1'], stylenames)
            for s in theme_container['styles'].objectValues():
                self.assert_(s.aq_explicit.isPortalStyle())
                self.assert_(s.render())
                self.assert_(s.preview())

    def test_addPortalStyle_PortalTabStyle(self):
        theme_container = self.theme_container
        theme_container.addPortalStyle(type_name='Portal Tab Style')
        theme_container.addPortalStyle(type_name='Portal Tab Style')
        styles = theme_container['styles'].objectValues()
        stylenames = [getattr(s,'title') for s in styles]
        self.assertEquals(['PortalTabStyle', 'PortalTabStyle1'], stylenames)
        for s in theme_container['styles'].objectValues():
            self.assert_(s.aq_explicit.isPortalStyle())
            self.assert_(s.render())
            self.assert_(s.preview())

    def test_addPortalStyle_FormStyle(self):
        theme_container = self.theme_container
        theme_container.addPortalStyle(type_name='Form Style')
        theme_container.addPortalStyle(type_name='Form Style')
        styles = theme_container['styles'].objectValues()
        stylenames = [getattr(s,'title') for s in styles]
        self.assertEquals(['FormStyle', 'FormStyle1'], stylenames)
        for s in theme_container['styles'].objectValues():
            self.assert_(s.aq_explicit.isPortalStyle())
            self.assert_(s.render())
            self.assert_(s.preview())

    def test_rename_style(self):
        theme_container = self.theme_container
        style1 = theme_container.addPortalStyle(type_name='Font Shape')
        style2 = theme_container.addPortalStyle(type_name='Font Shape')
        style1.edit(title='title1')
        style2.edit(title='title2')
        self.assert_(getattr(style1, 'title'), 'title1')
        self.assert_(getattr(style2, 'title'), 'title2')
        # rename to an existing style name
        style2.edit(title='title1')
        self.assert_(getattr(style2, 'title'), 'title11')

    def test_sanitize_style_title(self):
        theme_container = self.theme_container
        style = theme_container.addPortalStyle(type_name='Area Color')
        title = ' a sd %&1 -BfG ./\+*'
        style.edit(title=title)
        title = getattr(style, 'title')
        self.assertEquals(title, 'asd1BfG')

    def test_style_rebuild(self):
        theme_container = self.theme_container
        style = theme_container.addPortalStyle(type_name='Area Color')
        style.rebuild()

    def test_findParents_for_Templet(self):
        theme_container = self.theme_container
        style = theme_container.addPortalStyle(type_name='Area Color')
        page_container = theme_container.addThemePage()
        pageblock = page_container.addPageBlock()
        templet = pageblock.addContent(type_name='Text Box Templet')
        templet.color = style.getTitle()
        parents = style.findParents()
        self.assert_(parents == [templet])

    def test_findParents_PageBlock(self):
        theme_container = self.theme_container
        style = theme_container.addPortalStyle(type_name='Area Color')
        page_container = theme_container.addThemePage()
        pageblock = page_container.addPageBlock()
        templet = pageblock.addContent(type_name='Text Box Templet')
        pageblock.color = style.getTitle()
        parents = style.findParents()
        self.assert_(parents == [pageblock])

    def test_findParents_CellStyler(self):
        theme_container = self.theme_container
        style = theme_container.addPortalStyle(type_name='Area Color')
        page_container = theme_container.addThemePage()
        pageblock = page_container.addPageBlock()
        cellstyler = pageblock.addCellStyler(**{'xpos':0})
        cellstyler.color = style.getTitle()
        parents = style.findParents()
        self.assert_(parents == [cellstyler])

    def test_findParents_PageBlock_Templet_CellStyler(self):
        theme_container = self.theme_container
        style = theme_container.addPortalStyle(type_name='Area Color')
        page_container = theme_container.addThemePage()
        pageblock = page_container.addPageBlock()
        templet = pageblock.addContent(type_name='Text Box Templet')
        cellstyler = pageblock.addCellStyler(**{'xpos':0})
        templet.color = style.getTitle()
        cellstyler.color = style.getTitle()
        pageblock.color = style.getTitle()
        parents = style.findParents()
        self.assert_(pageblock in parents)
        self.assert_(cellstyler in parents)
        self.assert_(templet in parents)
        self.assert_(len(parents) == 3)

    def test_isOrphan(self):
        theme_container = self.theme_container
        style = theme_container.addPortalStyle(type_name='Area Color')
        page_container = theme_container.addThemePage()
        pageblock = page_container.addPageBlock()
        templet = pageblock.addContent(type_name='Text Box Templet')
        self.assert_(style.isOrphan())
        templet.color = style.getTitle()
        self.assert_(not style.isOrphan())

    def test_duplicate(self):
        theme_container = self.theme_container
        style = theme_container.addPortalStyle(type_name='Area Color')
        newstyle = style.duplicate()
        styles_folder = theme_container.getStylesFolder()
        self.assert_(len(styles_folder.objectValues('Area Color')) == 2)
        self.assert_(newstyle.meta_type == 'Area Color')
        self.assert_(newstyle.Area_border_color == style.Area_border_color)
        self.assert_(newstyle.Area_bg_color == style.Area_bg_color)
        self.assert_(newstyle.Area_bg_image == style.Area_bg_image)
        self.assert_(newstyle.Area_font_color == style.Area_font_color)

    def test_copy_to_theme(self):
        theme_container = self.theme_container
        tmtool = self.portal.portal_themes
        style = theme_container.addPortalStyle(type_name='Area Color')
        style.setAsDefault()
        dest_theme_container = tmtool.addPortalTheme(empty=1)
        style_dest = dest_theme_container.addPortalStyle(type_name='Area Color')
        style_dest.setAsDefault()
        default_style = dest_theme_container.getDefaultStyle()
        newstyle = style.copy_to_theme(dest_theme=dest_theme_container.getId())
        styles_folder = theme_container.getStylesFolder()
        self.assert_(len(styles_folder.objectValues('Area Color')) == 1)
        dest_styles_folder = dest_theme_container.getStylesFolder()
        self.assert_(len(dest_styles_folder.objectValues('Area Color')) == 2)
        self.assert_(newstyle.meta_type == 'Area Color')
        self.assert_(newstyle.Area_border_color == style.Area_border_color)
        self.assert_(newstyle.Area_bg_color == style.Area_bg_color)
        self.assert_(newstyle.Area_bg_image == style.Area_bg_image)
        self.assert_(newstyle.Area_font_color == style.Area_font_color)
        self.assert_(dest_theme_container.getDefaultStyle() == default_style)
        self.assert_(not newstyle.isDefaultStyle())


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPortalStyles))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)

