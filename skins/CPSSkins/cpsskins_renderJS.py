##parameters=theme=None, page=None, REQUEST=None, **kw

if REQUEST is not None:
    REQUEST.RESPONSE.setHeader('Content-Type', 'text/javascript')

tmtool = context.portal_themes
theme_container = tmtool.getThemeContainer(theme=theme)
page_container = theme_container.getPageContainer(page=page)
js = theme_container.renderJS(page=page)

# CPS Portlets
ptltool = getattr(context, 'portal_cpsportlets', None)
if ptltool is not None and page_container is not None:
    portlets = ptltool.getPortlets(context)
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
        if ptype_id not in done_types:
            js += portlet.render_js()
            done_types.append(ptype_id)

return '<!--\n%s\n-->' % js
