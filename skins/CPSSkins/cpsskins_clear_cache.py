##parameters=REQUEST=None, **kw

context.manage_clearCache()

if REQUEST is not None:
    url = REQUEST['HTTP_REFERER'] 
    REQUEST.RESPONSE.redirect(url)
