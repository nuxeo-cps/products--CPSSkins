
REQUEST = context.REQUEST

portlet = context

# set the edited portlet as the 'selected portlet'
context.cpsskins_setViewMode(selected_portlet=portlet.getId())

if REQUEST is not None:
    redirect_url = portlet.absolute_url() + '/edit_form'
    REQUEST.RESPONSE.redirect(redirect_url)
