##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

kw['title'] = kw.get('ptype_id', '')
context.createCPSPortlet(**kw)

url = context.absolute_url() + '/portlet_manage_form'
if REQUEST is None:
    return content
else:
    REQUEST.RESPONSE.redirect(url)
