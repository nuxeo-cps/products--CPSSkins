import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import re
import CPSSkinsTestCase
from Testing import ZopeTestCase

HTTP_OK = 200
HTTP_UNAUTHORIZED = 401
HTTP_REDIRECT = 302

class TestFunctional(ZopeTestCase.Functional,
                     CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        tmtool = self.portal.portal_themes
        self.tmtool = tmtool
        tmtool.manage_delObjects(tmtool.objectIds())
        self.theme_container = tmtool.addPortalTheme(empty=1)
        self.page_container = self.theme_container.addThemePage()
        self.pageblock = self.page_container.addPageBlock()
        self.basic_auth = '%s:secret' % self.login_id
        self.theme_url = self.theme_container.absolute_url(1)
        self.portal.REQUEST.SESSION = {}

class TestFunctionalAsManagerOrThemeManager(TestFunctional):
    """Base class for testing as 'Manager' or as 'ThemeManager'
    """

    # Adding objects
    def test_add_PortalTheme(self):
        tmtool = self.portal.portal_themes
        test_url = '/%s/cpsskins_theme_add' % tmtool.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        self.assert_(len(tmtool.getThemes()) == 2)

    def test_add_style(self):
        test_url = '/%s/cpsskins_style_add?type_name=%s&theme=%s' % \
            (self.theme_url, 'Area+Color', 'PortalTheme')
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        styles_dir = self.theme_container.getStylesFolder()
        styles = styles_dir.objectValues('Area Color')
        self.assert_(len(styles) == 1)

    def test_add_palette(self):
        test_url = '/%s/cpsskins_palette_add?type_name=%s&theme=%s' % \
            (self.theme_url, 'Palette+Color', 'PortalTheme')
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        palettes_dir = self.theme_container.getPalettesFolder()
        palettes = palettes_dir.objectValues('Palette Color')
        self.assert_(len(palettes) == 1)

    def test_add_cellhider(self):
        pageblock = self.pageblock
        test_url = '/%s/cpsskins_cellhider_add?xpos=0' % \
            self.pageblock.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        self.assert_(len(pageblock.getObjects()[0]['cellhider']) == 1)

    def test_add_cellsizer(self):
        pageblock = self.pageblock
        test_url = '/%s/cpsskins_cellsizer_add?xpos=0' % \
            pageblock.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        self.assert_(len(pageblock.getObjects()[0]['cellsizer']) == 1)

    def test_add_cellstyler(self):
        pageblock = self.pageblock
        test_url = '/%s/cpsskins_cellstyler_add?xpos=0' % \
            pageblock.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        self.assert_(len(pageblock.getObjects()[0]['cellstyler']) == 1)


    def test_addContent(self):
        pageblock = self.pageblock
        pageblock.maxcols = 2
        test_url = '/%s/cpsskins_content_add?xpos=%s&ypos=%s&type_name=%s' \
            % (pageblock.absolute_url(1), 1, 0, 'Text Box Templet')
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        templet = pageblock.objectValues('Text Box Templet')[0]
        self.assert_(templet.xpos == 1)

    def test_addPageBlock_at_the_top(self):
        test_url = '/%s/cpsskins_pageblock_add?pageblock_ypos=%s' \
            % (self.page_container.absolute_url(1), 0)
        response = self.publish(test_url, self.basic_auth)
        pageblocks = self.page_container.objectValues('Page Block')
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        self.assert_(len(pageblocks) == 2)
        self.assert_(pageblocks[1].getId() == self.pageblock.getId())

    def test_addPageBlock_at_the_bottom(self):
        orig_pageblock = self.pageblock
        test_url = '/%s/cpsskins_pageblock_add' % \
            self.page_container.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        pageblocks = self.page_container.objectValues('Page Block')
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        self.assert_(len(pageblocks) == 2)
        self.assert_(pageblocks[0].getId() == orig_pageblock.getId())

    # Modifying / deleting objects
    def test_pageblock_delete(self):
        pageblock = self.pageblock
        test_url = '/%s/cpsskins_object_delete' % pageblock.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        pageblocks = self.page_container.objectValues('Page Block')
        self.assert_(len(pageblocks) == 0)

    def test_Templet_delete(self):
        pageblock = self.pageblock
        templet = pageblock.addContent(type_name='Text Box Templet')
        test_url = '/%s/cpsskins_object_delete' % templet.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() !=  HTTP_UNAUTHORIZED )
        templets = pageblock.objectValues('Text Box Templet')
        self.assert_(len(templets) == 0)

    def test_delete_cellhider(self):
        pageblock = self.pageblock
        cellhider = pageblock.addCellHider(**{'xpos':0})
        test_url = '/%s/cpsskins_object_delete' % cellhider.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        self.assert_(pageblock.getObjects()[0]['cellhider'] == None)

    def test_delete_cellstyler(self):
        pageblock = self.pageblock
        cellstyler = pageblock.addCellStyler(**{'xpos':0})
        test_url = '/%s/cpsskins_object_delete' % cellstyler.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        self.assert_(pageblock.getObjects()[0]['cellstyler'] == None)

    def test_delete_cellsizer(self):
        pageblock = self.pageblock
        cellsizer = pageblock.addCellSizer(**{'xpos':0})
        test_url = '/%s/cpsskins_object_delete' % cellsizer.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        self.assert_(pageblock.getObjects()[0]['cellsizer'] == None)

    # Moving / copying objects
    def test_move_Cell_to_the_right(self):
        pageblock = self.pageblock
        pageblock.maxcols = int(2)
        templet = pageblock.addContent(type_name='Text Box Templet')
        templet.xpos = int(0)
        test_url = '/%s/cpsskins_move_cell?xpos=0&dir=right' % \
            pageblock.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        self.assert_(len(pageblock.getObjects()[0]['contents']) == 0)
        self.assert_(len(pageblock.getObjects()[1]['contents']) == 1)

    def test_move_Cell_to_the_left(self):
        pageblock = self.pageblock
        pageblock.maxcols = int(2)
        templet = pageblock.addContent(type_name='Text Box Templet')
        templet.xpos = int(1)
        test_url = '/%s/cpsskins_move_cell?xpos=0&dir=right' % \
            pageblock.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        self.assert_(len(pageblock.getObjects()[0]['contents']) == 1)
        self.assert_(len(pageblock.getObjects()[1]['contents']) == 0)

    def test_move_Templet_inside_same_PageBlock(self):
        utool = self.portal.portal_url
        pageblock = self.pageblock
        pageblock.maxcols = int(2)
        templet = pageblock.addContent(type_name='Text Box Templet')
        templet.xpos = int(1)
        test_url = '/%s/cpsskins_move_content?xpos=%s&ypos=%s' \
           % (templet.absolute_url(1), 0, 0)
        response = self.publish(test_url, self.basic_auth)
        templet_moved = pageblock.objectValues('Text Box Templet')[0]
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        self.assert_(templet_moved.xpos == 0)
        self.assert_(templet_moved.getVerticalPosition() == 0)

    def test_move_Templet_between_different_PageBlocks(self):
        utool = self.portal.portal_url
        pageblock_src = self.page_container.addPageBlock()
        pageblock_src.maxcols = int(2)
        pageblock_dest = self.page_container.addPageBlock()
        pageblock_dest.maxcols = int(2)
        templet = pageblock_src.addContent(type_name='Text Box Templet')
        templet.xpos = int(0)
        templet = pageblock_src.objectValues('Text Box Templet')[0]
        dest_block = utool.getRelativeUrl(pageblock_dest)
        test_url = '/%s/cpsskins_move_content?xpos=%s&ypos=%s&dest_block=%s' \
           % (templet.absolute_url(1), 1, 0, dest_block)
        response = self.publish(test_url, self.basic_auth)
        templets_in_dest = pageblock_dest.objectValues('Text Box Templet')
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        self.assert_(len(templets_in_dest) >= 0)

    def test_copy_Templet_to_another_Theme(self):
        tmtool = self.portal.portal_themes
        utool = self.portal.portal_url
        src_page_container = self.page_container
        dest_theme_container = tmtool.addPortalTheme(empty=1)
        dest_page_container = dest_theme_container.addThemePage()
        pageblock_src = self.pageblock
        pageblock_dest = dest_page_container.addPageBlock()
        pageblock_dest.maxcols = int(2)
        templet = pageblock_src.addContent(type_name='Text Box Templet')
        templet.xpos = int(0)
        templet_id = templet.getId()
        dest_block = utool.getRelativeUrl(pageblock_dest)
        test_url = '/%s/cpsskins_move_content' % templet.absolute_url(1)
        test_url += '?ypos=%s&dest_theme=%s' % \
            (0, dest_theme_container.getId())
        response = self.publish(test_url, self.basic_auth)
        templet_copied = pageblock_dest.objectValues('Text Box Templet')[0]
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        self.assert_(getattr(templet_copied, 'title'),
                     getattr(templet, 'title'))
        self.assert_(getattr(templet_copied, 'align'),
                     getattr(templet, 'align'))
        self.assert_(getattr(templet_copied, 'text'),
                     getattr(templet, 'text'))
        self.assert_(getattr(templet_copied, 'text_format'),
                     getattr(templet, 'text_format'))

    def test_copy_Templet_to_another_Page(self):
        tmtool = self.portal.portal_themes
        utool = self.portal.portal_url
        pageblock = self.pageblock
        dest_page_container = self.theme_container.addThemePage()
        templet = pageblock.addContent(type_name='Text Box Templet')
        templet.xpos = int(0)
        test_url = '/%s/cpsskins_move_content' % templet.absolute_url(1)
        test_url += '?dest_page=%s' % dest_page_container.getId()
        response = self.publish(test_url, self.basic_auth)
        templet_copied = dest_page_container.getTemplets()[0]
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        self.assert_(getattr(templet_copied, 'title'),
                     getattr(templet, 'title'))
        self.assert_(getattr(templet_copied, 'align'),
                     getattr(templet, 'align'))
        self.assert_(getattr(templet_copied, 'text'),
                     getattr(templet, 'text'))
        self.assert_(getattr(templet_copied, 'text_format'),
                     getattr(templet, 'text_format'))

    # Contextual menu
    def test_duplicate_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addContent(type_name='Text Box Templet')
        test_url = '/%s/cpsskins_content_action?action=duplicate' \
           % templet.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        templets = pageblock.objectValues('Text Box Templet')
        self.assert_(len(templets) == 2)

    def test_delete_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addContent(type_name='Text Box Templet')
        test_url = '/%s/cpsskins_content_action?action=delete' \
           % templet.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)
        templets = pageblock.objectValues('Text Box Templet')
        self.assert_(len(templets) == 0)

    def test_findStyle_for_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addContent(type_name='Text Box Templet')
        test_url = '/%s/cpsskins_find_mystyles?styleprop=color' \
           % templet.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)


