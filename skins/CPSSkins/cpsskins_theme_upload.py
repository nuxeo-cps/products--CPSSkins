##parameters=file=None, REQUEST=None

tmtool = context.portal_themes

if file:
    default_theme = tmtool.getDefaultThemeName()
    theme_id = tmtool.importTheme(file=file, REQUEST=REQUEST)
    theme = tmtool.getThemeContainer(theme=theme_id)
    theme.rebuild(setperms=1)

    tmtool.setDefaultTheme(default_theme)
    tmtool.setViewMode(theme=theme_id)

    url = theme.absolute_url() + '/cpsskins_themes_reconfig_form'
else:
    url = REQUEST['HTTP_REFERER']

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
