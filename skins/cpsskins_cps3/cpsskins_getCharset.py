##parameters=
#$Id$
"""
Called by cpsskins_main_template_macroless.pt to get the charset to use.
"""

from Products.CMFCore.utils import getToolByName

portal = getToolByName(context, 'portal_url').getPortalObject()
charset = portal.default_charset
if charset == 'unicode':
    charset = 'UTF-8'

return charset
