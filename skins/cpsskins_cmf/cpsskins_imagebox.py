##parameters=REQUEST=None, **kw

REQUEST = context.REQUEST

img = context
if context.i18n:
    lc = context.cpsskins_getlocalizer(root=1); 
    current_lang = context.getDefaultLang()
    if current_lang: 
        img_id = 'i18n_image_%s' % current_lang
        img = getattr(context.aq_inner.aq_explicit, img_id, context)

base_url = REQUEST.get('cpsskins_base_url', '')

height = img.height
width = img.width
title = img.title
tag = ''

img_url = base_url + context.portal_url.getRelativeUrl(img)
if context.use_internal_link:
    link = base_url
    internal_link = context.internal_link
    if internal_link != '/':
        link += internal_link
else:
    link = context.link
    
if link:
    tag += '<a href="%s">' % link

tag += '<img src="%s" width="%s" height="%s" border="0" alt="%s" />' % \
        (img_url, width, height, title) 

if link:
    tag += '</a>'

caption = context.caption
if caption:
    tag += '<br/>%s' % caption

return tag
