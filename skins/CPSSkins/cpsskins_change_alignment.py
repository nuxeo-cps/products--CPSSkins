##parameters=REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

alignprop = kw.get('alignprop', None)
if alignprop is None:
    return

context.change_alignment(alignment=alignprop)


tmtool.clearViewMode('scrollx', 'scrolly')

url = context.absolute_url() + '/edit_form'

if REQUEST is not None:
     REQUEST.RESPONSE.redirect(url)
