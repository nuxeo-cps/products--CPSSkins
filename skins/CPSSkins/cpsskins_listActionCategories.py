
list =  context.portal_actions.listFilteredActionsFor(context).keys()
if getattr(context, 'portal_actionicons', None) is None:
    return []

aitool = context.portal_actionicons
mtool = context.portal_membership

if not mtool.checkPermission('listActionIcons', aitool):
    return []

for icon in aitool.listActionIcons():
    category = icon.getCategory()
    if category not in list:
        list.append(category)

return list
