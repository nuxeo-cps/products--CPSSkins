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
  Calendar Templet
  a calendar with monthly events.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName

from BaseTemplet import BaseTemplet
from cpsskins_utils import getStyleList

factory_type_information = (
    {'id': 'Calendar Templet',
     'meta_type': 'Calendar Templet',
     'description': ('_calendar_templet_description_'),
     'icon': 'calendar_templet.gif',
     'product': 'CPSSkins',
     'factory': 'addCalendar',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseTemplet._aliases,
     'actions': BaseTemplet._actions,
    },
)

class Calendar(BaseTemplet):
    """
    Calendar Templet.
    """
    meta_type = 'Calendar Templet'
    portal_type = 'Calendar Templet'

    render_action = 'cpsskins_calendar'
    javascript_render_action = 'cpsskins_calendar.js'

    security = ClassSecurityInfo()

    _properties = BaseTemplet._properties + (
       {'id': 'show_month', 
        'type': 'boolean', 
        'mode': 'w', 
        'label': 'Show month', 
        'category': 'general',
        'default': 1
       },
       {'id': 'show_year', 
        'type': 'boolean', 
        'mode': 'w', 
        'label': 'Show year', 
        'category' : 'general',
        'default': 1
       },
       {'id': 'show_weekdays', 
        'type': 'boolean', 
        'mode': 'w', 
        'label': 'Show weekdays', 
        'category' : 'general',
        'default': 1
       },
       {'id': 'show_preview', 
        'type': 'boolean', 
        'mode': 'w', 
        'label': 'Show preview', 
        'category' : 'general',
        'default': 1
       },
       {'id': 'calendar_style', 
        'type': 'selection', 
        'mode': 'w', 
        'label': 'Calendar Style', 
        'select_variable': 'CalendarStylesList', 
        'category': 'style',
        'style': 'Calendar Style'
       },
    )

    def __init__(self, id, 
                       show_month = 1,
                       show_year = 1,
                       show_weekdays = 1,
                       show_preview = 1,
                       calendar_style = '',
                       **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.show_month = show_month
        self.show_year = show_year
        self.show_weekdays = show_weekdays
        self.show_preview = show_preview
        self.calendar_style = calendar_style

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """ Returns true if the Templet can be cached in RAM """

        return 1

    security.declarePublic('isAlignable')
    def isAlignable(self):
        """ Returns true if the Templet can be aligned horizontally """

        return None

    security.declarePublic('getCacheIndex')
    def getCacheIndex(self, REQUEST=None):
        """ returns the RAM cache index as a tuple (var1, var2, ...) """
       
        index = ()
        if REQUEST is None:
            REQUEST = self.REQUEST

        index += (REQUEST.get('cpsskins_language', 'en'), )

        portal_calendar = getToolByName(self, 'portal_calendar', None)
        if portal_calendar is None:
            return index

        year  = REQUEST.get('year',  None)
        month = REQUEST.get('month', None)
        if portal_calendar.getUseSession() == "True":
            session = REQUEST.get('SESSION', None)
            if session:
                if not year:   
                    year  = session.get('calendar_year',  None)
                if not month:  
                    month = session.get('calendar_month', None)
        if year:
            index += (year, )
        if month:
            index += (month, )

        index += (str(REQUEST.get('AUTHENTICATED_USER')), )
        return index

    security.declarePublic('CalendarStylesList')
    def CalendarStylesList(self):           
        """ Returns a list of Calendar styles"""

        return getStyleList(self, 'Calendar Style')

InitializeClass(Calendar)

def addCalendar(dispatcher, id, REQUEST=None, **kw):
    """Add an Calendar Templet."""
    ob = Calendar(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
