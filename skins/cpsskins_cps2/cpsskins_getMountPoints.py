mount_points = {}

portal_hierarchies = context.portal_hierarchies
for folder in portal_hierarchies.getHierarchies():
    obj = portal_hierarchies.getHierarchyById(folder)

    skiproot = getattr(obj, 'skiproot', 0)
    if skiproot:
        root_path = '/'
    else:
        root_path = '/' + getattr(obj, 'root', None) + '/'

    mount_points[folder] = root_path

return mount_points
