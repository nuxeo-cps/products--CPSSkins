list = ['/']

portal_trees = context.portal_trees

for root in context.cpsskins_listFolderRoots():
    for folder in portal_trees[root].getList(start_depth=0, stop_depth=1):
        if folder['id'].startswith('.'):
            continue
        path_url = '/' + folder['rpath'] + '/'
        list.append(path_url)

return list
