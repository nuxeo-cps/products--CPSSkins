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
  FontShape
  this style defines font sizes, links and decoration styles.
"""

from Globals import InitializeClass

from BaseStyle import BaseStyle

factory_type_information = (
    {'id': 'Font Shape',
     'meta_type': 'Font Shape',
     'description': ('_fontshape_description_'),
     'icon': 'fontshape.png',
     'product': 'CPSSkins',
     'factory': 'addFontShape',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseStyle._aliases,
     'actions': BaseStyle._actions,
    },
)


class FontShape(BaseStyle):
    """
    FontShape.
    """
    meta_type = 'Font Shape'
    portal_type = 'Font Shape'

    render_method = 'cpsskins_fontshape'
    preview_method = 'cpsskins_fontshape_preview'

    _properties = BaseStyle._properties + (
        {'id': 'Default_font', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Default_font', 
         'category' : 'general'
        },
        {'id': 'H1_font', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'H1_font', 
         'category' : 'H1'
        },
        {'id': 'H1_padding', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'H1_padding', 
         'category' : 'H1'
        },
        {'id': 'H1_border_width', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'H1_border_width', 
         'category' : 'H1'
        },
        {'id': 'H1_border_style', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'H1_border_style', 
         'category': 'H1', 
         'palette': 'Palette Border'
        },
        {'id': 'H2_font', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'H2_font', 
         'category' : 'H2'
        },
        {'id': 'H2_padding', 
         'type': 'string',  
         'mode': 'w', 
         'label': 'H2_padding', 
         'category' : 'H2'
        },
        {'id': 'H2_border_width', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'H2_border_width', 
         'category' : 'H2'
        },
        {'id': 'H2_border_style', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'H2_border_style', 
         'category': 'H2', 
         'palette': 'Palette Border'
        },
        {'id': 'H3_font', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'H3_font', 
         'category': 'font style', 
         'category': 'H3'
        },
        {'id': 'H3_padding', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'H3_padding', 
         'category': 'H3'
        },
        {'id': 'H3_border_width', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'H3_border_width', 
         'category': 'H3'
        },
        {'id': 'H3_border_style', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'H3_border_style', 
         'category': 'H3', 
         'palette': 'Palette Border'
        },
        {'id': 'H456_font', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'H456_font', 
         'category': 'font style', 
         'category': 'H456'
        },
        {'id': 'H456_padding', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'H456_padding', 
         'category': 'H456'
        },
        {'id': 'H456_border_width', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'H456_border_width', 
         'category': 'H456'
        },
        {'id': 'H456_border_style', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'H456_border_style', 
         'category': 'H456', 
         'palette': 'Palette Border'
        },
        {'id': 'P_font', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'P_font', 
         'category' : 'general'
        },
        {'id': 'STRONG_font', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'STRONG_font', 
         'category': 'general'
        },
        {'id': 'P_padding', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'P_padding', 
         'category': 'general'
        },
        {'id': 'A_link_decoration', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'A_link_decoration', 
         'category': 'general',
         'palette': 'Palette Border'
        },
        {'id': 'A_visited_decoration', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'A_visited_decoration', 
         'category': 'general',
         'palette': 'Palette Border'
        },
        {'id': 'A_active_decoration', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'A_active_decoration', 
         'category' : 'general',
         'palette': 'Palette Border'
        },
        {'id': 'A_hover_decoration', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'A_hover_decoration', 
         'category': 'general',
         'palette': 'Palette Border'
        },
    )

    def __init__(self, id, 
                 Default_font = '11px Verdana, Arial, Helvetica, sans-serif',
                 H1_font = 'normal 150% Verdana, Arial, Helvetica, sans-serif',
                 H1_padding = '0.8em 0em 0em 0em',
                 H1_border_width = '1px',
                 H1_border_style = 'none',
                 H2_font = 'bold 125% Verdana, Arial, Helvetica, sans-serif',
                 H2_padding = '0.6em 0em 0em 0em',
                 H2_border_width = '1px',
                 H2_border_style = 'none',
                 H3_font = 'bold 120% Verdana, Arial, Helvetica, sans-serif',
                 H3_padding = '0.6em 0em 0em 0em',
                 H3_border_width = '1px',
                 H3_border_style = 'none',
                 H456_font = 'bold 115% Verdana, Arial, Helvetica, sans-serif',
                 H456_padding = '0.4em 0em 0em 0em',
                 H456_border_width = '1px',
                 H456_border_style = 'none',
                 P_font = '100% Verdana, Arial, Helvetica, sans-serif',
                 STRONG_font = 'bold 100%',
                 P_padding = '0em',
                 A_link_decoration = 'none',
                 A_visited_decoration = 'none',
                 A_active_decoration = 'none',
                 A_hover_decoration = 'none',
                 **kw):
        apply(BaseStyle.__init__, (self, id), kw)
        self.Default_font = Default_font
        self.H1_font = H1_font
        self.H1_padding = H1_padding
        self.H1_border_width = H1_border_width
        self.H1_border_style = H1_border_style
        self.H2_font = H2_font
        self.H2_padding = H2_padding
        self.H2_border_width = H2_border_width
        self.H2_border_style = H2_border_style
        self.H3_font = H3_font
        self.H3_padding = H3_padding
        self.H3_border_width = H3_border_width
        self.H3_border_style = H3_border_style
        self.H456_font = H456_font
        self.H456_padding = H456_padding
        self.H456_border_width = H456_border_width
        self.H456_border_style = H456_border_style
        self.P_font = P_font
        self.P_padding = P_padding
        self.STRONG_font = STRONG_font
        self.A_link_decoration = A_link_decoration
        self.A_visited_decoration = A_visited_decoration
        self.A_active_decoration = A_active_decoration
        self.A_hover_decoration = A_hover_decoration

InitializeClass(FontShape)

def addFontShape(dispatcher, id, REQUEST=None, **kw):
    """Add an FontShape."""
    ob = FontShape(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
