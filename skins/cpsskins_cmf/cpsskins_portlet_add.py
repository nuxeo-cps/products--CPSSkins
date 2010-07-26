##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

ptype_id = kw.get('ptype_id')
if ptype_id is None:
   # redirect not so convenient (does HTTP_REFERER survives virtual hosting?)
   return # user stays on same page

title = kw.get('title', ptype_id)

dest_rurl = kw.get('dest_rurl')

# typically in a hidden input, but must be an integer
kw['order'] = int(kw.get('order', 0))

portal_path = context.portal_url.getPortalPath()

dest_folder = None
if dest_rurl:
    dest_folder = context.restrictedTraverse(portal_path + '/' + dest_rurl,
                                             default=None)
if dest_folder is None:
    dest_folder = context

ptltool = context.portal_cpsportlets
portlet_id = ptltool.createPortlet(context=context, **kw)
portlet_container = ptltool.getPortletContainer(context)
portlet = portlet_container.getPortletById(portlet_id)

if REQUEST is not None:
    url = portlet.absolute_url() + '/edit_form'
    REQUEST.RESPONSE.redirect(url)

