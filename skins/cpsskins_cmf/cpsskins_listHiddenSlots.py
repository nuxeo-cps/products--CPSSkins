##parameters=theme=None

if theme is None:
    return

tmtool = context.portal_themes
slots = context.cpsskins_listSlots()

for block in tmtool.getPageBlocks(theme=theme):
    objects = block.getObjects()
    for cell in objects.keys():

       for content in objects[cell]['contents']:
          if getattr(content.aq_explicit, 'isportalboxgroup', 0):
              slot = content.box_group
              if slot in slots:
                  slots.remove(slot)

          if getattr(content.aq_explicit, 'iscellblock', 0):
              cell_objects = content.getObjects()
              for cell2 in cell_objects.keys():

                  for cell_content in cell_objects[cell2]['contents']:
                      if getattr(cell_content.aq_explicit, 'isportalboxgroup', 0):
                          slot = cell_content.box_group
                          if slot in slots:
                              slots.remove(slot)

return slots
