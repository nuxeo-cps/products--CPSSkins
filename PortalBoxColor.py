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
  Portal Box Color
  this style defines the colors of portal boxes.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

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
        {'id': 'BoxTitle_bg_position',
         'type': 'string',
         'mode': 'w',
         'label': 'Background position',
         'visible': 'ifTitleBackgroundImage',
         'category': 'box title',
        },
        {'id': 'BoxTitle_bg_repeat',
         'type': 'selection',
         'mode': 'w',
         'label': 'Background repeat',
         'select_variable': 'listBackgroundRepeats',
         'visible': 'ifTitleBackgroundImage',
         'category': 'box title',
         'default': 'repeat',
         'i18n': 1,
         'i18n_prefix': '_option_bg_',
        },
        {'id': 'BoxBody_bg_color',
         'type': 'string',
         'mode': 'w',
         'label': 'BoxBody background color',
         'category': 'box body',
         'palette': 'Palette Color'
        },
        {'id': 'BoxBody_bg_position',
         'type': 'string',
         'mode': 'w',
         'label': 'Background position',
         'visible': 'ifBodyBackgroundImage',
         'category': 'box body',
        },
        {'id': 'BoxBody_bg_repeat',
         'type': 'selection',
         'mode': 'w',
         'label': 'Background repeat',
         'select_variable': 'listBackgroundRepeats',
         'visible': 'ifBodyBackgroundImage',
         'default': 'repeat',
         'category': 'box body',
         'i18n': 1,
         'i18n_prefix': '_option_bg_',
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

    security = ClassSecurityInfo()

    def __init__(self, id,
                 BoxTitle_bg_color = '#d0d0d0',
                 BoxTitle_border_color = '#999999',
                 BoxTitle_font_color = 'Black',
                 BoxTitle_bg_image = '',
                 BoxTitle_bg_position = '',
                 BoxTitle_bg_repeat = '',
                 BoxBody_bg_color = '#f3f3f9',
                 BoxBody_bg_image = '',
                 BoxBody_bg_position = '',
                 BoxBody_bg_repeat = '',
                 BoxBody_border_color = '#999999',
                 BoxBody_menuout_color = '#f6f6fc',
                 BoxBody_menuin_color = '#bdd2ee',
                 BoxBody_menuin_border_color = '#669999',
                 BoxBody_menuout_border_color = '#f6f6fc',
                 BoxBody_menuin_icon = '',
                 BoxBody_menuout_icon = '',
                       **kw):
        apply(BaseStyle.__init__, (self, id), kw)
        self.BoxTitle_bg_color = BoxTitle_bg_color
        self.BoxTitle_border_color = BoxTitle_border_color
        self.BoxTitle_bg_image = BoxTitle_bg_image
        self.BoxTitle_bg_position = BoxTitle_bg_position
        self.BoxTitle_bg_repeat = BoxTitle_bg_repeat
        self.BoxTitle_font_color = BoxTitle_font_color
        self.BoxBody_bg_color = BoxBody_bg_color
        self.BoxBody_bg_image = BoxBody_bg_image
        self.BoxBody_bg_position = BoxBody_bg_position
        self.BoxBody_bg_repeat = BoxBody_bg_repeat
        self.BoxBody_border_color = BoxBody_border_color
        self.BoxBody_menuout_color = BoxBody_menuout_color
        self.BoxBody_menuin_color = BoxBody_menuin_color
        self.BoxBody_menuin_border_color = BoxBody_menuin_border_color
        self.BoxBody_menuout_border_color = BoxBody_menuout_border_color
        self.BoxBody_menuin_icon = BoxBody_menuin_icon
        self.BoxBody_menuout_icon = BoxBody_menuout_icon

    security.declarePublic('listBackgroundRepeats')
    def listBackgroundRepeats(self):
        """Return a list of background repeat options"""

        list = ['repeat', 'repeat-x', 'repeat-y', 'no-repeat']
        return list

    security.declarePublic('ifTitleBackgroundImage')
    def ifTitleBackgroundImage(self):
        """Return True is there is a background image in the title"""

        if self.BoxTitle_bg_image:
            return 1
        return None

    security.declarePublic('ifBodyBackgroundImage')
    def ifBodyBackgroundImage(self):
        """Return True is there is a background image in the body"""

        if self.BoxBody_bg_image:
            return 1
        return None

InitializeClass(PortalBoxColor)

def addPortalBoxColor(dispatcher, id, REQUEST=None, **kw):
    """Add a Box Color."""
    ob = PortalBoxColor(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
