##parameters=REQUEST=None

tmtool = context.portal_themes
tmtool.manage_clearCaches()

tmtool.clearViewMode('theme', 'edit_mode')

if REQUEST is not None:
    url = context.portal_url()
    REQUEST.RESPONSE.redirect(url)
