# (C) Copyright 2005 Nuxeo SAS <http://nuxeo.com>
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
"""CPSSkins interfaces.
"""

import sys
try:
    from zope.interface import implements
    from zope.interface import Interface
    from OFS.interfaces import IPropertyManager
except ImportError:
    # Zope 3 not available
    if sys.exc_info()[2].tb_next is not None: raise
    def implements(*args): pass
    class Interface(object): pass
    class IPropertyManager(Interface): pass


class IThemeFolder(IPropertyManager):
    """Theme Folder.
    """

class IThemeTool(IThemeFolder):
    """Theme Tool.
    """

class IStyle(IPropertyManager):
    """Base interface for styles.
    """

class IPalette(IPropertyManager):
    """Base interface for palettes.
    """

class ICellModifier(IPropertyManager):
    """Base interface for cell modifiers.
    """

class IPageBlockContent(IPropertyManager):
    """Base interface for page block content (templets).
    """

class IOFSFile(Interface):
    """OFS File interface.
    """
