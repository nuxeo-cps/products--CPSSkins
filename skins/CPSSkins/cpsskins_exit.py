##parameters=REQUEST=None

tmtool = context.portal_themes
tmtool.manage_clearCaches()

if REQUEST is not None:
    url = context.portal_url()
    REQUEST.RESPONSE.redirect(url)
