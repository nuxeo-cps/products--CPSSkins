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
  Area Color
  this style defines the background, border and text colors of an area.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BaseStyle import BaseStyle

factory_type_information = (
    {'id': 'Area Color',
     'meta_type': 'Area Color',
     'description': ('_areacolor_description_'),
     'icon': 'area_color.png',
     'product': 'CPSSkins',
     'factory': 'addAreaColor',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases':  BaseStyle._aliases,
     'actions': BaseStyle._actions,
    },
)

class AreaColor(BaseStyle):
    """
    Area Color.
    """

    meta_type = 'Area Color'
    portal_type = 'Area Color'

    render_method = 'cpsskins_areacolor'
    preview_method = 'cpsskins_areacolor_preview'

    security = ClassSecurityInfo()

    _properties = BaseStyle._properties + (
        {'id': 'Area_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Area border color',
         'palette' : 'Palette Color'
        },
        {'id': 'Area_bg_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Area background color',
         'palette' : 'Palette Color'
        },
        {'id': 'Area_bg_image',
         'type': 'selection',
         'mode': 'w',
         'label': 'Area background image',
         'select_variable' : 'cpsskins_listBackgrounds',
         'image': 'backgrounds'
        },
        {'id': 'Area_bg_position',
         'type': 'string',
         'mode': 'w',
         'label': 'Area background position',
         'visible': 'ifBackgroundImage',
        },
        {'id': 'Area_bg_repeat',
         'type': 'selection',
         'mode': 'w',
         'label': 'Area background repeat',
         'select_variable': 'listBackgroundRepeats',
         'visible': 'ifBackgroundImage',
         'default': 'repeat',
         'i18n': 1,
         'i18n_prefix': '_option_bg_',
        },
        {'id': 'Area_font_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Area font color',
         'palette' : 'Palette Color'
        },
    )

    def __init__(self, id,
                 Area_border_color = '#CCC',
                 Area_bg_color = '#FFF',
                 Area_bg_image = '',
                 Area_bg_position = '',
                 Area_bg_repeat = '',
                 Area_font_color = '#000000',
                 **kw):

        apply(BaseStyle.__init__, (self, id), kw)
        self.Area_border_color = Area_border_color
        self.Area_bg_color = Area_bg_color
        self.Area_bg_image = Area_bg_image
        self.Area_bg_position = Area_bg_position
        self.Area_bg_repeat = Area_bg_repeat
        self.Area_font_color = Area_font_color

    security.declarePublic('listBackgroundRepeats')
    def listBackgroundRepeats(self):
        """Return a list of background repeat options"""

        list = ['repeat', 'repeat-x', 'repeat-y', 'no-repeat']
        return list

    security.declarePublic('ifBackgroundImage')
    def ifBackgroundImage(self):
        """Return True is there is a backround image"""

        if self.Area_bg_image:
            return 1
        return None

InitializeClass(AreaColor)

def addAreaColor(dispatcher, id, REQUEST=None, **kw):
    """Add an Area Color."""
    ob = AreaColor(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
