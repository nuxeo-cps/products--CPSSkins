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
  Box Corners
  this style defines the appearance of box corners.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BaseStyle import BaseStyle

factory_type_information = (
    {'id': 'Box Corners',
     'meta_type': 'Box Corners',
     'description': ('_boxcorners_description_'),
     'icon': 'box_corners.png',
     'product': 'CPSSkins',
     'factory': 'addBoxCorners',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases':  BaseStyle._aliases,
     'actions': BaseStyle._actions,
    },
)

class BoxCorners(BaseStyle):
    """
    Box Corners
    """

    meta_type = 'Box Corners'
    portal_type = 'Box Corners'

    render_method = 'cpsskins_boxcorners'
    preview_method = 'cpsskins_boxcorners_preview'

    security = ClassSecurityInfo()

    _properties = BaseStyle._properties + (
        {'id': 'Area_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Area border color',
         'palette' : 'Palette Color',
        },
        {'id': 'Area_bg_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Area background color',
         'palette' : 'Palette Color',
        },
        {'id': 'TopLeft_bg_image',
         'type': 'selection',
         'mode': 'w',
         'label': 'Top left image',
         'select_variable' : 'cpsskins_listBackgrounds',
         'image': 'backgrounds',
        },
        {'id': 'TopRight_bg_image',
         'type': 'selection',
         'mode': 'w',
         'label': 'Top right image',
         'select_variable' : 'cpsskins_listBackgrounds',
         'image': 'backgrounds',
        },
        {'id': 'BottomRight_bg_image',
         'type': 'selection',
         'mode': 'w',
         'label': 'Bottom right image',
         'select_variable' : 'cpsskins_listBackgrounds',
         'image': 'backgrounds',
        },
        {'id': 'BottomLeft_bg_image',
         'type': 'selection',
         'mode': 'w',
         'label': 'Bottom left image',
         'select_variable' : 'cpsskins_listBackgrounds',
         'image': 'backgrounds'
        },
    )

    def __init__(self, id,
                 Area_border_color = '#CCC',
                 Area_bg_color = '#FFF',
                 TopLeft_bg_image = '',
                 TopRight_bg_image = '',
                 BottomRight_bg_image = '',
                 BottomLeft_bg_image = '',
                 **kw):
        apply(BaseStyle.__init__, (self, id), kw)
        self.Area_border_color = Area_border_color
        self.Area_bg_color = Area_bg_color
        self.TopLeft_bg_image = TopLeft_bg_image
        self.TopRight_bg_image = TopRight_bg_image
        self.BottomRight_bg_image = BottomRight_bg_image
        self.BottomLeft_bg_image = BottomLeft_bg_image

InitializeClass(BoxCorners)

def addBoxCorners(dispatcher, id, REQUEST=None, **kw):
    """Add a Box Corner Style."""
    ob = BoxCorners(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
