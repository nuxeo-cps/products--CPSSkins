
REQUEST = context.REQUEST

if REQUEST is not None:
     REQUEST.RESPONSE.redirect(context.absolute_url() + '/content_status_modify?workflow_action=publish')
