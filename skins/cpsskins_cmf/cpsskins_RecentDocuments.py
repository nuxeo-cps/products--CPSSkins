
mtool = context.portal_membership
catalog = context.portal_catalog

if mtool.isAnonymousUser():
   return

recent=[]

member = mtool.getAuthenticatedMember()
if hasattr(member, 'last_login_time'):
    last_login_time = member.last_login_time

    results = catalog.searchResults(modified=last_login_time,
                                    modified_usage='range:min',
                                    sort_on='modified',
                                    sort_order='reverse',
                                    review_state='published',
                                   )
    for o in results[:5]:
        url=o.getURL()
        title=''
        if o.Title:
            title=o.Title
        else:
            title=o.getId
        recent.append( {'title':title
                       ,'url':url
                       ,'icon':o.getIcon} )
return recent
