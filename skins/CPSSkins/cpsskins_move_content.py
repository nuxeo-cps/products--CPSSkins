##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes
theme = tmtool.getRequestedThemeName(context=context)

xpos = kw.get('xpos', 0)
ypos = kw.get('ypos', 0)
direction = kw.get('direction', None)
dest_block = kw.get('dest_block', None)
dest_theme = kw.get('dest_theme', None)

if dest_theme and dest_theme != theme:
    newobj = context.copy_to_theme(dest_theme=dest_theme)
    for category in context.getApplicableStyles():
        style_propid = category['id']
        style = getattr(context, style_propid, None)
        if not style:
            continue
        styles = tmtool.findStylesFor(category=category['meta_type'], \
                                      object=context, title=style)
        if len(styles) > 0:
           if len(styles['object']) > 0:
                style_to_copy = styles['object'][0]
                newstyle = style_to_copy.copy_to_theme(dest_theme=dest_theme)
                prop_dict = {style_propid:newstyle.getTitle()}
                newobj.edit(**prop_dict)
    theme = dest_theme
    tmtool.setViewMode(theme=theme)
else:
    if direction:
        newobj = context.move(direction=direction)
    else:
        newobj = context.move_to_block(dest_block=dest_block, xpos=xpos, ypos=ypos)

if newobj is None:
    return

url = context.portal_url() + '/cpsskins_theme_manage_form'

# set the content as selected
tmtool.setViewMode(selected_content=newobj.getId())

if REQUEST is None:
    return newobj
else:
    REQUEST.RESPONSE.redirect(url)
