
ptltool = context.portal_portlets
box_id = context.box_id
portlet = ptltool.getPortletById(box_id)

rendered = ''
if portlet is not None:
    rendered = portlet.getContent().render(proxy=portlet) 
return rendered
