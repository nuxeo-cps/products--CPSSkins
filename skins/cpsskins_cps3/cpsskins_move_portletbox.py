##parameters=portlet_rurl=None, src_ypos=None, dest_ypos=None, src_slot=None, dest_slot=None, REQUEST=None

dest_ypos = int(dest_ypos)
src_ypos = int(src_ypos)

portal_path = context.portal_url.getPortalPath() + '/'

ptltool = context.portal_cpsportlets
portlets = ptltool.getPortlets(context=context, slot=dest_slot, sort=0)

if src_slot == dest_slot:
    found = 0
    for portlet in portlets: 
        order = portlet.getOrder()
        if order == dest_ypos and not found:
            found = 1
            portlet.setOrder(src_ypos)
            if src_ypos == dest_ypos:
                dest_ypos += 10
            break
else:
    new_ypos = 0
    found = 0
    for portlet in portlets: 
        order = portlet.getOrder()
        if order == dest_ypos and not found:
            found = 1
            new_ypos = order + 10
        if found:
            portlet.setOrder(new_ypos)
            new_ypos += 10

portlet = context.restrictedTraverse(portal_path + portlet_rurl)
if portlet is not None:
    portlet.setSlot(dest_slot)
    portlet.setOrder(dest_ypos)

if REQUEST is not None:
     url = context.absolute_url() + '/portlet_manage_form'
     REQUEST.RESPONSE.redirect(url)
