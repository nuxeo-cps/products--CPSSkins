# (C) Copyright 2004 Chalmers University Of Technology <http://www.chalmers.se>
# Author: Jean-Marc Orliaguet <jmo@ita.chalmers.se>
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
  CPSSkins Permissions
  - 'Manage Themes' : Permission to manage themes
"""

try:
    from Products.CMFCore.permissions import setDefaultRoles
except ImportError:
    from Products.CMFCore.CMFCorePermissions import setDefaultRoles

ManageThemes = 'Manage Themes'
setDefaultRoles(ManageThemes, ('Manager', 'Owner', 'ThemeManager'))

