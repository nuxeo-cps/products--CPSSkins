import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import filecmp
import unittest
from Testing import ZopeTestCase

import CPSSkinsTestCase

class TestUpgradeThemes(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        self.login('cpsskins_root')
        self.setupLocalEnvironment()

    def beforeTearDown(self):
        self.logout()

    def test_rebuild_themes(self):
        portal = self.portal
        tmtool = portal.portal_themes

        for theme_name, theme_id in getThemes().items():
            # remove existing themes
            ids = tmtool.objectIds()
            tmtool.manage_delObjects(ids)

            # import the theme from ../Install
            install_dir = os.path.abspath('../Install')
            old_file  = os.path.join(install_dir, '%s.zexp' % theme_name)
            new_file = os.path.join(self.export_dir, '%s.zexp' % theme_name)
            tmtool._importObjectFromFile(old_file, verify=0)
            get_transaction().commit()

            theme = tmtool[theme_id]
            # rebuild the theme
            theme.rebuild()
            get_transaction().commit()

            # rename 'theme_id' as 'theme_name'
            tmtool.manage_renameObject(theme_id, theme_name)
            # export the theme
            tmtool.manage_exportObject(theme_name)

            theme.setAsDefault()
            # compare the new file and the old file
            self.assert_(theme.render(shield=0, context_obj=self.portal))

    local_home = os.path.join(os.curdir, 'data')
    export_dir = os.path.join(local_home, 'export')

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

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUpgradeThemes))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)
