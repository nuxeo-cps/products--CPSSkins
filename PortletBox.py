# Copyright (c) 2003-2004 Chalmers University of Technology
# Authors: Jean-Marc Orliaguet <jmo@ita.chalmers.se>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# YoU should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#

__author__ = "Jean-Marc Orliaguet <jmo@ita.chalmers.se>"

"""
  Portlet Box Templet
  a box that contains a portlet.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.PropertyManager import PropertyManager

from Products.CMFCore.utils import getToolByName

from BaseTemplet import BaseTemplet
from CPSSkinsPermissions import ManageThemes

factory_type_information = (
    {'id': 'Portlet Box Templet',
     'description': ('_portletbox_templet_description_'),
     'meta_type': 'Portlet Box Templet',
     'icon': 'portletbox_templet.gif',
     'product': 'CPSSkins',
     'factory': 'addPortletBox',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseTemplet._aliases,
     'actions': BaseTemplet._actions,
    },
)

class PortletBox(BaseTemplet):
    """
    Portlet Box Templet.
    """
    meta_type = 'Portlet Box Templet'
    portal_type = 'Portlet Box Templet'

    isportletbox = 1

    render_action = 'cpsskins_portletbox'

    security = ClassSecurityInfo()

    manage_options = ( PropertyManager.manage_options     # Properties
                     + ( {'label': 'Preview',
                          'action': 'manage_templetPreview'}, )
                     )

    _properties = BaseTemplet._properties + (
       {'id': 'portlet_id', 
        'type': 'selection', 
        'mode': 'w', 
        'label': 'Portlet id', 
        'select_variable': 'cpsskins_select_portlet',
        'category': 'none',
       },
       {'id': 'portlet_type', 
        'type': 'selection', 
        'mode': 'w', 
        'label': 'Portlet type', 
        'select_variable': 'cpsskins_listPortletTypes',
        'category': 'general',
        'i18n': 1,
       },
    )

    def __init__(self, id, 
                 portlet_id = None, 
                 portlet_type = None,
                 **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.portlet_id = portlet_id
        self.portlet_type = portlet_type

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return 1

    security.declarePublic('getCacheIndex')
    def getCacheIndex(self, REQUEST=None):
        """ returns the RAM cache index as a tuple (var1, var2, ...) """
       
        # XXX: additional information should be obtained from the portlet.
        # 
        index = (self.boxid, )
        return index

    security.declarePublic('isPortalTemplet')
    def isPortalTemplet(self):
        """ is portal templet """
           
        return self.isportaltemplet

    security.declarePublic('isPortletBox')
    def isPortletBox(self):
        """ is portlet box """

        return self.isportletbox
           
    security.declareProtected(ManageThemes, 'edit')
    def edit(self, **kw):
        """
        Edit method, changes the properties 
        or creates a new global portlet.
        """

        portlet_type = kw.get('portlet_type', None) 
        if portlet_type is not None:
            ptype_id = self.getPortletType()

            # XXX CPS3 specific - should it be here?
            ptltool = getToolByName(self, 'portal_cpsportlets')

            # Create a global portlet on the fly and associate
            # the portlet id to this portlet box.
            if self.getPortletId() is None:
                portlet_id = ptltool.createPortlet(ptype_id=portlet_type, isglobal=1)
                if portlet_id is not None:
                    kw.update({'portlet_id': portlet_id}) 

            # Modify an existing portlet:
            elif portlet_type != ptype_id:
                old_portlet_id = self.getPortletId()
                portlet_id = ptltool.createPortlet(ptype_id=portlet_type, isglobal=1)
                if portlet_id is not None:
                    kw.update({'portlet_id': portlet_id}) 
                res = ptltool.deletePortlet(portlet_id=old_portlet_id, isglobal=1)
                if res:
                    # XXX: what to do?
                    pass

        self.manage_changeProperties(**kw)
        self.expireCache()

    #
    # Portlet interface.
    #
    security.declarePublic('getPortletId')
    def getPortletId(self):
        """Returns the id of the associated portlet."""

        return getattr(self, 'portlet_id', None)

    security.declarePublic('getPortletType')
    def getPortletType(self):
        """Returns the portal type of the associated portlet."""

        return None
        return getattr(self, 'portlet_type', None)

    # RAM Cache
    #
    security.declarePublic('getCacheIndex')
    def getCacheIndex(self, REQUEST=None):
        """ returns the RAM cache index as a tuple (var1, var2, ...) """
       
        index = ()
        # XXX to connect to CPSPortlets
        return index


InitializeClass(PortletBox)

def addPortletBox(dispatcher, id, REQUEST=None, **kw):
    """Add an Portlet Box Templet."""

    ob = PortletBox(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
