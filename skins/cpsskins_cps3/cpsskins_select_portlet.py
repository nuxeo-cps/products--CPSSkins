
ptltool = context.portal_portlets

list = []
for k, v in  ptltool.items():
    list.append(k)

return list
