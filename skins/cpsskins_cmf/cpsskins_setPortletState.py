##parameters=state=None, REQUEST=None

if state is None:
    return

context.setState(state=state)

if REQUEST is not None:
    url = REQUEST['HTTP_REFERER']
    REQUEST.RESPONSE.redirect(url)
