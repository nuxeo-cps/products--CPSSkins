##parameters=portlet_rurl=None, dest_rurl=None, redirect_rurl=None, REQUEST=None, **kw

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
    if redirect_rurl is None:
        redirect_url = context.absolute_url()
    else:
        redirect_url = context.portal_url() + '/' + redirect_rurl
    redirect_url += '/portlet_manage_form'
    REQUEST.RESPONSE.redirect(redirect_url)
