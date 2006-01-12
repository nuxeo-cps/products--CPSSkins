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
# YoU should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#

__author__ = "Jean-Marc Orliaguet <jmo@ita.chalmers.se>"

"""
  ImageBox Templet
  an image with a link and a caption.
"""

from Globals import InitializeClass
from Acquisition import aq_base
from AccessControl import ClassSecurityInfo
from OFS.PropertyManager import PropertyManager
from OFS.Image import Image
from OFS.Cache import Cacheable

from BaseTemplet import BaseTemplet
from ThemeFolder import ThemeFolder
from CPSSkinsPermissions import ManageThemes

factory_type_information = (
    {'id': 'Image Box Templet',
     'description': ('_imagebox_templet_description_'),
     'meta_type': 'Image Box Templet',
     'icon': 'imagebox_templet.png',
     'product': 'CPSSkins',
     'factory': 'addImageBox',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseTemplet._aliases,
     'actions': BaseTemplet._actions,
    },
)

# BBB: Image base class should go away at some point
class ImageBox(ThemeFolder, Image, BaseTemplet):
    """
    Image Box Templet.
    """
    meta_type = 'Image Box Templet'
    portal_type = 'Image Box Templet'

    render_method = 'cpsskins_imagebox'

    security = ClassSecurityInfo()

    manage_options = ( PropertyManager.manage_options     # Properties
                     + ( {'label': 'Preview',
                          'action': 'manage_templetPreview'}, )
                     ) + Cacheable.manage_options

    _properties = BaseTemplet._properties + (
        {'id': 'i18n',
         'type': 'boolean',
         'mode': 'w',
         'label': 'Translate the image',
         'default': 0,
        },
        {'id': 'caption',
         'type': 'string',
         'mode': 'w',
         'label': 'Image caption',
        },
        {'id': 'link',
         'type': 'string',
         'mode': 'w',
         'label': 'Link (http://, mailto: ...)',
        },
        {'id': 'use_internal_link',
         'type': 'boolean',
         'mode': 'w',
         'label': 'Use internal link?',
         'default': 0,
        },
        {'id': 'internal_link',
         'type': 'selection',
         'mode': 'w',
         'label': 'Internal link',
         'select_variable': 'cpsskins_listPaths',
         'visible': 'ifUseInternalLink',
        },
        )

    def __init__(self, id,
                 title = '',
                 i18n = 0,
                 caption = '',
                 link = '',
                 internal_link = '',
                 use_internal_link = 0,
                 file = '',
                 **kw) :
        Image.__init__(self, id, '', '')
        self.upload_image(file=file)
        BaseTemplet.__init__(self, id, title, **kw)
        self.i18n = i18n
        self.caption = caption
        self.link = link
        self.internal_link = internal_link
        self.use_internal_link = use_internal_link

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return 1

    security.declarePublic('isPortalTemplet')
    def isPortalTemplet(self):
        """ is portal templet """

        return self.isportaltemplet

    security.declarePublic('isImageBox')
    def isImageBox(self):
        """ Templet is an image box """

        return 1

    #
    # Properties
    #
    security.declarePublic('getI18nProperties')
    def getI18nProperties(self):
        """ Returns the list of i18n properties """

        return ['i18n']
    #
    # RAM Cache
    #
    security.declarePublic('getCacheParams')
    def getCacheParams(self):
        """Return a list of cache parameters
        """

        params = ['baseurl']
        if self.i18n:
            params.append('lang')
        return params

    security.declareProtected(ManageThemes, 'upload_image')
    def upload_image(self, REQUEST=None, **kw):
        """
        Uploads the image
        If the i18n attribute is set the image will be uploaded
        inside this folder and be called 'i18n_image_xx' where 'xx'
        is the 2-letter language code.
        """

        if REQUEST is not None:
            kw.update(REQUEST.form)
        file = kw.get('file', None)
        if not file or not file.filename:
            return

        if not getattr(self, 'i18n', 0):
            self.data = '' # BBB: clear old data
            img_id = 'image'
        else:
            lang_id = self.getDefaultLang()
            if lang_id is None:
                return
            img_id = 'i18n_image_%s' % lang_id

        if img_id in self.objectIds():
            self.manage_delObjects(img_id)
        img = Image(img_id, '', '')
        self._setObject(img_id, img)
        img = self._getOb(img_id)
        img.manage_upload(file)

        self.expireCache()

        if REQUEST is not None:
            url = self.absolute_url()
            REQUEST.RESPONSE.redirect(url + '/edit_form?portal_status_message=psm_image_uploaded')

    def index_html(self, REQUEST, RESPONSE):
        """Download the image as binary with headers.
        """
        if self.data != '':
            # BBB: image used to be stored in self (we inherit from Image)
            img = self
        else:
            img = self.image
        return Image.index_html(img, REQUEST, RESPONSE)

    security.declarePublic('getI18nImages')
    def getI18nImages(self):
        """Returns the internationalized images
           {id: <Image>, ...}
        """

        images = {}
        for obj in self.objectValues(('Portal Image', 'Image')):
            obj_id = obj.getId()
            if obj_id.startswith('i18n_image_'):
                images[obj_id] = obj
        return images

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
        self.ZCacheable_invalidate()
        self.expireCache()

    security.declarePublic('ifUseInternalLink')
    def ifUseInternalLink(self):
        """
        True if the 'use internal link' option is set
        """

        return getattr(self, 'use_internal_link', 0)

InitializeClass(ImageBox)

def addImageBox(dispatcher, id, REQUEST=None, **kw):
    """Add an Image Box Templet."""

    ob = ImageBox(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
