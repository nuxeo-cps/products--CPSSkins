##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes
action = kw.get('action', None)

if action == 'duplicate':
    context.duplicate()

if action == 'delete':
    tmtool.delObject(context)

url = context.portal_url() + '/cpsskins_theme_manage_form'

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
