
if not hasattr(context, 'portal_actionicons'):
    return []

aitool = context.portal_actionicons
actionicons = aitool.listActionIcons()

here_url = context.absolute_url()
portal_url = context.portal_url()

icons = []
for ai in actionicons:
    if '%s/%s' % (portal_url, ai.getIconURL()) == here_url:
        icons.append(ai)

return icons
