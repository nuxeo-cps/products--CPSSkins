##parameters=theme=None, REQUEST=None

if theme is None:
   return

tmtool = context.portal_themes
cookie_name = tmtool.getThemeCookieID()

if REQUEST is not None:
   RESPONSE = REQUEST.RESPONSE
   RESPONSE.setCookie(cookie_name, theme)

   url = REQUEST['HTTP_REFERER']
   RESPONSE.redirect(url)   
