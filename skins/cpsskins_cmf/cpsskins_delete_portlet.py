##parameters=portlet_id=None, redirect_url=None, REQUEST=None

if portlet_id is None:
    return

ptltool = context.portal_cpsportlets
ptltool.deletePortlet(portlet_id, context)

if REQUEST is not None:
     if redirect_url is None:
         redirect_url = context.absolute_url()
     psm = 'psm_portlet_deleted'
     url = redirect_url + \
     '/portlet_manage_form?portal_status_message=%s' % psm
     REQUEST.RESPONSE.redirect(url)
