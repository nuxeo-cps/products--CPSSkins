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

""" CPSSkins utilities """

import re
import random

from DateTime import DateTime
from Acquisition import  aq_base

from Products.CMFCore.CMFCorePermissions import View, AccessContentsInformation
from CPSSkinsPermissions import ManageThemes

from Products.CMFCore.utils import getToolByName, _getViewFor

def rebuild_properties(obj):
    """ This method rebuilds an object's property map (_properties) and
        to keep the property values up to date with the current property
        definition.

        If an unknown property field is found the method
        will look for a dictionary item called 'default' and the
        property value will be filled with the value of 'default'.

        Otherwise the property value will be reset to '' or 0 depending
        on its type.
    """

    prop_ids = obj.propertyIds()
    prop_maps = obj.propertyMap()
    #
    # Rebuild property maps
    #
    for prop_map in prop_maps:
        for prop in obj._properties:
            if prop['id'] == prop_map['id']:
                prop = prop_map.copy()

    #
    # Rebuild properties
    #
    new_prop_dict = {}
    new_prop_ids = []
    for prop_id in prop_ids:
        try:
            prop_value = obj.getProperty(prop_id)
        except AttributeError:
            prop_value = None
        else:
            continue

        if prop_value is None:
            #
            # Look for a default value ('default' in the _properties dictionary)
            #
            default_value = None
            for prop_map in prop_maps:
                if prop_id == prop_map['id']:
                    default_value = prop_map.get('default', None)
                    break

            if default_value is not None:
                prop_value = default_value
            else:
                prop_type = obj.getPropertyType(prop_id)
                if prop_type in ['int', 'boolean']:
                    prop_value = 0

                if prop_type in ['lines', 'string', 'text', \
                                 'selection', 'multiple selection']:
                    prop_value = ''

        if prop_value is not None and not hasattr(prop_value, 'aq_base'):
            new_prop_dict[prop_id] = prop_value

    if len(new_prop_dict) > 0:
        obj.manage_changeProperties(**new_prop_dict)
    return 1

def callAction(self, actionid, **kw):
    """
    Call the given action.
    """

    action = _getViewFor(self, view=actionid)
    if action and callable(action):
        return apply(action, (), kw)


def renderMeth(self, render_variable, **kw):
    """Renders a method (the value of 'render_variable')"""

    rendered = None
    actionid = getattr(self.aq_explicit, render_variable, None)
    if actionid is None:
        return
    meth = getattr(self, actionid, None)
    if meth is not None:
        if getattr(aq_base(meth), 'isDocTemp', 0):
            rendered = apply(meth, (self, self.REQUEST), kw)
        else:
            rendered = apply(meth, (), kw)
    return rendered


def getFreeId(container=None, try_id=None):
    """ This method looks for a free object id in the current folder
        and returns an id.
    """

    if container is None:
        return None

    ids = container.objectIds()
    if try_id is not None:
        if not try_id in ids:
            return try_id
    while 1:
        randomid = str(random.randrange(1, 2147483600))
        if not randomid in ids:
            break
    return randomid


def getFreeTitle(container=None, title='Noname'):
    """ This method looks for a free object title in a container
        and returns a title.

        If a title is passed as a parameter, the method will check first
        if the title is free.

        Otherwise a figure (1, 2, ...) will be added to the title
        until a free title is found.
    """

    if container is None:
        return None

    titles = [getattr(obj, 'title', None) for obj in container.objectValues()]

    new_title = title
    i = 0
    while 1:
        if titles is None:
            break
        if new_title not in titles:
            break
        i = i + 1
        new_title = title + str(i)
    return new_title

def canonizeStyleTitle(title=''):
    """ This method canonizes a CSS class title so that it can be used
        in a CSS file.
    """

    newtitle = ''
    for i in range(len(title)):
        character = title[i]
        if character.isalnum():
            newtitle += character
    return newtitle

