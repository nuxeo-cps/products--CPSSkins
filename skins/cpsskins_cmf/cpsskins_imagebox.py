##parameters=REQUEST=None, **kw

img = context
if context.i18n:
    lc = context.cpsskins_getlocalizer(root=1); 
    current_lang = context.getDefaultLang()
    if current_lang: 
        img_id = 'i18n_image_%s' % current_lang
        img = getattr(context.aq_explicit, img_id, context)
        
height = img.height
width = img.width
title = img.title
img_url = img.absolute_url()
tag = ''

if context.use_internal_link:
    link = context.portal_url() + context.internal_link
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
