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
  Palette Border
  these palettes define the border shapes used in the styles.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BasePalette import BasePalette

factory_type_information = (
    {'id': 'Palette Border',
     'meta_type': 'Palette Border',
     'description': ('_paletteborder_description_'),
     'icon': 'palette_border.png',
     'product': 'CPSSkins',
     'factory': 'addPaletteBorder',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BasePalette._aliases,
     'actions': BasePalette._actions,
    },
)

class PaletteBorder(BasePalette):
    """
    Palette Border.
    """
    meta_type = 'Palette Border'
    portal_type = 'Palette Border'

    preview_method = 'cpsskins_paletteborder_preview'

    security = ClassSecurityInfo()

    _properties = BasePalette._properties + (
        {'id': 'value',
         'type': 'string',
         'mode': 'w',
         'label': 'Border style'
        },
    )

    def __init__(self, id,
                       value = 'solid solid solid solid',
                       **kw):

        apply(BasePalette.__init__, (self, id), kw)
        self.value = value

InitializeClass(PaletteBorder)

def addPaletteBorder(dispatcher, id, REQUEST=None, **kw):
    """Add an Palette Border."""
    ob = PaletteBorder(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
