##parameters=REQUEST=None

tmtool = context.portal_themes
theme = tmtool.getRequestedThemeName()
theme_container = tmtool.getThemeContainer(theme=theme)
page = theme_container.getRequestedPageName(context_obj=here)
page_container = theme_container.getPageContainer(page=page)

boxes_styles = context.boxes_styles_get()

dict = {}
for i in range(10):
   dict[i] = {
        'authorized_styles': ('box_left_template',),
        'title': '',
        'directions': [
           { 'icon': 'img_box_moveup.png', 'xpos': -1, 'ypos_move': -1 },
           { 'icon': 'img_box_movedown.png', 'xpos': -1, 'ypos_move': 1 },
        ]
   }

for block in page_container.getPageBlocks():
     objects = block.getObjects(REQUEST=REQUEST)
     if objects is None:
         continue
     content_list = []
     for x_pos in range(int(block.maxcols)):
        objects_in_xpos = objects.get(x_pos, None)
        if objects_in_xpos is None:
           continue
        contents_in_xpos = objects_in_xpos['contents']
        for content in contents_in_xpos:
              if getattr(content.aq_explicit, 'isportalboxgroup', 0):
                  position =  getattr(content, 'position', None)
              else:
                  continue
              try:
                 position_int = int(position)
              except:
                 continue

              grid = {}
              grid['authorized_styles'] = ('box_left_template',)
              grid['title'] = content.title
              directions = []
              direction = {}
              direction['icon'] = 'img_box_moveup.png'
              direction['xpos'] = -1
              direction['ypos_move'] = -1
              directions.append(direction)

              direction = {}
              direction['icon'] = 'img_box_movedown.png'
              direction['xpos'] = -1
              direction['ypos_move'] = 1
              directions.append(direction)

              grid['directions'] = directions
              dict[position_int] = grid


# compatibility with NuxPortal
dict[1]['authorized_styles'] = ('box_std_template', )

return dict
