##parameters=portlet_id=None, REQUEST=None

if portlet_id is None:
    return

ptltool = context.portal_cpsportlets
cpsmcat = context.Localizer.default

ptltool.deletePortlet(portlet_id, context)

if REQUEST is not None:
     url = context.absolute_url() + \
     '/portlet_manage_form?portal_status_message=' + \
      cpsmcat('description_porlets_deleted')
     REQUEST.RESPONSE.redirect(url)
