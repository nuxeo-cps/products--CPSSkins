##parameters=cat=None,root=None

# CPS2
if hasattr(context, 'portal_messages'):
     return getattr(context, 'portal_messages')

# CMF / Plone1 / CPS3 
if hasattr(context, 'Localizer'):
    localizer = getattr(context, 'Localizer')
    if root:
        return localizer

    # returns a catalog if asked explicitly
    if cat:
        if hasattr(localizer, cat):
            return getattr(localizer, cat)

    # Localizer without translation service
    if not hasattr(context, 'translation_service'):
        return getattr(localizer, 'default', None)
   
# Plone2 / CPS3
return None
