##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

object = context.toggle()

url = context.absolute_url() + '/edit_form'

if REQUEST is None:
    return object
else:
    REQUEST.RESPONSE.redirect(url)
