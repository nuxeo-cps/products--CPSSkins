##parameters=cat=None, REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes
theme = tmtool.getRequestedThemeName(context=context)
theme_container = tmtool.getThemeContainer(theme=theme)

url = theme_container.absolute_url()

if cat not in ['image', 'style', 'palette']:
    return

if cat == 'image':
    url += '/cpsskins_edit_images' + \
           '?imagecat=' + kw.get('image', '')

elif cat == 'style':
    url += '/cpsskins_edit_styles' + \
           '?style=' + kw.get('style', '')

elif cat == 'palette':
    url += '/cpsskins_edit_palettes' + \
           '?palette=' + kw.get('palette', '')

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
