##parameters=theme=None, edit_mode='wysiwyg', REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

cellhider =  context.addCellHider(**kw)
if cellhider is None:
    return

if theme is None:
    theme = tmtool.getDefaultThemeName()

url = cellhider.absolute_url() + '/edit_form' + \
     '?theme=' + theme + '&edit_mode=' + edit_mode

if REQUEST is None:
    return cellhider
else:
    REQUEST.RESPONSE.redirect(url)
