##parameters=theme=None, edit_mode='wysiwyg', REQUEST=None,**kw

tmtool = context.portal_themes

if REQUEST is not None:
    kw.update(REQUEST.form)

themes_folder = tmtool.getThemeContainer(parent=1)
themes = tmtool.getThemes()   
mcat = context.cpsskins_getlocalizer()

default_theme_list =  kw.get('default_theme', [])
if default_theme_list is not None:
    default_theme = default_theme_list[0]
    tmtool.setDefaultTheme(default_theme)

current_theme = kw['theme']
del kw['theme']

theme_renderers = kw['theme_renderers']
themes_to_delete = kw.get('delete_themes', [])
themes_to_delete = filter(lambda s, l=themes_folder.objectIds(): s in l, \
                          themes_to_delete)

for i in range(len(themes)):
    params = {}
    theme = themes[i]
    params['theme_renderer'] = theme_renderers[i]
    theme.edit(**params)

for theme_id in themes_to_delete:
    if theme_id == default_theme:
        continue
    tmtool.delObject(themes_folder[theme_id])

theme_container = tmtool.getEffectiveThemeContainer(theme=default_theme)

if REQUEST is not None:
     url = theme_container.absolute_url() + '/cpsskins_themes_manager' + \
           '?edit_mode=' + edit_mode
     if default_theme:
        url = url + '&theme=' + default_theme 
     REQUEST.RESPONSE.redirect(url)
