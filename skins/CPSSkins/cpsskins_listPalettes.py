
list = []

for ti in context.portal_types.listTypeInfo():
   if ti.getActionById('isportalpalette', None):
       list.append(ti)
return list

