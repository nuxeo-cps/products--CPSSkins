##parameters=REQUEST=None

if getattr(context, 'isportaltheme', 0):
    context.rebuild(setperms=1)

if REQUEST is not None:
    url = REQUEST['HTTP_REFERER']
    REQUEST.RESPONSE.redirect(url)
