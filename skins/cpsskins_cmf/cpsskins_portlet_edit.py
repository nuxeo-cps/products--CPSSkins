
REQUEST = context.REQUEST

portlet = context

tmtool = context.portal_themes
# set the edited portlet as the 'selected portlet'
tmtool.setViewMode(selected_portlet=portlet.getId())

if REQUEST is not None:
    redirect_url = portlet.absolute_url() + '/edit_form'
    REQUEST.RESPONSE.redirect(redirect_url)
