##parameters=langs=None

mcat = context.cpsskins_getlocalizer()

tr_langs = []
for lang in langs:
    tr_lang = lang.copy()
    title = lang['title']
    if mcat:
        title = mcat(title)
    tr_lang['title'] = title
    tr_langs.append(tr_lang)

return tr_langs

