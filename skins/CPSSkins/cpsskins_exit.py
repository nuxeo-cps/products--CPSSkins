##parameters=REQUEST=None

tmtool = context.portal_themes
tmtool.manage_clearCaches()

view_mode = tmtool.getViewMode()
if view_mode.has_key('current_url'):
    url = view_mode['current_url']
else:
    url = context.portal_url()

tmtool.clearViewMode('theme', 'edit_mode', 'current_url')

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
