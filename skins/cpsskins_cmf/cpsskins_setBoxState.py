##parameters=boxid=None, state=None, REQUEST=None

if boxid is None or state is None:
   return

tmtool = context.portal_themes
current_theme, current_page = tmtool.getEffectiveThemeAndPageName()
cookie_name = 'cpsskins_%s_%s' % (current_theme, boxid)

if REQUEST is not None:
   RESPONSE = REQUEST.RESPONSE

   if state in ['minimized']:
       RESPONSE.setCookie(cookie_name, state)
   else:
       RESPONSE.expireCookie(cookie_name)

   url = REQUEST['HTTP_REFERER']
   REQUEST.RESPONSE.redirect(url)
