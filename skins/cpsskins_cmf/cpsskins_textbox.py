##parameters=REQUEST=None, **kw

text = context.text
i18n = context.i18n
text_format = context.text_format

if i18n:
    tmtool = context.portal_themes
    mcat = tmtool.getTranslationService(cat='default')
    if mcat is not None:
        text = mcat(text).encode("ISO-8859-15", 'ignore')

return context.render_text_as(text, text_format)
