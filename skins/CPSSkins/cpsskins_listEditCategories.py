
# category 'general' is by default
categories = ['general']

for propid in context.propertyIds():
    for obj in context.propertyMap():
        if obj['id'] == propid:
            visibility = obj.get('visible', None)
            is_visible = 0
            if visibility is not None:
                if getattr(context, visibility, None) is not None:
                    visible_meth = getattr(context, visibility)
                    if callable(visible_meth):
                        is_visible = apply(visible_meth, ())
                        if not is_visible:
                            continue

            category = obj.get('category', None)
            if category is None:
                continue
            if category not in categories and category is not 'none':
                categories.append(category)

if getattr(context.aq_explicit, 'isportletbox', None) is not None:
    if context.getPortletId() is not None:
        categories.append('Portlet')

return categories
