
list = []
# CPS Portlets
if getattr(context, 'portal_cpsportlets', None) is not None:
    list.extend(context.portal_cpsportlets.listPortletSlots())

# CPS3 Boxes
if getattr(context, 'portal_boxes', None) is not None:
    list.extend(context.getBoxSlots())
    list.append('closed')

return list
