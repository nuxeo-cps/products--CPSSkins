##parameters=text=None, words=None

if words is None:
    words = 20

import string
split_text = string.split(text, sep=' ', maxsplit=words)[0:words]
if split_text:
    res = ' '.join(split_text) + ' ...'
else:
    res = ''

return res

