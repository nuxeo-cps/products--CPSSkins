##parameters=portlet_id=None, redirect_rurl=None, REQUEST=None

if portlet_id is None:
    return

ptltool = context.portal_cpsportlets
ptltool.duplicatePortlet(portlet_id, context)

if REQUEST is not None:
    if redirect_rurl is None:
        redirect_url = context.absolute_url()
    else:
        redirect_url = context.portal_url() + '/' + redirect_rurl
    redirect_url += '/portlet_manage_form'
    REQUEST.RESPONSE.redirect(redirect_url)
