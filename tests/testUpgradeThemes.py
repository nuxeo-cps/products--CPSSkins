import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import filecmp
import unittest
from Testing import ZopeTestCase
from Acquisition import aq_base
from Testing.ZopeTestCase.utils import importObjectFromFile

import CPSSkinsTestCase

class TestUpgradeTheme(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        self.login('cpsskins_root')
        self.setupLocalEnvironment()

    def beforeTearDown(self):
        self.logout()

    def test_theme(self):
        portal = self.portal
        tmtool = portal.portal_themes
        theme_id = self.theme_id
        theme_name = self.theme_name
        # remove existing themes
        ids = tmtool.objectIds()
        tmtool.manage_delObjects(ids)
        # import the theme from ../Install
        install_dir = os.path.abspath('../Install')
        old_file  = os.path.join(install_dir, '%s.zexp' % theme_name)
        new_file = os.path.join(self.export_dir, '%s.zexp' % theme_name)
        tmtool._importObjectFromFile(old_file, verify=0)
        theme = tmtool[theme_id]
        # rebuild the theme
        theme.rebuild()
        # rename 'theme_id' as 'theme_name'
        tmtool.manage_renameObject(theme_id, theme_name)
        # export the theme
        tmtool.manage_exportObject(theme_name)
        # compare the new file and the old file
        self.assert_(self.filesize(old_file) == self.filesize(new_file))

    local_home = os.path.join(os.curdir, 'data')
    export_dir = os.path.join(local_home, 'export')

    def filesize(self, file):
        return os.stat(file)[6]

    def setupLocalEnvironment(self):
        # adapted from ZopeTestCase/testZODBCompat.py
        try:
            import App.config
        except ImportError:
            # Modify builtins
            builtins = getattr(__builtins__, '__dict__', __builtins__)
            self._ih = INSTANCE_HOME
            builtins['INSTANCE_HOME'] = self.local_home
            self._ch = CLIENT_HOME
            builtins['CLIENT_HOME'] = self.export_dir
        else:
            # Zope >= 2.7
            config = App.config.getConfiguration()
            self._ih = config.instancehome
            config.instancehome = self.local_home
            self._ch = config.clienthome
            config.clienthome = self.export_dir
            App.config.setConfiguration(config)

    def afterClear(self):
        # adapted from ZopeTestCase/testZODBCompat.py
        try:
            import App.config
        except ImportError:
            # Restore builtins
            builtins = getattr(__builtins__, '__dict__', __builtins__)
            if hasattr(self, '_ih'):
                builtins['INSTANCE_HOME'] = self._ih
            if hasattr(self, '_ch'):
                builtins['CLIENT_HOME'] = self._ch
        else:
            # Zope >= 2.7
            config = App.config.getConfiguration()
            if hasattr(self, '_ih'):
                config.instancehome = self._ih
            if hasattr(self, '_ch'):
                config.clienthome = self._ch
            App.config.setConfiguration(config)

def getThemes():
    themes = {
        'CMF-Printable': 'printable',
        'CMF-Plone': 'plone',
        'CPS2-Plone': 'plone',
        'CPS2-LightSkins': 'lightskins',
        'CPS3-LightSkins': 'lightskins',
        'CPS3-Plone': 'plone',
        'CPS3-Autumn': 'autumn',
        'CPS3-Default': 'default',
        'Plone-Plone': 'plone',
        'Plone2-Autumn': 'autumn',
        'Plone2-Plone': 'plone'
    }
    return themes

tests = []
for theme_name, theme_id in getThemes().items():
    class TestOneTheme(TestUpgradeTheme):
        theme_id = theme_id
        theme_name = theme_name
    tests.append(TestOneTheme)

def test_suite():
    suite = unittest.TestSuite()
    for test in tests:
        suite.addTest(unittest.makeSuite(test))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)