class TestFunctionalAsMember(TestFunctional):
    """Testing as 'Member'
    """
    login_id = 'cpsskins_user'

    # Only testing security

    def test_add_PortalTheme(self):
        tmtool = self.portal.portal_themes
        test_url = '/%s/cpsskins_theme_add' % tmtool.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        self.assert_(len(tmtool.getThemes()) == 1)

    def test_add_style(self):
        test_url = '/%s/cpsskins_style_add?type_name=%s&theme=%s' % \
            (self.theme_url, 'Area+Color', 'PortalTheme')
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        styles_dir = self.theme_container.getStylesFolder()
        styles = styles_dir.objectValues('Area Color')
        self.assert_(len(styles) == 0)

    def test_add_palette(self):
        test_url = '/%s/cpsskins_palette_add?type_name=%s&theme=%s' % \
            (self.theme_url, 'Palette+Color', 'PortalTheme')
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        palettes_dir = self.theme_container.getPalettesFolder()
        palettes = palettes_dir.objectValues('Palette Color')
        self.assert_(len(palettes) == 0)

    def test_add_cellhider(self):
        pageblock = self.pageblock
        test_url = '/%s/cpsskins_cellhider_add?xpos=0' % \
            pageblock.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        self.assert_(pageblock.getObjects()[0]['cellhider'] == None)

    def test_add_cellsizer(self):
        pageblock = self.pageblock
        test_url = '/%s/cpsskins_cellsizer_add?xpos=0' % \
            pageblock.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        self.assert_(pageblock.getObjects()[0]['cellsizer'] == None)

    def test_add_cellstyler(self):
        pageblock = self.pageblock
        test_url = '/%s/cpsskins_cellstyler_add?xpos=0' % \
            pageblock.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        self.assert_(pageblock.getObjects()[0]['cellstyler'] == None)

    def test_ZMI(self):
        test_url = '/%s/manage_main' % self.theme_url
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)

    def test_move_Cell_to_the_right(self):
        pageblock = self.pageblock
        pageblock.maxcols = int(2)
        templet = pageblock.addContent(type_name='Text Box Templet')
        templet.xpos = int(0)
        test_url = '/%s/cpsskins_move_cell?xpos=0&dir=right' % \
            pageblock.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        self.assert_(len(pageblock.getObjects()[0]['contents']) == 1)
        self.assert_(len(pageblock.getObjects()[1]['contents']) == 0)

    def test_move_Cell_to_the_left(self):
        pageblock = self.pageblock
        pageblock.maxcols = int(2)
        templet = pageblock.addContent(type_name='Text Box Templet')
        templet.xpos = int(1)
        test_url = '/%s/cpsskins_move_cell?xpos=0&dir=right' % \
            pageblock.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        self.assert_(len(pageblock.getObjects()[0]['contents']) == 0)
        self.assert_(len(pageblock.getObjects()[1]['contents']) == 1)

    def test_move_Templet_inside_same_PageBlock(self):
        utool = self.portal.portal_url
        pageblock = self.pageblock
        pageblock.maxcols = int(2)
        templet = pageblock.addContent(type_name='Text Box Templet')
        templet.xpos = int(1)
        dest_block = utool.getRelativeUrl(pageblock)
        test_url = '/%s/cpsskins_move_content?xpos=%s&ypos=%s&dest_block=%s' \
           % (templet.absolute_url(1), 0, 0, dest_block)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)

    def test_move_Templet_between_different_PageBlocks(self):
        pageblock_src = self.pageblock
        pageblock_dest = self.page_container.addPageBlock()
        pageblock_dest.maxcols = int(2)
        templet = pageblock_src.addContent(type_name='Text Box Templet')
        templet.xpos = int(0)
        test_url = '/%s/cpsskins_move_content?xpos=%s&ypos=%s&dest_block=%s' \
           % (templet.absolute_url(1), 1, 0, pageblock_dest.getId())
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)

    def test_addContent(self):
        pageblock = self.pageblock
        pageblock.maxcols = 2
        test_url = '/%s/cpsskins_content_add?xpos=%s&ypos=%s&type_name=%s' \
            % (pageblock.absolute_url(1), 1, 0, 'Text Box Templet')
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)

    def test_copy_Templet_to_another_Theme(self):
        tmtool = self.portal.portal_themes
        utool = self.portal.portal_url
        dest_theme_container = tmtool.addPortalTheme(empty=1)
        dest_page_container = dest_theme_container.addThemePage()
        pageblock_src = self.pageblock
        pageblock_dest = dest_page_container.addPageBlock()
        pageblock_dest.maxcols = int(2)
        templet = pageblock_src.addContent(type_name='Text Box Templet')
        templet.xpos = int(0)
        templet_id = templet.getId()
        dest_block = utool.getRelativeUrl(pageblock_dest)
        test_url = '/%s/cpsskins_move_content' % templet.absolute_url(1)
        test_url += '?ypos=%s&dest_theme=%s' \
           % (0, dest_theme_container.getId())
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)

    def test_copy_Templet_to_another_Page(self):
        tmtool = self.portal.portal_themes
        utool = self.portal.portal_url
        pageblock = self.pageblock
        dest_page_container = self.theme_container.addThemePage()
        templet = pageblock.addContent(type_name='Text Box Templet')
        templet.xpos = int(0)
        test_url = '/%s/cpsskins_move_content' % templet.absolute_url(1)
        test_url += '?dest_page=%s' % dest_page_container.getId()
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)

    # Contextual menu
    def test_duplicate_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addContent(type_name='Text Box Templet')

    def test_addPageBlock_at_the_top(self):
        test_url = '/%s/cpsskins_pageblock_add?pageblock_ypos=%s' % \
            (self.page_container.absolute_url(1), 0)
        response = self.publish(test_url, self.basic_auth)
        pageblocks = self.page_container.objectValues('Page Block')
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        self.assert_(len(pageblocks) == 1)

    def test_addPageBlock_at_the_bottom(self):
        test_url = '/%s/cpsskins_pageblock_add' % \
            self.page_container.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        pageblocks = self.page_container.objectValues('Page Block')
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        self.assert_(len(pageblocks) == 1)

    def test_duplicate_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addContent(type_name='Text Box Templet')
        test_url = '/%s/cpsskins_content_action?action=duplicate' \
           % templet.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        templets = pageblock.objectValues('Text Box Templet')
        self.assert_(len(templets) == 1)

    def test_delete_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addContent(type_name='Text Box Templet')
        test_url = '/%s/cpsskins_content_action?action=delete' \
           % templet.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        templets = pageblock.objectValues('Text Box Templet')
        self.assert_(len(templets) == 1)

    def test_findStyle_for_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addContent(type_name='Text Box Templet')
        test_url = '/%s/cpsskins_find_mystyles?styleprop=color' \
           % templet.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)

    def test_pageblock_delete(self):
        test_url = '/%s/cpsskins_object_delete' % \
            self.pageblock.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        pageblocks = self.page_container.objectValues('Page Block')
        self.assert_(len(pageblocks) == 1)

    def test_delete_cellhider(self):
        pageblock = self.pageblock
        cellhider = pageblock.addCellHider(**{'xpos':0})
        test_url = '/%s/cpsskins_object_delete' % cellhider.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        self.assert_(len(pageblock.getObjects()[0]['cellhider']) == 1)

    def test_delete_cellstyler(self):
        pageblock = self.pageblock
        cellstyler = pageblock.addCellStyler(**{'xpos':0})
        test_url = '/%s/cpsskins_object_delete' % cellstyler.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        self.assert_(len(pageblock.getObjects()[0]['cellstyler']) == 1)

    def test_delete_cellsizer(self):
        pageblock = self.pageblock
        cellsizer = pageblock.addCellSizer(**{'xpos':0})
        test_url = '/%s/cpsskins_object_delete' % cellsizer.absolute_url(1)
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)
        self.assert_(len(pageblock.getObjects()[0]['cellsizer']) == 1)

