##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes
theme = tmtool.addPortalTheme(**kw) 
if theme is None:
    return

themeid = theme.getId()

tmtool.setDefaultTheme(themeid)
theme.setTitle(themeid)

# switch to the new theme
tmtool.setViewMode(theme=themeid)

# set the edit mode to 'Mixed'
tmtool.setViewMode(edit_mode='mixed')

url = context.portal_url() + '/cpsskins_theme_manage_form'
if REQUEST is None:
    return theme
else:
    REQUEST.RESPONSE.redirect(url)
