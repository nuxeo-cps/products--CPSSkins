results = context.portal_catalog.searchResults(
    review_state='published',
    end={'query': context.ZopeTime(), 'range': 'min'},
    sort_on='start',
    )[:5]

events = []
for res in results:
    if hasattr(res.aq_explicit, 'getRID'):
        res = res.getObject()
    event = res.getContent()
    start = getattr(event, 'start', None)
    events.append({'url': event.absolute_url(),
                   'title': event.title_or_id(),
                   'icon': event.getIcon(),
                   'location': '',
                   'start': start and DateTime(start.strftime('%m/%d/%y')).ISO() or '',
                  })
return events

