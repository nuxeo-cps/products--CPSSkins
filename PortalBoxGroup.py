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
       {'id': 'boxlayout', 
        'type': 'selection', 
        'mode': 'w', 
        'label': 'Box layout', 
        'category': 'layout', 
        'select_variable': 'BoxLayoutList',
        'visible': 'hasPortlets',
        'i18n': 1,
        'i18n_prefix': '_option_',
       },
    )

    def __init__(self, id,
                 box_group = '0',
                 boxshape = 'LightSkins', 
                 boxcolor = 'Gray', 
                 boxlayout = 'standard',
                 **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.box_group = box_group
        self.boxshape = boxshape
        self.boxcolor = boxcolor
        self.boxlayout = boxlayout

    security.declarePublic('isPortalBoxGroup')
    def isPortalBoxGroup(self):
        """ Templet is portal box group """
           
        return self.isportalboxgroup

    security.declarePublic('isAlignable')
    def isAlignable(self):
        """ Returns true if the Templet can be aligned horizontally """

        return self.hasPortlets()

    security.declarePublic('BoxLayoutList')
    def BoxLayoutList(self):           
        """ Returns a list of orientations for this Templet"""

        layouts = ['standard', 
                   'one_frame', 
                   'notitle', 
                   'no_frames', 
                   'notitle_noframe']
        if self.hasPortlets():
            layouts.append('min_max')
        return layouts

    security.declarePublic('hasPortlets')
    def hasPortlets(self):
        """Return true if CPSPortlets is installed"""

        ptltool = getToolByName(self, 'portal_cpsportlets', None)
        if ptltool is not None:
            return 1

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return self.hasPortlets()

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

    security.declarePublic('applyBoxLayout')
    def applyBoxLayout(self, **kw):
        """Apply a box layout on the content"""

        return self.cpsskins_renderBox(**kw)
        
    #
    # Rendering.
    #
    security.declarePublic('render')
    def render(self, shield=0, **kw):
        """Renders the templet."""

        if not self.hasPortlets():
            return ''
        context = kw.get('context')
        slot = self.getSlot()
        ptltool = getToolByName(self, 'portal_cpsportlets', None)
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
            # add the box decoration
            rendered = self.applyBoxLayout(title=portlet.getTitle(),
                                           body=rendered,
                                           state=portlet.getState(),
                                           url=portlet.getRelativeUrl())
            all_rendered += rendered

        return all_rendered

    #
    # RAM Cache
    #
    security.declarePublic('getCacheIndex')
    def getCacheIndex(self, REQUEST=None, **kw):
        """Returns the RAM cache index as a tuple (var1, var2, ...)
        """
       
        slot = self.getSlot()
        context = kw.get('context')
        ptltool = getToolByName(self, 'portal_cpsportlets', None)
        portlets = ptltool.getPortlets(context, slot)

        # compute the total index by aggregating all portlet cache indexes.
        index = ()
        for portlet in portlets:
            index += (portlet.getId(),) + portlet.getCacheIndex()
        return index

InitializeClass(PortalBoxGroup)

def addPortalBoxGroup(dispatcher, id, REQUEST=None, **kw):
    """Add an Portal Box Group Templet."""
    ob = PortalBoxGroup(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
