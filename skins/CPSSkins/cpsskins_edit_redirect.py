##parameters=cat=None, REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

url = context.absolute_url()

if cat not in ['image', 'style', 'palette']:
    return

if cat == 'image':
    url += '/cpsskins_theme_manage_form' + \
           '?imagecat=' + kw.get('image', '')

elif cat == 'style':
    url += '/cpsskins_theme_manage_form' + \
           '?style=' + kw.get('style', '')

elif cat == 'palette':
    url += '/cpsskins_theme_manage_form' + \
           '?palette=' + kw.get('palette', '')

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
