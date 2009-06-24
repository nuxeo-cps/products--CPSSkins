# (C) Copyright 2008 Georges Racinet
# Author: Georges Racinet <georges@racinet.fr>
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
"""Common utilities for exports intended for CPS Designer Themes."""

from Products.CPSPortlets.DummyPortlet import DummyPortlet

DESIGNER_THEMES_EXPORT_PORTLET = DummyPortlet(
    'the_id',
    '<div cps:remove="True" cps:portlet="body">Here is the portlet body</div>',
    title='<span cps:remove="True" cps:portlet="title">portlet title</span>')

def is_cps_designer_themes_export(context):
    """Is the current rendering an export for CPS Designer Themes ?"""
    return bool(context.REQUEST.get('_cpsskins_designer_export'))

