portal = context.portal_url.getPortalObject()
paths = ['/', ]
for obj in portal.contentValues():
    if obj.getTypeInfo().getId() in ['Folder', 'Portal Folder', 'Plone Folder' ]:
        paths.append('/' + obj.getId() + '/')

return paths
