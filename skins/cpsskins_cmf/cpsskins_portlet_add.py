##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

kw['title'] = kw.get('ptype_id', '')
kw['context'] = context

ptltool = context.portal_cpsportlets
context.createCPSPortlet(REQUEST=REQUEST, **kw)
