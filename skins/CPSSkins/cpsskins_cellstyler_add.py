##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

cellstyler =  context.addCellStyler(**kw)
if cellstyler is None:
    return

url = context.portal_url() + '/cpsskins_theme_manage_form'

if REQUEST is None:
    return cellstyler
else:
    REQUEST.RESPONSE.redirect(url)
