##parameters=type_name=None, slot=None, REQUEST=None

ptltool = context.portal_cpsportlets
if type_name is not None:
    portlet_id = ptltool.createPortlet(ptype_id=type_name, context=context)

    portlets = ptltool.getPortlets(context=context)
    for portlet in portlets:
        if portlet_id == portlet.getId():
            # XXX fails here
            portlet.setSlot(slot_name=slot)

if REQUEST is not None:
    redirect_url = request.get('HTTP_REFERER')
    REQUEST.RESPONSE.redirect(redirect_url)

