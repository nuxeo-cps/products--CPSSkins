##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

goto = kw.get('goto', None)

tmtool = context.portal_themes
tmtool.delObject(context)

if goto == 'referer':
    url = REQUEST['HTTP_REFERER']
else:
    url = context.portal_url() + '/cpsskins_theme_manage_form'

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
