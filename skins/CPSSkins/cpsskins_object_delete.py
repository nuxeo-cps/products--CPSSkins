##parameters=theme=None, edit_mode='wysiwyg', REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

goto = kw.get('goto', None)
tmtool.delObject(context)

if goto == 'referer':
    url = REQUEST['HTTP_REFERER']  
else:
    if theme is None:
       theme = tmtool.getDefaultThemeName()
    url = context.aq_parent.absolute_url() + '/edit_form' + \
         '?theme=' + theme + '&edit_mode=' + edit_mode

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
