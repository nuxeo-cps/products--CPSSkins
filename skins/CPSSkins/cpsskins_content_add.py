##parameters=REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

theme = tmtool.getRequestedThemeName(context=context)
theme_container = tmtool.getThemeContainer(theme=theme)

content = context.addContent(**kw)
if content is None:
    return

tmtool.clearViewMode('scrollx', 'scrolly')

url = content.absolute_url() + '/edit_form'

default_styles = {}
for category in content.getApplicableStyles():
    style_propid =  category['id']
    type_name = category['meta_type']
    style = getattr(context, style_propid, None)
    styles = tmtool.findStylesFor(category=type_name, \
                                  object=content, title=style)
    if styles['object']:
        default_style = theme_container.getDefaultStyle(type_name)
    else:
        style = theme_container.addPortalStyle(type_name=type_name)
        default_style = getattr(style, 'title', '')
    default_styles[style_propid] = default_style

if default_styles:
    content.edit(**default_styles)
else:
    return

if REQUEST is None:
    return content
else:
    REQUEST.RESPONSE.redirect(url)
