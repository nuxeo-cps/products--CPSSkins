
path_roots = context.cpsskins_listFolderRoots()

paths = ['/']

portal_hierarchies = context.portal_hierarchies
for root in path_roots:
    root_obj = portal_hierarchies[root]
    hierlist = root_obj.getHierarchyList()

    skiproot = getattr(root_obj, 'skiproot', 0)
    root_path = '/' + getattr(root_obj, 'root') + '/'
    for h in hierlist:
        d = h['rurl'] + '/'
        if skiproot:
            d = d[len(root_path)-1:0]
        paths.append(d)

return paths
