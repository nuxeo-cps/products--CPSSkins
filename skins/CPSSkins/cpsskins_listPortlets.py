
list = []

for ti in context.portal_types.listTypeInfo():
    # skip the dummy portlet
    if ti.getId() == 'Dummy Portlet':
        continue
    if ti.getProperty('cps_is_portlet', 0):
        list.append(ti)
return list