class TestFunctionalAsManager(TestFunctionalAsManagerOrThemeManager):
    """Testing as 'Manager'
    """
    login_id = 'cpsskins_root'

    def test_ZMI(self):
        test_url = '/%s/manage_main' % self.theme_url
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED)


class TestFunctionalAsThemeManager(TestFunctionalAsManagerOrThemeManager):
    """Testing as 'Theme Manager'
    """
    login_id = 'cpsskins_theme_manager'

    def test_ZMI(self):
        test_url = '/%s/manage_main' % self.theme_url
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED)



class TestFunctionalCalendar(TestFunctional):
    """Testing the calendar Templet.
    """
    login_id = 'cpsskins_user'
    location_re = re.compile('Location: (.*)')

    def test_Calendar_browse_next_month(self):
        pageblock = self.pageblock
        templet = pageblock.addContent(type_name='Calendar Templet')
        base_url = '%s/cpsskins_calendar_browse' % self.portal.absolute_url(1)
        test_url = base_url + '?year:int=2004&month:int=8&dir=nextmonth'
        response = self.publish(test_url, self.basic_auth)
        location = self.location_re.search(response.getOutput())
        redirect_url = location and location.group(1)
        self.assert_(redirect_url.find('?year:int=2004&month:int=9') >= 0 )

    def test_Calendar_browse_prev_month(self):
        pageblock = self.pageblock
        templet = pageblock.addContent(type_name='Calendar Templet')
        base_url = '%s/cpsskins_calendar_browse' % self.portal.absolute_url(1)
        test_url = base_url + '?year:int=2004&month:int=8&dir=prevmonth'
        response = self.publish(test_url, self.basic_auth)
        location = self.location_re.search(response.getOutput())
        redirect_url = location and location.group(1)
        self.assert_(redirect_url.find('?year:int=2004&month:int=7') >= 0 )

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFunctionalAsManager))
    suite.addTest(unittest.makeSuite(TestFunctionalAsMember))
    suite.addTest(unittest.makeSuite(TestFunctionalAsThemeManager))
    suite.addTest(unittest.makeSuite(TestFunctionalCalendar))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)
