##parameters=portlet_id=None, REQUEST=None

if portlet_id is None:
    return

ptltool = context.portal_cpsportlets
ptltool.deletePortlet(portlet_id, context)

if REQUEST is not None:
     psm = 'psm_portlet_deleted'
     url = context.absolute_url() + \
     '/portlet_manage_form?portal_status_message=%s' % psm
     REQUEST.RESPONSE.redirect(url)
