##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

cellstyler =  context.addCellStyler(**kw)
if cellstyler is None:
    return

url = cellstyler.absolute_url() + '/edit_form'

if REQUEST is None:
    return cellstyler
else:
    REQUEST.RESPONSE.redirect(url)
