##parameters=REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

theme = tmtool.getRequestedThemeName(context=context)
theme_container = tmtool.getThemeContainer(theme=theme)
if theme_container is None:
    return

style = theme_container.addPortalStyle(**kw) 
if style is None:
    return

type_name = kw.get('type_name', None)
if type_name is None:
    return

url = style.absolute_url() + '/edit_form' + \
      '?style=' + type_name

if REQUEST is None:
    return style
else:
    REQUEST.RESPONSE.redirect(url)
