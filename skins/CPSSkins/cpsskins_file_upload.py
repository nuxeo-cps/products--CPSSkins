##parameters=file=None, REQUEST=None

if file:
    context.manage_upload(file)

if REQUEST is not None:
    url = REQUEST['HTTP_REFERER'] 
    REQUEST.RESPONSE.redirect(url)
