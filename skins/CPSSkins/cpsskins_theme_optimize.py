##parameters=REQUEST=None, theme=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes
theme_container = tmtool.getThemeContainer(theme=theme)

styles_dir = theme_container.getStylesFolder()

#
# Request parameters
#

merge_style_keys = filter(lambda key: key.startswith('merge_styles_'), \
                          kw.keys())
styles_to_delete = kw.get('delete_styles', [])
templets_to_delete = kw.get('delete_templets', [])
templets_to_cache = kw.get('cached_templets', [])
items_to_translate = kw.get('items_to_translate', [])

#
# Styles to merge
#

for k in merge_style_keys:
    styles = kw.get(k, [])
    nb_styles = len(styles)
    if nb_styles < 2:
        continue
    for i in range(nb_styles):
        style_obj = getattr(styles_dir, styles[i], None)
        if style_obj is None:
            continue
        style_title = style_obj.getTitle()
        if i == 0:
            new_title = style_title
        else:
            style_obj.findParents(newtitle=new_title)
            style_id = style_obj.getId()
            if style_id not in styles_to_delete:
                styles_to_delete.append(style_id)

#
# Styles to delete
#

styles_to_delete = filter(lambda s, l=styles_dir.objectIds(): s in l, \
                          styles_to_delete)
styles_dir.manage_delObjects(styles_to_delete)

#
# Templets to delete
#

if templets_to_delete:
    for templet_path in templets_to_delete:
        templet = context.restrictedTraverse(templet_path, default=None)
        if templet is not None:
             pageblock = templet.getContainer()
             pageblock.manage_delObjects([templet.getId()])

#
# Templets to cache
#

if templets_to_cache:
    for templet_path in templets_to_cache:
        templet = context.restrictedTraverse(templet_path, default=None)
        if templet is not None:
            templet.edit(cacheable=1)

#
# Items to translate
#

for templet in theme_container.getTemplets():
    i18n_templet_id = templet.getId()
    i18n_props = templet.getI18nProperties()
    prop_dict = {}
    for i18n_prop in i18n_props:
        prop_dict[i18n_prop] = 0
    for item in items_to_translate:
        split_item = item.split(':')
        if len(split_item) < 2:
            continue
        templet_id = split_item[0]
        if templet_id == i18n_templet_id:
            prop_id = split_item[1]
            prop_dict[prop_id] = 1
    templet.edit(**prop_dict)

#
# Redirection
#

if REQUEST is not None:
    url = context.portal_url() + '/cpsskins_theme_manage_form'
    REQUEST.RESPONSE.redirect(url)
