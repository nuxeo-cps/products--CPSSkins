##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes

cellsizer =  context.addCellSizer(**kw)
if cellsizer is None:
    return

# scroll position
scrollx = kw.get('scrollx', '0')
scrolly = kw.get('scrolly', '0')

tmtool.setViewMode(scrollx=scrollx)
tmtool.setViewMode(scrolly=scrolly)

url = cellsizer.aq_parent.absolute_url() + '/edit_form'

if REQUEST is None:
    return cellsizer
else:
    REQUEST.RESPONSE.redirect(url)
