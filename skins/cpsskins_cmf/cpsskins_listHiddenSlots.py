##parameters=theme=None

if theme is None:
    return

tmtool = context.portal_themes
slots = context.cpsskins_listSlots()

theme, page = tmtool.getEffectiveThemeAndPageName(editing=1)
theme_container = tmtool.getThemeContainer(theme=theme)
page_container = theme_container.getPageContainer(page=page)

for block in page_container.getPageBlocks():
    objects = block.getObjects()
    for cell in objects.keys():
       for content in objects[cell]['contents']:
          c = content.aq_inner.aq_explicit
          if not getattr(c, 'isportalboxgroup', 0):
              continue
          slot = content.box_group
          if slot in slots:
              slots.remove(slot)

          if not getattr(c, 'iscellblock', 0):
              continue

          cell_objects = content.getObjects()
          for cell2 in cell_objects.keys():
              for cell_content in cell_objects[cell2]['contents']:
                  cc = cell_content.aq_inner.aq_explicit
                  if not getattr(cc, 'isportalboxgroup', 0):
                      continue
                  slot = cell_content.box_group
                  if slot in slots:
                      slots.remove(slot)
return slots
