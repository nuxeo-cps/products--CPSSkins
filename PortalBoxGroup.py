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

    _properties = BaseTemplet._properties + \
                  SimpleBox._properties + (
        {'id': 'box_group', 
         'type':'string', 
         'mode':'w', 
         'label':'Slot name', 
         'slot': 'cpsskins_listBoxSlots', 
         'category': 'general'
        },
        {'id': 'macroless', 
         'type':'boolean', 
         'mode':'w', 
         'label':'Macroless', 
         'category': 'general',
         'default': 0,
        },
    )

    def __init__(self, id,
                 box_group = '0',
                 macroless = 0,
                 **kw):
        BaseTemplet.__init__(self, id, **kw)
        SimpleBox.__init__(self, **kw)
        self.box_group = box_group
        self.macroless = macroless 

    security.declarePublic('isRenderable')
    def isRenderable(self):
        """Returns true if the Templet can be rendered.
        """
        macroless = getattr(self, 'macroless', 0)
        return macroless

    security.declarePublic('isPortalBoxGroup')
    def isPortalBoxGroup(self):
        """ Templet is portal box group """
           
        return self.isportalboxgroup

    security.declarePublic('isAlignable')
    def isAlignable(self):
        """ Returns true if the Templet can be aligned horizontally """

        return self.hasPortlets()

    security.declarePublic('listBoxLayouts')
    def listBoxLayouts(self):           
        """Return a list of orientations for this Templet
        """
        layouts = self.cpsskins_listBoxLayouts('PortletBox')
        if self.hasPortlets():
            layouts.extend(['min_max',
                            'min_max_close',
                            'min_max_edit_close',
                           ])
        return layouts

    security.declarePublic('hasPortlets')
    def hasPortlets(self):
        """Return true if CPSPortlets is installed"""

        ptltool = getToolByName(self, 'portal_cpsportlets', None)
        if ptltool is not None:
            return 1
        return None

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return None

    security.declarePublic('isESICacheable')
    def isESICacheable(self):
        """ Returns true if the Templet can become an ESI fragment. 
            ESI is expected to be globally enabled in the theme.
        """

        if self.hasPortlets():
            return 1
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
        return None

    #
    # Rendering.
    #
    security.declarePublic('render')
    def render(self, shield=0, enable_esi=0, **kw):
        """Renders the templet."""

        if not self.hasPortlets():
            return ''

        context = kw.get('context_obj')
        slot = self.getSlot()
        ptltool = getToolByName(self, 'portal_cpsportlets', None)
        mtool = getToolByName(self, 'portal_membership')
        checkPerm = mtool.checkPermission
        portlets = ptltool.getPortlets(context, slot)

        boxedit = kw.get('boxedit')
        boxlayout = self.boxlayout

        boxclass = self.getCSSBoxClass()
        boxstyle = self.getCSSBoxLayoutStyle()

        renderBoxLayout = self.renderBoxLayout

        # edge-side includes
        render_esi = 0
        if enable_esi:
            if self.isESIFragment():
                render_esi = 1

        all_rendered = []
        for portlet in portlets:
            kw['portlet'] = portlet
            # render the box body
            if render_esi:
                rendered = portlet.render_esi(**kw)
            else:
                if shield:
                    try:
                        rendered = portlet.render_cache(**kw)
                    except:
                        rendered = '<blink>!!!</blink>'
                else:
                    rendered = portlet.render_cache(**kw)

            # do not render boxes with empty bodies
            if not boxedit and rendered == '':
                continue

            # open the box frame
            all_rendered.extend('<div style="%s"><div class="%s">' % \
                                 (boxstyle, boxclass) )

            # add the box decoration
            rendered = renderBoxLayout(boxlayout=boxlayout,
                                       title=portlet.title,
                                       body=rendered, **kw)
            if boxedit:
                kw['editable'] = checkPerm('Manage Portlets', portlet)
                # wrap the edition markup around the box in edit mode
                rendered = renderBoxLayout(boxlayout='portlet_edit',
                                           body=rendered,
                                           **kw)
            all_rendered.extend(rendered)
            # close the box frame
            all_rendered.extend('</div></div>')

        rendered = ''.join(all_rendered)
        # wrap a box slot in edit mode
        if boxedit:
            rendered = self.cpsskins_renderBoxSlot(
                slot=self,
                rendered=rendered, **kw)
        return rendered

    security.declarePublic('render_cache')
    def render_cache(self, shield=0, enable_esi=0, **kw):
        """Renders the cached version of the templet."""
        
        # Entire slots are not cached.
        return self.render(shield=shield, enable_esi=enable_esi, **kw)


InitializeClass(PortalBoxGroup)

def addPortalBoxGroup(dispatcher, id, REQUEST=None, **kw):
    """Add an Portal Box Group Templet."""
    ob = PortalBoxGroup(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
