##parameters=theme=None, edit_mode='wysiwyg', REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

if theme is None:
    theme = tmtool.getDefaultThemeName()

theme_container = tmtool.getThemeContainer(theme=theme)
if theme_container is None:
    return

palette = theme_container.addPortalPalette(**kw) 
if palette is None:
    return

type_name = kw.get('type_name', None)
if type_name is None:
    return

url = palette.absolute_url() + '/edit_form' + \
      '?theme=' + theme + '&edit_mode=' + edit_mode + \
      '&palette=' + type_name

if REQUEST is None:
    return palette
else:
    REQUEST.RESPONSE.redirect(url)
