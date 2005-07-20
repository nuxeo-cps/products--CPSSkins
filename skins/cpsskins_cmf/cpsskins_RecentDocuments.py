
mtool = context.portal_membership
if mtool.isAnonymousUser():
    return []

member = mtool.getAuthenticatedMember()

query = {
     'modified': member.last_login_time,
     'modified_usage': 'range:min',
     'sort_on': 'modified',
     'sort_order': 'reverse',
     'review_state': 'published',
     }

brains = context.portal_catalog(**query)

recent=[]

for brain in brains[:5]:
    obj = brain.getObject()
    recent.append(
        {'title': brain['Title'],
         'url': brain.getURL(),
         'icon': obj.getIcon(),
        })

return recent
