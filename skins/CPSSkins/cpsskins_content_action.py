##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes
action = kw.get('action', None)

selected_obj = context
if action == 'duplicate':
    selected_obj = context.duplicate()
    url = context.absolute_url() + '/cpsskins_theme_manage_form'

elif action == 'set_styles':
    url = context.absolute_url() + '/edit_form?cat=style'

elif action == 'set_layout':
    url = context.absolute_url() + '/edit_form?cat=layout'

elif action == 'set_default':
    context.setAsDefault()
    tmtool.setViewMode(theme=context.getId())
    url = context.portal_url() + '/cpsskins_theme_manage_form'

elif action == 'manage_theme':
    tmtool.setViewMode(theme=context.getId(), themes_panel='theme')
    url = context.portal_url() + '/cpsskins_theme_manage_form'

if action == 'delete':
    tmtool.delObject(context)
    tmtool.clearViewMode('selected_content')
    url = context.portal_url() + '/cpsskins_theme_manage_form'
else:
    # set the content as selected
    tmtool.setViewMode(selected_content=selected_obj.getId())

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
