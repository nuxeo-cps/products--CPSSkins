##parameters=theme=None, REQUEST=None, **kw

tmtool = context.portal_themes
tmtool.manage_clearCaches()

if REQUEST is None:
    REQUEST = context.REQUEST
kw.update(REQUEST.form)

theme = kw.get('theme')

if theme is None:
    theme = tmtool.getDefaultThemeName()

tmtool.setViewMode(theme=theme)

theme_container = tmtool.getEffectiveThemeContainer(theme=theme)
if theme_container is not None:
    url = theme_container.absolute_url() + '/edit_form'

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
