
list = []

for ti in context.portal_types.listTypeInfo():
   if ti.getProperty('cps_is_portlet', 0):
       list.append(ti)
return list
