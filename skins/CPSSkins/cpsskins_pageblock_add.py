##parameters=theme=None, REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

pageblock = context.addPageBlock(**kw)
if pageblock is None:
    return

if theme is None:
    theme = tmtool.getDefaultThemeName()

url = pageblock.absolute_url() + '/edit_form' + \
     '?edit_mode=layout' + '&theme=' + theme

if REQUEST is None:
    return pageblock
else:
    REQUEST.RESPONSE.redirect(url)
