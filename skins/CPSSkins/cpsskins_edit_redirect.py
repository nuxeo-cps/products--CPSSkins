##parameters=theme=None, edit_mode='wysiwyg', cat=None, REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

theme = kw.get('theme', None)
if theme is None:
    theme = tmtool.getDefaultThemeName()
theme_container = tmtool.getThemeContainer(theme=theme)

url = theme_container.absolute_url()
prefs = '&theme=' + theme + '&edit_mode=' + edit_mode

if cat not in ['image', 'style', 'palette']:
    return

if cat == 'image':
    url += '/cpsskins_edit_images' + \
           '?imagecat=' + kw.get('image', '') + prefs

elif cat == 'style':
    url += '/cpsskins_edit_styles' + \
           '?style=' + kw.get('style', '') + prefs

elif cat == 'palette':
    url += '/cpsskins_edit_palettes' + \
           '?palette=' + kw.get('palette', '') + prefs

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
