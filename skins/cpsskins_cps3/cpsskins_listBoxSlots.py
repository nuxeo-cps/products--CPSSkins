
list = []

for box in context.getBoxSlots():
    list.append(box)

list.append('closed')

return list
