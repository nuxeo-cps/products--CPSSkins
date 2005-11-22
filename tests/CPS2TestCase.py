#
# CPSTestCase
#

from Testing import ZopeTestCase

ZopeTestCase.installProduct('CMFCalendar')
ZopeTestCase.installProduct('CMFCore')
ZopeTestCase.installProduct('CMFDefault')
ZopeTestCase.installProduct('CMFTopic')
ZopeTestCase.installProduct('DCWorkflow')
ZopeTestCase.installProduct('Event')
ZopeTestCase.installProduct('Localizer')
ZopeTestCase.installProduct('MailHost', quiet=1)
ZopeTestCase.installProduct('NuxCPS')
ZopeTestCase.installProduct('NuxCPSDocuments')
ZopeTestCase.installProduct('NuxCPSMembersPrivateArea')
ZopeTestCase.installProduct('NuxCPSMessageCatalog')
ZopeTestCase.installProduct('NuxCPSPreferences')
ZopeTestCase.installProduct('NuxCPSSubscription')
ZopeTestCase.installProduct('NuxCPSXMLImportExport')
ZopeTestCase.installProduct('NuxDocument')
ZopeTestCase.installProduct('NuxExtendedWorkflow')
ZopeTestCase.installProduct('NuxHierarchies')
ZopeTestCase.installProduct('NuxMetaDirectories')
ZopeTestCase.installProduct('NuxPortal')
ZopeTestCase.installProduct('NuxUserGroups')
ZopeTestCase.installProduct('NuxWorkgroup')
ZopeTestCase.installProduct('PortalContentFolder')
ZopeTestCase.installProduct('Scheduler')
ZopeTestCase.installProduct('VersionManager')
ZopeTestCase.installProduct('WorkflowSchema')

from AccessControl.SecurityManagement \
    import newSecurityManager, noSecurityManager
from AccessControl.User import User

from Acquisition import aq_base
import time

try:
    import transaction
except ImportError:
    # BBB: for Zope 2.7
    from Products.CMFCore.utils import transaction


class CPSTestCase(ZopeTestCase.PortalTestCase):
    pass


def setupCPSSite(app, id='portal', quiet=0):
    '''Creates a CPS site.'''
    if not hasattr(aq_base(app), id):
        _start = time.time()
        if not quiet:
            ZopeTestCase._print('Adding CPS Site ... ')
        # Add user and log in
        uf = app.acl_users
        uf._doAddUser('CPSTestCase', '', ['Manager'], [])
        user = uf.getUserById('CPSTestCase').__of__(uf)
        newSecurityManager(None, user)
        # Add CPS Site
        factory = app.manage_addProduct['NuxCPS']
        factory.manage_addCPSSite(id,
            root_password1="passwd", root_password2="passwd",
            langs_list=['en'])
        # Log out
        noSecurityManager()
        transaction.commit()
        if not quiet:
            ZopeTestCase._print('done (%.3fs)\n' % (time.time()-_start,))

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

# Create a CPS site in the test (demo-) storage
app = ZopeTestCase.app()
# PortalTestCase expects object to be called "portal", not "cps"
setupCPSSite(app, id='portal')
ZopeTestCase.close(app)

