##parameters=REQUEST=None

psm = 'cpsportlets_portlet_created_psm'

portlet = context

# set the newly created portlet as the 'selected portlet'
context.cpsskins_setViewMode(selected_portlet=portlet.getId())

if REQUEST is not None:
    action_path = portlet.getTypeInfo().immediate_view
    redirect_url = '%s/%s?portal_status_message=%s' % \
                   (portlet.absolute_url(), action_path, psm)
    REQUEST.RESPONSE.redirect(redirect_url)
