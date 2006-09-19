# Copyright (c) 2006 Nuxeo SAS
# Authors: G. Racinet <gracinet@nuxeo.com>
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

import logging
from StringIO import StringIO

from OFS.interfaces import IObjectManager

logger = logging.getLogger('CPSSkins.upgrade')

def update_flash(container, flashbox):
    if flashbox.hasObject('flash_file'):
        logger.info('  nothing to do')
        return
    
    flash = StringIO(flashbox.data)
    flash.filename = 'flash.swf' # required
    flashbox.manage_upload(file=flash,
                           content_type='application/x-shockwave-flash')
    

def update_image(container, imagebox):
   if not getattr(imagebox, 'i18n', 0):
       img_id = 'image'
   else:
       lang_id = self.getDefaultLang()
       if lang_id is None:
           logger.warn('ImageBox pretends to be i18n but has no default lang')
       img_id = 'i18n_image_%s' % lang_id
       logger.info(' subobject id: %s', img_id)

   if imagebox.hasObject(img_id):
       logger.info('  nothing to do')
       return
    
   image = StringIO(imagebox.data)
   image.filename = 'image'
   imagebox.upload_image(file=image)
    

def treeCrawl(start, actions):
    subs = []
    for ob in start.objectValues():
        if IObjectManager.providedBy(ob):
            subs.append(ob)
        action = actions.get(ob.meta_type)
        if action is not None:
            logger.info('Upgrading %s', ob.absolute_url())
            action(start, ob)
            
    for sub in subs:
        treeCrawl(sub, actions)

def upgrade_342_343_flash_image(portal):
    thtool = getattr(portal, 'portal_themes', None)
    if thtool is None:
        # happens while upgrading from pre-CPSSkins CPS instances
        logger.info('No existing Themes Tool')
        return
    treeCrawl(thtool, {'Flash Box Templet': update_flash,
                       'Image Box Templet': update_image})
