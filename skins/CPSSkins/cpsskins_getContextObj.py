##parameters=context_rurl=None

context_obj = None
if context_rurl is not None:
    portal_url = context.portal_url(relative=1)
    if portal_url != '/':
        portal_url = '/' + portal_url
    context_obj = context.restrictedTraverse(portal_url + context_rurl, default=None)

if context_obj is None:
    context_obj = context.REQUEST.get('context_obj', context)

return context_obj
