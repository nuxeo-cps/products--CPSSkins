##parameters=REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

alignprop = kw.get('alignprop', None)
if alignprop is None:
    return

context.change_alignment(alignment=alignprop)

# set the content as selected
tmtool.setViewMode(selected_content=context.getId())

url = context.portal_url() + '/cpsskins_theme_manage_form'

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
