##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes
theme = tmtool.getRequestedThemeName(context=context)
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

imagecat = kw.get('imagecat', '')
url = '%s/cpsskins_image_edit_form?imagecat=%s' % \
      (context.absolute_url(), imagecat) 

if REQUEST is None:
    return img
else:
    REQUEST.RESPONSE.redirect(url)
