results = context.portal_catalog.searchResults(
    review_state='published',
    end={'query': context.ZopeTime(), 'range': 'min'},
    sort_on='start',
    )[:5]

events = []
for res in results:
    event_start = res.start
    if hasattr(res.aq_explicit, 'getRID'):
        res = res.getObject()
    events.append({'url': res.absolute_url(),
                   'title': res.title_or_id(),
                   'icon': res.getIcon(),
                   'location': '',
                   'start': event_start.ISO(),
                  })
return events
