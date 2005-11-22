#
# CPSTestCase
#

import time
import os, tempfile
from Testing import ZopeTestCase

import Products
from Products.ExternalMethod.ExternalMethod import ExternalMethod

from AccessControl.SecurityManagement \
    import newSecurityManager, noSecurityManager

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

try:
    import transaction
except ImportError:
    # BBB: for Zope 2.7
    from Products.CMFCore.utils import transaction

class CPSTestCase(ZopeTestCase.PortalTestCase):
    def setUp(self):
        ZopeTestCase.PortalTestCase.setUp(self)

        # Some skins need sessions (not sure if it's a good thing).
        # Localizer too.
        # Both lines below are needed.
        SESSION = {}
        self.portal.REQUEST['SESSION'] = SESSION
        self.portal.REQUEST.SESSION = SESSION

class CPSInstaller:
    def __init__(self, app, quiet=0):
        if not quiet:
            ZopeTestCase._print('Adding Portal Site ... ')
        self.app = app
        self._start = time.time()
        self._quiet = quiet

    def install(self, portal_id):
        self.addUser()
        self.login()
        self.addPortal(portal_id)
        self.logout()

    def addUser(self):
        uf = self.app.acl_users
        uf._doAddUser('CPSTestCase', '', ['Manager'], [])

    def login(self):
        uf = self.app.acl_users
        user = uf.getUserById('CPSTestCase').__of__(uf)
        newSecurityManager(None, user)

    def addPortal(self, portal_id, version=None):
        factory = self.app.manage_addProduct['CPSDefault']

        # CPS 3.2
        try:
            factory.manage_addCPSDefaultSite(portal_id,
                root_password1="passwd",
                root_password2="passwd",
                langs_list=['en']
                )
        # > CPS 3.2
        except TypeError:
            factory.manage_addCPSDefaultSite(portal_id,
                langs_list=['en'],
                manager_email='webmaster@localhost',
                manager_password='passwd',
                manager_password_confirmation='passwd',
                )

    def logout(self):
        noSecurityManager()
        transaction.commit()
        if not self._quiet:
            ZopeTestCase._print('done (%.3fs)\n'
                % (time.time() - self._start,))


def setupPortal(PortalInstaller=CPSInstaller):
    # Create a CPS site in the test (demo-) storage
    app = ZopeTestCase.app()
    # Set up Error Log:
    from Products.SiteErrorLog.SiteErrorLog import manage_addErrorLog
    if 'error_log' not in app.objectIds():
        manage_addErrorLog(app)
    # PortalTestCase expects object to be called "portal", not "cps"
    if hasattr(app, 'portal'):
        app.manage_delObjects(['portal'])
    PortalInstaller(app).install('portal')
    ZopeTestCase.close(app)

