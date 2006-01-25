#
# CPSTestCase
#

import time
import os, tempfile
from Testing import ZopeTestCase

ZopeTestCase.installProduct('BTreeFolder2', quiet=1)
ZopeTestCase.installProduct('CMFCalendar', quiet=1)
ZopeTestCase.installProduct('CMFCore', quiet=1)
ZopeTestCase.installProduct('CMFDefault', quiet=1)
ZopeTestCase.installProduct('CMFTopic', quiet=1)
ZopeTestCase.installProduct('DCWorkflow', quiet=1)
ZopeTestCase.installProduct('Localizer', quiet=1)
ZopeTestCase.installProduct('MailHost', quiet=1)
ZopeTestCase.installProduct('CPSCore', quiet=1)
ZopeTestCase.installProduct('CPSDefault', quiet=1)
ZopeTestCase.installProduct('CPSDirectory', quiet=1)
ZopeTestCase.installProduct('NuxUserGroups', quiet=1)
ZopeTestCase.installProduct('TranslationService', quiet=1)
ZopeTestCase.installProduct('SiteAccess', quiet=1)

ZopeTestCase.installProduct('CPSForum', quiet=1)
ZopeTestCase.installProduct('CPSSubscriptions', quiet=1)
ZopeTestCase.installProduct('CPSSchemas', quiet=1)
ZopeTestCase.installProduct('CPSDocument', quiet=1)
ZopeTestCase.installProduct('PortalTransforms', quiet=1)
ZopeTestCase.installProduct('FCKeditor', quiet=1)
ZopeTestCase.installProduct('Epoz', quiet=1)

# Optional, but must be installed if the exist:
ZopeTestCase.installProduct('Five', quiet=1)
ZopeTestCase.installProduct('CMFonFive', quiet=1)
ZopeTestCase.installProduct('CPSSharedCalendar', quiet=1)

# other products
for product in ('CPSWorkflow', 'CPSBoxes', 'NuxMetaDirectories',
                'CPSRSS', 'CPSChat', 'CPSCalendar',
                'CPSMailingLists', 'CPSCollector',
                'CPSMailBoxer', 'CPSPortlets', 'CPSNewsLetters',
                'CPSNavigation', 'CPSUserFolder', 'CPSWiki'):
    try:
        ZopeTestCase.installProduct(product, quiet=1)
    except:
        pass

import transaction

from Products.CPSDefault.tests.CPSTestCase import CPSTestCase, MANAGER_ID

class CPSSkinsTestCase(CPSTestCase):

    def afterSetUp(self):
        self.login(MANAGER_ID)
        CPSTestCase.afterSetUp(self)

    def beforeTearDown(self):
        CPSTestCase.beforeTearDown(self)
        self.logout()

    def _setupUser(self):
        CPSTestCase._setupUser(self)
        aclu = self.portal.acl_users
        users = (
            {'id': 'cpsskins_root',
             'roles': ['Manager']
            },
            {'id': 'cpsskins_user',
             'roles': ['Member']
            },
            {'id': 'cpsskins_theme_manager',
             'roles': ['Member', 'ThemeManager'],
            })
        for user in users:
            aclu._doAddUser(user['id'], 'secret', user['roles'], [])
