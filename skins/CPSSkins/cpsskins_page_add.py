##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes

theme_container = context
if not getattr(theme_container.aq_inner.aq_explicit, 'isportaltheme', 0):
    return

page_container = theme_container.addThemePage()
if page_container is None:
    return

page = page_container.getId()

# switch to the new theme
tmtool.setViewMode(page=page)

url = context.portal_url() + '/cpsskins_theme_manage_form'
if REQUEST is None:
    return theme
else:
    REQUEST.RESPONSE.redirect(url)
