results = context.portal_catalog.searchResults(review_state='published', 
                                              end={'query': context.ZopeTime(), 'range': 'min'},
                                              portal_types=('Event', 'ATEvent'),
                                              )[:5]
events = [] 
for res in results:
    if hasattr(res.aq_explicit, 'getRID'):
        res = res.getObject()
    events.append({
                    'url': res.absolute_url(),
                    'title': res.title_or_id(),
                    'icon': res.getIcon(),
                    'location': res.location,
                    'start': DateTime(res.start().strftime('%d/%m/%y'))
                  }
                 )

return events
