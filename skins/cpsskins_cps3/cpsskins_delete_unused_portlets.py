##parameters=theme=None, REQUEST=None

ptltool = context.portal_cpsportlets
cpsmcat = context.Localizer.default

hidden_slots = context.cpsskins_listHiddenSlots(theme=theme)

for hidden_slot in hidden_slots:
    portlets = ptltool.getPortlets(context, hidden_slot, sort=0)

    for portlet in portlets:
        ptltool.deletePortlet(portlet_id=portlet.getId(), context=context)

if REQUEST is not None:
     url = context.absolute_url() + \
     '/portlet_manage_form?portal_status_message=' + \
      cpsmcat('description_unused_porlets_deleted')
     REQUEST.RESPONSE.redirect(url)