def canonizeId(self):
    """ This method canonizes a Zope Id
    """

    current_id = self.getId()
    new_id = ''
    for i in range(len(current_id)):
        character = current_id[i]
        if character.isalnum() or character in ['_', '-']:
            new_id += character

    if new_id.startswith('copy_of_'):
        new_id = new_id[len('copy_of_'):]

    if new_id != current_id:
        container = self.aq_parent
        new_id = getFreeId(container)
        container.manage_renameObject(current_id, new_id)

def verifyThemePerms(self):
    """ This method sets the correct permissions on an object
        belonging to a theme.
    """

    self.manage_permission(ManageThemes, [], acquire=1)
    self.manage_permission(View, [], acquire=1)
    self.manage_permission(AccessContentsInformation, [], acquire=1)

def detectPortalType(self):
    """ This methods attempts to detect the portal type
    """

    portal_type = 'CMF'
    utool = getToolByName(self, 'portal_url')
    portal = utool.getPortalObject()
    meta_type = portal.meta_type

    # CPS2
    if getToolByName(self, 'portal_hierarchies', None) is not None:
        return 'CPS2'

    # CPS3
    cps_version = getattr(portal, 'cps_version', '')
    if cps_version.startswith('CPS3'):
        return 'CPS3'

    if meta_type == 'CPSDefault Site':
        return 'CPS3'

    # Plone
    migrationtool = getToolByName(self, 'portal_migration', None)
    if migrationtool is not None:
        version = migrationtool.getInstanceVersion()
        if version.startswith('2'):
            return 'Plone2'
        if version.startswith('1'):
            return 'Plone'

    return portal_type


def getObjectVisibility(self, REQUEST):
    """ Return 1 if the object if visible """

    lang_list = self.languages
    utool = getToolByName(self, 'portal_url')
    if lang_list:
        portal = utool.getPortalObject()
        if 'Localizer' in portal.objectIds():
            lctool = portal.Localizer
        else:
            lctool = getToolByName(self, 'portal_messages', None)
        if lctool is None:
            return None
        selected_language = lctool.get_selected_language()
        if selected_language not in lang_list:
            return None

    visibility = self.visibility
    if visibility == 'always':
        return 1

    if visibility == 'if_authenticated':
        mtool = getToolByName(self, 'portal_membership')
        if not mtool.isAnonymousUser():
           return 1

    if visibility == 'if_anonymous':
        mtool = getToolByName(self, 'portal_membership')
        if mtool.isAnonymousUser():
            return 1

    if visibility == 'time_limited':
        now = DateTime()
        effective_date = self.EffectiveDate()
        expiration_date = self.ExpirationDate()
        if effective_date != 'None':
           if now < DateTime(effective_date):
              return None
        if expiration_date != 'None':
           if now >= DateTime(expiration_date):
              return None
        return 1

    if visibility in ['only_in', 'everywhere_except_in', \
                      'starting_from', 'up_till']:
        if REQUEST is None:
            return None

        portal_url = utool(relative=0)

        url = None
        # simulated URL
        rurl = REQUEST.form.get('sim_url', None)
        if rurl:
            url = rurl

        # real URL
        if rurl is None:
            url_obj = REQUEST.get('context_obj', None)
            if url_obj is not None:
                url = utool.getRelativeContentURL(url_obj)
                if url:
                    url = '/' + url + '/'
                else:
                    url = '/'

        if url is None:
            return None

        url_path = url
        paths = [(p == '/' and '' or p) for p in self.visibility_paths]

        if visibility == 'only_in':
            if url_path in paths:
                return 1

        if visibility == 'everywhere_except_in':
            if url_path not in paths:
                return 1

        if visibility == 'starting_from':
            for p in paths:
                if url_path.startswith(p):
                    return 1

        if visibility == 'up_till':
            for p in paths:
                if p.startswith(url_path):
                     return 1

    if visibility == 'if_secure_connection':
        if REQUEST is not None:
            theBase = REQUEST['BASE0'].split('//')[0]
            if theBase == 'https:':
                return 1


