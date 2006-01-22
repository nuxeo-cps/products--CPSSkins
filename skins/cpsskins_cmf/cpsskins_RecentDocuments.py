

MAX_DOCUMENTS = 5

mtool = context.portal_membership
if mtool.isAnonymousUser():
    return []

member = mtool.getAuthenticatedMember()

query = {
     # XXX: are we sure that every member has a last_login_time attribute ?
     'modified': {'query': getattr(member, 'last_login_time', 0),
                  'range': 'min'},
     'sort_on': 'modified',
     'sort_order': 'reverse',
     'review_state': 'published',
     }

brains = context.portal_catalog(**query)

recent = []

for brain in brains[:MAX_DOCUMENTS]:
    obj = brain.getObject()
    recent.append(
        {'title': brain['Title'],
         'url': brain.getURL(),
         'icon': obj.getIcon(),
        })

return recent
