

# CPS Portlets
if hasattr(context, 'portal_cpsportlets'):
    return context.portal_portlets.getPortletSlots()

# Fallback to CPS Boxes
list = []
for box in context.getBoxSlots():
    list.append(box)

list.append('closed')
return list
