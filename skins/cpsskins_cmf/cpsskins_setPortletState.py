##parameters=state='', REQUEST=None

if not state:
    return

context.setState(state=state, REQUEST=REQUEST)

if REQUEST is not None:
    url = REQUEST['HTTP_REFERER']
    REQUEST.RESPONSE.redirect(url)
