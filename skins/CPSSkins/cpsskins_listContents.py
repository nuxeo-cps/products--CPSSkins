
list = []

for ti in context.portal_types.listTypeInfo():
    if ti.getActionById('isportaltemplet', None):
        list.append(ti)

    if ti.getActionById('iscellblock', None):
        list.insert(0, ti)
return list
