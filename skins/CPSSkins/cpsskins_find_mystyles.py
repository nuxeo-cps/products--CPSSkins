##parameters=theme=None, edit_mode='wysiwyg', REQUEST=None, **kw

tmtool = context.portal_themes 
if REQUEST is not None:
    kw.update(REQUEST.form)

meta_type = kw.get('styleprop', None)
if meta_type is None:
    return

if theme is None:
    theme = tmtool.getDefaultThemeName()

theme_container = tmtool.getThemeContainer(theme=theme)
mystyle_objs = theme_container.findStyles(meta_type=meta_type)

if len(mystyle_objs) == 0:
    newstyle = theme_container.addPortalStyle(type_name=meta_type)
    mystyle_objs = [newstyle]

oldstyle = context.getStyle(meta_type=meta_type)
if oldstyle is None:
    oldstyle = mystyle_objs[0]

parents = oldstyle.findParents()
style = oldstyle

if len(parents) == 1:
    for s in tmtool.findStylesFor(meta_type, context)['object']:
        if s.getTitle() == meta_type:
            style = s
else:
    style = oldstyle.duplicate()
    context.setStyle(style=style, meta_type=meta_type)

if style is None:
    return

url = style.absolute_url() + '/edit_form?edit_mode=' + edit_mode + \
     '&style=' + meta_type + '&theme=' + theme

if REQUEST is None:
    return style

REQUEST.RESPONSE.redirect(url)
