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
  Document Info Templet
  information about the current document, i.e. its title, the date of last
  modification, the name of the creator, etc.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from BaseTemplet import BaseTemplet

factory_type_information = (
    {'id': 'Document Info Templet',
     'meta_type': 'Document Info Templet',
     'description': ('_documentinfo_templet_description_'),
     'icon': 'documentinfo_templet.gif',
     'product': 'CPSSkins',
     'factory': 'addDocumentInfo',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseTemplet._aliases,
     'actions': BaseTemplet._actions,
    },
)

class DocumentInfo(BaseTemplet):
    """
    Document Info Templet.
    """
    meta_type = 'Document Info Templet'
    portal_type = 'Document Info Templet'

    render_action = 'cpsskins_documentinfo'

    security = ClassSecurityInfo()

    _properties = BaseTemplet._properties + (
        {'id': 'content', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Content', 
         'select_variable': 'ContentList',
         'i18n': 1,
         'i18n_prefix': '_option_docinfo_',
        },
    )

    def __init__(self, id, 
                 content = 'title',
                 **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.content = content

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return 1

    security.declarePublic('getCacheParams')
    def getCacheParams(self):
        """Return a list of cache parameters"
        """
        params = ['lang', 'object:path']
        return params

    security.declarePublic('ContentList')
    def ContentList(self):
        """ Returns a list of styles or layouts for this Templet"""

        list = ['title', 'last_modified', 'created_by']
        return list

InitializeClass(DocumentInfo)

def addDocumentInfo(dispatcher, id, REQUEST=None, **kw):
    """Add a Document Info Templet."""
    ob = DocumentInfo(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
