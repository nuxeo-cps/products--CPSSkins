mount_points = {}

for folder in context.cpsskins_listFolderRoots():
    mount_points[folder] = '/' + folder

return mount_points
