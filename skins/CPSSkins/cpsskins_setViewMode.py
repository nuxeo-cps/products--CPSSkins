##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

if REQUEST is None:
    REQUEST = context.REQUEST
session = REQUEST.SESSION

session_key = 'cpsskins_view_mode'

if not session.has_key(session_key):
    session[session_key] = {}

mode = {}
if kw.has_key('fullscreen'):
    mode['fullscreen'] = kw['fullscreen']

session[session_key].update(mode)

url = REQUEST.get('HTTP_REFERER')
REQUEST.RESPONSE.redirect(url)
