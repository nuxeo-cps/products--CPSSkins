##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

meta_type = kw.get('styleprop', None)
if meta_type is None:
    return

tmtool = context.portal_themes 
theme = tmtool.getRequestedThemeName(context_obj=context)
theme_container = tmtool.getThemeContainer(theme=theme)

mystyle_objs = theme_container.findStyles(meta_type=meta_type)

if len(mystyle_objs) == 0:
    newstyle = theme_container.addPortalStyle(type_name=meta_type)
    mystyle_objs = [newstyle]

oldstyle = context.getStyle(meta_type=meta_type)
if oldstyle is None:
    oldstyle = theme_container.addPortalStyle(type_name=meta_type)

style = oldstyle
for s in tmtool.findStylesFor(meta_type, context)['object']:
    if s.getTitle() == meta_type:
        style = s
    break

if style is None:
    return

context.setStyle(style=style, meta_type=meta_type)

url = style.absolute_url() + '/edit_form?' + \
     'style=' + meta_type

if REQUEST is None:
    return style

REQUEST.RESPONSE.redirect(url)
