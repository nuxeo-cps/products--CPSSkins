##parameters=theme=None, edit_mode='wysiwyg', REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

theme_container = tmtool.getThemeContainer(theme=theme)
templet = context.addTemplet(**kw)
if templet is None:
    return

if theme is None:
    theme = tmtool.getDefaultThemeName()

url = templet.absolute_url() + '/edit_form' + \
      '?theme=' + theme + '&edit_mode=' + edit_mode

default_styles = {}
for category in templet.getApplicableStyles():
    style_propid =  category['id']
    type_name = category['meta_type']
    style = getattr(context, style_propid, None)
    styles = tmtool.findStylesFor(category=type_name, \
                                  object=templet, title=style)
    if styles['object']:
        default_style = theme_container.getDefaultStyle(type_name)
    else:
        style = theme_container.addPortalStyle(type_name=type_name)
        default_style = getattr(style, 'title', '')
    default_styles[style_propid] = default_style
if default_styles:
    templet.edit(**default_styles)
else:
    return

if REQUEST is None:
    return templet
else:
    REQUEST.RESPONSE.redirect(url)
