##parameters=REQUEST=None, **kw

text = context.text
i18n = getattr(context, 'i18n', 0)
text_format = getattr(context, 'text_format', 'html')

if i18n:
    mcat = context.cpsskins_getlocalizer(cat='default')
    if mcat is not None:
        text = mcat(text)

return context.render_text_as(text, text_format)
