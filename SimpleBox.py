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
'rounded_box': """<div class="roundedBox">
<div class="ul"></div><div class="ur"></div>
<div class="body" style="border: none">%s</div>
<div class="ll"></div><div class="lr"></div>
</div>""",
}

BOX_LAYOUT_MACRO = 'cpsskins_BoxLayouts'

class SimpleBox:
    """
    Simple Box.
    """

    security = ClassSecurityInfo()

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
            return BOX_LAYOUTS['rounded_box'] % body

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

InitializeClass(SimpleBox)
