
ptltool = getattr(context, 'portal_cpsportlets', None)

if ptltool is not None:
    return ptltool.listPortletSlots()

return []
