##parameters=theme=None, REQUEST=None, **kw

tmtool = context.portal_themes
tmtool.manage_clearCaches()

if REQUEST is None:
    REQUEST = context.REQUEST
kw.update(REQUEST.form)

theme = kw.get('theme')
# get the current theme
if theme is None:
    theme = tmtool.getRequestedThemeName(context=context)

# set the current theme
tmtool.setViewMode(theme=theme)

# set the default edit mode
view_mode = tmtool.getViewMode()
edit_mode = view_mode and view_mode.get('edit_mode') or None
if edit_mode is None:
    tmtool.setViewMode(edit_mode='wysiwyg')

theme_container = tmtool.getEffectiveThemeContainer(theme=theme)
if theme_container is not None:
    url = theme_container.absolute_url() + '/edit_form'

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
