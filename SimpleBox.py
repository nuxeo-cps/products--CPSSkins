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
  Simple Box
  a generic box
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

import ExtensionClass

BOX_LAYOUTS = {
    'standard': {
        'markup': """<div class="title">%s</div>
                     <div class="body">%s</div>""",
        },

    'plain': {
        'markup': """%s""",
        },

    'one_frame': {
        'markup': """<div class="body"><h4>%s</h4>%s</div>""",
        },

    'notitle_noframe': {
        'markup': """<div class="body" style="border: none">%s</div>""",
        },

    'notitle': {
        'markup': """<div class="body">%s</div>""",
        },

    'no_frames': {
        'markup': """<div class="title" style="border: none">%s</div>
                     <div class="body" style="border: none">%s</div>
                  """,
        },

    'rounded_box': {
        'markup': """<div class="cpsskinsBoxCorners">
                     <div class="rbtop"><div></div></div>
                     <div class="title">%s</div>
                     <div class="body">%s</div>
                     <div class="rbbot"><div></div></div></div>
                  """,
        },

    'rounded_box_notitle': {
        'markup': """<div class="cpsskinsBoxCorners">
                     <div class="rbtop"><div></div></div>
                     <div class="body">%s</div>
                     <div class="rbbot"><div></div></div>
                     </div>
                  """,
        },

    'horizontal_menu': {
        'markup': """<div class="cpsskinsTabs body">%s</div>""",
        },
}

BOX_LAYOUT_MACRO = 'cpsskins_BoxLayouts'

class SimpleBox(ExtensionClass.Base):
    """
    Simple Box.
    """

    security = ClassSecurityInfo()

    _properties = (
       {'id': 'boxshape',
        'type': 'selection',
        'mode': 'w',
        'label': 'Box shape',
        'select_variable': 'listBoxShapes',
        'category': 'style',
        'style': 'Portal Box Shape'
       },
       {'id': 'boxcolor',
        'type': 'selection',
        'mode': 'w',
        'label': 'Box color',
        'select_variable': 'listBoxColors',
        'category': 'style',
        'style': 'Portal Box Color'
       },
       {'id': 'boxcorners',
        'type': 'selection',
        'mode': 'w',
        'label': 'Box corners',
        'select_variable': 'listBoxCorners',
        'category': 'style',
        'style': 'Box Corners'
       },
       {'id': 'portaltabstyle',
        'type': 'selection',
        'mode': 'w',
        'label': 'Tab style',
        'select_variable': 'listTabStyles',
        'category': 'style',
        'style': 'Portal Tab Style'
       },
       {'id': 'boxlayout',
        'type': 'selection',
        'mode': 'w',
        'label': 'Box layout',
        'category': 'layout',
        'select_variable': 'listBoxLayouts',
        'i18n': 1,
        'i18n_prefix': '_option_',
       },
    )

    def __init__(self,
                 boxshape='',
                 boxcolor='',
                 boxcorners='',
                 portaltabstyle='',
                 boxlayout = 'standard',
                 **kw):
        self.boxshape = boxshape
        self.boxcolor = boxcolor
        self.boxcorners = boxcorners
        self.portaltabstyle = portaltabstyle
        self.boxlayout = boxlayout

    #
    # CSS
    #
    security.declarePublic('getCSSBoxClass')
    def getCSSBoxClass(self):
        """Return the CSS box class for this Templet.
        """

        boxclass = []
        try:
            boxcolor = self.boxcolor
            boxshape = self.boxshape
            boxcorners = self.boxcorners
            portaltabstyle = self.portaltabstyle
            if boxcolor:
                boxclass.append('boxColor%s' % boxcolor)
            if boxshape:
                boxclass.append('boxShape%s' % boxshape)
            if boxcorners:
                boxclass.append('boxCorner%s' % boxcorners)
            if portaltabstyle:
                boxclass.append('portalTab%s' % portaltabstyle)

        # rebuild the templet if some attributes are missing.
        # a simple page reload will display the correct results.
        except AttributeError:
            self.rebuild()

        # XXX move this to box layouts
        if self.boxlayout != 'plain':
            orientation = getattr(self, 'orientation', '')
            if orientation == 'horizontal':
                boxclass.append('cpsskinsTab')
            elif self.boxlayout != 'horizontal_menu':
                boxclass.append('cpsskinsBox')

        if len(boxclass) > 0:
            return ' '.join(boxclass)
        return ''

    #
    # Rendering
    #
    security.declarePublic('renderBoxLayout')
    def renderBoxLayout(self, boxlayout='', title='', body='', **kw):
        """Render the box layout.
        """
        if boxlayout == 'standard' or boxlayout == '':
            return BOX_LAYOUTS['standard']['markup'] % (title, body)
        if boxlayout == 'plain':
            return BOX_LAYOUTS['plain']['markup'] % body
        elif boxlayout == 'one_frame':
            return BOX_LAYOUTS['one_frame']['markup'] % (title, body)
        elif boxlayout == 'notitle':
            return BOX_LAYOUTS['notitle']['markup'] % body
        elif boxlayout == 'no_frames':
            return BOX_LAYOUTS['no_frames']['markup'] % (title, body)
        elif boxlayout == 'notitle_noframe':
            return BOX_LAYOUTS['notitle_noframe']['markup'] % body
        elif boxlayout == 'rounded_box':
            return BOX_LAYOUTS['rounded_box']['markup'] % (title, body)
        elif boxlayout == 'rounded_box_notitle':
            return BOX_LAYOUTS['rounded_box_notitle']['markup'] % body
        elif boxlayout == 'horizontal_menu':
            return BOX_LAYOUTS['horizontal_menu']['markup'] % body

        macro_path = self.restrictedTraverse(
            '%s/macros/%s' % (BOX_LAYOUT_MACRO, boxlayout),
            default=None)

        if macro_path is None:
            return ''
        rendered = self.cpsskins_renderBoxLayout(
            title=title,
            body=body,
            macro_path=macro_path,
            **kw)
        return rendered

InitializeClass(SimpleBox)
