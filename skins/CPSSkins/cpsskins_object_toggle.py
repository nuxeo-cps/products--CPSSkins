##parameters=theme=None, edit_mode='wysiwyg', REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

object = context.toggle()

if theme is None:
    theme = tmtool.getDefaultThemeName()

url = context.absolute_url() + '/edit_form' + \
      '?edit_mode=' + edit_mode + '&theme=' + theme

if REQUEST is None:
    return object
else:
    REQUEST.RESPONSE.redirect(url)
