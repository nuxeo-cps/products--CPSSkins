##parameters=portlet_id=None, redirect_rurl=None, REQUEST=None

if REQUEST is None:
    REQUEST = context.REQUEST

if portlet_id is None:
    return

ptltool = context.portal_cpsportlets
ptltool.deletePortlet(portlet_id, context)

if REQUEST is not None:
     if redirect_rurl is None:
         redirect_url = context.absolute_url()
     else:
         redirect_url = context.portal_url() + '/' + redirect_rurl
     psm = 'psm_portlet_deleted'
     url = redirect_url + \
     '/portlet_manage_form?portal_status_message=%s' % psm
     REQUEST.RESPONSE.redirect(url)
