
REQUEST=context.REQUEST

context_url = REQUEST.get('context_url', None)
if context_url is None:
    context_url = context.getContextUrl()

breadcrumb_set = getattr(REQUEST, 'breadcrumb_set', None)
return context.getBreadCrumbs(url=context_url, breadcrumb_set=breadcrumb_set)
