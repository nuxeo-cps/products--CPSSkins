
ptltool = context.portal_cpsportlets
portlet_id = getattr(context, 'portlet_id', None)
portlet = ptltool.getPortletById(portlet_id)

return portlet_id

rendered = ''
if portlet is not None:
    rendered = portlet.render(proxy=portlet) 
return rendered
