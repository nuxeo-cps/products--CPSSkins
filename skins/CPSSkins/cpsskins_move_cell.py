##parameters=xpos=None, dir=None, REQUEST=None

if dir not in ['left', 'right']:
    return

context.moveCell(xpos=xpos, dir=dir)

url = REQUEST['HTTP_REFERER']

if REQUEST is not None:
   REQUEST.RESPONSE.redirect(url)
