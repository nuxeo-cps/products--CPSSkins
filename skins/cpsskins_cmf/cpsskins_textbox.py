##parameters=REQUEST=None, **kw

text = context.text
i18n = context.i18n
text_format = context.text_format

if i18n:
    mcat = context.cpsskins_getlocalizer(cat='default')
    if mcat is not None:
        text = mcat(text)

return context.render_text_as(text, text_format)
