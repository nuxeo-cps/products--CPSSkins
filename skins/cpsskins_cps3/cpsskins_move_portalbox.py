##parameters=box_url=None, src_ypos=None, dest_ypos=None, src_slot=None, dest_slot=None, REQUEST=None

dest_ypos = int(dest_ypos)
src_ypos = int(src_ypos)

btool = context.portal_boxes
portal_url = context.portal_url(relative=1) + '/'

sboxes = btool.getBoxes(context, include_only_in_subfolder=1)
sboxes = btool.filterBoxes(sboxes, slot=dest_slot, keep_closed=1)

if src_slot == dest_slot:
    found = 0
    for box in sboxes: 
        order = int(box['settings']['order'])
        if order == dest_ypos and not found:
            found = 1
            box = box['box']
            box.edit(order=src_ypos)
            if src_ypos == dest_ypos:
                dest_ypos += 10
            break
else:
    new_ypos = 0
    found = 0
    for box in sboxes: 
        order = int(box['settings']['order'])
        if order == dest_ypos and not found:
            found = 1
            new_ypos = order + 10
        if found:
            box = box['box']
            box.edit(order=new_ypos)
            new_ypos += 10

box = context.restrictedTraverse(portal_url + box_url)
box.edit(box_url=box_url, slot=dest_slot, order=dest_ypos)

if REQUEST is not None:
     url = context.absolute_url() + '/box_manage_form'
     REQUEST.RESPONSE.redirect(url)
