
list = []

# CPS Portlets
if getattr(context, 'portal_cpsportlets', None) is not None:
    list = context.portal_cpsportlets.listPortletSlots()

return list
