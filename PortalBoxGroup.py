# Copyright (c) 2003-2005 Chalmers University of Technology
# (C) Copyright 2007 Nuxeo SAS <http://nuxeo.com>
# Authors:
# Jean-Marc Orliaguet <jmo@ita.chalmers.se>
# M.-A. Darche <madarche@nuxeo.com>
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
# $Id$

__author__ = "Jean-Marc Orliaguet <jmo@ita.chalmers.se>"

"""
  Portal Box Group
  a slot that displays the original portal boxes.
"""

import logging
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName

from crashshield import shield_apply
from crashshield import CrashShieldException
from BaseTemplet import BaseTemplet
from SimpleBox import SimpleBox
from designerexport import DESIGNER_THEMES_EXPORT_PORTLET
from designerexport import is_cps_designer_themes_export

logger = logging.getLogger('Products.CPSSkins.PortalBoxGroup')

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
        {'id': 'box_title_i18n',
         'type': 'boolean',
         'mode': 'w',
         'label': 'Translate the box title',
         'category': 'general',
         'i18n': 1,
        },
       {'id': 'orientation',
        'type': 'selection',
        'mode': 'w',
        'label': 'List orientation',
        'select_variable': 'listOrientations',
        'category': 'layout',
        'i18n': 1,
        'i18n_prefix': '_option_',
       },
    )

    box_group = '0'
    macroless = 0
    box_title_i18n = 0
    orientation = 'vertical'

    def __init__(self, id,
                 box_group = '0',
                 macroless = 0,
                 box_title_i18n = 0,
                 orientation = 'vertical',
                 **kw):
        BaseTemplet.__init__(self, id, **kw)
        SimpleBox.__init__(self, **kw)
        self.box_group = box_group
        self.macroless = macroless
        self.box_title_i18n = box_title_i18n
        self.orientation = orientation

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
        """Return a list of layouts for this Templet.
        """
        layouts = self.cpsskins_listBoxLayouts('PortletBox')
        if self.hasPortlets():
            layouts.extend(['min_max',
                            'min_max_close',
                            'min_max_edit_close',
                           ])
        return layouts

    security.declarePublic('listOrientations')
    def listOrientations(self):
        """ Returns a list of orientations for this Templet"""

        list = ['horizontal', 'vertical']
        return list

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
    def getCSSLayoutStyle(self, level=2):
        """Returns the CSS layout style for this Templet.
        level = 1 for CSS1 browsers
        level = 2 for CSS2 browsers
        """

        if level == 1:
            return ''
        height = self.templet_height
        css = 'text-align: %s;' % self.align

        if height:
            css += 'height:%s' % height

        if css:
            return css
        return ''

    security.declarePublic('getCSSBoxStyle')
    def getCSSBoxLayoutStyle(self):
        """Returns the CSS layout style for boxes inside this slot."""

        css = ''
        padding = self.padding
        if padding:
            if padding not in ('0', '0pt', '0in', '0pc', '0mm',
                               '0cm', '0px', '0em', '0ex'):
                css += 'padding:%s;' % padding
        return css

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
        utool = getToolByName(self, 'portal_url')
        checkPerm = mtool.checkPermission
        charset = utool.getPortalObject().default_charset

        box_title_i18n = self.box_title_i18n
        if box_title_i18n:
            tmtool = getToolByName(self, 'portal_themes')
            mcat = tmtool.getTranslationService(cat='default')
        boxedit = kw.get('boxedit')
        boxlayout = self.boxlayout

        boxclass = self.getCSSBoxClass()
        boxstyle = self.getCSSBoxLayoutStyle()

        renderBoxLayout = self.renderBoxLayout

        dthm_export = is_cps_designer_themes_export(self)
        all_rendered = []
        if dthm_export:
            portlets = [DESIGNER_THEMES_EXPORT_PORTLET,]
            attrs = ['cps:slot="%s"' % slot]
            if box_title_i18n:
                attrs.append('cps:translate-titles="true"')
            all_rendered.append('<div %s>' % ' '.join(attrs))
        else:
            portlets = ptltool.getPortlets(context, slot, **kw)

        # edge-side includes
        render_esi = 0
        if enable_esi:
            if self.isESIFragment():
                render_esi = 1

        if boxedit:
            bmf = ptltool.getBottomMostFolder(context=context)
            kw['folder_editable'] = checkPerm('Manage Portlets', bmf)
            kw['folder_rurl'] = utool.getRelativeUrl(bmf)


        for portlet in portlets:
            kw['portlet'] = portlet
            # render the box body
            if render_esi:
                rendered = portlet.render_esi(**kw)
            else:
                if shield:
                    try:
                        __traceback_info__="portlet id: " + portlet.getId()
                        rendered = shield_apply(portlet, 'render_cache', **kw)
                    except CrashShieldException:
                        rendered = '<blink>!!!</blink>'
                else:
                    rendered = portlet.render_cache(**kw)

            # do not render boxes with empty bodies
            if not boxedit and rendered.strip() == '':
                continue

            # open the box frame
            if boxstyle or boxclass:
                has_frame = True
                enclosing_attrs = []
                if boxstyle:
                    enclosing_attrs.append('style="%s"' % boxstyle)
                elif boxclass:
                    enclosing_attrs.append('class="%s"' % boxclass)
            if dthm_export:
                if not has_frame:
                    has_frame = True
                    enclosing_attrs = ['cps:remove="True"']
                enclosing_attrs.append('cps:portlet="frame"')

            if has_frame:
                all_rendered.append('<div %s>' % ' '.join(enclosing_attrs))

            if boxstyle and boxclass:
                all_rendered.append('<div class="%s">' % boxclass)

            # add the box decoration
            title = portlet.title
            if box_title_i18n and mcat is not None:
                title = mcat(title)
                if charset != 'unicode':
                    try:
                        title = title.encode(charset, 'ignore')
                    except (UnicodeDecodeError, LookupError):
                        logger.warn("problem with title=%r", repr(title),
                                    exc_info=True)
            rendered = renderBoxLayout(
                boxlayout=boxlayout,
                title=title,
                body=rendered,
                **kw)
            if boxedit:
                kw['editable'] = checkPerm('Manage Portlets', portlet)
                portlet_folder = portlet.getLocalFolder()
                kw['portlet_folder_rurl'] = utool.getRelativeUrl(portlet_folder)
                # wrap the edition markup around the box in edit mode
                rendered = renderBoxLayout(
                    boxlayout='portlet_edit',
                    body=rendered,
                    **kw)
            all_rendered.append(rendered)
            # close the box frame
            if boxstyle and boxclass:
                all_rendered.append('</div>')
            if has_frame:
                all_rendered.append('</div>')

        if dthm_export:
                all_rendered.append('</div>')
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
