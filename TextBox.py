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
  Text Box Templet
  a box that displays plain text or HTML.
"""

from cgi import escape

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.PythonScripts.standard import structured_text, newline_to_br
try: 
    from Products.PythonScripts.standard \
    import restructured_text as structured_text
except ImportError:
    pass

from BaseTemplet import BaseTemplet

factory_type_information = (
    {'id': 'Text Box Templet',
     'meta_type': 'Text Box Templet',
     'description': ('_textbox_templet_description_'),
     'icon': 'textbox_templet.png',
     'product': 'CPSSkins',
     'factory': 'addTextBox',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseTemplet._aliases,
     'actions': BaseTemplet._actions,
    },
)

class TextBox(BaseTemplet):
    """
    Text Box Templet.
    """
    meta_type = 'Text Box Templet'
    portal_type = 'Text Box Templet'

    render_method = 'cpsskins_textbox'

    security = ClassSecurityInfo()

    _properties = BaseTemplet._properties + (
        {'id': 'text',
         'type': 'text',
         'mode': 'w',
         'label': 'Your text',
        },
        {'id': 'text_format',
         'type': 'selection',
         'mode': 'w',
         'label': 'Text format',
         'select_variable': 'listTextFormats',
         'default': 'html',
         'i18n': 1,
         'i18n_prefix': '_option_',
        },
        {'id': 'i18n',
         'type': 'boolean',
         'mode': 'w',
         'label': 'Translate the text',
         'default': 0,
        },
      )

    def __init__(self, id,
                 text='Your text here',
                 text_format='html',
                 i18n = 0,
                 **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.text = text
        self.text_format = text_format
        self.i18n = i18n

    security.declarePublic('render_text_as')
    def render_text_as(self, text='', fmt=None):
        """ render the text as structured text / plain text / HTML (default) """
        if fmt == 'stx':
            text = structured_text(text)
        if fmt == 'plain text':
            text = newline_to_br(escape(text))
        return text

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return 1

    security.declarePublic('getCacheParams')
    def getCacheParams(self):
        """Return a list of cache parameters"
        """

        params = []
        if self.i18n:
            params.append('lang')
        return params

    security.declarePublic('listTextFormats')
    def listTextFormats(self):
        """ return a list of render formats (stx, plain, html) """

        return ['html', 'plain text', 'stx']

    security.declarePublic('getI18nProperties')
    def getI18nProperties(self):
        """ Returns the list of i18n properties """

        return ['i18n']

InitializeClass(TextBox)

def addTextBox(dispatcher, id, REQUEST=None, **kw):
    """Add a Text Box Templet."""
    ob = TextBox(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
