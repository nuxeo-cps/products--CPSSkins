
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase
from Testing import ZopeTestCase

_print = ZopeTestCase._print

try:
    from Products.ZChecker import Check
except:
    has_zchecker = 0
    _print('ZChecker is not installed. Will not run it ...\n')
else:
    has_zchecker = 1

ignoredObjectIds = []
CPSSKINS_SKINS = ['CPSSkins',
                  'cpsskins_cmf',
                  'cpsskins_cps2',
                  'cpsskins_cps3',
                  'cpsskins_plone',
                  'cpsskins_plone2']

class TestSkins(CPSSkinsTestCase.CPSSkinsTestCase):
    """ Test skins with zchecker """

    def afterSetUp(self):
        factory = self.portal.manage_addProduct['ZChecker']
        factory.manage_addZChecker('zchecker')

    def testSkins(self):
        '''Runs the ZChecker on skins'''
        # dont break old zchecker instances
        if hasattr(self.portal.zchecker, 'setIgnoreObjectIds'):
            self.portal.zchecker.setIgnoreObjectIds(ignoredObjectIds)

        dirs = self.portal.portal_skins.objectValues()
        for dir in dirs:
            if dir.getId() not in CPSSKINS_SKINS:
                continue
            results = self.portal.zchecker.checkObjects(dir.objectValues())
            for result in results:
                self._report(result)

    def _report(self, result):
        msg = result['msg']
        obj = result['obj']
        if msg:
            _print('\n------\n%s\n' %self._skinpath(obj))
            for line in msg:
                _print('%s\n' %line)
        else:
            _print('.')

    def _skinpath(self, obj):
        path = obj.absolute_url(1)
        path = path.split('/')
        return '/'.join(path[1:])


def test_suite():
    suite = unittest.TestSuite()
    if has_zchecker:
        suite.addTest(unittest.makeSuite(TestSkins))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)

