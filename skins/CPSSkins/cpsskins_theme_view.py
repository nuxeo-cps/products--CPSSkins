
theme = context.getId()

REQUEST = context.REQUEST

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(context.portal_url() + '/?theme=' + theme)
