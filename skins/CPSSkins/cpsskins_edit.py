##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes

context.edit(**kw)

# category
cat = kw.get('cat')
if getattr(context.aq_explicit, 'isportletbox', 0) and kw.get('portlet_type'):
    cat = 'Portlet'

# redirect url
url = kw.get('redirect_url')

kw['selected_content'] = context.getId()

# save scroll position
tmtool.setViewMode(**kw)

if REQUEST is not None:
    if url is None:
        url = context.absolute_url() + '/edit_form'

    if cat:
        url += '?cat=' + cat
    REQUEST.RESPONSE.redirect(url)
