##parameters=theme=None, edit_mode='wysiwyg', REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

cellsizer =  context.addCellSizer(**kw)
if cellsizer is None:
    return

if theme is None:
    theme = tmtool.getDefaultThemeName()

# scroll position
scrollx = kw.get('scrollx', '0')
scrolly = kw.get('scrolly', '0')

url = cellsizer.absolute_url() + '/edit_form' + \
     '?theme=' + theme + "&edit_mode=" + edit_mode + \
     '&scrollx=' + scrollx + '&scrolly=' + scrolly

if REQUEST is None:
    return cellsizer
else:
    REQUEST.RESPONSE.redirect(url)
