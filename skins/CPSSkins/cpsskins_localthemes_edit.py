##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

theme_id = kw.get('theme_id')

tmtool = context.portal_themes
localtheme_propid = tmtool.getLocalThemeID()

# make sure that the local theme is not already defined in a folder object
if localtheme_propid not in context.objectIds():
    if theme_id:
        # the property exists already.
        if context.hasProperty(localtheme_propid):
            themes = context.getProperty(localtheme_propid)
            themes += (theme_id, )
            context.manage_changeProperties(**{localtheme_propid: themes})
        else:
            context.manage_addProperty(localtheme_propid, theme_id, 'lines')
    elif context.hasProperty(localtheme_propid):
        context.manage_delProperties([localtheme_propid])

if REQUEST is not None:
    message = 'psm_local_theme_updated'
    redirect_url = context.absolute_url() + '/cpsskins_localthemes_form' \
                  + '?portal_status_message=%s' % message
    REQUEST.RESPONSE.redirect(redirect_url)
