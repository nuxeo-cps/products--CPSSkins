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

    render_action = 'cpsskins_portletbox'

    security = ClassSecurityInfo()

    manage_options = ( PropertyManager.manage_options     # Properties
                     + ( {'label': 'Preview',
                          'action': 'manage_templetPreview'}, )
                     )

    _properties = BaseTemplet._properties

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        # XXX not cacheable yet
        return None

    security.declarePublic('isPortalTemplet')
    def isPortalTemplet(self):
        """ is portal templet """
           
        return self.isportaltemplet

    #
    # Properties
    #

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
