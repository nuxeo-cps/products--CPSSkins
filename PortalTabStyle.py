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
  Portal Tab Style
  this style defines the appearance of portal tabs.
"""

from Globals import InitializeClass

from BaseStyle import BaseStyle

factory_type_information = (
    {'id': 'Portal Tab Style',
     'meta_type': 'Portal Tab Style',
     'description': ('_portaltabstyle_description_'),
     'icon': 'portaltab_style.png',
     'product': 'CPSSkins',
     'factory': 'addPortalTabStyle',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseStyle._aliases,
     'actions': BaseStyle._actions,
    },
)

class PortalTabStyle(BaseStyle):
    """
    Portal Tab Style.
    """
    meta_type = 'Portal Tab Style'
    portal_type = 'Portal Tab Style'

    render_method = 'cpsskins_portaltabstyle'
    preview_method = 'cpsskins_portaltabstyle_preview'

    _properties = BaseStyle._properties + (
        {'id': 'HorizontalMargin',
         'type': 'string',
         'mode': 'w',
         'label': 'Horizontal margin',
         'category':'general'
        },
        {'id': 'VerticalPadding',
         'type': 'string',
         'mode': 'w',
         'label': 'Vertical padding',
         'category':'general'
        },
        {'id': 'HorizontalPadding',
         'type': 'string',
         'mode': 'w',
         'label': 'Horizontal padding',
         'category':'general'
        },
        {'id': 'Tab_width',
         'type': 'string',
         'mode': 'w',
         'label': 'Tab width',
         'category':'general'
        },
        {'id': 'Tabs_bg_image',
         'type': 'selection',
         'mode': 'w',
         'label': 'Background image',
         'select_variable': 'cpsskins_listBackgrounds',
         'category': 'general',
         'image': 'backgrounds',
        },
        {'id': 'Tab_bottom_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Bottom border color',
         'category': 'default tab',
         'palette': 'Palette Color'
        },
        {'id': 'TabIn_bottom_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Bottom border color',
         'category': 'selected tab',
         'palette': 'Palette Color'
        },
        {'id': 'Tab_left_bg_image',
         'type': 'selection',
         'mode': 'w',
         'label': 'Left-side image',
         'select_variable': 'cpsskins_listBackgrounds',
         'category': 'default tab',
         'image': 'backgrounds',
        },
        {'id': 'Tab_right_bg_image',
         'type': 'selection',
         'mode': 'w',
         'label': 'Right-side image',
         'select_variable': 'cpsskins_listBackgrounds',
         'category': 'default tab',
         'image': 'backgrounds',
        },
        {'id': 'TabIn_left_bg_image',
         'type': 'selection',
         'mode': 'w',
         'label': 'Left-side image',
         'select_variable': 'cpsskins_listBackgrounds',
         'category': 'selected tab',
         'image': 'backgrounds',
        },
        {'id': 'TabIn_right_bg_image',
         'type': 'selection',
         'mode': 'w',
         'label': 'Right-side image',
         'select_variable': 'cpsskins_listBackgrounds',
         'category': 'selected tab',
         'image': 'backgrounds',
        },
    )

    def __init__(self, id,
                 HorizontalMargin = '1px',
                 VerticalPadding = '3px',
                 HorizontalPadding = '3px',
                 Tab_width = '',
                 Tabs_bg_image = '',
                 Tab_left_bg_image = '',
                 Tab_right_bg_image = '',
                 TabIn_left_bg_image = '',
                 TabIn_right_bg_image = '',
                 Tab_bottom_border_color = '',
                 TabIn_bottom_border_color = '',
                 **kw):
        apply(BaseStyle.__init__, (self, id), kw)
        self.HorizontalMargin = HorizontalMargin
        self.VerticalPadding = VerticalPadding
        self.HorizontalPadding = HorizontalPadding
        self.Tab_width = Tab_width
        self.Tabs_bg_image = Tabs_bg_image
        self.Tab_left_bg_image = Tab_left_bg_image
        self.Tab_right_bg_image = Tab_right_bg_image
        self.TabIn_left_bg_image = TabIn_left_bg_image
        self.TabIn_right_bg_image = TabIn_right_bg_image
        self.Tab_bottom_border_color = Tab_bottom_border_color
        self.TabIn_bottom_border_color = TabIn_bottom_border_color

InitializeClass(PortalTabStyle)

def addPortalTabStyle(dispatcher, id, REQUEST=None, **kw):
    """Add a Portal Tab Style."""
    ob = PortalTabStyle(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
