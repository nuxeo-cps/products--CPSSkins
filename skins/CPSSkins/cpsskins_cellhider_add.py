##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes

cellhider =  context.addCellHider(**kw)
if cellhider is None:
    return

url = context.portal_url() + '/cpsskins_theme_manage_form'

# save scroll position
view_mode = tmtool.setViewMode(**kw)

if REQUEST is None:
    return cellhider
else:
    REQUEST.RESPONSE.redirect(url)
