##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

goto = kw.get('goto', None)

tmtool = context.portal_themes
tmtool.delObject(context)

if goto == 'referer':
    url = REQUEST['HTTP_REFERER']  
else:
    url = context.aq_parent.absolute_url() + '/edit_form'

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
