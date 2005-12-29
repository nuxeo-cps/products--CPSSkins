# Copyright (c) 2005 Nuxeo SAS <http://nuxeo.com>
# Author: Florent Guillaume <fg@nuxeo.com>
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
# $Id$
"""GenericSetup-based I/O for themes.
"""

from Acquisition import aq_base
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import BodyAdapterBase
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.utils import ObjectManagerHelpers
from Products.GenericSetup.utils import PropertyManagerHelpers

from zope.component import adapts
from zope.interface import implements
from Products.GenericSetup.interfaces import INode
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.interfaces import IFilesystemExporter
from Products.GenericSetup.interfaces import IFilesystemImporter
from Products.CPSSkins.interfaces import IThemeTool
from Products.CPSSkins.interfaces import IOFSFile
from OFS.interfaces import IPropertyManager


TOOL = 'portal_themes'
NAME = 'themes'

def exportThemeTool(context):
    """Export Theme tool and vocabularies as a set of XML files.
    """
    site = context.getSite()
    tool = getToolByName(site, TOOL, None)
    if tool is None:
        logger = context.getLogger(NAME)
        logger.info("Nothing to export.")
        return
    exportObjects(tool, '', context)

def importThemeTool(context):
    """Import Theme tool and vocabularies from XML files.
    """
    site = context.getSite()
    tool = getToolByName(site, TOOL)
    importObjects(tool, '', context)


class ThemeToolXMLAdapter(XMLAdapterBase, ObjectManagerHelpers,
                          PropertyManagerHelpers):
    """XML importer and exporter for Theme tool.
    """

    adapts(IThemeTool, ISetupEnviron)
    implements(IBody)

    _LOGGER_ID = NAME
    name = NAME

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('object')
        node.appendChild(self._extractToolProperties())
        node.appendChild(self._extractObjects())
        self._logger.info("Theme tool exported.")
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        if self.environ.shouldPurge():
            self._purgeToolProperties()
            self._purgeObjects()
        self._initToolProperties(node)
        self._initObjects(node)
        self._logger.info("Theme tool imported.")

    def _extractToolProperties(self):
        tmtool = self.context
        fragment = self._doc.createDocumentFragment()

        child = self._doc.createElement('property')
        child.setAttribute('name', 'accesskey')
        text = self._doc.createTextNode(tmtool.getAccessKey())
        child.appendChild(text)
        fragment.appendChild(child)

        child = self._doc.createElement('property')
        child.setAttribute('name', 'debug_mode')
        text = self._doc.createTextNode(str(bool(tmtool.debug_mode)))
        child.appendChild(text)
        fragment.appendChild(child)

        # TODO: external themes, method themes

        return fragment

    def _purgeToolProperties(self):
        # TODO: purge external themes, method themes
        return

    def _initToolProperties(self, node):
        tmtool = self.context
        for child in node.childNodes:
            if child.nodeName != 'property':
                continue
            name = child.getAttribute('name')
            value = self._getNodeText(child)
            if name == 'accesskey':
                tmtool.manage_setAccessKey(value)
            elif name == 'debug_mode':
                tmtool.debug_mode = self._convertToBoolean(value)

        # TODO: external themes, method themes


class PropertyManagerXMLAdapter(XMLAdapterBase, ObjectManagerHelpers,
                                PropertyManagerHelpers):
    """XML importer and exporter for a property-based object.

    This also adapts subobjects.
    """

    adapts(IPropertyManager, ISetupEnviron) # adapts many things
    implements(IBody)

    _LOGGER_ID = NAME

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('object')
        node.appendChild(self._extractProperties())
        node.appendChild(self._extractObjects())
        ob = self.context
        self._logger.info("%s %r exported." % (ob.meta_type, ob.getId()))
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        if self.environ.shouldPurge():
            self._purgeProperties()
            self._purgeObjects()
        self._initProperties(node)
        self._initObjects(node)
        ob = self.context
        self._logger.info("%s %r imported." % (ob.meta_type, ob.getId()))


class FileBodyAdapter(BodyAdapterBase):
    """Body exporter/importer for files or images.
    """

    adapts(IOFSFile, ISetupEnviron)
    implements(IBody)

    _LOGGER_ID = 'file'

    def __init__(self, context, environ):
        super(FileBodyAdapter, self).__init__(context, environ)
        # Used during export
        self.mime_type = self.context.getContentType()

    def _exportBody(self):
        """Export the object as a file body.
        """
        ob = self.context
        self._logger.info("%s %r exported." % (ob.__class__.__name__,
                                               ob.getId()))
        return str(ob.data)

    def _importBody(self, body):
        """Import the object from the file body.
        """
        ob = self.context
        ob.manage_upload(body)
        self._logger.info("%s %r imported." % (ob.__class__.__name__,
                                               ob.getId()))

    body = property(_exportBody, _importBody)
