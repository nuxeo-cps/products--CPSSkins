##parameters=REQUEST=None

tmtool = context.portal_themes
cookie_name = tmtool.getThemeCookieID()

if REQUEST is not None:
   RESPONSE = REQUEST.RESPONSE
   RESPONSE.expireCookie(cookie_name)

   url = REQUEST['HTTP_REFERER']   
   REQUEST.RESPONSE.redirect(url)     
