##parameters=theme=None, edit_mode='wysiwyg', REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

theme_container = tmtool.getThemeContainer(theme=theme)
if theme_container is None:
    return

file = kw.get('file', None)
if file is None:
    return

kw['id'] = context.getId()
img = theme_container.editPortalImage(**kw) 
if img is None:
    return

if theme is None:
    theme = tmtool.getDefaultThemeName()

imagecat = kw.get('imagecat', '')
url = '%s/cpsskins_image_edit_form?theme=%s&edit_mode=%s&imagecat=%s' % \
      (context.absolute_url(), theme, edit_mode, imagecat) 

if REQUEST is None:
    return img
else:
    REQUEST.RESPONSE.redirect(url)