def getApplicableStylesFor(self):
    """ Returns the list of styles by meta type and style's identifier
        applicable to the current object
    """
    list = []
    tmtool = getToolByName(self, 'portal_themes')

    style_types = tmtool.listStyleMetaTypes()
    for propid in self.propertyIds():
        prop_map = self.propertyMap()
        for obj in prop_map:
            if obj['id'] == propid:
                style = obj.get('style')
                id = obj.get('id')
                if style and style in style_types:
                    list.append({'id': id, 'meta_type': style})
                break
    return list

def getStyleList(self, meta_type):
    """ Returns a list of styles by meta type"""

    tmtool = getToolByName(self, 'portal_themes')
    styles = tmtool.findStylesFor(category = meta_type, object=self)
    if styles:
        return styles['title']

def getDefaultLang(self):
    """ Returns the code name of the current language """

    langs = []
    lc = getToolByName(self, 'portal_messages', None)
    if lc is None:
        lc = getattr(self, 'Localizer', None)

    default_lang = None
    if lc is not None:
        if hasattr(lc, 'get_languages_map'):
            get_languages_map = lc.get_languages_map
            if callable(get_languages_map):
                langs = get_languages_map()
                for lang in langs:
                    if lang['selected']:
                        default_lang = lang['id']
                        break
    return default_lang


def getAvailableLangs(self):
    """ Returns a list of available languages"""

    langs = []
    lc = getToolByName(self, 'portal_messages', None)
    if lc is None:
        lc = getattr(self, 'Localizer', None)

    if lc is not None:
        if hasattr(lc, 'get_available_languages'):
            available_langs = lc.get_available_languages
            if callable(available_langs):
                langs = available_langs()
    return langs


def isBroken(self):
    """ Checks whether the object is broken """

    if not hasattr(self, 'meta_type'):
        return 1
    meta_type = getattr(self, 'meta_type')
    if meta_type == 'Broken Because Product is Gone':
        return 1
    return None


def moveToLostAndFound(self, obj):
    """ moves the object to the lost+found folder of the theme"""

    tmtool = getToolByName(self, 'portal_themes')

    container = obj.aq_parent
    cookie = container.manage_cutObjects(obj.getId())
    theme_container = tmtool.getPortalThemeRoot(object=obj)
    lost_and_found = theme_container.getLostAndFoundFolder(create=1)
    if lost_and_found is None:
        return None
    try:
        res = lost_and_found.manage_pasteObjects(cookie)
        new_id = res[0]['new_id']
        newobj = getattr(lost_and_found, new_id)
        manage_perms = newobj.manage_permission
        manage_perms(View, roles=['Manager'], acquire=0)
        manage_perms(AccessContentsInformation, roles=['Manager'], acquire=0)
    except:
        container.manage_delObjects(obj.getId())


def css_slimmer(css):
    """ reduces the size of a CSS file """

    css_comments = re.compile(r'/\*.*?\*/', re.MULTILINE|re.DOTALL)
    css = css_comments.sub('', css)
    css = re.sub(r'\s\s+', '', css)
    css = re.sub(r'\s+{','{', css)
    css = re.sub(r'\s}','}', css)
    css = re.sub(r'}','}\n', css)
    css = re.sub(r'>\s+', '>\n', css)
    css = re.sub(r'\s+<', '\n<', css)
    css = re.sub(r';\n', ';', css)
    css = re.sub(r'{\n', '{', css)
    css = re.sub(r'\n\n','\n', css)
    css = re.sub(r';}','}', css)
    css = re.sub(r',\n',',', css)
    return css

def html_slimmer(html):
    """ reduces the size of HTML code """

    html = re.sub(r'>\s+<','> <', html)
    html = re.sub(r'\n\s+\n','', html)
    html = re.sub(r'\n','', html)
    return html

