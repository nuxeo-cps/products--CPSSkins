##parameters=REQUEST=None

tmtool = context.portal_themes
tmtool.manage_clearCaches()

view_mode = tmtool.getViewMode()
url = view_mode.get('current_url')

if url is None:
    url = context.portal_url()

tmtool.clearViewMode(
    'theme',
    'page',
    'edit_mode',
    'current_url')

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
