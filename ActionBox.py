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
  Action Box
  a toolbar containing action buttons with icons.
"""

import md5

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName

from BaseTemplet import BaseTemplet

factory_type_information = (
    {'id': 'Action Box Templet',
     'meta_type': 'Action Box Templet',
     'description': ('_actionbox_templet_description_'),
     'icon': 'actionbox_templet.gif',
     'product': 'CPSSkins',
     'factory': 'addActionBox',
     'immediate_view': 'cpsskins_edit_form',
     'filter_content_types': 0,
     'global_allow': 0,
     'aliases':  BaseTemplet._aliases,
     'actions':  BaseTemplet._actions,
     },
)

class ActionBox(BaseTemplet):
    """
    Action Box Templet.
    """

    meta_type = 'Action Box Templet'
    portal_type = 'Action Box Templet'

    render_action = 'cpsskins_actionbox'

    security = ClassSecurityInfo()

    _properties = BaseTemplet._properties + (
        {'id': 'actions_to_display', 
         'type': 'multiple selection', 
         'mode': 'w', 
         'label': 'Action categories',  
         'select_variable': 'actionIconsList', 
         'category': 'general'
        },
        {'id': 'style', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Appearance', 
         'select_variable': 'StyleList', 
         'category': 'layout',
         'i18n': 1, 
         'i18n_prefix': '_option_',
        },
        {'id': 'orientation', 
         'type': 'selection', 
         'mode': 'w', 
         'label': 'Box orientation', 
         'select_variable': 'OrientationList', 
         'category': 'layout',
         'default': 'vertical',
         'i18n': 1, 
         'i18n_prefix': '_option_',
        },
    )

    def __init__(self, id, 
                 style='text and icons', 
                 actions_to_display=['user:login', 'user:logout'],  
                 orientation = 'horizontal',
                 **kw):
        apply(BaseTemplet.__init__, (self, id), kw)
        self.actions_to_display = actions_to_display
        self.style = style
        self.orientation = orientation

    security.declarePublic('isCacheable')
    def isCacheable(self):
        """Returns true if the Templet can be cached in RAM"""

        return 1

    security.declarePublic('isAlignable')
    def isAlignable(self):
        """Returns true if the Templet can be aligned horizontally"""

        if getattr(self, 'orientation', '') == 'vertical':
            return 1

    security.declarePublic('getCacheParams')
    def getCacheParams(self):
        """Return a list of cache parameters"
        """
        params = ['user', 'actions']
        if self.style in ['text only', 'text and icons']:
            params.append('lang')
        return params

    security.declarePublic('StyleList')
    def StyleList(self):
        """Returns a list of styles or layouts for this Templet"""

        list = ['text only', 
                'text and icons', 
                'icons only']
        return list

    security.declarePublic('OrientationList')
    def OrientationList(self):           
        """Returns a list of orientations for this Templet"""
                                   
        list = [ 'horizontal', 'vertical']
        return list  

    security.declarePublic('actionIconsList')
    def actionIconsList(self):           
        """Returns a list of action icons in category:id format"""

        actions = []
        aitool = getToolByName(self, 'portal_actionicons', None)
        if aitool is None:
            return []

        mtool = getToolByName(self, 'portal_membership')
        if mtool.checkPermission('listActionIcons', aitool):
            actionicons = aitool.listActionIcons()
            for actionicon in actionicons:
                actions.append('%s:%s' % (actionicon.getCategory(), 
                                          actionicon.getActionId()))
        return actions

    security.declarePublic('getActionsIconInfo')
    def getActionsIconInfo(self, REQUEST=None, **kw):           
        """Returns actions icon information"""

        if REQUEST is None:
            return
        atool = getToolByName(self, 'portal_actions')
        tmtool = getToolByName(self, 'portal_themes')

        actions = REQUEST.get('cpsskins_cmfactions', None)
        if actions is None:
            context_obj = kw.get('context_obj')
            actions = atool.listFilteredActionsFor(context_obj)

        actions_to_display = self.actions_to_display
        actionicons = tmtool.getIconsInfo(actions_to_display)
        actionicons_keys = actionicons.keys() 
        actioniconsinfo = []
        actions_has_key = actions.has_key
        for action in actions_to_display:
            if action.find(':') == -1:
                continue
            category, action_id = action.split(':')
            if (category, action_id) in actionicons_keys:
                action_icon = actionicons[category, action_id]
            else:
                action_icon = None
            if actions_has_key(category):
                for ac in actions[category]:
                    if ac.get('id') == action_id:
                        actioniconsinfo.append( 
                            {'url': ac.get('url'),
                             'title': ac.get('name'),
                             'action_icon': action_icon,
                            }
                        )
                        break
        return actioniconsinfo

InitializeClass(ActionBox)

def addActionBox(dispatcher, id, REQUEST=None, **kw):
    """Add an Action Box Templet."""
    ob = ActionBox(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
