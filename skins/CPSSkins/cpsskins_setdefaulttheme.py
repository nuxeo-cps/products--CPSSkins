##parameters=default_theme=None, REQUEST=None

tmtool = context.portal_themes
tmtool.setDefaultTheme(default_theme=default_theme)

if REQUEST is not None:
    url = REQUEST['HTTP_REFERER']
    REQUEST.RESPONSE.redirect(url)


