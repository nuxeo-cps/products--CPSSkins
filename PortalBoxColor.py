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
  Portal Box Color
  this style defines the colors of portal boxes.
"""

from Globals import InitializeClass

from BaseStyle import BaseStyle

factory_type_information = (
    {'id': 'Portal Box Color',
     'meta_type': 'Portal Box Color',
     'description': ('_boxcolor_description_'),
     'icon': 'box_color.png',
     'product': 'CPSSkins',
     'factory': 'addPortalBoxColor',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseStyle._aliases,
     'actions': BaseStyle._actions,
    },
)

class PortalBoxColor(BaseStyle):
    """
    Portal Box Color.
    """
    meta_type = 'Portal Box Color'
    portal_type = 'Portal Box Color'

    render_method = 'cpsskins_portalboxcolor'
    preview_method = 'cpsskins_portalboxcolor_preview'

    _properties = BaseStyle._properties + (
        {'id': 'BoxTitle_bg_color',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxTitle background color',
         'category': 'box title',
         'palette': 'Palette Color'
        },
        {'id': 'BoxTitle_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxTitle border color',
         'category': 'box title',
         'palette': 'Palette Color'
        },
        {'id': 'BoxBody_bg_color',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody background color',
         'category': 'box body',
         'palette': 'Palette Color'
        },
        {'id': 'BoxBody_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody border color',
         'category': 'box body',
         'palette': 'Palette Color'
        },
        {'id': 'BoxBody_menuout_color',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody menuout color',
         'palette': 'Palette Color',
         'category':'menu item',
        },
        {'id': 'BoxBody_menuout_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody menuout border color',
         'palette': 'Palette Color',
         'category':'menu item',
        },
        {'id': 'BoxBody_menuin_color',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody menuin color',
         'palette': 'Palette Color',
         'category':'selected menu item',
        },
        {'id': 'BoxBody_menuin_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody menuin border color',
         'palette': 'Palette Color',
         'category':'selected menu item',
        },
        {'id': 'BoxTitle_font_color',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxTitle font color',
         'category': 'box title',
         'palette': 'Palette Color',
        },
        {'id': 'BoxTitle_bg_image',
         'type': 'selection',
         'mode': 'w',
         'label': 'BoxTitle background image',
         'select_variable': 'cpsskins_listBackgrounds',
         'category': 'box title',
         'image': 'backgrounds',
        },
        {'id': 'BoxBody_bg_image',
         'type': 'selection',
         'mode': 'w',
         'label': 'BoxBody background image',
         'select_variable': 'cpsskins_listBackgrounds',
         'category': 'box body',
         'image': 'backgrounds',
        },
        {'id': 'BoxBody_menuin_icon',
         'type': 'selection',
         'mode': 'w',
         'label': 'BoxBody menuin icon',
         'select_variable': 'cpsskins_listIcons',
         'image': 'icons',
         'category':'selected menu item',
        },
        {'id': 'BoxBody_menuout_icon',
         'type': 'selection',
         'mode': 'w',
         'label': 'BoxBody menuout icon',
         'select_variable': 'cpsskins_listIcons',
         'category':'menu item',
         'image': 'icons',
        },
    )

    def __init__(self, id,
                 BoxTitle_bg_color = '#d0d0d0',
                 BoxTitle_border_color = '#999999',
                 BoxBody_bg_color = '#f3f3f9',
                 BoxBody_border_color = '#999999',
                 BoxBody_menuout_color = '#f6f6fc',
                 BoxBody_menuin_color = '#bdd2ee',
                 BoxBody_menuin_border_color = '#669999',
                 BoxBody_menuout_border_color = '#f6f6fc',
                 BoxBody_menuin_icon = '',
                 BoxBody_menuout_icon = '',
                 BoxTitle_font_color = 'Black',
                 BoxTitle_bg_image = '',
                 BoxBody_bg_image = '',
                       **kw):
        apply(BaseStyle.__init__, (self, id), kw)
        self.BoxTitle_bg_color = BoxTitle_bg_color
        self.BoxTitle_border_color = BoxTitle_border_color
        self.BoxBody_bg_color = BoxBody_bg_color
        self.BoxBody_border_color = BoxBody_border_color
        self.BoxBody_menuout_color = BoxBody_menuout_color
        self.BoxBody_menuin_color = BoxBody_menuin_color
        self.BoxBody_menuin_border_color = BoxBody_menuin_border_color
        self.BoxBody_menuout_border_color = BoxBody_menuout_border_color
        self.BoxBody_menuin_icon = BoxBody_menuin_icon
        self.BoxBody_menuout_icon = BoxBody_menuout_icon
        self.BoxTitle_font_color = BoxTitle_font_color
        self.BoxTitle_bg_image = BoxTitle_bg_image
        self.BoxBody_bg_image = BoxBody_bg_image

InitializeClass(PortalBoxColor)

def addPortalBoxColor(dispatcher, id, REQUEST=None, **kw):
    """Add a Box Color."""
    ob = PortalBoxColor(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
