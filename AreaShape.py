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
  Area Shape
  this style defines the border style and thickness of an area.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BaseStyle import BaseStyle

factory_type_information = (
    {'id': 'Area Shape',
     'meta_type': 'Area Shape',
     'description': ('_areashape_description_'),
     'icon': 'area_shape.png',
     'product': 'CPSSkins',
     'factory': 'addAreaShape',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseStyle._aliases,
     'actions': BaseStyle._actions,
    },
)

class AreaShape(BaseStyle):
    """Area Shape."""

    meta_type = 'Area Shape'
    portal_type = 'Area Shape'

    render_method = 'cpsskins_areashape'
    preview_method = 'cpsskins_areashape_preview'

    security = ClassSecurityInfo()

    _properties = BaseStyle._properties + (
        {'id': 'Area_border_style',
         'type': 'string',
         'mode': 'w',
         'label': 'Area border style',
         'palette': 'Palette Border',
        },
        {'id': 'Area_border_width',
         'type': 'string',
         'mode': 'w',
         'label': 'Area border width',
        },
        {'id': 'Area_text_transform',
         'type': 'selection',
         'mode': 'w',
         'label': 'Area text transform',
         'select_variable': 'listTextTransforms',
         'default': 'none',
         'i18n': 1,
         'i18n_prefix': '_option_text_transform_',
        },
    )

    def __init__(self, id,
                 Area_border_style = 'solid',
                 Area_border_width = '1px',
                 Area_text_transform = 'none',
                 **kw):

        apply(BaseStyle.__init__, (self, id), kw)
        self.Area_border_style = Area_border_style
        self.Area_border_width = Area_border_width
        self.Area_text_transform = Area_text_transform

    security.declarePublic('listTextTransforms')
    def listTextTransforms(self):
        """Return a list of text transformations"""

        list = ['none', 'capitalize', 'uppercase', 'lowercase']
        return list

InitializeClass(AreaShape)

def addAreaShape(dispatcher, id, REQUEST=None, **kw):
    """Add an Area Shape."""
    ob = AreaShape(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
