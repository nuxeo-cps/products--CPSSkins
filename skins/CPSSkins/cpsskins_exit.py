##parameters=REQUEST=None

tmtool = context.portal_themes

if REQUEST is not None:
    url = context.portal_url()
    REQUEST.RESPONSE.redirect(url)
