##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes

context.edit(**kw)

# set the scroll position
scrollx = kw.get('scrollx', '0')
scrolly = kw.get('scrolly', '0')

tmtool.setViewMode(scrollx=scrollx)
tmtool.setViewMode(scrolly=scrolly)

# category
cat = kw.get('cat')

# redirect url
url = kw.get('redirect_url')

if REQUEST is not None:
   if url is None:
       url = context.absolute_url() + '/edit_form'

   if cat:
         url += '?cat=' + cat
   REQUEST.RESPONSE.redirect(url)
