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
from SimpleBox import SimpleBox
from cpsskins_utils import html_slimmer

factory_type_information = (
    {'id': 'Portal Box Group Templet',
     'meta_type': 'Portal Box Group Templet',
     'description': ('_portalboxgroup_templet_description_'),
     'icon': 'portalboxgroup_templet.png',
     'product': 'CPSSkins',
     'factory': 'addPortalBoxGroup',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseTemplet._aliases,
     'actions': BaseTemplet._actions,
    },
)

class PortalBoxGroup(BaseTemplet, SimpleBox):
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
        {'id': 'renderable', 
         'type':'boolean', 
         'mode':'w', 
         'label':'Renderable', 
         'category': 'general',
         'default': 0,
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
                 renderable = 0,
                 boxshape = 'LightSkins', 
                 boxcolor = 'Gray', 
                 boxlayout = 'standard',
                 **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.box_group = box_group
        self.boxshape = boxshape
        self.boxcolor = boxcolor
        self.boxlayout = boxlayout
        self.renderable = renderable

    security.declarePublic('isRenderable')
    def isRenderable(self):
        """Returns true if the Templet can be rendered.
        """
        return getattr(self, 'renderable', 0)

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
            layouts.extend(['min_max', 'min_max_close',
                            'min_max_edit_close'])
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

        return None

    security.declarePublic('isESICacheable')
    def isESICacheable(self):
        """ Returns true if the Templet can become an ESI fragment. 
            ESI is expected to be globally enabled in the theme.
        """

        return None

    security.declarePublic('getSlot')
    def getSlot(self):
         """Return the slot name"""

         return self.box_group

    #
    # CSS
    #
    security.declarePublic('getCSSLayoutStyle')
    def getCSSLayoutStyle(self):
        """Returns the CSS layout style for this Templet."""

        css = ''
        height = self.templet_height

        if height:
            css += 'height:%s' % height
        return css

    security.declarePublic('getCSSBoxStyle')
    def getCSSBoxLayoutStyle(self):
        """Returns the CSS layout style for boxes inside this slot."""

        css = ''
        padding = self.padding

        if padding:
            if padding not in ('0', '0pt', '0in', '0pc', '0mm',
                               '0cm', '0px', '0em', '0ex'):
                css += 'padding:%s;' % padding

        if css:
            return css

    #
    # Rendering.
    #
    security.declarePublic('render')
    def render(self, shield=0, **kw):
        """Renders the templet."""

        if not self.hasPortlets():
            return ''
        context = kw.get('context_obj')
        slot = self.getSlot()
        ptltool = getToolByName(self, 'portal_cpsportlets', None)
        portlets = ptltool.getPortlets(context, slot)

        boxedit = kw.get('boxedit')
        boxlayout = self.boxlayout
        if boxedit:
            boxlayout = 'portlet_edit'

        boxclass = self.getCSSBoxClass()
        boxstyle = self.getCSSBoxLayoutStyle()

        renderBoxLayout = self.renderBoxLayout

        all_rendered = []
        for portlet in portlets:
            # add the box frame
            all_rendered.extend('<div style="%s"><div class="%s">' % \
                                 (boxstyle, boxclass)
                               )
            rendered = portlet.render_cache(**kw)
            # add the box decoration
            all_rendered.extend(renderBoxLayout(boxlayout=boxlayout,
                                                title=portlet.title,
                                                body=html_slimmer(rendered),
                                                portlet=portlet, **kw)
                               )
            all_rendered.extend('</div></div>')

        rendered = ''.join(all_rendered)
        # draw a slot in edit mode
        if boxedit:
            rendered = self.cpsskins_renderBoxSlot(slot=self,
                                                   rendered=rendered)
        return rendered

    security.declarePublic('render_cache')
    def render_cache(self, shield=0, **kw):
        """Renders the cached version of the templet."""
        
        # Entire slots are not cached.
        return self.render(shield=shield, **kw)


InitializeClass(PortalBoxGroup)

def addPortalBoxGroup(dispatcher, id, REQUEST=None, **kw):
    """Add an Portal Box Group Templet."""
    ob = PortalBoxGroup(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
