##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

newobj = context.duplicate()

url = newobj.absolute_url() + '/cpsskins_edit_form'

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
