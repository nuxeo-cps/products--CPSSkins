##parameters=REQUEST=None

context.setAsDefault()

if REQUEST is not None:
    url = REQUEST['HTTP_REFERER']
    REQUEST.RESPONSE.redirect(url)

