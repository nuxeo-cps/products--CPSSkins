##parameters=theme=None, edit_mode='wysiwyg', REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes

xpos = kw.get('xpos', 0)
ypos = kw.get('ypos', 0)
direction = kw.get('direction', None)
dest_pageblock = kw.get('dest_pageblock', None)
dest_theme = kw.get('dest_theme', None)

if dest_theme and dest_theme != theme:
    newobj = context.copy_to_theme(dest_theme=dest_theme)
    for category in context.getApplicableStyles():
        style_propid = category['id']
        style = getattr(context, style_propid, None)
        styles = tmtool.findStylesFor(category=category['meta_type'], \
                                      object=context, title=style)
        if len(styles) > 0:
           if len(styles['object']) > 0:
                style_to_copy = styles['object'][0]
                newstyle = style_to_copy.copy_to_theme(dest_theme=dest_theme)
                prop_dict = {style_propid:newstyle.getTitle()}
                newobj.edit(**prop_dict)
    theme = dest_theme
else:
    if direction:
        newobj = context.move(direction=direction)
    else:
        newobj = context.move_to_pageblock(dest_pageblock, xpos, ypos)

if newobj is None:
    return

if theme is None:
    theme = tmtool.getDefaultThemeName()
url = newobj.absolute_url() + '/edit_form' + \
      '?theme=' + theme + '&edit_mode=' + edit_mode

if REQUEST is None:
    return newobj
else:
    REQUEST.RESPONSE.redirect(url)
