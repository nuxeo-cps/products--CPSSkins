##parameters=theme_renderer=None

if theme_renderer is None:
   return 'default'

if theme_renderer not in context.cpsskins_listThemeRenderers():
   return 'default'

if theme_renderer == 'automatic':
   info = context.cpsskins_browser_detection()

   browser = info[0]
   version = info[1]

   if browser in ['Netscape']:
      return 'compatible'

   if browser in ['Lynx', 'Links']:
      return 'textonly'

   return 'default'

return theme_renderer
