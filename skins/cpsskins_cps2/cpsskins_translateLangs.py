##parameters=langs=None

mcat = context.cpsskins_getlocalizer()

tr_langs = []
for lang in langs:
    tr_lang = lang.copy()
    tr_lang['title'] = mcat('_lang_%s' % lang['title'])
    tr_langs.append(tr_lang)

return tr_langs

