##parameters=theme=None, REQUEST=None

if theme is None:
    return

tmtool = context.portal_themes
cookie_name = tmtool.getThemeCookieID()

if REQUEST is not None:
    RESPONSE = REQUEST.RESPONSE
    RESPONSE.setCookie(cookie_name, theme)

    redirect_url = REQUEST['HTTP_REFERER'] or context.absolute_url()
    RESPONSE.redirect(redirect_url)
