##parameters=theme=None, edit_mode='wysiwyg', REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

theme_container = tmtool.getThemeContainer(theme=theme)
if theme_container is None:
    return

imagecat = context.getId()
kw['imagecat'] = imagecat

file = kw.get('file', None)
if file is None:
    return

img = theme_container.addPortalImage(**kw) 
if img is None:
    return

if theme is None:
    theme = tmtool.getDefaultThemeName()

url = '%s/cpsskins_edit_images?theme=%s&edit_mode=%s&imagecat=%s' % \
      (theme_container.absolute_url(), theme, edit_mode, imagecat) 

if REQUEST is None:
    return img
else:
    REQUEST.RESPONSE.redirect(url)
