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
  Portal Box Shape
  this style defines the shapes of portal boxes.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BaseStyle import BaseStyle

factory_type_information = (
    {'id': 'Portal Box Shape',
     'meta_type': 'Portal Box Shape',
     'description': ('_boxshape_description_'),
     'icon': 'box_shape.png',
     'product': 'CPSSkins',
     'factory': 'addPortalBoxShape',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseStyle._aliases,
     'actions': BaseStyle._actions,
    },
)

class PortalBoxShape(BaseStyle):
    """
    Portal Box Shape.
    """
    meta_type = 'Portal Box Shape'
    portal_type = 'Portal Box Shape'

    render_method = 'cpsskins_portalboxshape'
    preview_method = 'cpsskins_portalboxshape_preview'

    security = ClassSecurityInfo()

    _properties = BaseStyle._properties + (
        {'id': 'BoxTitle_font',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxTitle font',
         'category':'box title',
        },
        {'id': 'BoxTitle_border_style',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxTitle border style',
         'category': 'box title',
         'palette': 'Palette Border',
        },
        {'id': 'BoxTitle_border_width',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxTitle border width',
         'category': 'box title',
        },
        {'id': 'BoxTitle_padding',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxTitle padding',
         'category': 'box title',
        },
        {'id': 'BoxTitle_display',
         'type': 'selection',
         'mode': 'w',
         'label': 'BoxTitle display',
         'select_variable': 'listDisplayStyles',
         'category': 'box title',
         'i18n': 1,
         'i18n_prefix': '_option_',
        },
        {'id': 'BoxBody_border_style',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody border style',
         'category': 'box body',
         'palette': 'Palette Border',
        },
        {'id': 'BoxBody_border_width',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody border width',
         'category': 'box body',
        },
        {'id': 'BoxBody_padding',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody padding',
         'category':'box body',
        },
        {'id': 'BoxBody_menuin_padding',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody menuin padding',
         'category': 'selected menu item',
        },
        {'id': 'BoxBody_menuout_padding',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody menuout padding',
         'category': 'menu item',
        },
        {'id': 'BoxBody_menuout_border_style',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody menuout border style',
         'palette': 'Palette Border',
         'category': 'menu item',
        },
        {'id': 'BoxBody_menuout_border_width',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody menuout border width',
         'category': 'menu item',
        },
        {'id': 'BoxBody_menuout_margin',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody menuout margin',
         'category': 'menu item',
        },
        {'id': 'BoxBody_menuin_border_style',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody menuin border style',
         'palette': 'Palette Border',
         'category': 'selected menu item',
        },
        {'id': 'BoxBody_menuin_border_width',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody menuin border width',
         'category': 'selected menu item',
        },
        {'id': 'BoxBody_menuin_margin',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody menuin margin',
         'category': 'selected menu item',
        },
    )

    def __init__(self, id,
                 BoxTitle_border_style = 'none solid none none',
                 BoxTitle_border_width = '1px',
                 BoxTitle_padding = '0em 1.2em 0em 0.9em',
                 BoxTitle_display = 'inline-block',
                 BoxTitle_font = '12px arial, sans-serif',
                 BoxBody_border_style = 'none solid solid none',
                 BoxBody_border_width = '1px',
                 BoxBody_padding = '0.5em 0.5em 0.5em 0.5em',
                 BoxBody_menuin_padding = '1px 4px 1px 13px',
                 BoxBody_menuout_padding = '1px 4px 1px 13px',
                 BoxBody_menuin_border_style = 'inset',
                 BoxBody_menuin_border_width = '1px',
                 BoxBody_menuin_margin = '0em',
                 BoxBody_menuout_border_style = 'none',
                 BoxBody_menuout_border_width = '1px',
                 BoxBody_menuout_margin = '0em',
                 **kw):
        apply(BaseStyle.__init__, (self, id), kw)
        self.BoxTitle_border_style = BoxTitle_border_style
        self.BoxTitle_border_width = BoxTitle_border_width
        self.BoxTitle_padding = BoxTitle_padding
        self.BoxTitle_display = BoxTitle_display
        self.BoxTitle_font = BoxTitle_font
        self.BoxBody_border_style = BoxBody_border_style
        self.BoxBody_border_width = BoxBody_border_width
        self.BoxBody_padding = BoxBody_padding
        self.BoxBody_menuin_padding = BoxBody_menuin_padding
        self.BoxBody_menuout_padding = BoxBody_menuout_padding
        self.BoxBody_menuin_border_style = BoxBody_menuin_border_style
        self.BoxBody_menuin_border_width = BoxBody_menuin_border_width
        self.BoxBody_menuin_margin = BoxBody_menuin_margin
        self.BoxBody_menuout_border_style = BoxBody_menuout_border_style
        self.BoxBody_menuout_border_width = BoxBody_menuout_border_width
        self.BoxBody_menuout_margin = BoxBody_menuout_margin

    security.declarePublic('listDisplayStyles')
    def listDisplayStyles(self):
        """ Returns a list of display styles"""

        list = ['block', 'inline']
        return list

InitializeClass(PortalBoxShape)

def addPortalBoxShape(dispatcher, id, REQUEST=None, **kw):
    """Add a Portal Box Shape."""
    ob = PortalBoxShape(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
