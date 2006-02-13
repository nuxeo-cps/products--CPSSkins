# Copyright (c) 2003-2005 Chalmers University of Technology
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
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#

__author__ = "Jean-Marc Orliaguet <jmo@ita.chalmers.se>"

"""
  Main Content
  the main content area where documents are displayed.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName

from BaseTemplet import BaseTemplet

factory_type_information = (
    {'id': 'Main Content Templet',
     'meta_type': 'Main Content Templet',
     'description': ('_maincontent_templet_description_'),
     'icon': 'maincontent_templet.png',
     'product': 'CPSSkins',
     'factory': 'addMainContent',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases':  BaseTemplet._aliases,
     'actions':  BaseTemplet._actions,
    },
)

class MainContent(BaseTemplet):
    """
    Main Content Templet.
    """
    meta_type = 'Main Content Templet'
    portal_type = 'Main Content Templet'

    render_method = 'cpsskins_maincontent'

    ismaincontent = 1

    security = ClassSecurityInfo()

    _properties = BaseTemplet._properties + ()

    def __init__(self, id, **kw):
        apply(BaseTemplet.__init__, (self, id), kw)

    security.declarePublic('isRenderable')
    def isRenderable(self):
        """Returns true if the Templet can be rendered.
        """
        return None

    security.declarePublic('isMainContent')
    def isMainContent(self):
        """ Templet is main content """

        return 1

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return None

    security.declarePublic('isESICacheable')
    def isESICacheable(self):
        """ Returns true if the Templet can become an ESI fragment.
            ESI is expected to be globally enabled in the theme.
        """

        return None

    security.declarePublic('can_delete')
    def can_delete(self):
        """ Can the templet be deleted ?"""

        return 1

    security.declarePublic('render')
    def render(self, template=None, **kw):
        """Render the main content area by switching to a 'macroless' skin
        inside the request.
        """
        rendered = ''
        if template is None:
            return self.cpsskins_maincontent()
        portal = getToolByName(self, 'portal_url').getPortalObject()
        portal.changeSkin('CPSSkins-macroless')
        rendered = template.pt_render()
        portal.changeSkin('CPSSkins')
        return rendered

InitializeClass(MainContent)

def addMainContent(dispatcher, id, REQUEST=None, **kw):
    """Add a Main Content Templet."""
    ob = MainContent(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
