##parameters=theme=None, edit_mode='wysiwyg', REQUEST=None, **kw

tmtool = context.portal_themes
if REQUEST is not None:
    kw.update(REQUEST.form)

alignprop = kw.get('alignprop', None)
if alignprop is None:
    return

context.change_alignment(alignment=alignprop)

if theme is None:
    theme = tmtool.getDefaultThemeName()

url = context.absolute_url() + '/edit_form' + \
     '?theme=' + theme + '&edit_mode=' + edit_mode

if REQUEST is not None:
     REQUEST.RESPONSE.redirect(url)
