

# CPS Portlets
if getattr(context, 'portal_cpsportlets', None) is not None:
    return context.portal_cpsportlets.getPortletSlots()

# Fallback to CPS Boxes
list = []
for box in context.getBoxSlots():
    list.append(box)

list.append('closed')
return list
