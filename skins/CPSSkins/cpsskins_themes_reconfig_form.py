##parameters=theme=None, REQUEST=None, **kw

tmtool = context.portal_themes
tmtool.manage_clearCaches()

if REQUEST is None:
    REQUEST = context.REQUEST
kw.update(REQUEST.form)

# get the current theme
theme = kw.get('theme')
if theme is None:
    theme = tmtool.getRequestedThemeName(context=context)

# vertical scroll position
scrolly = kw.get('scrolly')
if scrolly is not None:
    tmtool.setViewMode(scrolly=scrolly)

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
