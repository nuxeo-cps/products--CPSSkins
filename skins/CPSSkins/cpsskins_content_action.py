##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes
action = kw.get('action', None)

if action == 'duplicate':
    newobj = context.duplicate()

    # set the content as selected
    if newobj is not None:
        tmtool.setViewMode(selected_content=newobj.getId())

if action == 'delete':
    tmtool.delObject(context)
    tmtool.clearViewMode('selected_content')

url = context.portal_url() + '/cpsskins_theme_manage_form'

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
