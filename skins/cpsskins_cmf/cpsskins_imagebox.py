##parameters=**kw

from cgi import escape

REQUEST = context.REQUEST

img = context
if context.i18n:
    tmtool = context.portal_themes
    lc = tmtool.getTranslationService(root=1);
    current_lang = context.getDefaultLang()
    if current_lang:
        img_id = 'i18n_image_%s' % current_lang
        img = getattr(context.aq_inner.aq_explicit, img_id, context)

base_url = REQUEST.get('cpsskins_base_url')
if base_url is None:
    base_url = context.cpsskins_getBaseUrl()

height = img.height
width = img.width
title = img.title
tag = ''

img_url = base_url + context.portal_url.getRelativeUrl(img)
if context.use_internal_link:
    link = base_url
    internal_link = context.internal_link
    if internal_link:
        link += internal_link[1:]
else:
    link = context.link

if link:
    tag += '<a href="%s" title="%s">' % (escape(link), escape(title))

tag += '<img src="%s/index_html" width="%s" height="%s" alt="%s" />' % \
        (escape(img_url), width, height, escape(title))

if link:
    tag += '</a>'

caption = context.caption
if caption:
    tag += '<br/>%s' % escape(caption)

return tag
