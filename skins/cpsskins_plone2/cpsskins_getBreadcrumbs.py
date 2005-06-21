
result = []

# Plone 2.0.x
breadcrumbs = getattr(context, 'breadcrumbs', None)
if breadcrumbs is not None and callable(breadcrumbs):
    for name, url in breadcrumbs():
        result.append({'id': name,
                        'title': name,
                        'url': url,
                      })
# Plone 2.1
else:
    for bc in context.plone_utils.createBreadCrumbs(context):
        name = bc['Title']
        result.append({'id': name,
                       'title': name,
                       'url': bc['absolute_url'],
                      })
return result
