##parameters=type_name=None, slot=None, order=None, REQUEST=None

ptltool = context.portal_cpsportlets
if type_name is not None:
    portlet_id = ptltool.createPortlet(ptype_id=type_name, 
                                       slot=slot, 
                                       order=order,
                                       context=context)

if REQUEST is not None:
    redirect_url = REQUEST.get('HTTP_REFERER')
    REQUEST.RESPONSE.redirect(redirect_url)

