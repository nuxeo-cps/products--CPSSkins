##parameters=REQUEST=None, **kw

img = context
if getattr(context, 'i18n', 0):
    lc = context.cpsskins_getlocalizer(root=1); 
    current_lang = context.getDefaultLang()
    if current_lang: 
        img_id = 'i18n_image_%s' % current_lang
        img = getattr(context.aq_explicit, img_id, context)
        
height = getattr(img, 'height', '0')
width = getattr(img, 'width', '0')
title = getattr(img, 'title', '')
img_url = img.absolute_url()
tag = ''

if getattr(context, 'use_internal_link', 0):
    link = context.portal_url() + getattr(context, 'internal_link', '')
else:
    link = getattr(context, 'link', '')
    
if link:
    tag += '<a href="%s">' % link

tag += '<img src="%s" width="%s" height="%s" border="0" alt="%s" />' % \
        (img_url, width, height, title) 

if link:
    tag += '</a>'

caption = getattr(context, 'caption', '')
if caption:
    tag += '<br/>%s' % caption

return tag
