##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes

theme = tmtool.getRequestedThemeName(context_obj=context)
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

url = img.absolute_url() + '/cpsskins_image_edit_form?imagecat=' + imagecat

if REQUEST is None:
    return img
else:
    REQUEST.RESPONSE.redirect(url)
