##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

cellhider =  context.addCellHider(**kw)
if cellhider is None:
    return

url = context.portal_url() + '/cpsskins_theme_manage_form'

if REQUEST is None:
    return cellhider
else:
    REQUEST.RESPONSE.redirect(url)
