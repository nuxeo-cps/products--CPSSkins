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
  Calendar Style
  this style defines the calendar's visual appearance.  
"""

from Globals import InitializeClass

from BaseStyle import BaseStyle

factory_type_information = (
    {'id': 'Calendar Style',
     'meta_type': 'Calendar Style',
     'description': ('_calendarstyle_description_'),
     'icon': 'calendar_style.png',
     'product': 'CPSSkins',
     'factory': 'addCalendarStyle',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases': BaseStyle._aliases,
     'actions': BaseStyle._actions,
    },
)

class CalendarStyle(BaseStyle):
    """
    Calendar Style.
    """
    meta_type = 'Calendar Style'
    portal_type = 'Calendar Style'

    render_action = 'cpsskins_calendarstyle'
    preview_action = 'cpsskins_calendarstyle_preview'

    _properties = BaseStyle._properties + (
        {'id': 'Header_bg_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Header background color', 
         'category' : 'colors',
         'palette': 'Palette Color'
        },
        {'id': 'Header_font_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Header font color', 
         'category' : 'colors',
         'palette': 'Palette Color'
        },
        {'id': 'Weekdays_border_color',  
         'type': 'string', 
         'mode': 'w', 
         'label': 'Weekdays border color', 
         'category' : 'colors',
         'palette': 'Palette Color'
        },
        {'id': 'Weekdays_bg_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Weekdays background color', 
         'category' : 'colors',
         'palette': 'Palette Color'
        },
        {'id': 'Weekdays_font_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Weekdays font color', 
         'category' : 'colors',
         'palette': 'Palette Color'
        },
        {'id': 'Days_bg_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Days background color', 
         'category' : 'colors',
         'palette': 'Palette Color'
        },
        {'id': 'Days_font_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Days font color', 
         'category' : 'colors',
         'palette': 'Palette Color'
        },
        {'id': 'Event_border_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Event border color', 
         'category' : 'colors',
         'palette': 'Palette Color'
        },
        {'id': 'Event_bg_color', 
         'type': 'string',  
         'mode': 'w', 
         'label': 'Event background color', 
         'category' : 'colors',
         'palette': 'Palette Color'
        },
        {'id': 'Event_font_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Event font color', 
         'category' : 'colors',
         'palette': 'Palette Color'
        },
        {'id': 'Today_border_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Today border color', 
         'category' : 'colors',
         'palette': 'Palette Color'
        },
        {'id': 'Preview_border_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Preview border color', 
         'category' : 'colors',
         'palette': 'Palette Color'
        },
        {'id': 'Preview_bg_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Preview background color', 
         'category' : 'colors',
         'palette': 'Palette Color'
        },
        {'id': 'Preview_font_color', 
         'type': 'string', 
         'mode': 'w', 
         'label': 'Preview font color', 
         'category' : 'colors',
         'palette': 'Palette Color'
        },
    )

    def __init__(self, id, 
                 Weekdays_border_color = '#999999',
                 Header_bg_color = '#e9e9e9',
                 Header_font_color = '#000000',
                 Weekdays_bg_color = '#d0d0d0',
                 Weekdays_font_color = '#000000',
                 Days_bg_color = '#ffffff',
                 Days_font_color = '#000000',
                 Event_bg_color = '#f0f0c0',
                 Event_font_color = '#000066',
                 Event_border_color = '#999999',
                 Preview_bg_color = '#ffffbb',
                 Preview_font_color = '#000000',
                 Preview_border_color = '#000000',
                 Today_border_color = '#ffa500',
                 **kw):
        apply(BaseStyle.__init__, (self, id), kw)
        self.Weekdays_border_color = Weekdays_border_color
        self.Header_bg_color = Header_bg_color
        self.Header_font_color = Header_font_color
        self.Weekdays_bg_color = Weekdays_bg_color
        self.Weekdays_font_color = Weekdays_font_color
        self.Days_bg_color = Days_bg_color
        self.Days_font_color = Days_font_color
        self.Event_border_color = Event_border_color
        self.Event_bg_color = Event_bg_color
        self.Event_font_color = Event_font_color
        self.Preview_border_color = Preview_border_color
        self.Preview_bg_color = Preview_bg_color
        self.Preview_font_color = Preview_font_color
        self.Today_border_color = Today_border_color

InitializeClass(CalendarStyle)

def addCalendarStyle(dispatcher, id, REQUEST=None, **kw):
    """Add a Calendar Style."""
    ob = CalendarStyle(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
