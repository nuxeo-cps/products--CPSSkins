##parameters=theme=None, edit_mode='wysiwyg', REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

cellsizer =  context.addCellSizer(**kw)
if cellsizer is None:
    return

if theme is None:
    theme = tmtool.getDefaultThemeName()

url = cellsizer.absolute_url() + '/edit_form' + \
     '?theme=' + theme + "&edit_mode=" + edit_mode

if REQUEST is None:
    return cellsizer
else:
    REQUEST.RESPONSE.redirect(url)
