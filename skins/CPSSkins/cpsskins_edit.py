##parameters=cat='', REQUEST=None, **kw

if REQUEST is None:
    REQUEST = context.REQUEST

kw.update(REQUEST.form)

tmtool = context.portal_themes
context.edit(**kw)

c = context.aq_inner.aq_explicit
# category
if getattr(c, 'isportletbox', 0) and kw.get('portlet_type'):
    cat = 'Portlet'

# redirect url
url = kw.get('redirect_url')

if getattr(c, 'isportaltemplet', 0) or getattr(c, 'iscellblock', 0):
    kw['selected_content'] = context.getId()

# save scroll position
tmtool.setViewMode(**kw)

if REQUEST is not None:
    if url is None:
        url = context.absolute_url() + '/edit_form'
    if cat:
        url += '?cat=' + cat
    REQUEST.RESPONSE.redirect(url)
