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
  CollapsibleMenu Style
  this style defines the visual appearance of collapsible menus.
"""

from Globals import InitializeClass

from BaseStyle import BaseStyle

factory_type_information = (
    {'id': 'Collapsible Menu Style',
     'meta_type': 'Collapsible Menu Style',
     'description': ('_collapsiblemenustyle_description_'),
     'icon': 'collapsiblemenu_style.png',
     'product': 'CPSSkins',
     'factory': 'addCollapsibleMenuStyle',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseStyle._aliases,
     'actions': BaseStyle._actions,
    },
)

class CollapsibleMenuStyle(BaseStyle):
    """
    Collapsible Menu Style.
    """
    meta_type = 'Collapsible Menu Style'
    portal_type = 'Collapsible Menu Style'

    render_action = 'cpsskins_collapsiblemenustyle'
    preview_action = 'cpsskins_collapsiblemenustyle_preview'

    _properties = BaseStyle._properties + (
        {'id': 'topmenu_border_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Top menu border color', 
         'category': 'topmenu', 
         'palette' : 'Palette Color'
        },
        {'id': 'topmenu_border_style', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Top menu border style', 
         'category': 'topmenu', 
         'palette': 'Palette Border'
        },
        {'id': 'topmenu_bg_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Top menu background color', 
         'category': 'topmenu',  
         'palette' : 'Palette Color'
        },
        {'id': 'topmenu_hover_bg_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Top menu hover background color', 
         'category':'topmenu', 
         'palette': 'Palette Color'
        },
        {'id': 'submenu_border_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Sub-menu border color', 
         'category': 'submenus', 
         'palette': 'Palette Color'
        },
        {'id': 'submenu_border_style', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Sub-menu border style', 
         'category': 'submenus', 
         'palette' : 'Palette Border'
        },
        {'id': 'submenu_bg_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Sub-menu background color', 
         'category': 'submenus', 
         'palette': 'Palette Color'
        },
        {'id': 'submenu_hover_bg_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Sub-menu hover background color', 
         'category': 'submenus', 
         'palette': 'Palette Color'
        },
        {'id': 'topmenu_font_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Top menu font color', 
         'category' : 'topmenu', 
         'palette' : 'Palette Color'
        },
        {'id': 'topmenu_hover_font_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Top menu hover font color', 
         'category': 'topmenu', 
         'palette': 
         'Palette Color'
        },
        {'id': 'submenu_font_color', 
         'type': 'string', 
          'mode': 'w', 
          'label': 'Sub-menu font color', 
          'category': 'submenus', 
          'palette': 'Palette Color'
        },
        {'id': 'submenu_hover_font_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Sub-menu hover font color', 
         'category': 'submenus', 
         'palette': 'Palette Color'
        },
        {'id': 'topmenu_font', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Top menu font', 
         'category': 'topmenu'
        },
        {'id': 'submenu_font', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Sub-menu font', 
         'category' : 'submenus'
        },
    )

    def __init__(self, id, 
                 topmenu_border_color = '#999999', 
                 topmenu_border_style = 'solid', 
                 topmenu_bg_color = '#c0c0c0',
                 topmenu_hover_bg_color = '#ececec',
                 submenu_border_color = '#c0c0c0',
                 submenu_border_style = 'none none solid solid',
                 submenu_bg_color = '#e0e0e0',
                 submenu_hover_bg_color = '#f3f3f3',
                 topmenu_font_color = 'Black',
                 topmenu_hover_font_color = 'Black',
                 submenu_font_color = 'Black', 
                 submenu_hover_font_color = 'Black', 
                 topmenu_font = 'bold 11px Verdana, Arial, sans-serif',
                 submenu_font = '11px Verdana, Arial, sans-serif',
                 **kw):
        apply(BaseStyle.__init__, (self, id), kw)
        self.topmenu_border_color = topmenu_border_color
        self.topmenu_border_style = topmenu_border_style
        self.topmenu_bg_color = topmenu_bg_color
        self.topmenu_hover_bg_color = topmenu_hover_bg_color
        self.submenu_border_color = submenu_border_color
        self.submenu_border_style = submenu_border_style
        self.submenu_bg_color = submenu_bg_color
        self.submenu_hover_bg_color = submenu_hover_bg_color
        self.topmenu_font_color = topmenu_font_color
        self.topmenu_hover_font_color = topmenu_hover_font_color
        self.submenu_font_color = submenu_font_color
        self.submenu_hover_font_color = submenu_hover_font_color
        self.topmenu_font = topmenu_font
        self.submenu_font = submenu_font

InitializeClass(CollapsibleMenuStyle)

def addCollapsibleMenuStyle(dispatcher, id, REQUEST=None, **kw):
    """Add a CollapsibleMenu Style."""
    ob = CollapsibleMenuStyle(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
