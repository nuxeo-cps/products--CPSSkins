##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes

cellstyler =  context.addCellStyler(**kw)
if cellstyler is None:
    return

# save scroll position
view_mode = tmtool.setViewMode(**kw)

url = context.portal_url() + '/cpsskins_theme_manage_form'

if REQUEST is None:
    return cellstyler
else:
    REQUEST.RESPONSE.redirect(url)
