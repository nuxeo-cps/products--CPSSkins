##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

kw['title'] = kw.get('ptype_id', '')

dest_rurl = kw.get('dest_rurl')

portal_path = context.portal_url.getPortalPath()

dest_folder = None
if dest_rurl:
    dest_folder = context.restrictedTraverse(portal_path + '/' + dest_rurl,
                                             default=None)
if dest_folder is None:
    dest_folder = context
kw['context'] = dest_folder

ptltool = context.portal_cpsportlets
context.createCPSPortlet(REQUEST=REQUEST, **kw)
