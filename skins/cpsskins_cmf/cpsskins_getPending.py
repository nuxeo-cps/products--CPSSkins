results = context.portal_catalog.searchResults(review_state='pending') 

docs = [] 
for doc in results:
    if hasattr(doc.aq_explicit, 'getRID'):
        doc = doc.getObject()
    docs.append(doc)

return docs
