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
  Simple Box
  a generic box
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName

BOX_LAYOUTS = {
# standard box
'standard': """<div class="title">%s</div><div class="body">%s</div>""",
# one frame
'one_frame': """<div class="body"><h4>%s</h4><br/>%s</div>""",
# no title no frame
'notitle_noframe': """<div class="body" style="border: none">%s</div>""",
# no title
'notitle': """<div class="body">%s</div>""",
# no frames
'no_frames': """<div class="title" style="border: none">%s</div>
<div class="body" style="border: none">%s</div>""",
# rounded box
'rounded_box': """<div class="rbtop"><div></div></div>
<div class="title">%s</div><div class="body">%s</div>
<div class="rbbot"><div></div></div>""",
# rounded box without title
'rounded_box_notitle': """<div class="rbtop"><div></div></div>
<div class="body">%s</div><div class="rbbot"><div></div></div>""",
}

BOX_LAYOUT_MACRO = 'cpsskins_BoxLayouts'

class SimpleBox:
    """
    Simple Box.
    """

    security = ClassSecurityInfo()

    _properties = (
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
       {'id': 'boxcorners', 
        'type': 'selection', 
        'mode': 'w', 
        'label': 'Box corners', 
        'select_variable': 'BoxCornersList', 
        'category': 'style', 
        'style': 'Box Corners'
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

    def __init__(self,
                 boxshape='',
                 boxcolor='',
                 boxcorners='',
                 boxlayout = 'standard',
                 **kw):
        self.boxshape = boxshape
        self.boxcolor = boxcolor
        self.boxcorners = boxcorners
        self.boxlayout = boxlayout

    #
    # Rendering
    #
    security.declarePublic('renderBoxLayout')
    def renderBoxLayout(self, boxlayout='', title='', body='', **kw):
        """Render the box layout.
        """
        if boxlayout == 'standard' or boxlayout == '': 
            return BOX_LAYOUTS['standard'] % (title, body)
        elif boxlayout == 'one_frame':
            return BOX_LAYOUTS['one_frame'] % (title, body)
        elif boxlayout == 'notitle':
            return BOX_LAYOUTS['notitle'] % body
        elif boxlayout == 'noframe':
            return BOX_LAYOUTS['no_frames'] % (title, body)
        elif boxlayout == 'notitle_noframe':
            return BOX_LAYOUTS['notitle_noframe'] % body
        elif boxlayout == 'rounded_box':
            return BOX_LAYOUTS['rounded_box'] % (title, body)
        elif boxlayout == 'rounded_box_notitle':
            return BOX_LAYOUTS['rounded_box_notitle'] % body

        macro_path = self.restrictedTraverse('%s/macros/%s' %\
                                             (BOX_LAYOUT_MACRO, boxlayout),
                                             default=None
                                            )
        if macro_path is None:
            return ''

        rendered = self.cpsskins_renderBoxLayout(title=title,
                                                 body=body,
                                                 macro_path=macro_path,
                                                 **kw)
        return rendered

    security.declarePublic('getCSSBoxClass')
    def getCSSBoxClass(self):
        """Return the CSS box class for this Templet.
        """

        boxclass = []

        try:
            boxcolor = self.boxcolor
            boxshape = self.boxshape
            boxcorners = self.boxcorners
            if boxcolor:
                boxclass.append('boxColor%s' % boxcolor)
            if boxshape:
                boxclass.append('boxShape%s' % boxshape)
            if boxcorners:
                boxclass.append('boxCorners%s cpsskinsBoxCorners' % boxcorners)

        # rebuild the templet if some attributes are missing.
        # a simple page reload will display the correct results.
        except AttributeError:
            self.rebuild()

        orientation = getattr(self, 'orientation', '')
        if orientation == 'horizontal':
            boxclass.append('cpsskinsTab')
        else:
            boxclass.append('cpsskinsBox')

        if boxclass:
            return ' '.join(boxclass)
        return ''


InitializeClass(SimpleBox)
