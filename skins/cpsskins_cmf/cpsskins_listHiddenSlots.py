##parameters=theme=None

if theme is None:
    return

tmtool = context.portal_themes
slots = context.cpsskins_listSlots()

for block in tmtool.getPageBlocks(theme=theme):
    objects = block.getObjects()
    for cell in objects.keys():
       for templet in objects[cell]['templets']:
          if templet.aq_explicit.isPortalBoxGroup():
              slot = getattr(templet, 'box_group', None)
              if slot in slots:
                  slots.remove(slot)
return slots
