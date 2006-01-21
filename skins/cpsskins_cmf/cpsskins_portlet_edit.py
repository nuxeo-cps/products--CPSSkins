##parameters=REQUEST=None
#$Id$

from Products.CMFCore.utils import getToolByName

portlet = context

tmtool = getToolByName(context, 'portal_themes')

# set the edited portlet as the 'selected portlet'
tmtool.setViewMode(selected_portlet=portlet.getId())

if REQUEST is not None:
    redirect_url = portlet.absolute_url() + '/edit_form'
    REQUEST.RESPONSE.redirect(redirect_url)
