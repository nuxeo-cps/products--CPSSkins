##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

context.edit(**kw)

# theme and edit mode
theme = kw.get('theme', None)
if theme is None:
    tmtool = context.portal_themes
    theme = tmtool.getDefaultThemeName()

edit_mode = kw.get('edit_mode', 'wysiwyg')

# scroll position
scrollx = kw.get('scrollx', 0)
scrolly = kw.get('scrolly', 0)

# category
cat = kw.get('cat')

if REQUEST is not None:
   url = context.absolute_url() + '/edit_form' + \
         '?theme=' + theme + '&edit_mode=' + edit_mode + \
         '&scrollx=' + scrollx + '&scrolly=' + scrolly
   if cat:
         url += '&cat=' + cat
   REQUEST.RESPONSE.redirect(url)
