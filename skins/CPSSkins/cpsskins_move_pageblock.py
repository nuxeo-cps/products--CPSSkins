##parameters=direction=None, REQUEST=None

if direction not in ['up', 'down']:
    return

context.move(direction=direction)

url = REQUEST['HTTP_REFERER']

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
