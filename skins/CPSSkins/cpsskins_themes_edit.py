##parameters=REQUEST=None,**kw

tmtool = context.portal_themes

if REQUEST is not None:
    kw.update(REQUEST.form)

themes_folder = tmtool.getThemeContainer(parent=1)
themes = tmtool.getThemes()
mcat = tmtool.getTranslationService()

default_theme_list =  kw.get('default_theme', [])
if default_theme_list is not None:
    default_theme = default_theme_list[0]
    tmtool.setDefaultTheme(default_theme)

current_theme = kw['theme']
del kw['theme']

themes_to_delete = kw.get('delete_themes', [])
themes_to_delete = filter(lambda s, l=themes_folder.objectIds(): s in l, \
                          themes_to_delete)

for i in range(len(themes)):
    params = {}
    theme = themes[i]
    theme.edit(**params)

for theme_id in themes_to_delete:
    if theme_id == default_theme:
        continue
    tmtool.delObject(themes_folder[theme_id])

theme_container = tmtool.getThemeContainer(theme=default_theme)

if REQUEST is not None:
     url = context.portal_url() + '/cpsskins_theme_manage_form'
     if default_theme:
         tmtool.setViewMode(theme=default_theme)
     REQUEST.RESPONSE.redirect(url)
