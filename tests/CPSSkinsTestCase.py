
# CPSSkinsTestCase
#

from Testing import ZopeTestCase
from Products.ExternalMethod.ExternalMethod import ExternalMethod

from AccessControl.SecurityManagement \
    import newSecurityManager, noSecurityManager

ZopeTestCase.installProduct('PageTemplates', quiet=1)
ZopeTestCase.installProduct('PythonScripts', quiet=1)
ZopeTestCase.installProduct('ExternalMethod', quiet=1)

# Optional products
ZopeTestCase.installProduct('Localizer', quiet=1)
ZopeTestCase.installProduct('TranslationService', quiet=1)
ZopeTestCase.installProduct('CMFCalendar', quiet=1)

try: ZopeTestCase.installProduct('CMFActionIcons', quiet=1)
except: pass
try: ZopeTestCase.installProduct('ZChecker', quiet=1)
except: pass

ZopeTestCase.installProduct('CPSSkins', quiet=1)

import time
import os

import CPSSkinsTestCase

ERROR_LOG_ID = 'error_log'

# session management
def setViewMode(self, **kw):
    """ """
    self.fake_session = {}
    self.fake_session.update(kw)

def getViewMode(self):
    """ """
    return getattr(self, 'fake_session', {})

from Products.CPSSkins.PortalThemesTool import PortalThemesTool
PortalThemesTool.setViewMode = setViewMode
PortalThemesTool.getViewMode = getViewMode

# This one is needed by ProxyTool.
def get_selected_language(self):
    """ """
    return self._default_language

localizer = 1
try:
   from Products.Localizer.Localizer import Localizer
   Localizer.get_selected_language = get_selected_language
except:
   localizer = 0

# Dummy portal_catalog.

from OFS.SimpleItem import SimpleItem
class DummyTranslationService(SimpleItem):
    meta_type = 'Translation Service'
    id = 'translation_service'
    def translate(self, domain, msgid, *args, **kw):
        return msgid

# Dummy MessageCatalog
class DummyMessageCatalog:
    def __call__(self, message, *args, **kw):
        return message

    def get_selected_language(self):
        "xxx"
        return 'fr'

    def get_languages(self):
        return ['en', 'fr']

    def manage_import(self, *args, **kw):
        pass

    def wl_isLocked(self):
        return None # = False

target = os.environ.get('CPSSKINS_TARGET', 'CMF')

# CMF (CMFTestCase.CMFTestCase)
if target == 'CMF':
   import CMFTestCase
   sourceskin = 'Basic'

   class CPSSkinsTestCase(CMFTestCase.CMFTestCase):
       '''Base test case for CPSSkins testing under CMF
       '''

# CPS2 (NuxCPS.CPSTestCase)
if target == 'CPS2':
   import CPS2TestCase
   sourceskin = 'Basic'

   class CPSSkinsTestCase(CPS2TestCase.CPSTestCase):
       '''Base test case for CPSSkins testing under CPS2
       '''

# CPS3 (CPSDefault.CPSTestCase)
if target == 'CPS3':
   import CPS3TestCase
   sourceskin = 'Basic'

   class CPSSkinsTestCase(CPS3TestCase.CPSTestCase):
       '''Base test case for CPSSkins testing under CPS3
       '''

# Plone2 (CMFPlone.PloneTestCase)
if target == 'Plone2':
   import Plone2TestCase
   sourceskin = 'Plone Default'

   class CPSSkinsTestCase(Plone2TestCase.PloneTestCase):
       '''Base test case for CPSSkins testing under Plone2
       '''

quiet = 0
class CPSSkinsInstaller:
    def __init__(self, app, quiet=0):
        self.app = app
        self._start = time.time()
        self._quiet = quiet

    def install(self, portal_id, target, quiet):
        self.addUser()
        self.login()
        self.fixupCMFCalendar(portal_id, quiet)
        self.setup(portal_id, target, quiet)
        if localizer==1:
            self.fixupTranslationServices(portal_id)
        self.install_themes(portal_id, quiet)
        self.fixupErrorLog(portal_id)

    def addUser(self):
        uf = self.app.acl_users
        uf._doAddUser('CPSSkinsTestCase', '', ['Manager'], [])

    def login(self):
        uf = self.app.acl_users
        user = uf.getUserById('CPSSkinsTestCase').__of__(uf)
        newSecurityManager(None, user)

    def setup(self, portal_id, target, quiet):
        portal = getattr(self.app, portal_id)
        if not quiet:
            ZopeTestCase._print('Setting up CPSSkins ... \n')
        factory = portal.manage_addProduct['CPSSkins']
        factory.manage_addCPSSkins(portal_id, SourceSkin=sourceskin, \
             Target=target, ReinstallDefaultThemes=1)

    # Change translation_service to DummyTranslationService
    def fixupTranslationServices(self, portal_id):
        portal = getattr(self.app, portal_id)
        portal.translation_service = DummyTranslationService()
        localizer = portal.Localizer
        for domain in localizer.objectIds():
            setattr(localizer, domain, DummyMessageCatalog())

    def install_themes(self, portal_id, quiet):
        portal = getattr(self.app, portal_id)
        tmtool = portal.portal_themes
        if not quiet:
            ZopeTestCase._print('Installing CPSSkins test themes ...\n')
        zexpdir = os.path.join(os.curdir, 'data')
        for themeid in ['theme1', 'empty']:
           zexppath  = os.path.join(zexpdir, '%s.zexp' % themeid)
           ZopeTestCase.utils.importObjectFromFile(tmtool, zexppath)

    # remove ignored exceptions
    def fixupErrorLog(self, portal_id):
        portal = getattr(self.app, portal_id)
        if ERROR_LOG_ID in portal.objectIds():
            portal[ERROR_LOG_ID].setProperties(keep_entries=0, \
                                copy_to_zlog=0, ignored_exceptions=())


    # install CMF Calendar for testing
    def fixupCMFCalendar(self, portal_id, quiet):
        portal = getattr(self.app, portal_id)
        portal_objectIds = portal.objectIds()
        if 'portal_calendar' not in portal_objectIds:
            if not quiet:
                ZopeTestCase._print('Installing CMFCalendar ...\n')
            install = ExternalMethod('install_cmfcalendar',
                                     'CMFCalendar',
                                     'CMFCalendar.Install',
                                     'install' )
            portal._setObject('install_cmfcalendar', install)
            portal.install_cmfcalendar()

    def logout(self):
        noSecurityManager()
        get_transaction().commit()

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

def setupTestUsers(app, portal_id):
    """Set up the test users"""
    portal = getattr(app, portal_id)
    uf = portal.acl_users
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
        uf._doAddUser(user['id'], 'secret', user['roles'], [])

# Install

if target == 'CMF':
   portal_id='cmf'
   CMFTestCase.setupCMFSite()
   CMFTestCase.setupCMFSkins()
   app = ZopeTestCase.app()

if target == 'CPS2':
   portal_id='portal'
   CPS2TestCase.setupCPSSite()
   app = ZopeTestCase.app()

if target == 'CPS3':
   portal_id='portal'
   CPS3TestCase.setupPortal()
   app = ZopeTestCase.app()

if target == 'Plone2':
   portal_id='portal'
   app = ZopeTestCase.app()
   Plone2TestCase.setupPloneSite(app)

setupTestUsers(app, portal_id)
ZopeTestCase.utils.setupCoreSessions(app)
CPSSkinsInstaller(app).install(portal_id, target, quiet=0)

ZopeTestCase.close(app)
