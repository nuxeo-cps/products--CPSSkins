##parameters=REQUEST=None

if REQUEST is not None:
    REQUEST.RESPONSE.setHeader('Content-Type', 'text/javascript')

js = context.renderJS()

# CPS Portlets
ptltool = getattr(context, 'portal_cpsportlets', None)
if ptltool is not None:
    context_obj = context.REQUEST.get('context_obj')
    portlets = ptltool.getPortlets(context_obj)
    slots = context.getSlots()
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
