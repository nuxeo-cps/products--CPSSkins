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
# YoU should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#

__author__ = "Jean-Marc Orliaguet <jmo@ita.chalmers.se>"

"""
  FlashBox Templet
  a Macromedia Flash(tm) box with a caption.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CMFDefault.File import File

from CPSSkinsPermissions import ManageThemes
from BaseTemplet import BaseTemplet

from swfHeaderData import analyseContent

factory_type_information = (
    {'id': 'Flash Box Templet',
     'meta_type': 'Flash Box Templet',
     'description': ('_flashbox_templet_description_'),
     'icon': 'flashbox_templet.png',
     'product': 'CPSSkins',
     'factory': 'addFlashBox',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseTemplet._aliases,
     'actions': BaseTemplet._actions,
    },
)

class FlashBox(File, BaseTemplet):
    """
    Flash Box Templet.
    """
    meta_type = 'Flash Box Templet'
    portal_type = 'Flash Box Templet'

    render_method = 'cpsskins_flashbox'

    security = ClassSecurityInfo()
    manage_options = File.manage_options

    _properties = BaseTemplet._properties + (
        {'id': 'caption',
         'type': 'string',
         'mode': 'w',
         'label': 'Flash caption',
         'category': 'general'
        },
        {'id': 'flash_width',
         'type': 'int',
         'mode': 'w',
         'label': 'Flash movie width',
         'category': 'layout'
        },
        {'id': 'flash_height',
         'type': 'int',
         'mode': 'w',
         'label': 'Flash movie height',
         'category': 'layout'
        },
    )

    def __init__(self, id, title,
                       caption = '',
                       flash_width = 0,
                       flash_height = 0,
                       file = '',
                       content_type = '',
                       precondition = '',
                       subject=(),
                       description='',
                       contributors=(),
                       effective_date=None,
                       expiration_date=None,
                       format='application/x-shockwave-flash',
                       language='',
                       rights='',
                       **kw):
        apply(File.__init__,
                (self, id, title,
                 file, content_type, precondition, subject, description,
                 contributors, effective_date, expiration_date,
                 format, language, rights))
        apply(BaseTemplet.__init__, (self, id), kw)
        self.caption = caption
        self.flash_width = flash_width
        self.flash_height = flash_height

    security.declarePublic('isFlashBox')
    def isFlashBox(self):
        """ Templet is portal flash box """

        return 1

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return 1

    security.declarePublic('getCacheParams')
    def getCacheParams(self):
        """Return a list of cache parameters"
        """
        return []

    security.declareProtected(ManageThemes, 'manage_upload')
    def manage_upload(self, file='', content_type=''):

        data, size = self._read_data(file)
        content_type = self._get_content_type(file, data, id, content_type)
        self.update_data(data, content_type, size)
        file.seek(0)
        data = file.read()
        filesize = len(data)
        analysed = analyseContent(data,filesize)
        self.flash_height = analysed['height']
        self.flash_width = analysed['width']

    security.declareProtected(ManageThemes, 'edit')
    def edit(self, **kw):
        """
        Default edit method, changes the properties.
        """

        # remove unknown properties
        for prop in kw.keys():
            if self.hasProperty(prop):
                continue
            del kw[prop]

        self.manage_changeProperties(**kw)

InitializeClass(FlashBox)

def addFlashBox(dispatcher, id, REQUEST=None, **kw):
    """Add an Flash Box Templet."""

    ob = FlashBox(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
