##parameters=portlet_id=None, redirect_url=None, REQUEST=None

if portlet_id is None:
    return

ptltool = context.portal_cpsportlets
ptltool.duplicatePortlet(portlet_id, context)

if REQUEST is not None:
     if redirect_url is None:
         redirect_url = context.absolute_url()
     redirect_url += '/portlet_manage_form'
     REQUEST.RESPONSE.redirect(redirect_url)
