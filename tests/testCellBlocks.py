import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase

from Testing import ZopeTestCase

class TestCellBlocks(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        tmtool = self.portal.portal_themes
        tmtool.manage_delObjects(tmtool.objectIds())
        self.theme_container = tmtool.addPortalTheme(empty=1)
        self.page_container = self.theme_container.addThemePage()
        self.pageblock = self.page_container.addPageBlock()

    def test_CellBlock(self):
        pageblock = self.pageblock
        cellblock = pageblock.addContent(type_name='Cell Block', xpos=0, ypos=0)
        cellblock.rebuild()
        cellblock.expireCache()
        self.assert_(cellblock.isCellBlock())
        self.assert_(cellblock.isRenderable())

    def test_getVerticalPosition(self):
        pageblock = self.pageblock
        cellblock = pageblock.addContent(type_name='Cell Block', xpos=0, ypos=0)
        self.assert_(cellblock.getVerticalPosition() == 0)

    def test_move_CellBlock_up(self):
        pageblock = self.pageblock
        cellblock1 = pageblock.addContent(type_name='Cell Block', xpos=0, ypos=0)
        cellblock2 = pageblock.addContent(type_name='Cell Block', xpos=0, ypos=1)
        self.assert_(cellblock1.getVerticalPosition() == 0)
        self.assert_(cellblock2.getVerticalPosition() == 1)
        cellblock2.move('up')
        pos1 = cellblock1.getVerticalPosition()
        pos2 = cellblock2.getVerticalPosition()
        self.assert_(pos2 < pos1)

    def test_move_CellBlock_down(self):
        pageblock = self.pageblock
        cellblock1 = pageblock.addContent(type_name='Cell Block', xpos=0, ypos=0)
        cellblock2 = pageblock.addContent(type_name='Cell Block', xpos=0, ypos=1)
        self.assert_(cellblock1.getVerticalPosition() == 0)
        self.assert_(cellblock2.getVerticalPosition() == 1)
        cellblock1.move('down')
        pos1 = cellblock1.getVerticalPosition()
        pos2 = cellblock2.getVerticalPosition()
        self.assert_(pos1 > pos2)

    def test_addCellSizer(self):
        pageblock = self.pageblock
        cellblock = pageblock.addContent(type_name='Cell Block', xpos=0, ypos=0)
        cellsizer = cellblock.addCellSizer(xpos=0, cellwidth='100%')
        self.assert_(cellblock.objectValues('Cell Sizer') == [cellsizer])

    def test_getTemplets(self):
        pageblock = self.pageblock
        cellblock = pageblock.addContent(type_name='Cell Block', xpos=0, ypos=0)
        templet = cellblock.addContent(type_name='Text Box Templet')
        self.assert_(cellblock.objectValues('Text Box Templet') == [templet])

    def test_getObjects(self):
        pageblock = self.pageblock
        cellblock = pageblock.addContent(type_name='Cell Block', xpos=int(0), ypos=0)
        cellblock.maxcols = int(2)
        objects = cellblock.getObjects()
        self.assert_(objects[0]['contents'] == [])
        self.assert_(objects[1]['contents'] == [])
        self.assert_(objects[0]['cellsizer'] == None)
        self.assert_(objects[1]['cellsizer'] == None)

        templet = cellblock.addContent(type_name='Text Box Templet')
        templet.xpos = 0
        objects = cellblock.getObjects()
        self.assert_(objects[0]['contents'] == [templet])
        self.assert_(objects[1]['contents'] == [])
        self.assert_(objects[0]['cellsizer'] == None)
        self.assert_(objects[1]['cellsizer'] == None)

        cellsizer = cellblock.addCellSizer(xpos=0, cellwidth='100%')
        objects = cellblock.getObjects()
        self.assert_(objects[0]['cellsizer'] == cellsizer)
        self.assert_(objects[1]['cellsizer'] == None)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCellBlocks))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)

