#
# CPSTestCase
#

import time

import os, tempfile
from Testing import ZopeTestCase

import Products
from Products.ExternalMethod.ExternalMethod import ExternalMethod

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


from AccessControl.SecurityManagement \
    import newSecurityManager, noSecurityManager


# The folowing are patches needed because Localizer doesn't work
# well within ZTC

# This one is needed by ProxyTool.
def get_selected_language(self):
    """ """
    return self._default_language

from Products.Localizer.Localizer import Localizer
Localizer.get_selected_language = get_selected_language

# CPSPortlets
try:
    from Products.CPSPortlets import CPSPortlet
except ImportError:
    has_cpsportlets = 0
else:
    has_cpsportlets = 1

from AccessControl.SecurityManagement \
    import newSecurityManager, noSecurityManager
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

# This one is needed by ProxyTool.
def get_selected_language(self):
    """ """
    return self._default_language

from Products.Localizer.Localizer import Localizer
Localizer.get_selected_language = get_selected_language

from OFS.SimpleItem import SimpleItem
class DummyTranslationService(SimpleItem):
    meta_type = 'Translation Service'
    id = 'translation_service'

    def translate(self, domain, msgid, *args, **kw):
        return msgid

    def __call__(self, *args, **kw):
        return self.translate('default', *args, **kw)

    def getDomainInfo(self):
        return [(None, 'Localizer/default')]

    def manage_addDomainInfo(self, domain, path, REQUEST=None, **kw):
        pass

    def getDefaultLanguage(self):
        return 'en'

    def getSelectedLanguage(self):
        return 'en'

class DummyMessageCatalog(SimpleItem):
    security = ClassSecurityInfo()
    def __call__(self, message, *args, **kw):
        #return self.gettext(self, message, lang, args, kw)
        return message

    security.declarePublic('gettext')
    def gettext(self, message, lang=None, *args, **kw):
        if message == 'words_meaningless' and lang == 'en':
            message = "a the this these those of am is are has have or and i maybe perhaps"
        elif message == 'words_meaningless' and lang == 'fr':
            message = "un une le la les l de des ces est sont a ont ou et je voici"
        return message

    def get_selected_language(self):
        "xxx"
        return 'fr'

    def get_languages(self):
        return ['en', 'fr', 'de']

    def manage_import(self, *args, **kw):
        pass

    def wl_isLocked(self):
        return None # = False

InitializeClass(DummyMessageCatalog)


from StringIO import StringIO
from Products.Localizer import LocalizerStringIO
from types import UnicodeType
# Un-patch LocalizerStringIO
def LocalizerStringIO_write(self, s):
    StringIO.write(self, s)
# Hack around Unicode problem
def LocalizerStringIO_getvalue(self):
    if self.buflist:
        for buf in self.buflist:
            if type(buf) == UnicodeType:
                self.buf += buf.encode('latin-1')
            else:
                self.buf += buf
        self.buflist = []
    return self.buf
LocalizerStringIO.write = LocalizerStringIO_write
LocalizerStringIO.getvalue = LocalizerStringIO_getvalue

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
        if has_cpsportlets:
            self.fixupCPSPortlets(portal_id)
        self.fixupTranslationServices(portal_id)
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

    # Change translation_service to DummyTranslationService
    def fixupTranslationServices(self, portal_id):
        portal = getattr(self.app, portal_id)
        # XXX don't know why we use a fake translation service
        # we only need to add getSelectedLanguage and getLanguage methods
        # to TranslationService.Domain.DummyDomain to use the real one
        portal.translation_service = DummyTranslationService()
        localizer = portal.Localizer
        for domain in localizer.objectIds():
            setattr(localizer, domain, DummyMessageCatalog())

    # Install CPSPortlets (not installed by default in CPSDefault)
    def fixupCPSPortlets(self, portal_id):
        portal = getattr(self.app, portal_id)
        portal_objectIds = portal.objectIds()
        if 'portal_cpsportlets' not in portal_objectIds:
            ZopeTestCase._print('Installing CPSPortlets ...\n')
            install = ExternalMethod('install_cpsportlets',
                                     'CPSPortlets',
                                     'CPSPortlets.install',
                                     'install' )
            portal._setObject('install_cpsportlets', install)
            portal.install_cpsportlets()

    def logout(self):
        noSecurityManager()
        get_transaction().commit()
        if not self._quiet:
            ZopeTestCase._print('done (%.3fs)\n'
                % (time.time() - self._start,))


def optimize():
    '''Significantly reduces portal creation time.'''
    def __init__(self, text):
        # Don't compile expressions on creation
        self.text = text
    from Products.CMFCore.Expression import Expression
    Expression.__init__ = __init__

    def _cloneActions(self):
        # Don't clone actions but convert to list only
        return list(self._actions)
    from Products.CMFCore.ActionProviderBase import ActionProviderBase
    ActionProviderBase._cloneActions = _cloneActions

optimize()

def setupPortal(PortalInstaller=CPSInstaller):
    # Create a CPS site in the test (demo-) storage
    app = ZopeTestCase.app()
    # PortalTestCase expects object to be called "portal", not "cps"
    if hasattr(app, 'portal'):
        app.manage_delObjects(['portal'])
    PortalInstaller(app).install('portal')
    ZopeTestCase.close(app)

