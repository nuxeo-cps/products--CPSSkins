##parameters=portlet_url=None, src_ypos=None, dest_ypos=None, src_slot=None, dest_slot=None, REQUEST=None

dest_ypos = int(dest_ypos)
src_ypos = int(src_ypos)

ptltool = context.portal_cpsportlets
portlets = ptltool.getPortlets(context, slot=dest_slot)

if src_slot == dest_slot:
    found = 0
    for portlet in portlets: 
        order = portlet.getOrder()
        if order == dest_ypos and not found:
            found = 1
            portlet.edit(order=src_ypos)
            if src_ypos == dest_ypos:
                dest_ypos += 10
            break
else:
    new_ypos = 0
    found = 0
    for portlet in portlets: 
        order = int(portlet.getOrder())
        if order == dest_ypos and not found:
            found = 1
            new_ypos = order + 10
        if found:
            box.edit(order=new_ypos)
            new_ypos += 10

portlet = context.restrictedTraverse(portlet_url)
portlet.edit(slot=dest_slot, order=dest_ypos)

if REQUEST is not None:
     url = context.absolute_url() + '/portlet_manage_form'
     REQUEST.RESPONSE.redirect(url)
