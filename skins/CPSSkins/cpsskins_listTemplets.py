
list = []

for ti in context.portal_types.listTypeInfo():
   if ti.getActionById('isportaltemplet', None):
       list.append(ti)
return list
