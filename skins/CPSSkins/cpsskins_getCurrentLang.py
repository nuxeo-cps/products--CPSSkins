
# Localizer (CMF, Plone1, CPS3)
localizer =  getattr(context, 'Localizer', None)
if localizer is not None:
    return localizer.get_selected_language()

# PloneLanguageTool (Plone2)
ptool = getattr(context, 'portal_languages', None)
if ptool is not None:
    boundLanguages = ptool.getLanguageBindings()
    if boundLanguages:
       return boundLanguages[0]

# Portal messages (CPS2)
mcat = getattr(context, 'portal_messages', None)
if mcat is not None:
    return mcat.get_selected_language()

# PlacelessTranslation service
REQUEST = context.REQUEST
if REQUEST is not None:
    accept_language = REQUEST.get('HTTP_ACCEPT_LANGUAGE')
    if accept_language:
        accept_language = accept_language.split(',')
        if len(accept_language) > 0:
            return accept_language[0]

return 'en'
