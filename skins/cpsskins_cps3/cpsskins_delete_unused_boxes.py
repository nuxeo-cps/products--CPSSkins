##parameters=theme=None, REQUEST=None

btool = context.portal_boxes
cpsmcat = context.Localizer.default

hidden_slots = context.cpsskins_listHiddenSlots(theme=theme)

for hidden_slot in hidden_slots:
    sboxes = btool.getBoxes(context, include_only_in_subfolder=1) 
    sboxes = btool.filterBoxes(sboxes, slot=hidden_slot, keep_closed=1)

    for box in sboxes:
        box_obj = box['box']
        box_container = box_obj.aq_parent
        box_container.manage_delObjects([box_obj.getId()])

if REQUEST is not None:
     url = context.absolute_url() + '/box_manage_form?portal_status_message=' + cpsmcat('description_unused_boxes_deleted')
     REQUEST.RESPONSE.redirect(url)

