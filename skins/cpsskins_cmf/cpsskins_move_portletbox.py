##parameters=portlet_rurl=None, dest_rurl=None, REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

portal_path = context.portal_url.getPortalPath() + '/'
portlet = context.restrictedTraverse(portal_path + portlet_rurl)

dest_folder = None
if dest_rurl is not None:
    dest_folder = context.restrictedTraverse(portal_path + dest_rurl)

ptltool = context.portal_cpsportlets
portlet = ptltool.movePortlet(portlet=portlet,
                              dest_folder=dest_folder,
                              **kw)

tmtool = context.portal_themes
tmtool.setViewMode(selected_portlet=portlet.getId())

if REQUEST is not None:
     url = context.absolute_url() + '/portlet_manage_form'
     REQUEST.RESPONSE.redirect(url)
