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
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#

__author__ = "Jean-Marc Orliaguet <jmo@ita.chalmers.se>"

"""
  Portal Box Group
  a slot that displays the original portal boxes.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName

from BaseTemplet import BaseTemplet

factory_type_information = (
    {'id': 'Portal Box Group Templet',
     'meta_type': 'Portal Box Group Templet',
     'description': ('_portalboxgroup_templet_description_'),
     'icon': 'portalboxgroup_templet.gif',
     'product': 'CPSSkins',
     'factory': 'addPortalBoxGroup',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseTemplet._aliases,
     'actions': BaseTemplet._actions,
    },
)

class PortalBoxGroup(BaseTemplet):
    """
    Portal Box Group Templet.
    """
    meta_type = 'Portal Box Group Templet'
    portal_type = 'Portal Box Group Templet'

    isportalboxgroup = 1
 
    security = ClassSecurityInfo()

    _properties = BaseTemplet._properties + (
        {'id': 'box_group', 
         'type':'string', 
         'mode':'w', 
         'label':'Slot name', 
         'slot': 'cpsskins_listBoxSlots', 
         'category': 'general'
        },
        {'id': 'boxshape', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Box shape', 
         'select_variable': 'BoxShapesList', 
         'category': 'style', 
         'style': 'Portal Box Shape'
        },
        {'id': 'boxcolor', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Box color', 
         'select_variable': 'BoxColorsList', 
         'category': 'style', 
         'style': 'Portal Box Color'
        },
    )

    def __init__(self, id,
                 box_group = '0',
                 boxshape = 'LightSkins', 
                 boxcolor = 'Gray', 
                 **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.box_group = box_group
        self.boxshape = boxshape
        self.boxcolor = boxcolor

    security.declarePublic('isPortalBoxGroup')
    def isPortalBoxGroup(self):
        """ Templet is portal box group """
           
        return self.isportalboxgroup

    security.declarePublic('isAlignable')
    def isAlignable(self):
        """ Returns true if the Templet can be aligned horizontally """

        return None

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        ptltool = getToolByName(self, 'portal_cpsportlets', None)
        if ptltool is not None:
            # XXX should also ask the Portlet's schema
            return 1

    security.declarePublic('isESICacheable')
    def isESICacheable(self):
        """ Returns true if the Templet can become an ESI fragment. 
            ESI is expected to be globally enabled in the theme.
        """

        return None

    security.declarePublic('BoxShapesList')
    def BoxShapesList(self):           
        """ Returns a list of Portal Box Shape styles"""

        tmtool = getToolByName(self, 'portal_themes')
        styles = tmtool.findStylesFor(category = 'Portal Box Shape', 
                                      object=self)
        if styles: 
            return styles['title']

    security.declarePublic('BoxColorsList')
    def BoxColorsList(self):           
        """ Returns a list of Portal Box Color styles"""

        tmtool = getToolByName(self, 'portal_themes')
        styles = tmtool.findStylesFor(category = 'Portal Box Color', 
                                      object=self)
        if styles: 
            return styles['title']


    security.declarePublic('getSlot')
    def getSlot(self):
         """Return the slot name"""

         return self.box_group

    #
    # Rendering.
    #
    security.declarePublic('render')
    def render(self, shield=0, **kw):
        """Renders the templet."""

        ptltool = getToolByName(self, 'portal_cpsportlets', None)
        if ptltool is None:
            return ''
        context = kw.get('context')
        slot = self.getSlot()
        portlets = ptltool.getPortlets(context, slot)

        all_rendered = ''
        for portlet in portlets:
            rendered = ''
            # crash shield
            if shield:
                try:
                    rendered = portlet.render() 
                # could be anything
                except:
                    rendered = self.cpsskins_brokentemplet()
            else:
                rendered = portlet.render()
            all_rendered += rendered

        return all_rendered

InitializeClass(PortalBoxGroup)

def addPortalBoxGroup(dispatcher, id, REQUEST=None, **kw):
    """Add an Portal Box Group Templet."""
    ob = PortalBoxGroup(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
