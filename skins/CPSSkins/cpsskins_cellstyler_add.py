##parameters=theme=None, edit_mode='wysiwyg', REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

cellstyler =  context.addCellStyler(**kw)
if cellstyler is None:
    return

if theme is None:
    theme = tmtool.getDefaultThemeName()

url = cellstyler.absolute_url() + '/edit_form' + \
     '?theme=' + theme + '&edit_mode=' + edit_mode

if REQUEST is None:
    return cellstyler
else:
    REQUEST.RESPONSE.redirect(url)
