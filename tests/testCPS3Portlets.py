import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSSkinsTestCase
from Testing import ZopeTestCase

HTTP_OK = 200
HTTP_UNAUTHORIZED = 401
HTTP_REDIRECT = 302

try:
    from Products.CPSPortlets import CPSPortlet
except ImportError:
    has_cpsportlets = 0
    ZopeTestCase._print('CPSPortlets is not installed. Skipping the tests.\n')
else:
    has_cpsportlets = 1

class TestCPSPortlets(CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        CPSSkinsTestCase.CPSSkinsTestCase.afterSetUp(self)
        tmtool = self.portal.portal_themes
        tmtool.manage_delObjects(tmtool.objectIds())
        self.theme_container = tmtool.addPortalTheme(empty=1)
        self.pageblock = self.theme_container.addPageBlock()

    def test_Portlet_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addContent(type_name='Portlet Box Templet')
        self.assertEquals('Portlet Box Templet', getattr(templet, 'title'))
        self.assert_(templet.aq_explicit.isPortalTemplet())
        self.assert_(templet.aq_explicit.isPortletBox())

    def test_PortalBoxGroup_Templet(self):
        pageblock = self.pageblock
        templet = pageblock.addContent(type_name='Portal Box Group Templet')
        self.assert_(not templet.aq_explicit.isCacheable())

class TestFunctional(ZopeTestCase.Functional,
                     CPSSkinsTestCase.CPSSkinsTestCase):

    def afterSetUp(self):
        self.login('cpsskins_root')
        self.portal.portal_membership.createMemberArea()
        self.basic_auth = '%s:secret' % self.login_id
        self.ptltool = self.portal.portal_cpsportlets

    def beforeTearDown(self):
        self.logout()

class TestFunctionalAsManager(TestFunctional):
    """Base class for testing as 'Manager'
    """
    login_id = 'cpsskins_root'

    def test_delete_portlet(self):
        ptltool = self.ptltool
        working_context = self.portal.workspaces
        working_slot = 'slot'
        portlet_id = ptltool.createPortlet(ptype_id='Dummy Portlet',
                                           context=working_context,
                                           slot=working_slot,
                                           order=1)
        container = ptltool.getPortletContainer(context=working_context)
        portlet = container.getPortletById(portlet_id)
        test_url = '/%s/cpsskins_delete_portlet?portlet_id=%s' % \
                   (portlet.getLocalFolder().absolute_url(1), portlet.getId() )
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() != HTTP_UNAUTHORIZED )
        self.assert_(container.getPortletById(portlet_id) == None)

class TestFunctionalAsMember(TestFunctional):
    """Testing as 'Member'
    """
    login_id = 'cpsskins_user'

    def test_delete_portlet(self):
        ptltool = self.ptltool
        working_context = self.portal.workspaces
        working_slot = 'slot'
        portlet_id = ptltool.createPortlet(ptype_id='Dummy Portlet',
                                           context=working_context,
                                           slot=working_slot,
                                           order=1)
        container = ptltool.getPortletContainer(context=working_context)
        portlet = container.getPortletById(portlet_id)
        test_url = '/%s/cpsskins_delete_portlet?portlet_id=%s' % \
                   (portlet.getLocalFolder().absolute_url(1), portlet.getId() )
        response = self.publish(test_url, self.basic_auth)
        self.assert_(response.getStatus() == HTTP_UNAUTHORIZED )
        self.assert_(container.getPortletById(portlet_id) != None)

def test_suite():
    suite = unittest.TestSuite()
    target = os.environ.get('CPSSKINS_TARGET', 'CMF')
    if target == 'CPS3' and has_cpsportlets:
        #suite.addTest(unittest.makeSuite(TestCPSPortlets))
        suite.addTest(unittest.makeSuite(TestFunctionalAsManager))
        suite.addTest(unittest.makeSuite(TestFunctionalAsMember))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=2)

