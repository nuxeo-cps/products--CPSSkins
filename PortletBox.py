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

from cpsskins_utils import html_slimmer

factory_type_information = (
    {'id': 'Portlet Box Templet',
     'description': ('_portletbox_templet_description_'),
     'meta_type': 'Portlet Box Templet',
     'icon': 'portletbox_templet.png',
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
         'select_variable': 'PortletTypesList',
         'category': 'general',
         'i18n': 1,
         'i18n_prefix': '',
         'i18n_suffix': '',
         'i18n_default_domain': 1,
         'i18n_transform': 'getPortletTypeTitle',
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
         'i18n': 1,
         'i18n_prefix': '_option_',
        },
    )

    def __init__(self, id, 
                 portlet_id = None, 
                 portlet_type = None,
                 boxshape = 'LightSkins', 
                 boxcolor = 'Gray', 
                 boxlayout = 'standard',
                 **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.portlet_id = portlet_id
        self.portlet_type = portlet_type
        self.boxshape = boxshape
        self.boxcolor = boxcolor
        self.boxlayout = boxlayout

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return None

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

            # CPSPortlets
            ptltool = getToolByName(self, 'portal_cpsportlets', None)
            if ptltool is not None:

                # Create a global portlet on the fly and associate
                # the portlet id to this portlet box.
                if self.getPortletId() is None:
                    portlet_id = ptltool.createPortlet(ptype_id=portlet_type) 
                    if portlet_id is not None:
                        kw.update({'portlet_id': portlet_id}) 

                # Modify an existing portlet:
                elif portlet_type != ptype_id:
                    old_portlet_id = self.getPortletId()
                    portlet_id = ptltool.createPortlet(ptype_id=portlet_type)
                    if portlet_id is not None:
                        kw.update({'portlet_id': portlet_id}) 
                    res = ptltool.deletePortlet(portlet_id=old_portlet_id)
                    if res:
                        # XXX: what to do?
                        pass

        # remove unknown properties
        for prop in kw.keys():
            if self.hasProperty(prop):
                continue
            del kw[prop]

        self.manage_changeProperties(**kw)
        self.expireCache()

    # 
    # Properties
    # 
    security.declarePublic('getPortletTypeTitle')
    def getPortletTypeTitle(self, ptype=None):
        """Returns the title associated to a given type
           or the portal type id if the title is empty.
        """

        ttool = getToolByName(self, 'portal_types')
        if ptype is None:
            return

        title = ''
        fti = ttool.getTypeInfo(ptype)
        if fti is not None:
            title = fti.title_or_id()
        return title

    security.declarePublic('BoxLayoutList')
    def BoxLayoutList(self):           
        """ Returns a list of orientations for this Templet"""

        layouts = ['standard', 
                   'one_frame', 
                   'notitle', 
                   'no_frames', 
                   'notitle_noframe']
        return layouts

    #
    # Portlet interface.
    #
    security.declarePublic('getPortletId')
    def getPortletId(self):
        """Returns the id of the associated portlet."""

        return self.portlet_id

    security.declarePublic('getPortletType')
    def getPortletType(self):
        """Returns the portal type of the associated portlet."""

        return self.portlet_type

    security.declarePublic('PortletTypesList')
    def PortletTypesList(self):
        """Returns the list of available portlets types."""

        ptltool = getToolByName(self, 'portal_cpsportlets', None)
        if ptltool is not None:
            return ptltool.listPortletTypes()

    security.declareProtected(ManageThemes, 'setPortletId')
    def setPortletId(self, portlet_id=None):
        """Set the id of the associated portlet."""

        self.portlet_id = portlet_id

    #
    # CSS
    #
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

        ptltool = getToolByName(self, 'portal_cpsportlets', None)
        if ptltool is None:
            return ''
        portlet_id = self.getPortletId()
        portlet = ptltool.getPortletById(portlet_id)

        boxlayout = self.boxlayout
        if boxlayout == '':
            boxlayout = 'standard'

        boxclass = self.getCSSBoxClass()
        boxstyle = self.getCSSBoxLayoutStyle()

        macro_path = self.unrestrictedTraverse('cpsskins_BoxLayouts/macros/%s' % \
                                               boxlayout, default=None)
        if macro_path is None:
            return ''

        rendered = ''
        if portlet is not None:
            # crash shield
            if shield:
                try:
                    rendered = portlet.render_cache(**kw)
                # could be anything
                except:
                    rendered = self.cpsskins_brokentemplet(**kw)
            else:
                rendered = portlet.render_cache(**kw)

            title = self.title
            body = html_slimmer(rendered)

            # add the box decoration$
            rendered = self.cpsskins_renderPortletBox(title=title,
                                                      body=body,
                                                      boxclass=boxclass,
                                                      boxstyle=boxstyle,
                                                      macro_path=macro_path,
                                                      portlet=portlet)
        return rendered

    #
    # RAM Cache
    #
    security.declarePublic('getCustomCacheIndex')
    def getCustomCacheIndex(self, **kw):
        """Returns the custom RAM cache index as a tuple (var1, var2, ...)
        """
        
        # CPSPortlets
        # overriding BaseTemplet's getCustomCacheIndex()
        ptltool = getToolByName(self, 'portal_cpsportlets', None)
        if ptltool is None:
            return None
        portlet_id = self.getPortletId()
        portlet = ptltool.getPortletById(portlet_id)
        if portlet is not None:
            return portlet.getCacheIndex(**kw)
        return None

InitializeClass(PortletBox)

def addPortletBox(dispatcher, id, REQUEST=None, **kw):
    """Add an Portlet Box Templet."""

    ob = PortletBox(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
