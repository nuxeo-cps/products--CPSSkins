##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

context.edit(**kw)

if REQUEST is not None:
   url = REQUEST['HTTP_REFERER']
   REQUEST.RESPONSE.redirect(url)

