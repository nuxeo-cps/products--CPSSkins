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
  Form Style.
  this style defines the appearance of forms and of form elements.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BaseStyle import BaseStyle

factory_type_information = (
    {'id': 'Form Style',
     'meta_type': 'Form Style',
     'description': ('_formstyle_description_'),
     'icon': 'form_style.png',
     'product': 'CPSSkins',
     'factory': 'addFormStyle',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases':  BaseStyle._aliases,
     'actions': BaseStyle._actions,
    },
)

class FormStyle(BaseStyle):
    """
    Form Style.
    """

    meta_type = 'Form Style'
    portal_type = 'Form Style'

    render_method = 'cpsskins_formstyle'
    preview_method = 'cpsskins_formstyle_preview'

    security = ClassSecurityInfo()

    _properties = BaseStyle._properties + (
        {'id': 'Form_padding',
         'type': 'string',
         'mode': 'w',
         'label': 'Form padding',
         'category': 'Form',
        },
        {'id': 'Form_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Area border color',
         'palette' : 'Palette Color',
         'category': 'Form',
        },
        {'id': 'Form_border_style',
         'type': 'string',
         'mode': 'w',
         'label': 'Area border style',
         'palette': 'Palette Border',
         'category': 'Form',
        },
        {'id': 'Form_border_width',
         'type': 'string',
         'mode': 'w',
         'label': 'Area border width',
         'category': 'Form',
        },
        {'id': 'Form_bg_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Area background color',
         'palette' : 'Palette Color',
         'category': 'Form',
        },
        {'id': 'Form_font_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Area font color',
         'palette' : 'Palette Color',
         'category': 'Form',
        },
        {'id': 'Element_padding',
         'type': 'string',
         'mode': 'w',
         'label': 'Area padding',
         'category': 'Elements',
        },
        {'id': 'Element_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Area border color',
         'palette' : 'Palette Color',
         'category': 'Elements',
        },
        {'id': 'Element_active_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Area active border color',
         'palette' : 'Palette Color',
         'category': 'Elements',
        },
        {'id': 'Element_border_style',
         'type': 'string',
         'mode': 'w',
         'label': 'Area border style',
         'palette': 'Palette Border',
         'category': 'Elements',
        },
        {'id': 'Element_border_width',
         'type': 'string',
         'mode': 'w',
         'label': 'Area border width',
         'category': 'Elements',
        },
        {'id': 'Element_bg_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Area background color',
         'palette' : 'Palette Color',
         'category': 'Elements',
        },
        {'id': 'Element_active_bg_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Area active background color',
         'palette' : 'Palette Color',
         'category': 'Elements',
        },
        {'id': 'Element_font_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Area font color',
         'palette' : 'Palette Color',
         'category': 'Elements',
        },
        {'id': 'Button_padding',
         'type': 'string',
         'mode': 'w',
         'label': 'Padding',
         'category': 'Buttons',
        },
        {'id': 'Button_border_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Area border color',
         'palette' : 'Palette Color',
         'category': 'Buttons',
        },
        {'id': 'Button_border_style',
         'type': 'string',
         'mode': 'w',
         'label': 'Area border style',
         'palette' : 'Palette Color',
         'category': 'Buttons',
        },
        {'id': 'Button_border_width',
         'type': 'string',
         'mode': 'w',
         'label': 'Area border width',
         'palette' : 'Palette Color',
         'category': 'Buttons',
        },
        {'id': 'Button_bg_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Background color',
         'palette' : 'Palette Color',
         'category': 'Buttons',
        },
        {'id': 'Button_hover_bg_color',
         'type': 'string',
         'mode': 'w',
         'label': 'Hover background color',
         'palette' : 'Palette Color',
         'category': 'Buttons',
        },
        {'id': 'Button_bg_image',
         'type': 'selection',
         'mode': 'w',
         'label': 'Background image',
         'select_variable' : 'cpsskins_listBackgrounds',
         'image': 'backgrounds',
         'category': 'Buttons',
        },
        {'id': 'Button_hover_bg_image',
         'type': 'selection',
         'mode': 'w',
         'label': 'Hover background image',
         'select_variable' : 'cpsskins_listBackgrounds',
         'image': 'backgrounds',
         'category': 'Buttons',
        },
    )

    def __init__(self, id,
                 Form_padding = '0.3em',
                 Form_border_color = '#eee',
                 Form_border_style = 'solid',
                 Form_border_width = '1px',
                 Form_bg_color = '#f0f0f0',
                 Form_font_color = '#000',
                 Element_border_color = '#bbb',
                 Element_active_border_color = '#fc3',
                 Element_border_style = 'solid',
                 Element_border_width = '1px',
                 Element_bg_color = '',
                 Element_active_bg_color = '#ffd',
                 Element_font_color = '',
                 Element_padding = '',
                 Button_padding = '',
                 Button_border_color = '#999 #333 #333 #999',
                 Button_border_style = 'solid',
                 Button_border_width = '1px',
                 Button_bg_color = '#f0f0f0',
                 Button_hover_bg_color = '#fff',
                 Button_bg_image = '',
                 Button_hover_bg_image = '',
                 **kw):

        apply(BaseStyle.__init__, (self, id), kw)
        self.Form_padding = Form_padding
        self.Form_border_color = Form_border_color
        self.Form_border_style = Form_border_style
        self.Form_border_width = Form_border_width
        self.Form_bg_color = Form_bg_color
        self.Form_font_color = Form_font_color
        self.Element_border_color = Element_border_color
        self.Element_active_border_color = Element_active_border_color
        self.Element_border_style = Element_border_style
        self.Element_border_width = Element_border_width
        self.Element_bg_color = Element_bg_color
        self.Element_active_bg_color = Element_active_bg_color
        self.Element_font_color = Element_font_color
        self.Element_padding = Element_padding
        self.Button_padding = Button_padding
        self.Button_border_color = Button_border_color
        self.Button_border_style = Button_border_style
        self.Button_border_width = Button_border_width
        self.Button_bg_color = Button_bg_color
        self.Button_hover_bg_color = Button_hover_bg_color
        self.Button_bg_image = Button_bg_image
        self.Button_hover_bg_image = Button_hover_bg_image

InitializeClass(FormStyle)

def addFormStyle(dispatcher, id, REQUEST=None, **kw):
    """Add a Form Style."""
    ob = FormStyle(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
