##parameters=portlet_rurl=None, src_rurl=None, dest_rurl=None, REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

portal_path = context.portal_url.getPortalPath() + '/'
portlet = context.restrictedTraverse(portal_path + portlet_rurl)

if src_rurl is not None:
    src_folder = context.restrictedTraverse(portal_path + src_rurl)

if dest_rurl is not None:
    dest_folder = context.restrictedTraverse(portal_path + dest_rurl)
else:
    dest_folder = src_folder

ptltool = context.portal_cpsportlets
portlet = ptltool.movePortlet(portlet=portlet,
                              src_folder=src_folder,
                              dest_folder=dest_folder,
                              **kw)

context.cpsskins_setViewMode(selected_portlet=portlet.getId())

if REQUEST is not None:
     url = context.absolute_url() + '/portlet_manage_form'
     REQUEST.RESPONSE.redirect(url)
