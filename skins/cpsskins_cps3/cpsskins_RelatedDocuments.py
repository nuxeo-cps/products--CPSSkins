##parameters=obj=None

related=[]
subjects=None

if obj is None:
    obj=context

obj = obj.getContent()

if hasattr(obj.aq_explicit, 'Subject'):
    subjects=obj.Subject()

ptool = context.portal_proxies
wtool = context.portal_workflow
utool = context.portal_url


if subjects:
   for o in context.portal_catalog( Subject = subjects
                                  , sort_on = 'portal_type'
                                  , sort_order = 'reverse'  ):
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

        url=o.getURL()
        title=''
        if url != obj.absolute_url():
            related.append( {'title': proxy.Title()
                            ,'url': utool.getRelativeUrl(proxy)
                            ,'icon':proxy.getIcon()} )

return related
