
# Localizer (CMF, Plone1, CPS3)
if hasattr(context, 'Localizer'):
    localizer = getattr(context, 'Localizer')
    return localizer.get_selected_language()
   
# PloneLanguageTool (Plone2)
if hasattr(context, 'portal_languages'):
    ptool = context.portal_languages
    boundLanguages = ptool.getLanguageBindings()
    if boundLanguages:
       return boundLanguages[0]

# Portal messages (CPS2)
if hasattr(context, 'portal_messages'):
    mcat = getattr(context, 'portal_messages')
    return mcat.get_selected_language()

# PTS
REQUEST = context.REQUEST
if REQUEST is not None:
    accept_language = REQUEST.get('HTTP_ACCEPT_LANGUAGE')
    if accept_language:
        accept_language = accept_language.split(',')
        if len(accept_language) > 0:
            return accept_language[0]

return 'en'
