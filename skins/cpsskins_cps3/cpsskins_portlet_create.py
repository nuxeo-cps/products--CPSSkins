##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

ptype_id = kw.get('ptype_id')

ptltool = context.portal_cpsportlets
if ptype_id is not None:
    portlet_id = ptltool.createPortlet(context=context, **kw)

if REQUEST is not None:
    redirect_url = REQUEST.get('HTTP_REFERER')
    REQUEST.RESPONSE.redirect(redirect_url)

