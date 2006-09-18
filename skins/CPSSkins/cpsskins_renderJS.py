##parameters=theme=None, page=None, REQUEST=None, **kw

tmtool = context.portal_themes
theme_container = tmtool.getThemeContainer(theme=theme)
page_container = theme_container.getPageContainer(page=page)

theme_container.setCacheHeaders(content_type='text/javascript', page=page)

js = ''
# CPS Portlets
ptltool = getattr(context, 'portal_cpsportlets', None)
if ptltool is not None and page_container is not None:
    portlets = ptltool.getPortlets(context=context, guard_check=0)
    slots = page_container.getSlots()
    done_types = []
    for portlet in portlets:
        if portlet.getSlot() not in slots:
            continue
        ti = portlet.getTypeInfo()
        if ti is None:
            continue
        ptype_id = ti.getId()
        # XXX: use the cache
        if ptype_id not in done_types or ptype_id == 'Custom Portlet':
            js += portlet.render_js()
            done_types.append(ptype_id)

return '<!--\n%s\n//-->' % js
