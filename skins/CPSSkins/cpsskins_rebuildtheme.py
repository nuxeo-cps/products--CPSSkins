##parameters=REQUEST=None

if getattr(context.aq_inner.aq_explicit, 'isportaltheme', 0):
    context.rebuild(setperms=1)

if REQUEST is not None:
    url = context.portal_url() + '/cpsskins_theme_manage_form' +\
          '?portal_status_message=_Theme_rebuilt_'
    REQUEST.RESPONSE.redirect(url)
