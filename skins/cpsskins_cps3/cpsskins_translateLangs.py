##parameters=langs=None

mcat = context.Localizer.default

tr_langs = []
for lang in langs:
    tr_lang = lang.copy()
    tr_lang['title'] = mcat('label_language_%s' % lang['id'])
    tr_langs.append(tr_lang)

return tr_langs

