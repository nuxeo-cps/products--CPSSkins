mtool = context.portal_membership

if mtool.isAnonymousUser():
   return

recent=[]

ptool = context.portal_proxies
wtool = context.portal_workflow
utool = context.portal_url

member = mtool.getAuthenticatedMember()
last_login_time = member.last_login_time

results = context.portal_catalog.searchResults(modified=last_login_time,
                                            modified_usage='range:min',
                                            sort_on='modified',
                                            sort_order='reverse',
                                            )
n = 0
for o in results:
    if n >= 5:
         break

    doc_id = o.getPath().split('/')[-1]
    i_proxies = ptool.getProxiesFromObjectId(doc_id)

    for i_proxy in i_proxies:
        proxy = i_proxy['object']

        try:
            title = proxy.Title()
        except (AttributeError):
            continue

        if (wtool.getInfoFor(proxy, 'review_state','nostate') != 'published'):
            continue

        recent.append( {'title': proxy.Title()
                         ,'url': utool.getRelativeUrl(proxy)
                         ,'icon':proxy.getIcon()} )
        n += 1
return recent
