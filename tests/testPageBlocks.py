import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase

class TestPageBlocks(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        CPSSkinsTestCase.CPSSkinsTestCase.afterSetUp(self)
        tmtool = self.portal.portal_themes
        tmtool.manage_delObjects(tmtool.objectIds())
        self.theme_container = tmtool.addPortalTheme(empty=1)
        self.page_container = self.theme_container.addThemePage()
        self.pageblock = self.page_container.addPageBlock()

    def test_move_PageBlock_up(self):
        pageblock1 = self.pageblock
        pageblock2 = self.page_container.addPageBlock()
        pageblock2.move('up')
        pos1 = pageblock1.getVerticalPosition()
        pos2 = pageblock2.getVerticalPosition()
        self.assert_(pos2 < pos1)

    def test_move_PageBlock_down(self):
        pageblock1 = self.pageblock
        pageblock2 = self.page_container.addPageBlock()
        pageblock1.move('down')
        pos1 = pageblock1.getVerticalPosition()
        pos2 = pageblock2.getVerticalPosition()
        self.assert_(pos1 > pos2)

    def test_getPageBlocks(self):
        self.page_container.addPageBlock()
        self.assert_(len(self.page_container.getPageBlocks()) == int(2))

    def test_moveCell_right(self):
        pageblock = self.pageblock
        pageblock.maxcols = int(2)
        templet = pageblock.addContent(type_name='Text Box Templet')
        templet.xpos = int(0)
        cellstyler = pageblock.addCellStyler(**{'xpos':0})
        cellhider = pageblock.addCellHider(**{'xpos':0})
        cellsizer = pageblock.addCellSizer(**{'xpos':0})
        pageblock.moveCell(**{'xpos': 0, 'dir': 'right'})
        self.assert_(pageblock.getObjects()[0]['contents'] == [])
        self.assert_(pageblock.getObjects()[0]['cellstyler'] == None)
        self.assert_(pageblock.getObjects()[0]['cellsizer'] == None)
        self.assert_(pageblock.getObjects()[0]['cellhider'] == None)
        self.assert_(pageblock.getObjects()[1]['contents'] == [templet])
        self.assert_(pageblock.getObjects()[1]['cellstyler'] == cellstyler)
        self.assert_(pageblock.getObjects()[1]['cellsizer'] == cellsizer)
        self.assert_(pageblock.getObjects()[1]['cellhider'] == cellhider)

    def test_moveCell_left(self):
        pageblock = self.pageblock
        pageblock.maxcols = int(2)
        templet = pageblock.addContent(type_name='Text Box Templet')
        templet.xpos = int(1)
        cellstyler = pageblock.addCellStyler(**{'xpos':1})
        cellhider = pageblock.addCellHider(**{'xpos':1})
        cellsizer = pageblock.addCellSizer(**{'xpos':1})
        pageblock.moveCell(**{'xpos': 1, 'dir': 'left'})
        self.assert_(pageblock.getObjects()[1]['contents'] == [])
        self.assert_(pageblock.getObjects()[1]['cellstyler'] == None)
        self.assert_(pageblock.getObjects()[1]['cellsizer'] == None)
        self.assert_(pageblock.getObjects()[1]['cellhider'] == None)
        self.assert_(pageblock.getObjects()[0]['contents'] == [templet])
        self.assert_(pageblock.getObjects()[0]['cellstyler'] == cellstyler)
        self.assert_(pageblock.getObjects()[0]['cellsizer'] == cellsizer)
        self.assert_(pageblock.getObjects()[0]['cellhider'] == cellhider)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPageBlocks))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)

