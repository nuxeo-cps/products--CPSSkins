##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes
src_theme, src_page = tmtool.getEffectiveThemeAndPageName(editing=1)
theme_container = tmtool.getThemeContainer(theme=src_theme)

xpos = kw.get('xpos', 0)
ypos = kw.get('ypos', 0)
direction = kw.get('direction')
dest_block = kw.get('dest_block')
dest_theme = kw.get('dest_theme')
dest_page = kw.get('dest_page')

# if the destination theme is not specified assume that
# it is the current theme
if dest_theme is None:
    dest_theme = src_theme

dest_theme_container = tmtool.getThemeContainer(dest_theme)
if dest_theme_container is None:
    return

# if the destination page is not specified choose the requested page
if not dest_page:
    req_theme, req_page = tmtool.getRequestedThemeAndPageName(editing=1)
    dest_page_container = dest_theme_container.getPageContainer(page=req_page)
    if dest_page_container is None:
        dest_page_container = dest_theme_container.getDefaultPage()
    if dest_page_container is None:
        dest_page_container = dest_theme_container.addThemePage()
    dest_page = dest_page_container.getId()

# content will be duplicated
if dest_theme != src_theme or dest_page != src_page:
    newobj = context.copy_to_theme(dest_theme, dest_page)
    for category in context.getApplicableStyles():
        style_propid = category['id']
        style = getattr(context, style_propid, None)
        if not style:
            continue
        # do not copy styles between the pages of a same theme.
        if dest_theme == src_theme:
            continue
        styles = tmtool.findStylesFor(category=category['meta_type'], \
                                      object=context, title=style)
        if len(styles) > 0:
           if len(styles['object']) > 0:
                style_to_copy = styles['object'][0]
                newstyle = style_to_copy.copy_to_theme(dest_theme)
                prop_dict = {style_propid:newstyle.getTitle()}
                newobj.edit(**prop_dict)
    # switch to the destination theme and page
    tmtool.setViewMode(theme=dest_theme, page=dest_page)
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
