##parameters=portlet_rurl=None, REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

portal_path = context.portal_url.getPortalPath() + '/'
portlet = context.restrictedTraverse(portal_path + portlet_rurl)

ptltool = context.portal_cpsportlets
ptltool.movePortlet(portlet=portlet, context=context, **kw)

if REQUEST is not None:
     url = context.absolute_url() + '/portlet_manage_form'
     url += '?selected_portlet=' + portlet.getId()
     REQUEST.RESPONSE.redirect(url)
