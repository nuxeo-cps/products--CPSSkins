##parameters=theme=None, edit_mode=None, REQUEST=None, **kw

tmtool = context.portal_themes

if REQUEST is not None:
    kw.update(REQUEST.form)

theme = tmtool.addPortalTheme(**kw) 
if theme is None:
    return

themeid = theme.getId()
tmtool.setDefaultTheme(themeid)
theme.setTitle(themeid)

url = theme.absolute_url() + '/edit_form' + \
     '?theme=' + themeid + '&edit_mode=mixed'

if REQUEST is None:
    return theme
else:
    REQUEST.RESPONSE.redirect(url)
