##parameters=REQUEST=None

if getattr(context.aq_inner.aq_explicit, 'isportaltheme', 0):
    context.rebuild(setperms=1)

if REQUEST is not None:
    url = REQUEST['HTTP_REFERER']
    REQUEST.RESPONSE.redirect(url)
