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
  FontColor
  this style defines the font, link and decoration colors.
"""

from Globals import InitializeClass

from BaseStyle import BaseStyle

factory_type_information = (
    {'id': 'Font Color',
     'meta_type': 'Font Color',
     'description': ('_fontcolor_description_'),
     'icon': 'fontcolor.png',
     'product': 'CPSSkins',
     'factory': 'addFontColor',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseStyle._aliases,
     'actions': BaseStyle._actions,
    },
)

class FontColor(BaseStyle):
    """
    FontColor.
    """
    meta_type = 'Font Color'
    portal_type = 'Font Color'

    render_method = 'cpsskins_fontcolor'
    preview_method = 'cpsskins_fontcolor_preview'

    _properties = BaseStyle._properties + (
        {'id': 'H1_font_color',
         'type': 'string',
         'mode': 'w',
         'label': 'H1_font_color',
         'category': 'H1',
         'palette': 'Palette Color'
        },
        {'id': 'H1_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'H1_border_color',
         'category': 'H1',
         'palette': 'Palette Color'
        },
        {'id': 'H1_bg_color',
         'type': 'string',
         'mode': 'w',
         'label': 'H1_bg_color',
         'category': 'H1',
         'palette': 'Palette Color'
        },
        {'id': 'H2_font_color',
         'type': 'string',
         'mode': 'w',
         'label': 'H2_font_color',
         'category': 'H2',
         'palette': 'Palette Color'
        },
        {'id': 'H2_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'H2_border_color',
         'category': 'H2',
         'palette': 'Palette Color'
        },
        {'id': 'H2_bg_color',
         'type': 'string',
         'mode': 'w',
         'label': 'H2_bg_color',
         'category': 'H2',
         'palette': 'Palette Color'
        },
        {'id': 'H3_font_color',
         'type': 'string',
         'mode': 'w',
         'label': 'H3_font_color',
         'category': 'H3',
         'palette': 'Palette Color'
        },
        {'id': 'H3_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'H3_border_color',
         'category': 'H3',
         'palette': 'Palette Color'
        },
        {'id': 'H3_bg_color',
         'type': 'string',
         'mode': 'w',
         'label': 'H3_bg_color',
         'category': 'H3',
         'palette': 'Palette Color'
        },
        {'id': 'H456_font_color',
         'type': 'string',
         'mode': 'w',
         'label': 'H456_font_color',
         'category': 'H456',
         'palette': 'Palette Color'
        },
        {'id': 'H456_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'H456_border_color',
         'category': 'H456',
         'palette': 'Palette Color'
        },
        {'id': 'H456_bg_color',
         'type': 'string',
         'mode': 'w',
         'label': 'H456_bg_color',
         'category': 'H456',
         'palette': 'Palette Color'
        },
        {'id': 'A_link',
         'type': 'string',
         'mode': 'w',
         'label': 'A link',
         'palette': 'Palette Color'
        },
        {'id': 'A_visited',
         'type': 'string',
         'mode': 'w',
         'label': 'A visited',
         'palette': 'Palette Color'
        },
        {'id': 'A_active',
         'type': 'string',
         'mode': 'w',
         'label': 'A active',
         'palette': 'Palette Color'
        },
        {'id': 'A_hover',
         'type': 'string',
         'mode': 'w',
         'label': 'A hover',
         'palette': 'Palette Color'
        },
)

    def __init__(self, id,
                 A_link = '#003399',
                 A_visited = '#003399',
                 A_active = '#003399',
                 A_hover = '#3399FF',
                 H1_font_color = 'Black',
                 H2_font_color = 'Black',
                 H3_font_color = 'Black',
                 H456_font_color = 'Black',
                 H1_border_color = '#666666',
                 H1_bg_color = '',
                 H2_border_color = '#666666',
                 H2_bg_color = '',
                 H3_border_color = '#666666',
                 H3_bg_color = '',
                 H456_border_color = '#666666',
                 H456_bg_color = '',
                 **kw):
        apply(BaseStyle.__init__, (self, id), kw)

        self.A_link = A_link
        self.A_visited = A_visited
        self.A_active = A_active
        self.A_hover = A_hover
        self.H1_font_color = H1_font_color
        self.H2_font_color = H2_font_color
        self.H3_font_color = H3_font_color
        self.H456_font_color = H456_font_color
        self.H1_border_color = H1_border_color
        self.H1_bg_color = H1_bg_color
        self.H2_border_color = H2_border_color
        self.H2_bg_color = H2_bg_color
        self.H3_border_color = H3_border_color
        self.H3_bg_color = H3_bg_color
        self.H456_border_color = H456_border_color
        self.H456_bg_color = H456_bg_color

InitializeClass(FontColor)

def addFontColor(dispatcher, id, REQUEST=None, **kw):
    """Add an FontColor."""
    ob = FontColor(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
